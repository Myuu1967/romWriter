import sys

def hexdump(file_path, bytes_per_line=32):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: ファイル '{file_path}' が見つかりません")
        return

    for i in range(0, len(data), bytes_per_line):
        chunk = data[i:i + bytes_per_line]
        hex_part = ' '.join(f"{b:02X}" for b in chunk)
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print(f"{i:08X}  {hex_part:<48}  {ascii_part}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python hexdump.py <binファイル名>")
    else:
        hexdump(sys.argv[1])
