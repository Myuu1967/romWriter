from machine import Pin, UART
import utime
import gc, sys

def writeByte(val):  # 1byteの値を74HC595に書き込む
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
    global dataPins
    """指定アドレスにデータをセットする"""
    for i in range(8):
        num = (data >> i) & 1
        dataPins[i].value(num)
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
    global dataPins
    num = 0
    for i in range(8):
        num += (dataPins[i].value() << i)
    return num

def writeRom2716(buffer, size):
    address = 0
    progress_mark = 0  # 表示済みの進捗
    size_10 = size / 10
    write_count = 16
    errCnt = 0

    setDataPinOutput()
　　  # 各ROM固有の初期設定
    VPP.value(1)
    _CE.value(0)
    _OE.value(1)

    for data in buffer:
        setAddress(address)
        n = 0
        while n < write_count:
            setData(data)
            utime.sleep_us(3)
            
            # 各ROM固有の書き込みパルス操作
            _CE.value(1)
            utime.sleep_ms(50)
            _CE.value(0)
            utime.sleep_us(3)

            setDataPinInput()
            utime.sleep_us(3)
            _OE.value(0)
            utime.sleep_us(2)
            read_value = readByteFromBus()
            _OE.value(1)
            
            utime.sleep_us(2)
            
            if read_value == data:
                break
            n += 1
            setDataPinOutput()

            if n >= write_count:
                errCnt += 1

        if errCnt >= 100:
            VPP.value(0)
            break

        address += 1
        #進捗状況を表示させる
        new_mark = address // size_10
        if new_mark > progress_mark:
            progress_mark = new_mark
            if progress_mark == 10:
                print("100% completed!!")
            else:
                print(f"{progress_mark * 10}% arrived...")

    VPP.value(0)


def writeRom2732(buffer, size):
    address = 0
    progress_mark = 0  # 表示済みの進捗
    size_10 = size / 10
    write_count = 16
    errCnt = 0

    setDataPinOutput()
    _CE.value(1)  # 最初に無効化しておく
    VPP.value(1)

    for data in buffer:
        setAddress(address)
        n = 0
        while n < write_count:
            setData(data)
            utime.sleep_us(3)

            # 各ROM固有の書き込みパルス操作
            _CE.value(0)
            utime.sleep_ms(50)
            _CE.value(1)
            utime.sleep_us(3)

            VPP.value(0)
            utime.sleep_us(3)

            setDataPinInput()
            utime.sleep_us(3)
            _CE.value(0)
            utime.sleep_us(2)
            read_value = readByteFromBus()

            _CE.value(1)
            utime.sleep_us(1)

            VPP.value(1)
            utime.sleep_us(2)
            
            if read_value == data:
                break
            n += 1
            setDataPinOutput()

            if n >= write_count:
                errCnt += 1

        if errCnt >= 100:
            VPP.value(0)
            break

        address += 1
        #進捗状況を表示させる
        new_mark = address // size_10
        if new_mark > progress_mark:
            progress_mark = new_mark
            if progress_mark == 10:
                print("100% completed!!")
            else:
                print(f"{progress_mark * 10}% arrived...")

    VPP.value(0)
    
def writeRom2764(buffer, size):
    address = 0
    progress_mark = 0  # 表示済みの進捗
    size_10 = size / 10
    write_count = 25
    errCnt = 0

    setDataPinOutput()
    # 各ROM固有の初期設定
    VPP.value(1)
    _CE.value(0)
    _OE.value(1)
    _PGM.value(1)

    for data in buffer:
        setAddress(address)
        n = 0
        while n < write_count:
            setData(data)
            utime.sleep_us(3)
            # 各ROM固有の書き込みパルス操作
            _PGM.value(0)
            utime.sleep_ms(1)
            _PGM.value(1)
            utime.sleep_us(3)

            setDataPinInput()
            utime.sleep_us(3)
            _OE.value(0)
            utime.sleep_us(2)

            read_value = readByteFromBus()
            _OE.value(1)
            utime.sleep_us(2)
            
            if read_value == data:
                break
            n += 1
            setDataPinOutput()

            if n >= write_count:
                errCnt += 1

        if errCnt >= 100:
            VPP.value(0)
            break

        address += 1
        #進捗状況を表示させる
        new_mark = address // size_10
        if new_mark > progress_mark:
            progress_mark = new_mark
            if progress_mark == 10:
                print("100% completed!!")
            else:
                print(f"{progress_mark * 10}% arrived...")

    VPP.value(0)

def writeRom27128(buffer, size):
    address = 0
    progress_mark = 0  # 表示済みの進捗
    size_10 = size / 10
    write_count = 25
    errCnt = 0

    setDataPinOutput()
    # 各ROM固有の初期設定
    VPP.value(1)
    _CE.value(0)
    _PGM.value(1)
    _OE.value(1)

    for data in buffer:
        setAddress(address)
        n = 0
        while n < write_count:
            setData(data)
            utime.sleep_us(3)
            # 各ROM固有の書き込みパルス操作
            _PGM.value(0)
            utime.sleep_ms(1)
            _PGM.value(1)
            utime.sleep_us(3)

            setDataPinInput()
            utime.sleep_us(3)
            _OE.value(0)
            utime.sleep_us(2)
            read_value = readByteFromBus()
            _OE.value(1)

            utime.sleep_us(2)
            
            if read_value == data:
                break
            n += 1
            setDataPinOutput()

            if n >= write_count:
                errCnt += 1

        if errCnt >= 100:
            VPP.value(0)
            break

        address += 1
        #進捗状況を表示させる
        new_mark = address // size_10
        if new_mark > progress_mark:
            progress_mark = new_mark
            if progress_mark == 10:
                print("100% completed!!")
            else:
                print(f"{progress_mark * 10}% arrived...")

    VPP.value(0)

def writeRom27256(buffer, size):
    address = 0
    progress_mark = 0  # 表示済みの進捗
    size_10 = size / 10
    write_count = 25
    errCnt = 0

    setDataPinOutput()
    # 各ROM固有の初期設定
    VPP.value(1)
    _CE.value(1)
    _OE.value(1)

    for data in buffer:
        setAddress(address)
        n = 0
        while n < write_count:
            setData(data)
            utime.sleep_us(3)
        # 各ROM固有の書き込みパルス操作
            _CE.value(0)
            utime.sleep_ms(1)
            _CE.value(1)

            setDataPinInput()
            utime.sleep_us(5)
            _OE.value(0)
            utime.sleep_us(2)
            read_value = readByteFromBus()
            _OE.value(1)
            
            utime.sleep_us(2)
            
            if read_value == data:
                break
            n += 1
            setDataPinOutput()

            if n >= write_count:
                errCnt += 1

        if errCnt >= 100:
            VPP.value(0)
            break

        address += 1
        #進捗状況を表示させる
        new_mark = address // size_10
        if new_mark > progress_mark:
            progress_mark = new_mark
            if progress_mark == 10:
                print("100% completed!!")
            else:
                print(f"{progress_mark * 10}% arrived...")

    VPP.value(0)
    
def writeRom27512(buffer, size):
    address = 0
    progress_mark = 0  # 表示済みの進捗
    size_10 = size / 10
    write_count = 25
    n = 0
    errCnt = 0

    setDataPinOutput()
    # 各ROM固有の初期設定
    VPP.value(1)
    _CE.value(1)

    for data in buffer:
        setAddress(address)
        n = 0
        while n < write_count:
            setData(data)
            utime.sleep_us(3)
            # 各ROM固有の書き込みパルス操作
            _CE.value(0)
            utime.sleep_ms(1)
            _CE.value(1)
            utime.sleep_us(3)
            VPP.value(0)

            setDataPinInput()
            utime.sleep_us(5)
            _CE.value(0)
            utime.sleep_us(2)
            read_value = readByteFromBus()
            _CE.value(1)
            VPP.value(1)
            utime.sleep_us(2)
            
            if read_value == data:
                break
            n += 1
            setDataPinOutput()

            if n >= write_count:
                errCnt += 1

        if errCnt >= 100:
            VPP.value(0)
            break

        address += 1
        #進捗状況を表示させる
        new_mark = address // size_10
        if new_mark > progress_mark:
            progress_mark = new_mark
            if progress_mark == 10:
                print("100% completed!!")
            else:
                print(f"{progress_mark * 10}% arrived...")

    VPP.value(0)
    
def eraceLEDs():
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

# ----- main routine -----

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

dir_245 = pins[3] # GP5
dir_245.value(1)  # value: 0:B-> A, 1:A-> B

VPP  = pins[4]    # GP6
_CE  = pins[5]    # GP7
_OE  = pins[6]    # GP8
_PGM = pins[7]    # GP9

VPP.value(0)      # GP6   VPP
_CE.value(0)      # GP7   _CE
_OE.value(0)      # GP8   _OE
_PGM.value(0)     # GP9   _PGM

# --- ROM情報（容量と書き込み関数） ---
ROM_OPTIONS = {
    0: ("2716", 2048, writeRom2716),
    1: ("2732", 4096, writeRom2732),
    2: ("2764", 8192, writeRom2764),
    3: ("27128", 16384, writeRom27128),
    4: ("27256", 32768, writeRom27256),
    5: ("27512", 65536, writeRom27512),
}

# === 設定 ===
ROM_SELECT = 4  # ← PC側と合わせて 0〜5 を選択
ROM_INFO = ROM_OPTIONS.get(ROM_SELECT)
if ROM_INFO is None:
    print(f"未定義のROM番号: {ROM_SELECT}")
    sys.exit()

ROM_TYPE, ROM_SIZE, ROM_FUNC = ROM_INFO

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
    while len(received_buffer) < ROM_SIZE:
        if uart.any():
            data = uart.read()
            if data:
                received_buffer += data
                print(f"{len(data)} bytes 受信, 合計: {len(received_buffer)} bytes")
        utime.sleep_ms(2)

    print("size:",target_size)
    print("受信完了、ROM書き込み開始")
    start_time = utime.ticks_ms()

    # --- 書き込み実行 ---
    ROM_FUNC(received_buffer, ROM_SIZE)

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
