@echo on
set filename=data/rom_dump_%1.bin
@REM set filename=%1.bin

@REM Made file name: %filename%

python hexdump.py %filename%