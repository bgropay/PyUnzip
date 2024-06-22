print("Program berjalan... Tekan Ctrl+C atau Ctrl+Z untuk mencoba menghentikan.")

try:
    while True:
        pass  # Program utama berjalan di sini
except KeyboardInterrupt:
    print("Mengabaikan Ctrl+C!")
except SystemExit:
    print("Mengabaikan Ctrl+Z!")
