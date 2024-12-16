import serial

# 設定 Serial 通訊參數
SERIAL_PORT = '/dev/ttyACM0'  # 根據實際情況，若 Arduino 是第一個 USB 設備，則通常為 ttyUSB0
BAUD_RATE = 9600

def main():
    try:
        # 打開 Serial 連接
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
       
        while True:
            # 從 Arduino 接收數據
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                print(f"Received PM2.5 Value: {data} μg/m³")

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Program stopped by user.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")

if __name__ == "__main__":
    main()