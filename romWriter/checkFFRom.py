from machine import Pin, UART
import utime
import gc

# === 設定 ===
ROM_SELECT = 3  # ← PC側と合わせて 0〜5 を選択
select = 1 # 0:0xFF 1:0-255

# --- ROM情報（容量と書き込み関数） ---
ROM_OPTIONS = {
    0: ("2716", 2048),
    1: ("2732", 4096),
    2: ("2764", 8192),
    3: ("27128", 16384),
    4: ("27256", 32768),
    5: ("27512", 65536),
}

ROM_INFO = ROM_OPTIONS.get(ROM_SELECT)
if ROM_INFO is None:
    print(f"未定義のROM番号: {ROM_SELECT}")
    sys.exit()

ROM_TYPE, ROM_SIZE = ROM_INFO

def _write_byte(val):
    for i in range(8):
        clk.value(0)
        bit = ((val << i) & 0b10000000)>>7
        sdi.value(bit)
        clk.value(1)
        utime.sleep_us(period)

def setDataPinOutput():
    dir_245.value(1)    # value: 0:B-> A, 1:A-> B
    data_pins = [Pin(i, Pin.OUT) for i in dataPinList]

# GPIOピンの設定（GP0〜GP3を出力）
pinList = list(range(2, 10))
pins = [Pin(i, Pin.OUT) for i in pinList]

dataPinList = list(range(10, 18))
data_pins = [Pin(i, Pin.IN, Pin.PULL_DOWN) for i in dataPinList]

# pin = Pin(16, Pin.IN, Pin.PULL_UP)  # 内部プルアップを有効にする
# pin = Pin(16, Pin.IN, Pin.PULL_DOWN)  # 内部プルダウンを有効にする

sdi   = pins[0]     # GP2
clk   = pins[1]     # GP3
latch = pins[2]     # GP4

period = 1

dir_245 = pins[3]   # GP5
dir_245.value(0)    # value: 0:B-> A, 1:A-> B

VPP = pins[4]     # GP6
_CE  = pins[5]     # GP7
_OE  = pins[6]     # GP8
_PGM  = pins[7]     # GP9

VPP.value(1)    # GP6
_CE.value(0)     # GP7
_OE.value(0)     # GP8
_PGM.value(1)     # GP9

countFF    = 0
countTrue  = 0
countError = 0

gc.collect()  # ガベージコレクションを実行
# errData1 = []
# errData2 = []

received_buffer = bytearray()

# ===================================

# print("UART受信開始")

# while len(received_buffer) < ROM_SIZE:
#     if uart.any():
#         data = uart.read()
#         if data:
#             received_buffer += data
#             print(f"{len(data)} bytes 受信, 合計: {len(received_buffer)} bytes")
#         utime.sleep_ms(2)


# for num in range(0x2000): # 8192
index = 0
start_time = utime.ticks_ms()
progress_mark = 0  # 表示済みの進捗（10%, 20%, ...）

errData = []
size_10 = ROM_SIZE / 10
for num in range(ROM_SIZE):
    # address をセット
    upper = (num >> 8) & 0xFF
    lower = num & 0xFF
    
    latch.value(0)
    _write_byte(upper)   # upper bit
    _write_byte(lower)   # lower bit
    latch.value(1)

    utime.sleep_us(2)

    romValue = sum([(data_pins[i].value() << i) for i in range(8)])

    if select == 0:
        if romValue == 0xFF:
            countFF += 1
        else:
            countError += 1
            errData.append([num, romValue])
            
    else:
        if romValue == lower:
            countTrue += 1
        else:
            countError += 1
            errData.append([num, lower, romValue])

    #進捗状況を表示させる
    new_mark = int(num / size_10)
    if new_mark > progress_mark:
        progress_mark = new_mark
        if progress_mark == 10:
            print("100% completed!!")
        else:
            print(f"{progress_mark * 10}% arrived...")

    utime.sleep_us(2)  # 送信の安定時間

end_time = utime.ticks_ms()
elapsed_time = utime.ticks_diff(end_time, start_time)

if select == 0:
    print(f"countFF:{countFF}")
    print(f"countError:{countError}")
    for err in errData:
        print(f"address:{err[0]:04X}, rom:{err[1]:02X}")
    for err in errData:
        print(f"address:{err[0]:04X}, rom:{err[1]:08b}")
else:
    print(f"countTrue:{countTrue}")
    print(f"countError:{countError}")
    for err in errData:
        print(f"address:{err[0]:04X}, true:{err[1]:02X}, rom:{err[2]:02X}")
    for err in errData:
        print(f"address:{err[0]:04X}, true:{err[1]:08b}, rom:{err[2]:08b}")

print(f"経過時間: {elapsed_time} [μs]")

for i in range(3, 8):  # 0 から len(pins)-1 までのインデックスを使う
    pins[i].value(0)

# GPIOピンの設定（GP10〜GP17を出力）
dataPins = [Pin(i, Pin.OUT) for i in dataPinList]
dir_245.value(1)    # value: 0:B-> A, 1:A-> B

for i in range(8):
    dataPins[i].value(0)

latch.value(0)
_write_byte(0)
_write_byte(0)
latch.value(1)

VPP.value(0)    # GP6
_CE.value(0)     # GP7
_OE.value(0)     # GP8
_PGM.value(0)     # GP9

dir_245.value(1)    # value: 0:B-> A, 1:A-> B
