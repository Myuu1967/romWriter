# filename = "GRANTBAS.bin"
filename2 = "data/rom_dump_2025041601.bin"

err = []

# 0: 0xFF 1: 0-255
select = 1 
# with open(filename, 'rb') as f1, open(filename2, 'rb') as f2:
#     while True:
#         data1 = f1.read(1)
#         data2 = f2.read(1)

#         if not data1 or not data2:
#             break  # どちらかのファイルが終了したら終了

#         val1 = int.from_bytes(data1, byteorder='little')
#         val2 = int.from_bytes(data2, byteorder='little')

#         if val1 != val2:
#             err.append([num, val1, val2])

#         num += 1

num = 0
with open(filename2, 'rb') as f:
    while True:
        data = f.read(1)

        if not data:
            break  # どちらかのファイルが終了したら終了

        val = int.from_bytes(data, byteorder='little')

        lower = num & 0xFF

        if select == 0 and val != 0xFF:
            err.append([num, val])
        elif select == 1 and val != lower:
            err.append([num, lower, val])

        num += 1

errNum = len(err)
print(f"errNum: {errNum}")
print()

# エラーを表示（必要に応じて1つの形式だけ使ってください）
if select == 0: 
    for er in err:
        print( f"Address: 0x{er[0]:04X}, Expected: 0x{er[1]:02X}, Real Number 0xFF")
    for er in err:
         print( f"Address: 0x{er[0]:016b}, Expected: 0x{er[1]:08b}, Real Number 0b11111111")
elif select == 1: 
    for er in err:
        print( f"Address: 0x{er[0]:04X}, Expected: 0x{er[1]:02X}, Real Number 0x{er[2]:02X}")
    for er in err:
         print( f"Address: 0x{er[0]:04X}, Expected: 0b{er[1]:08b}, Real Number 0b{er[2]:08b}")



