import serial
import re
import paho.mqtt.client as mqtt

# 串列通訊設定
SERIAL_PORT = '/dev/ttyACM0'  # 根據實際情況選擇，通常是 ttyACM0 或 ttyUSB0
BAUD_RATE = 9600

# MQTT 設定
BROKER_ADDRESS = "192.168.0.197"  # 電腦端 MQTT Broker 的 IP
TOPIC_SEND = "hello/group1/rpi2pc"  # 上行 Topic：樹莓派傳送給電腦

# 初始化 MQTT
client = mqtt.Client()

def extract_pm25(data):
    """
    從接收到的字串中提取 PM2.5 數值。
    格式範例: "Raw Signal Value (0-1023): 62.00 - Voltage: 0.30 - Dust Density: -31.93 ug/m3"
    """
    match = re.search(r"Dust Density: ([\-\d.]+) ug/m3", data)
    if match:
        try:
            pm25_value = float(match.group(1))  # 提取數值並轉換為浮點數
            return pm25_value
        except ValueError:
            return None
    return None

def main():
    try:
        # 初始化 MQTT 連接
        client.connect(BROKER_ADDRESS)
        client.loop_start()

        # 打開 Serial 連接
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
        
        while True:
            # 從 Arduino 接收數據
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                print(f"Raw Data Received: {data}")

                # 提取 PM2.5 數值
                pm25 = extract_pm25(data)
                if pm25 is not None:
                    print(f"Extracted PM2.5 Value: {pm25:.2f} μg/m³")
                    
                    # 發送數值到電腦端 (MQTT)
                    client.publish(TOPIC_SEND, f"{pm25:.2f}")
                    print(f"Sent PM2.5 Value: {pm25:.2f} μg/m³")
                else:
                    print("No valid PM2.5 data found.")

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Program stopped by user.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")
        client.loop_stop()
        print("MQTT connection closed.")

if __name__ == "__main__":
    main()
