from machine import Pin, UART
import utime
import sys

ROM_SELECT = 3  # ← PC側と合わせて 0〜5 を選択

# --- ROM情報（容量と書き込み関数） ---
ROM_OPTIONS = {
    0: ("2716", 2048),
    1: ("2732", 4096),
    2: ("2764", 8192),
    3: ("27128", 16384),
    4: ("27256", 32768),
    5: ("27512", 65536),
}

# === 設定 ===
ROM_INFO = ROM_OPTIONS.get(ROM_SELECT)
if ROM_INFO is None:
    print(f"未定義のROM番号: {ROM_SELECT}")
    sys.exit()

ROM_TYPE, ROM_SIZE = ROM_INFO

# --- GPIO 初期化 ---
pinList = list(range(2, 10))
pins = [Pin(i, Pin.OUT) for i in pinList]
sdi, clk, latch, dir_245, VPP, _CE, _OE, _PGM = pins
dataPinList = list(range(10, 18))
dataPins = [Pin(i, Pin.IN, Pin.PULL_UP) for i in dataPinList]
led25 = Pin(25, Pin.OUT)
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

# --- 信号線初期化 ---
period = 1
led25.value(0)
dir_245.value(0) # value: 0:B-> A, 1:A-> B
VPP.value(1)
_CE.value(0)
_OE.value(0)
_PGM.value(1)

# --- 関数定義 ---
def writeByte(val):
    for i in range(8):
        clk.value(0)
        bit = ((val << i) & 0x80) >> 7
        sdi.value(bit)
        clk.value(1)
        utime.sleep_us(period)

def setAddress(address):
    upper = (address >> 8) & 0xFF
    lower = address & 0xFF
    latch.value(0)
    writeByte(upper)
    writeByte(lower)
    latch.value(1)

def readByteFromBus():
    return sum(pin.value() << i for i, pin in enumerate(dataPins))

def eraceLEDs():
    for i in range(3, 8):
        pins[i].value(0)
    for pin in dataPins:
        pin.init(Pin.OUT)
        pin.value(0)
    latch.value(0)
    writeByte(0)
    writeByte(0)
    latch.value(1)
    dir_245.value(1)

def readRom(size):
    for address in range(size):
        setAddress(address)
        utime.sleep_us(2)
        val = readByteFromBus()
        uart.write(val.to_bytes(1, 'little'))
        utime.sleep_us(2)

# --- メイン処理 ---
def main():
    print(f"ROMタイプ: {ROM_TYPE}, サイズ: {ROM_SIZE} バイト")
    start_time = utime.ticks_ms()

    try:
        led25.value(0)
        readRom(ROM_SIZE)
    except Exception as e:
        print("エラーが発生しました:", e)
    else:
        end_time = utime.ticks_ms()
        elapsed = utime.ticks_diff(end_time, start_time)
        print("転送完了")
        print(f"経過時間: {elapsed} ms")
        led25.value(1)
    finally:
        eraceLEDs()

# --- スクリプトが直接実行されたときだけ実行 ---
if __name__ == "__main__":
    main()
