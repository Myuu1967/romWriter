from machine import Pin, UART
import utime
import gc, sys

def writeByte(val):
    """
    1バイトのデータをシフトレジスタに書き込む。

    Args:
        val (int): 書き込む1バイトデータ
    """
    for i in range(8):
        clk.value(0)
        bit = ((val << i) & 0b10000000)>>7
        sdi.value(bit)
        clk.value(1)
        utime.sleep_us(period)

def setAddress(address):
    upper = (address >> 8) & 0xFF
    lower = address & 0xFF

    latch.value(0)
    writeByte(upper)   # upper bit
    writeByte(lower)   # lower bit
    latch.value(1)
#     utime.sleep_us(1)

def setData(data):
    """指定アドレスにデータをセットする"""
    for i, pin in enumerate(dataPins):
        pin.value((byte >> i) & 1)
#     utime.sleep_us(1)

def setDataPinInput():
    global dataPins
    dir_245.value(0)    # value: 0:B-> A, 1:A-> B
    dataPins = [Pin(i, Pin.IN, Pin.PULL_DOWN) for i in dataPinList]

def setDataPinOutput():
    global dataPins
    dir_245.value(1)    # value: 0:B-> A, 1:A-> B
    dataPins = [Pin(i, Pin.OUT) for i in dataPinList]

def readByteFromBus():
    return sum(pin.value() << i for i, pin in enumerate(dataPins))

def genericWriteToROM(buffer, size, write_count, setup_pins, \
                      pulse_func, verify_func):
    address = 0
    progress_mark = 0  # 表示済みの進捗（10%, 20%, ...）

    setDataPinOutput()
    setup_pins()  # 各ROM固有の初期設定

    for data in buffer:
        setAddress(address)
        n = 0
        while n < write_count:
            setData(data)
            utime.sleep_us(3)
            pulse_func()  # 各ROM固有の書き込みパルス操作
            utime.sleep_us(3)

            setDataPinInput()
            utime.sleep_us(3)
            read_value = verify_func()
            utime.sleep_us(2)
            
            if read_value == data:
                break
            n += 1
            setDataPinOutput()

        address += 1
        #進捗状況を表示させる
        new_mark = int((address / size) * 10)
        if new_mark > progress_mark:
            progress_mark = new_mark
            if progress_mark == 10:
                print("100% completed!!")
            else:
                print(f"{progress_mark * 10}% arrived...")

    VPP.value(0)

def writeDataToROM_2716(buffer, size):
    def setup():
        VPP.value(1)
        _CE.value(0)
        _OE.value(1)

    def pulse():
        _CE.value(1)
        utime.sleep_ms(50)
        _CE.value(0)

    def verify():
        _OE.value(0)
        utime.sleep_us(2)
        value = readByteFromBus()
        _OE.value(1)
        return value

    genericWriteToROM(buffer, size, write_count=10, setup_pins=setup, pulse_func=pulse, verify_func=verify)


def writeDataToROM_2732(buffer, size):
    def setup():
        _CE.value(1)  # 最初に無効化しておく
        VPP.value(1)

    def pulse():
        _CE.value(0)
        utime.sleep_ms(50)
        _CE.value(1)
        utime.sleep_us(3)
        VPP.value(0)

    def verify():
        utime.sleep_us(3)
        _CE.value(0)
        utime.sleep_us(2)
        value = readByteFromBus()
        _CE.value(1)
        utime.sleep_us(1)
        VPP.value(1)
        return value

    genericWriteToROM(buffer, size, write_count=10, setup_pins=setup, pulse_func=pulse, verify_func=verify)

def writeDataToROM_2764(buffer, size):
    def setup():
        VPP.value(1)
        _CE.value(0)
        _OE.value(1)
        _PGM.value(1)

    def pulse():
        _PGM.value(0)
        utime.sleep_ms(1)
        _PGM.value(1)

    def verify():
        _OE.value(0)
        utime.sleep_us(2)
        value = readByteFromBus()
        _OE.value(1)
        return value

    genericWriteToROM(buffer, size, write_count=16, setup_pins=setup, pulse_func=pulse, verify_func=verify)

def writeDataToROM_27128(buffer, size):
    def setup():
        VPP.value(1)
        _CE.value(0)
        _PGM.value(1)
        _OE.value(1)

    def pulse():
        _PGM.value(0)
        utime.sleep_ms(1)
        _PGM.value(1)

    def verify():
        _OE.value(0)
        utime.sleep_us(2)
        value = readByteFromBus()
        _OE.value(1)
        return value

    genericWriteToROM(buffer, size, write_count=16, setup_pins=setup, pulse_func=pulse, verify_func=verify)

def writeDataToROM_27256(buffer, size):
    def setup():
        VPP.value(1)
        _CE.value(1)
        _OE.value(1)

    def pulse():
        _CE.value(0)
        utime.sleep_ms(1)
        _CE.value(1)

    def verify():
        utime.sleep_us(5)
        _OE.value(0)
        utime.sleep_us(2)
        value = readByteFromBus()
        _OE.value(1)
        return value

    genericWriteToROM(buffer, size, write_count=16, setup_pins=setup, pulse_func=pulse, verify_func=verify)

def writeDataToROM_27512(buffer, size):
    def setup():
        VPP.value(1)
        _CE.value(1)

    def pulse():
        _CE.value(0)
        utime.sleep_ms(1)
        _CE.value(1)
        utime.sleep_us(3)
        VPP.value(0)

    def verify():
        _CE.value(0)
        utime.sleep_us(2)
        value = readByteFromBus()
        _CE.value(1)
        VPP.value(1)
        return value

    genericWriteToROM(buffer, size, write_count=25, setup_pins=setup, pulse_func=pulse, verify_func=verify)

def eraceLEDs():
#     led25.value(0)

    for pin in pins:  # GP2~GP9
        pin.value(0)

    dir_245.value(1)    # value: 0:B-> A, 1:A-> B
    for dataPin in dataPins:  # GP10~GP17
        dataPin.value(0)

    latch.value(0)
    writeByte(0)
    writeByte(0)
    latch.value(1)

    dir_245.value(0)    # value: 0:B-> A, 1:A-> B

    VPP.value(0)    # GP6
    _CE.value(0)    # GP7
    _OE.value(0)    # GP8
    _PGM.value(0)   # GP9

# main routine

# GPIOピンの設定（GP2〜GP9を出力）
pinList = list(range(2, 10))
pins = [Pin(i, Pin.OUT) for i in pinList]

# GPIOピンの設定（GP10〜GP17を出力）
dataPinList = list(range(10, 18))
dataPins = [Pin(i, Pin.OUT) for i in dataPinList]

sdi   = pins[0]     # GP2
clk   = pins[1]     # GP3
latch = pins[2]     # GP4

# 74HC595に1バイト書き込んだ後のの待ち時間
# writeByte(val)内で使用
period = 2

dir_245 = pins[3]   # GP5
dir_245.value(1)    # value: 0:B-> A, 1:A-> B

VPP = pins[4]     # GP6
_CE  = pins[5]     # GP7
_OE  = pins[6]     # GP8
_PGM  = pins[7]     # GP9

VPP.value(0)    # GP6   VPP
_CE.value(0)     # GP7   _CE
_OE.value(0)     # GP8   _OE
_PGM.value(0)     # GP9   _PGM

# --- ROM情報（容量と書き込み関数） ---
ROM_INFO = {
    2716:   {"size": 2048,   "write_func": writeDataToROM_2716},
    2732:   {"size": 4096,   "write_func": writeDataToROM_2732},
    2764:   {"size": 8192,   "write_func": writeDataToROM_2764},
    27128:  {"size": 16384,  "write_func": writeDataToROM_27128},
    27256:  {"size": 32768,  "write_func": writeDataToROM_27256},
    27512:  {"size": 65536,  "write_func": writeDataToROM_27512},
}

# --- ROMタイプ指定 ---
RomType = 2716  # ←ここを変更するだけでOK！

# --- ROM情報の取得 ---
rom_info = ROM_INFO.get(RomType)

if rom_info is None:
    print(f"未対応のROMタイプ: {RomType}")
    sys.exit()

target_size = rom_info["size"]
write_func = rom_info["write_func"]

# --- UARTとLED初期化 ---
uart = UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))
led25 = machine.Pin(25, machine.Pin.OUT)
led25.value(0)

# --- バッファ初期化 ---
gc.collect()
received_buffer = bytearray()

print("UART受信開始(Ctrl+Cで中止可能)")

# --- 受信処理 ---
try:
    while len(received_buffer) < target_size:
        if uart.any():
            data = uart.read()
            if data:
                received_buffer += data
                print(f"{len(data)} bytes 受信, 合計: {len(received_buffer)} bytes")
        utime.sleep_ms(2)

    print("受信完了、ROM書き込み開始")
    start_time = utime.ticks_ms()

    # --- 書き込み実行 ---
    write_func(received_buffer, target_size)

    end_time = utime.ticks_ms()
    elapsed_time = utime.ticks_diff(end_time, start_time)

    print("ROMへの書き込み完了")
    led25.value(1)
    print(f"経過時間: {elapsed_time} [ms]")

# --- 割り込み時処理 ---
except KeyboardInterrupt:
    print("Ctrl+Cにより処理を中断しました。")
    uart.deinit()
    eraceLEDs()
    sys.exit()

# --- エラー時処理 ---
except Exception as e:
    print(f"異常が発生しました: {e}")
    uart.deinit()
    eraceLEDs()
    sys.exit()

# --- 終了処理 ---
finally:
    print("安全に終了しました")
    uart.deinit()
    eraceLEDs()