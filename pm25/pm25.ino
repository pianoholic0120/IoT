#include <SoftwareSerial.h>
//#include <SeeedOLED.h>
///#include <Wire.h>

SoftwareSerial BTSerial(0, 1); // Rx, Tx for HC-05
int measurePin = A0; 
int ledPower = 2;

int samplingTime = 280;    
int deltaTime = 40;        
int sleepTime = 9680;      

float voMeasured = 0;      
float calcVoltage = 0;     
float dustDensity = 0;     
bool uploadMode = false;
char mode='0';
String userCode = "";
String longitude = "";
bool waitingForResult = false;

void setup() {
  Serial.begin(9600); 
  BTSerial.begin(9600);
  pinMode(ledPower, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  //Wire.begin();
  //SeeedOled.init();
  //SeeedOled.clearDisplay();
  //SeeedOled.setNormalDisplay();
  //SeeedOled.setPageMode();
  //SeeedOled.setTextXY(0,0);
}

void loop() {
  // 從手機(HC-05)接收指令
  //Serial.print("HEllo\n");
  if (BTSerial.available()) {
    //Serial.print("H\n");
    String cmd = BTSerial.readStringUntil('\n');
    cmd.trim();
    //Serial.print(cmd);
    //Serial.print("\n");
    if (cmd.length()==4) {
      mode = cmd.charAt(0);
      String last3 = cmd.substring(1); 
      if (mode=='1'||mode=='2') {
        longitude = last3;
        //Serial.print(cmd);
        Serial.println(cmd); // 直接將指令傳給RPi
        //Serial.print("\n");
      } else if (mode=='3'||mode=='4') {
        userCode = last3; 
        //Serial.print(cmd);
        Serial.println(cmd);
        //Serial.print("\n");
      }
    }
  }

  // 若是模式2，Arduino應該偵測PM2.5並上傳給RPi
  // 但實際上PM2.5的上傳應由RPi詢問或定期執行，這裡先每秒讀取一次並上傳(需RPi配合)
  if (mode=='2'|| mode == '1'|| mode == '3' || mode == '4') {
    measurePM25AndPrint();
  }

  // 從RPi接收資料(如最後一行或回歸結果)
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    // 若為回傳的資訊(如模式1取得最後一行資料，或模式4取得回歸結果)
    // 模式1: PC回傳站點最後一行資料 -> Arduino需轉發給手機
    // 模式4: PC回傳回歸結果與PM2.5 -> Arduino需轉發給手機
    if (mode=='1' || mode=='4') {
      //data = float(data);
      data.toFloat();
      Serial.println(data);
      BTSerial.print(data); 
    }
    data.toFloat();
    
    //Serial.print(data);
    
  }
}

void measurePM25AndPrint() {
  digitalWrite(ledPower, LOW);
  delayMicroseconds(samplingTime);
  voMeasured = analogRead(measurePin);
  delayMicroseconds(deltaTime);
  digitalWrite(ledPower, HIGH);
  delayMicroseconds(sleepTime);

  calcVoltage = voMeasured * (5.0 / 1024.0);
  dustDensity = 0.17 * calcVoltage - 0.1;
  if (dustDensity < 0) dustDensity = 0;

  float pm25_ugm3 = dustDensity * 1000;
  // 超過安全值(假設50ug/m3)就亮LED
  if (pm25_ugm3 > 50) {
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    digitalWrite(LED_BUILTIN, LOW);
  }

  // 將pm2.5資料傳給RPi
  // 格式可自行定義，這裡直接傳pm2.5值
  Serial.println(pm25_ugm3);
  delay(1000);
}

