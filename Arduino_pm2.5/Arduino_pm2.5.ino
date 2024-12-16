int measurePin = 0; // Connect dust sensor to Arduino A0 pin
int ledPower = 2;   // Connect dust sensor LED pin to Arduino D2

int samplingTime = 280;    // LED 開啟時間 (微秒)
int deltaTime = 40;        // 等待穩定時間
int sleepTime = 9680;      // LED 關閉時間

float voMeasured = 0;      // ADC 讀取的值
float calcVoltage = 0;     // 計算後的電壓值
float dustDensity = 0;     // PM2.5 濃度值 (mg/m³)

void setup() {
  Serial.begin(9600); // 設定 Serial 傳輸速率
  pinMode(ledPower, OUTPUT);
}

void loop() {
  // 啟動 LED，讀取 GP2Y10 感測器值
  digitalWrite(ledPower, LOW); // 啟動 LED
  delayMicroseconds(samplingTime);

  voMeasured = analogRead(measurePin); // 讀取 ADC 數值 (0-1023)
  delayMicroseconds(deltaTime);

  digitalWrite(ledPower, HIGH); // 關閉 LED
  delayMicroseconds(sleepTime);

  // 將 ADC 數值轉換為電壓 (5V 電源)
  calcVoltage = voMeasured * (5.0 / 1024.0);

  // 根據 GP2Y10 線性方程式計算 PM2.5 濃度 (mg/m3)
  dustDensity = 0.17 * calcVoltage - 0.1;

  // 避免濃度出現負值
  if (dustDensity < 0) {
    dustDensity = 0;
  }

  // 輸出原始電壓和 PM2.5 濃度 (μg/m3)
  Serial.print("Raw Signal Value (0-1023): ");
  Serial.print(voMeasured);

  Serial.print(" - Voltage: ");
  Serial.print(calcVoltage, 2); // 保留 2 位小數

  Serial.print(" - Dust Density: ");
  Serial.print(dustDensity * 1000, 2); // 轉換為 μg/m³
  Serial.println(" ug/m3");

  delay(1000); // 每秒輸出一次數據
}
