import serial
import time
import numpy as np

# ポート設定
serial_port = 'COM16'
baud_rate = 9600
# bin_filename = 'GRANTBAS.bin' # 送信するバイナリファイル名

# data_set = np.zeros(256)
data_set = []
for i in range(256):  # 128 * 256 = 32768
    data_set.append(i)

ser = serial.Serial(serial_port, baud_rate, timeout=1)
print("UARTに接続しました。")

p = 0
# with open(bin_filename, 'rb') as f:
    # while True:
    #     data = f.read(256)  # バッファサイズ（256バイトずつ送信）
    #     if not data:
    #         break
    #     # ser.write(data_set)
    #     ser.write(data)
    #     time.sleep(0.01)  # 送信速度調整のための待機
for i in range(8):
    # バッファサイズ（256バイトずつ送信）
    ser.write(data_set)
    # ser.write(data)
    time.sleep(0.001)  # 送信速度調整のための待機

print("送信完了しました。")

