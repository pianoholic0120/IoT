import os
import csv
import paho.mqtt.client as mqtt

BROKER_ADDRESS = "10.47.250.117"
TOPIC_SEND = "hello/group1/pc2rpi"
TOPIC_RECEIVE = "hello/group1/rpi2pc"

DATA_FOLDER = "./air_quality/"
USER_FOLDER = "./users/"
RESULT_FOLDER = "./users_results/"

def on_connect(client, userdata, flags, rc):
    print("PC: Connected to MQTT broker:", rc)
    client.subscribe(TOPIC_RECEIVE)

def read_last_line(file_path):
    if not os.path.exists(file_path):
        return "No history data"
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if len(lines)>1:
        return lines[-1].strip()
    else:
        return "No history data"

def do_regression(user_code):
    # 模擬回歸計算
    user_file = os.path.join(USER_FOLDER, f"{user_code}.csv")
    if not os.path.exists(user_file):
        return "No user data"
    # 假設回歸結果為 "Result:0.95, PM2.5:30"
    result = "Result:0.95, PM2.5:30"
    if not os.path.exists(RESULT_FOLDER):
        os.makedirs(RESULT_FOLDER)
    with open(os.path.join(RESULT_FOLDER, f"{user_code}_result.txt"), "w") as f:
        f.write(result)
    return "REG_DONE"

def get_regression_result(user_code):
    result_file = os.path.join(RESULT_FOLDER, f"{user_code}_result.txt")
    if os.path.exists(result_file):
        with open(result_file, "r") as f:
            return f.read().strip()
    return "No regression result"

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8').strip()
    print("PC received from RPi:", payload)
    # 判斷指令
    if payload in ["Zhongzheng","Nangang"]:
        # 回傳最後一行
        file_path = os.path.join(DATA_FOLDER, f"{payload}.csv")
        last_line = read_last_line(file_path)
        client.publish(TOPIC_SEND, last_line)

    elif "," in payload:
        # 可能是REGCALC,userXXX 或 REGRESULT,userXXX 或 station,pm25
        parts = payload.split(",")
        if parts[0] == "REGCALC":
            user_code = parts[1]
            status = do_regression(user_code)
            client.publish(TOPIC_SEND, status)
        elif parts[0] == "REGRESULT":
            user_code = parts[1]
            res = get_regression_result(user_code)
            client.publish(TOPIC_SEND, res)
        else:
            # station,pm25
            station = parts[0]
            pm25 = parts[1]
            file_path = os.path.join(DATA_FOLDER, f"{station}.csv")
            file_exists = os.path.exists(file_path)
            with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(["Station","Date","AQI","PM2.5"])
                from datetime import datetime
                now = datetime.now().strftime("%Y/%m/%d %H:%M")
                writer.writerow([station, now, "N/A", pm25])
            client.publish(TOPIC_SEND, f"Data for {station} updated: {pm25}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_ADDRESS)
client.loop_forever()
