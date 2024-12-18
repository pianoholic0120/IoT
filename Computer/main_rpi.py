import os
import serial
import time
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER_ADDRESS = "192.168.0.197"  
TOPIC_SEND = "hello/group1/rpi2pc"
TOPIC_RECEIVE = "hello/group1/pc2rpi"

client = mqtt.Client()
ser = None

current_mode = '0'
longitude = 0
user_code = ""
current_station = "Da'an"
pm25_buffer = None
regression_result = None

def on_connect(client, userdata, flags, rc):
    print("RPi: Connected to MQTT broker with result code:", rc)
    client.subscribe(TOPIC_RECEIVE)

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8').strip()
    print("RPi received from PC:", payload)
    global regression_result, pm25_buffer, current_mode
    if current_mode=='1':
        # payload為最後一行站點資料，直接回給Arduino
        ser.write((payload+"\n").encode('utf-8'))
    elif current_mode=='3':
        # 收到回歸計算完成的結果
        regression_result = payload
        # 可以直接回傳告訴Arduino已準備好，或等mode='4'時再取得
    elif current_mode=='4':
        # PC回傳的回歸結果與PM2.5值
        ser.write((payload+"\n").encode('utf-8'))

def main():
    global current_mode, longitude, user_code, current_station, regression_result
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_ADDRESS)
    client.loop_start()

    global ser
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    print("RPi connected to Arduino serial.")

    while True:
        if ser.in_waiting > 0:
            cmd = ser.readline().decode('utf-8').strip()
            if len(cmd)==4:
                # 4位數字指令
                current_mode = cmd[0]
                last3 = cmd[1:]
                if current_mode=='1' or current_mode=='2':
                    longitude = int(last3)
                    if longitude < 121:
                        current_station = "Zhongzheng"
                    else:
                        current_station = "Nangang"
                    if current_mode=='1':
                        # 請求PC提供該站最後一行資料
                        # 傳指令給PC，例如傳測站名稱
                        client.publish(TOPIC_SEND, current_station)
                    # mode 2則是Arduino會一直上傳PM2.5值，RPi接收後上傳給PC
                elif current_mode=='3' or current_mode=='4':
                    user_code = "user" + last3
                    if current_mode=='3':
                        # 請PC進行回歸計算
                        client.publish(TOPIC_SEND, f"REGCALC,{user_code}")
                    elif current_mode=='4':
                        # 請PC回傳回歸結果與PM2.5值
                        client.publish(TOPIC_SEND, f"REGRESULT,{user_code}")

            else:
                # 非4碼指令，可能是PM2.5值(mode=2時Arduino傳上來)
                line = cmd
                # 檢查是否為PM2.5數值
                try:
                    pm25 = float(line)
                    # 上傳給PC儲存
                    client.publish(TOPIC_SEND, f"{current_station},{pm25}")
                except ValueError:
                    pass

        time.sleep(0.5)

if __name__ == "__main__":
    main()
