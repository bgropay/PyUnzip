print("Program berjalan... Tekan Ctrl+C atau Ctrl+Z untuk mencoba menghentikan.")

while True:
    try:
        while True:
             pass  # Program utama berjalan di sini
    except KeyboardInterrupt:
        print("Mengabaikan Ctrl+C!")
        continue
    except Exception:
        print("Mengabaikan Ctrl+Z!")
        continue
