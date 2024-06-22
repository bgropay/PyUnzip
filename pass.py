import signal
import sys

# Handler untuk SIGINT (Ctrl+C)
def signal_handler(sig, frame):
    print('Mengabaikan Ctrl+C!')

# Handler untuk SIGTSTP (Ctrl+Z)
def signal_handler_tstp(sig, frame):
    print('Mengabaikan Ctrl+Z!')

# Tangkap sinyal SIGINT dan SIGTSTP
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTSTP, signal_handler_tstp)

print("Program berjalan... Tekan Ctrl+C atau Ctrl+Z untuk mencoba menghentikan.")

# Program loop untuk mempertahankan script tetap berjalan
while True:
    try:
        pass  # Lakukan sesuatu di sini
    except KeyboardInterrupt:
        pass  # Mengabaikan Ctrl+C
