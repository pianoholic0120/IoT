# 硬體準備
# 樹莓派 (Raspberry Pi)
# PM2.5 感測器（如 SDS011）
# 溫度感測器（如 DHT22）
# HC-05/06 藍牙模組
# 心率數據來源（可選用心率感測器或檔案數據）
# 硬體連接
# 連接 PM2.5 感測器：
# SDS011 使用 UART 介面，接到樹莓派的 GPIO Pins。
# 連接溫度感測器：
# DHT22 使用 GPIO 信號，需拉高電阻。
# 連接藍牙模組：
# TX, RX 分別接樹莓派 GPIO。

# sudo apt update
# sudo apt install python3-pip
# pip3 install pyserial Adafruit_DHT pandas numpy

import serial
import Adafruit_DHT
import time
import pandas as pd
import numpy as np
from scipy.stats import linregress
from datetime import datetime
import bluetooth

# PM2.5 感測器配置 (SDS011)
def read_pm25():
    ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=2)
    data = ser.read(10)
    if data[0] == 170 and data[1] == 192:
        pm25 = int.from_bytes(data[2:4], byteorder='little') / 10.0
        return pm25
    return None

# 溫度感測器配置 (DHT22)
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

def read_temp():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return temperature

# 模擬心率資料
def generate_heart_rate():
    return np.random.normal(80, 5)  # 平均心率 80, 標準差 5

# 資料收集
def collect_data():
    pm25 = read_pm25()
    temp = read_temp()
    heart_rate = generate_heart_rate()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return timestamp, pm25, temp, heart_rate

# 資料儲存與處理
def save_data_to_csv(data):
    df = pd.DataFrame(data, columns=['timestamp', 'pm25', 'temperature', 'heart_rate'])
    df.to_csv('sensor_data.csv', index=False)

# 分析資料
def analyze_data(df):
    # 平均與標準差
    stats = df.describe()
    print("統計數據:\n", stats)
    
    # 回歸分析
    regression = linregress(df['pm25'], df['heart_rate'])
    print(f"回歸結果: Slope={regression.slope}, Intercept={regression.intercept}, R-value={regression.rvalue}")

    return stats, regression

# 傳輸資料 (藍牙)
def send_data_via_bluetooth(data):
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_socket.bind(("", bluetooth.PORT_ANY))
    server_socket.listen(1)
    port = server_socket.getsockname()[1]
    print(f"等待連接，請在手機端搜尋此設備，端口號 {port}...")
    client_socket, address = server_socket.accept()
    print(f"已連接到 {address}")
    client_socket.send(data)
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    collected_data = []
    for _ in range(10):  # 收集10組數據
        collected_data.append(collect_data())
        time.sleep(2)

    save_data_to_csv(collected_data)
    df = pd.read_csv('sensor_data.csv')
    stats, regression = analyze_data(df)
    send_data_via_bluetooth(df.to_csv(index=False))