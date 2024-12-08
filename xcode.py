# 創建專案
# 打開 XCode，選擇 App 專案模板。
# 設定 App 名稱和包名。
# 確保啟用藍牙權限，修改 Info.plist：

# <key>NSBluetoothAlwaysUsageDescription</key>
# <string>需要藍牙來接收數據</string>

import UIKit
import CoreBluetooth

class ViewController: UIViewController, CBCentralManagerDelegate, CBPeripheralDelegate {
    var centralManager: CBCentralManager!
    var peripheral: CBPeripheral!

    override func viewDidLoad() {
        super.viewDidLoad()
        centralManager = CBCentralManager(delegate: self, queue: nil)
    }

    // 藍牙狀態更新
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        if central.state == .poweredOn {
            central.scanForPeripherals(withServices: nil, options: nil)
        } else {
            print("藍牙未開啟或不支援")
        }
    }

    // 發現藍牙設備
    func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {
        self.peripheral = peripheral
        central.stopScan()
        central.connect(peripheral, options: nil)
    }

    // 已連接設備
    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        peripheral.delegate = self
        peripheral.discoverServices(nil)
    }

    // 接收數據
    func peripheral(_ peripheral: CBPeripheral, didUpdateValueFor characteristic: CBCharacteristic, error: Error?) {
        guard let data = characteristic.value else { return }
        let receivedString = String(data: data, encoding: .utf8)
        print("收到數據: \(receivedString!)")
        
        // 數據處理和風險分析邏輯
        analyzeRisk(from: receivedString!)
    }

    // 分析風險
    func analyzeRisk(from data: String) {
        // 假設資料格式為 CSV，處理風險計算邏輯
        // 更新 UI 顯示風險結果
        DispatchQueue.main.async {
            // 更新 UI
        }
    }
}

# 結果呈現與測試

# 流程
# 在樹莓派上啟動資料收集程式。
# 確保手機藍牙開啟，配對 HC-05/06 模組。
# 啟動手機 App，開始接收數據。
# 手機端根據回歸分析結果顯示風險，例如：
# 綠色：心率正常。
# 黃色：心率異常。
# 紅色：高度危險。
# 測試與優化
# 測試數據準確性和回歸結果。
# 調整藍牙傳輸間隔以優化性能。
# 確保手機端顯示友好並符合需求。
# 這整個過程提供了完整的數據流、分析和視覺化框架，可根據需求進一步擴展和優化！