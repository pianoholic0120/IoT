# Virtual Environment

    source ./final/bin/activate

# Converting Garmin FIT to CSV 

First, install `fitparse`

    sudo pip3 install fitparse

Then you can execute 

    python3 fit_to_csv.py

This will create a bunch of CSVs for all of your workouts in that directory (You will be asked to enter the directory in terminal after running fit_to_csv.py). The files will be stored in the directory you designate. 

# Parsing data from Garmin Account Management

Execute

    python3 parse_and_sort_data.py

This will create a csv file, 'merged_and_sorted_with_filled_timestamps.csv',containing the corresponding data (heart_rate and timestamp) from csv files in the user-designated directory. The parsed file contains two columns, heart_rate and timestamp, where the data is presented in sequence following the timestamp chronologically.

# Arduino codes with GP2Y10 data sending to Raspberry Pi 
* using SERIAL_PORT = /dev/ttyACM0
* verify and compile the Arduino code first under the path **./Arduino_pm2.5/Arduino_pm2.5.ino**
* connecting Arduino and Raspberry Pi using usb cable

## Prerequisites

    pip3 install paho-mqtt


## i. Execute the following code on computer

    cd ./Computer/
    python3 main.py

## ii. Send the location to the computer through MQTT with Raspberry Pi

The computer will locate the location and either fetch the data from the backend if available or appending the given data from Raspberry Pi to its database.

    mosquitto_pub -h <your ip(inet)> -d -t hello/group1/rpi2pc -m "<your location>" 

for instance, 

    mosquitto_pub -h 127.0.0.1 -d -t hello/group1/rpi2pc -m "Taipei" 
the procedure is optional, if not provided, the location will utilize Da'an as default.

## iii. Execute the following code on Raspberry Pi

    python3 rpi_pm25_to_pc.py
this will obtain the data from Arduino and send it to the northbound with the computer backend


### 傳輸概述：

首先會用手機利用HC-05透過Arduino發送訊息給樹莓派，格式會是包含四個數字的string，例如：‘1120', '2121', '3002', '4001'，第一個數字代表模式，‘1’表示需從電腦調用對應資料而不會傳遞pm2.5偵測器的資料，'2'表示把Arduino收集到的PM2.5資料傳給樹莓派並請上傳電腦，'3'則是開始進行回歸計算，‘4’則表示rpi要把回歸結果資料傳回給Arduino，並且Arduino要能夠把回傳值傳回給手機（回傳值包含回歸結果數字和PM2.5數值），第一位'1'和'2'後面跟著的三位數字表示東經經度，若小於121則需向電腦調用Zhongzheng站的csv資料，反之則是用Nangang站的資料，而第一位'3'和'4'後面的三個數字則表示使用者代號，也就是要使用第幾個使用者的代號做回歸運算，也因此要使用該使用者的對應csv檔案計算回歸。Rpi需根據收到的Arduino string訊號做不同的任務，依情況適當寫入電腦中對應的檔案或是從電腦提取對應檔案中最後一行的資料等，並且當Arduino 偵測的PM2.5值超過安全值時讓Arduino的LED燈亮起。
