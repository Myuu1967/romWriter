import serial
import os
import datetime
import re
import sys

# === ROM種別一覧（番号指定用）===
ROM_OPTIONS = {
    0: ("2716", 2048),
    1: ("2732", 4096),
    2: ("2764", 8192),
    3: ("27128", 16384),
    4: ("27256", 32768),
    5: ("27512", 65536)
}

# === 設定 ===
ROM_SELECT = 3  # ← 0〜5の番号を指定
COM_PORT = "COM12"
BAUDRATE = 115200

# ROM情報取得
ROM_INFO = ROM_OPTIONS.get(ROM_SELECT)
if ROM_INFO is None:
    print(f"未定義のROM番号: {ROM_SELECT}")
    sys.exit(1)

ROM_TYPE, ROM_SIZE = ROM_INFO

def get_next_filename(base_dir):
    # 保存先ディレクトリ
    data_dir = os.path.join(base_dir, "oke", "Pico", "2025", "ROM", "PCside", "data")
    os.makedirs(data_dir, exist_ok=True)

    # 今日の日付
    today = datetime.datetime.now().strftime("%Y%m%d")
    pattern = re.compile(rf"rom_dump_{today}(\d{{2}})\.bin")

    max_counter = -1
    for filename in os.listdir(data_dir):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))
            max_counter = max(max_counter, num)

    next_counter = max_counter + 1
    while True:
        filename = f"rom_dump_{today}{next_counter:02d}.bin"
        full_path = os.path.join(data_dir, filename)
        if not os.path.exists(full_path):
            return full_path
        next_counter += 1

def print_progress(current, total, bar_length=40):
    percent = current / total
    filled_len = int(bar_length * percent)
    bar = "█" * filled_len + "-" * (bar_length - filled_len)
    print(f"\r[{bar}] {percent * 100:5.1f}% ({current}/{total} bytes)", end='')

def main():
    base_drive = "F:\\"
    next_file_path = get_next_filename(base_drive)
    print(f"次に保存するファイル: {next_file_path}")
    print(f"ROMタイプ: {ROM_TYPE}（{ROM_SIZE}バイト）")
    print("Picoからのデータを待機中...")

    # シリアルポートを開く
    try:
        ser = serial.Serial(COM_PORT, BAUDRATE, timeout=None)
    except serial.SerialException as e:
        print(f"シリアルポートのオープンに失敗しました: {e}")
        return

    received_data = 0

    try:
        with open(next_file_path, "wb") as f:
            while received_data < ROM_SIZE:
                chunk_size = min(1024, ROM_SIZE - received_data)
                data = ser.read(chunk_size)

                if data:
                    f.write(data)
                    received_data += len(data)
                    print_progress(received_data, ROM_SIZE)
                else:
                    print("\nデータの受信がタイムアウトしました。")
                    break

        if received_data == ROM_SIZE:
            print("\nROMデータを正常に受信し、保存しました！")
        else:
            print(f"\n受信が不完全です: {received_data} / {ROM_SIZE} バイト")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
