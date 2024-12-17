import os
import serial
import re
import time
import threading
from datetime import datetime
import paho.mqtt.client as mqtt

# 串列通訊設定
SERIAL_PORT = '/dev/ttyACM0'  # 根據實際情況選擇，通常是 ttyACM0 或 ttyUSB0
BAUD_RATE = 9600

# MQTT 設定
BROKER_ADDRESS = "10.47.101.223"  # 電腦端 MQTT Broker 的 IP
TOPIC_SEND = "hello/group1/rpi2pc"  # 上行 Topic：樹莓派傳送給電腦
TOPIC_RECEIVE = "hello/group1/pc2rpi"  # 下行 Topic：電腦回傳給樹莓派

# MQTT 客戶端
client = mqtt.Client()

# 全域變數
current_station = "Da'an"  # 預設測站名稱
upload_data = False  # 是否上傳資料
stop_thread = False  # 控制程式結束的旗標


def extract_pm25(data):
    """從接收到的字串中提取 PM2.5 數值"""
    match = re.search(r"Dust Density: ([\-\d.]+) ug/m3", data)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None


def on_connect(client, userdata, flags, rc):
    """MQTT 連接成功的回調函數"""
    print("Connected to MQTT broker with result code:", rc)
    client.subscribe(TOPIC_RECEIVE)  # 訂閱電腦端回傳的資料 Topic


def on_message(client, userdata, msg):
    """接收電腦端傳回資料的回調函數"""
    payload = msg.payload.decode("utf-8").strip()
    print(f"Data received from PC: {payload}")


def send_station_name():
    """發送測站名稱到電腦端"""
    client.publish(TOPIC_SEND, f"{current_station}")
    print(f"Sent station name: {current_station} to PC")


def upload_pm25_data(ser):
    """從 Arduino 持續讀取 PM2.5 數據並上傳到電腦端"""
    global stop_thread
    while not stop_thread:
        if upload_data and ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            pm25 = extract_pm25(data)
            if pm25 is not None:
                now = datetime.now().strftime("%Y/%m/%d %H:%M")
                print(f"[{now}] PM2.5: {pm25:.2f} μg/m³ at {current_station}")
                client.publish(TOPIC_SEND, f"{pm25:.2f}")
                print(f"Sent PM2.5 data to PC: {pm25:.2f} μg/m³")
            else:
                print("Invalid PM2.5 data format from Arduino.")
        time.sleep(1)  # 每秒檢查一次串列資料


def main():
    global current_station, upload_data, stop_thread
    try:
        # 初始化 MQTT
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(BROKER_ADDRESS)
        client.loop_start()

        # 初始化串列通訊
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.\n")

        # 使用者決定是否上傳資料
        user_input = input("Do you want to upload PM2.5 data? (y/n): ").strip().lower()
        upload_data = user_input == 'y'

        # 輸入測站名稱
        station_input = input("Please enter the station name (or press Enter to skip): ").strip()
        if station_input:
            current_station = station_input
        print(f"Current station: {current_station}")
        send_station_name()

        # 啟動 PM2.5 資料上傳執行緒
        upload_thread = threading.Thread(target=upload_pm25_data, args=(ser,))
        upload_thread.start()

        # 非阻塞輸入，用來更新測站名稱
        while True:
            new_station_input = input("Enter new station name to update (or press Enter to skip): ").strip()
            if new_station_input:
                current_station = new_station_input
                send_station_name()
                print(f"Station updated to: {current_station}")

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Program stopped by user.")
    finally:
        stop_thread = True  # 結束執行緒
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")
        client.loop_stop()
        print("MQTT connection closed.")


if __name__ == "__main__":
    main()