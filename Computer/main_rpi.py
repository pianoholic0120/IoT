import os
import serial
import time
import csv
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
pm25_buffer = None  # 儲存最新的 PM2.5 值
regression_result = None  # 儲存風險預測結果


def risk_prediction(m, b, cor, p, air):
    """風險預測函式"""
    if cor < 0.25 or p > 0.5:
        return 0
    elif m * air >= 5:
        return 1
    else:
        return 2


def on_connect(client, userdata, flags, rc):
    """MQTT 連接成功的回調函式"""
    print("RPi: Connected to MQTT broker with result code:", rc)
    client.subscribe(TOPIC_RECEIVE)


def on_message(client, userdata, msg):
    """接收電腦端傳回的資料"""
    payload = msg.payload.decode('utf-8').strip()
    print("RPi received from PC:", payload)
    global regression_result, current_mode
    if current_mode == '1':
        ser.write((payload + "\n").encode('utf-8'))  # 回傳站點資料給 Arduino
    elif current_mode == '4':
        ser.write((payload + "\n").encode('utf-8'))  # 回傳回歸結果和 PM2.5 值給 Arduino


def main():
    global current_mode, longitude, user_code, current_station, pm25_buffer, regression_result
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
            if len(cmd) == 4:
                current_mode = cmd[0]
                last3 = cmd[1:]

                if current_mode == '1' or current_mode == '2':
                    longitude = int(last3)
                    current_station = "Zhongzheng" if longitude < 121 else "Nangang"
                    if current_mode == '1':
                        client.publish(TOPIC_SEND, current_station)  # 向電腦請求站點最後一行
                    elif current_mode == '2':
                        # Mode 2 啟動，等待 PM2.5 數據並存入 CSV 檔案
                        print(f"Entering Mode 2: Storing PM2.5 data for {current_station}.")

                elif current_mode == '3':
                    # Mode 3 啟動：停止上傳 PM2.5 值，開始風險預測
                    user_code = "user" + last3
                    print(f"Entering Mode 3: Fetching risk data for {user_code}.")
                    # 從 risk.csv 中提取對應行的數據
                    risk_file = "./risk.csv"
                    try:
                        with open(risk_file, "r", encoding="utf-8") as f:
                            reader = csv.reader(f)
                            for row in reader:
                                if row[0] == user_code:  # 找到對應使用者編號的行
                                    m, b, cor, p = map(float, row[1:5])  # 提取 4 個數字
                                    # 計算風險
                                    regression_result = risk_prediction(m, b, cor, p, pm25_buffer)
                                    print(f"Risk Prediction: {regression_result}")
                                    break
                    except FileNotFoundError:
                        print("Error: risk.csv not found.")
                        regression_result = None

                elif current_mode == '4':
                    # Mode 4 啟動：回傳風險預測結果和 PM2.5 值
                    if regression_result is not None and pm25_buffer is not None:
                        result_msg = f"Risk:{regression_result}, PM2.5:{pm25_buffer}"
                        ser.write((result_msg + "\n").encode('utf-8'))
                        print(f"Sent to Arduino: {result_msg}")

            else:
                # Mode 2 時接收 PM2.5 值
                if current_mode == '2':
                    try:
                        pm25 = float(cmd)
                        pm25_buffer = pm25  # 儲存最新 PM2.5 值
                        print(f"Received PM2.5: {pm25} μg/m³ for {current_station}")

                        # 將資料存入對應測站的 CSV
                        data_folder = "./air_quality/"
                        if not os.path.exists(data_folder):
                            os.makedirs(data_folder)
                        file_path = os.path.join(data_folder, f"{current_station}.csv")
                        file_exists = os.path.exists(file_path)
                        with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
                            writer = csv.writer(csvfile)
                            if not file_exists:
                                writer.writerow(["Station", "Date", "AQI", "PM2.5"])
                            now = datetime.now().strftime("%Y/%m/%d %H:%M")
                            writer.writerow([current_station, now, "N/A", pm25])
                        print(f"Saved PM2.5 data to {file_path}.")
                    except ValueError:
                        print("Invalid PM2.5 value received.")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
