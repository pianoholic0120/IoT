import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

file_name = input("請輸入要分析的檔案名稱（包含路徑）：")

try:
    df = pd.read_csv(file_name)
    if 'Time' not in df.columns:
        raise ValueError("CSV 檔案必須包含 'Time' 列")
except Exception as e:
    print(f"讀取檔案時發生錯誤：{e}")
    exit()

print("可用的列名稱：")
print(df.columns.tolist())

x_axis = input("請選擇作為 x 軸的列名稱：")
y_axis = input("請選擇作為 y 軸的列名稱：")

if x_axis not in df.columns or y_axis not in df.columns:
    print("所選的列名稱不存在於資料中，請確認後再試。")
    exit()

if x_axis == 'Time':
    df[x_axis] = pd.to_datetime(df[x_axis])

plt.figure(figsize=(12, 6))
plt.plot(df[x_axis], df[y_axis], marker='o', linestyle='-', label=y_axis)
plt.title(f'{y_axis} Over {x_axis}', fontsize=14)
plt.xlabel(x_axis, fontsize=12)
plt.ylabel(y_axis, fontsize=12)

if x_axis == 'Time':
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))

plt.grid(visible=True)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.hist(df[y_axis], bins=10, color='skyblue', edgecolor='black')
plt.title(f'Histogram of {y_axis}', fontsize=14)
plt.xlabel(y_axis, fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

plt.figure(figsize=(6, 6))
plt.boxplot(df[y_axis], patch_artist=True)
plt.title(f'Box Plot of {y_axis}', fontsize=14)
plt.ylabel(y_axis, fontsize=12)
plt.grid(axis='y')
plt.tight_layout()
plt.show()
