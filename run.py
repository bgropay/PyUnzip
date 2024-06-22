#!/usr/bin/env python3

import os
import time
import sys
import termios
import tty
import itertools
import string
import colorama
import pyzipper


# Mengubah output warna teks
m = colorama.Fore.LIGHTRED_EX    # merah
h = colorama.Fore.LIGHTGREEN_EX  # hijau
b = colorama.Fore.LIGHTBLUE_EX   # biru
k = colorama.Fore.LIGHTYELLOW_EX # kuning
c = colorama.Fore.LIGHTCYAN_EX   # cyan
p = colorama.Fore.LIGHTWHITE_EX  # putih
r = colorama.Style.RESET_ALL     # reset
bm = colorama.Back.LIGHTRED_EX   # background merah

# Token yang benar
token_benar = "kunyuk is here"

# Mengecek jenis sistem operasi
so = os.name

while True:
    # Bersihkan layar terminal
    if so == "nt":
        os.system("cls")
    elif so == "posix":
        os.system("clear")
    else:
        print(f"{m}[-] {p}Sistem operasi Anda tidak mendukung untuk menjalankan program PyUnzip :({r}")
        exit(1)
    
    if so == "posix":
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            print(f"{c}[»] {p}Masukkan Token: ", end="", flush=True)
            input_token = ""
            while True:
                char = sys.stdin.read(1)
                if char == "\n" or char == "\r":
                    break
                if char == "\x7f":  # Backspace key
                    if len(input_token) > 0:
                        input_token = input_token[:-1]
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                else:
                    input_token += char
                    sys.stdout.write("*")
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    elif so == "nt":
        import msvcrt
        print(f"{c}[»] {p}Masukkan Token: ", end="", flush=True)
        input_token = ""
        while True:
            char = msvcrt.getch()
            if char in {b'\r', b'\n'}:  # Enter key
                break
            elif char == b'\x08':  # Backspace key
                if len(input_token) > 0:
                    input_token = input_token[:-1]
                    syimport msvcrts.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                input_token += char.decode("utf-8")
                sys.stdout.write("*")
                sys.stdout.flush()

    print()  # Move to the next line

    # Animasi loading
    print(f"{b}[*] {p}Verifikasi Token ", end="", flush=True)
    spinner = ["|", "/", "-", "\\"]
    for _ in range(10):
        for char in spinner:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\b")
    
    print()  # Move to the next line

    # Memeriksa apakah token yang dimasukkan benar
    if input_token == token_benar:
        print(f"{h}[+] {p}Token benar.{r}")
        time.sleep(3)
        break  # Keluar dari loop jika login berhasil
    else:
        print(f"{m}[-] {p}Token salah. Silahkan coba lagi.{r}")
        time.sleep(3)

# Membersihkan layar terminal berdasarkan sistem operasi
if so == "nt":
    os.system("cls")
elif so == "posix":
    os.system("clear")
else:
    print(f"{m}[-] {p}Sistem operasi Anda tidak mendukung untuk menjalankan program PyUnzip :({r}")
    exit(1)

# *************** BANNER ***************
print(f"""{p}******************************************************{r}
{p}* {h}[+] {p}Program   : {k}PyUnzip                            {p}*{r}
{p}* {h}[+] {p}Pembuat   : {k}BgRopay                            {p}*{r}
{p}* {h}[+] {p}Deskripsi : {k}Crack Kata Sandi File Zip          {p}*{r}
{p}* {h}[+] {p}Github    : {k}https://github.com/bgropay/pyunzip {p}*{r}
{p}******************************************************{r}

{bm}{p}:: Program ini hanya untuk tujuan Edukasi dan Pembelajaran. ::{r}
{bm}{p}:: Jangan gunakan program ini untuk tujuan ilegal.          ::{r}
""")

# *************** INPUT FILE ZIP ***************
while True:
    try:
        input_zip = input(f"{c}[»] {p}Masukkan jalur ke file Zip: ")
        if not os.path.isfile(input_zip):
            print(f"{m}[-] {p}File Zip {input_zip} tidak ditemukan.{r}")
            continue
        if not input_zip.endswith(".zip"):
            print(f"{m}[-] {p}File {input_zip} bukan file Zip.{r}")
            continue
        break
    # Error handling KeyboardInterrupt
    except KeyboardInterrupt:
        print(f"\n{m}[-] {p}Keluar...{k}:({r}")
        exit(1)

# *************** MEMILIH METODE SERANGAN ***************
x = 1
print("\nMetode serangan yang tersedia:\n")
list_metode_serangan = ["Brute Force Attack", "Dictionary Attack"]
for metode in list_metode_serangan:
    print(f"{x}. {metode}")
    x += 1
print("")
while True:
    try:
        metode_serangan = input(f"{c}[»] {p}Pilih metode serangan: ")
        if metode_serangan not in ["1", "2"]:
            print(f"{m}[-] {p} Metode serangan '{metode_serangan}' tidak tersedia.{r}")
            continue
        break
    except KeyboardInterrupt:
        print(f"\n{m}[-] {p}Keluar...{k}:({r}")
        exit(1)

kata_sandi_ditemukan = False

# *************** BRUTE FORCE ATTACK ***************
if metode_serangan == "1":
    # input panjang minimal kata sandi 
    while True:
        try:
            min_length = int(input(f"{c}[»] {p}Masukkan panjang minimal kata sandi: "))
            if min_length <= 0:
                print(f"{m}[-] {p}Panjang minimal kata sandi harus lebih dari 0.{r}")
                continue
            break
        except ValueError:
            print(f"{m}[-] {p}Masukkan nilai angka yang valid.{r}")
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)

    # input panjang maksimal kata sandi
    while True:
        try:
            max_length = int(input(f"{c}[»] {p}Masukkan panjang maksimal kata sandi: "))
            if max_length < min_length:
                print(f"{m}[-] {p}Panjang maksimal kata sandi harus lebih dari atau sama dengan panjang minimal kata sandi.{r}")
                continue
            break
        except ValueError:
            print(f"{m}[-] {p}Masukkan nilai angka yang valid.{r}")
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)
            
    # *************** MEMILIH JENIS KOMBINASI KARAKTER ***************
    kombinasi_karakter = ""
    while True:
        try:
            while True:
                pilih_huruf_kecil = input(f"{c}[»] {p}Gunakan huruf kecil? [iya/tidak]: ").lower()
                if pilih_huruf_kecil in ["iya", "tidak"]:
                    if pilih_huruf_kecil == "iya":
                        kombinasi_karakter += string.ascii_lowercase
                    break
                else:
                    print(f"{m}[-] {p}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{r}")

            while True:
                pilih_huruf_besar = input(f"{c}[»] {p}Gunakan huruf besar? [iya/tidak]: ").lower()
                if pilih_huruf_besar in ["iya", "tidak"]:
                    if pilih_huruf_besar == "iya":
                        kombinasi_karakter += string.ascii_uppercase
                    break
                else:
                    print(f"{m}[-] {p}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{r}")

            while True:
                pilih_angka = input(f"{c}[»] {p}Gunakan angka? [iya/tidak]: ").lower()
                if pilih_angka in ["iya", "tidak"]:
                    if pilih_angka == "iya":
                        kombinasi_karakter += string.digits
                    break
                else:
                    print(f"{m}[-] {p}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{r}")

            while True:
                pilih_simbol = input(f"{c}[»] {p}Gunakan simbol? [iya/tidak]: ").lower()
                if pilih_simbol in ["iya", "tidak"]:
                    if pilih_simbol == "iya":
                        kombinasi_karakter += string.punctuation
                    break
                else:
                    print(f"{m}[-] {p}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{r}")

            if not kombinasi_karakter:
                print(f"{m}[-] {p}Anda harus memilih setidaknya satu jenis karakter.{r}")
                continue
            break
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)

    input(f"\n{h}Tekan [Enter] untuk memulai proses Cracking...{r}")
  
    # Membersihkan layar terminal berdasarkan sistem operasi
    if so == "nt":
        os.system("cls")
    elif so == "posix":
        os.system("clear")
    else:
        print(f"{m}[-] {p}Sistem operasi Anda tidak mendukung untuk menjalankan program PyUnzip :({r}")
        exit(1)
    
    # *************** CRACK KATA SANDI FILE ZIP DENGAN METODE SERANGAN BRUTE FORCE ATTACK ***************
    try:
        with pyzipper.AESZipFile(input_zip) as fz:
            for length in range(min_length, max_length + 1):
                for attempt in itertools.product(kombinasi_karakter, repeat=length):
                    kata_sandi = ''.join(attempt)
                    try:
                        fz.pwd = kata_sandi.encode("latin-1")
                        if fz.testzip() is None:
                            print(f"{p}--------------------------------------------------{r}")
                            print(f"{h}[+] {p}Kata sandi ditemukan: {h}{kata_sandi}{r}")
                            print(f"{p}--------------------------------------------------{r}")
                            kata_sandi_ditemukan = True
                            exit(0)
                    # Error handling KeyboardInterrupt
                    except KeyboardInterrupt:
                        print(f"\n{m}[-] {p}Keluar...{k}:({r}")
                        exit(1)
                    except Exception:
                        print(f"{m}[-] {p}Kata sandi salah: {m}{kata_sandi}{r}")
                        continue
        # Jika kata sandi tidak ditemukan
        if not kata_sandi_ditemukan:
            print(f"{p}--------------------------------------------------{r}")
            print(f"{m}[-] {p}Kata sandi tidak ditemukan dalam rentang panjang dan karakter yang diberikan.{r}")
            print(f"{p}--------------------------------------------------{r}")
    except Exception as e:
        print(f"{m}[-] {p}Kesalahan terjadi: {m}{e}{r}")

# *************** DICTIONARY ATTACK ***************
if metode_serangan == "2":
    # input file Wordlist
    while True:
        try:
            input_wordlist = input(f"{c}[»] {p}Masukkan jalur ke file Wordlist: ")
            if not os.path.isfile(input_wordlist):
                print(f"{m}[-] {p}File Wordlist {input_wordlist} tidak ditemukan.{r}")
                continue
            break
        # Error handling KeyboardInterrupt
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)

    input(f"\n{h}Tekan [Enter] untuk memulai proses Cracking...{r}")
  
    # Membersihkan layar terminal berdasarkan sistem operasi
    if so == "nt":
        os.system("cls")
    elif so == "posix":
        os.system("clear")
    else:
        print(f"{m}[-] {p}Sistem operasi Anda tidak mendukung untuk menjalankan program PyUnzip :({r}")
        exit(1)
    
    # *************** CRACK KATA SANDI FILE ZIP DENGAN METODE SERANGAN DICTIONARY ATTACK ***************
    try:
        with pyzipper.AESZipFile(input_zip) as fz:
            with open(input_wordlist, encoding="latin-1", errors="ignore") as fw:
                for baris_file in fw:
                    kata_sandi = baris_file.strip()
                    try:
                        fz.pwd = kata_sandi.encode("latin-1")
                        if fz.testzip() is None:
                            print(f"{p}--------------------------------------------------{r}")
                            print(f"{h}[+] {p}Kata sandi ditemukan: {h}{kata_sandi}{r}")
                            print(f"{p}--------------------------------------------------{r}")
                            kata_sandi_ditemukan = True
                            exit(0)
                    # Error handling KeyboardInterrupt
                    except KeyboardInterrupt:
                        print(f"\n{m}[-] {p}Keluar...{k}:({r}")
                        exit(1)
                    except Exception:
                        print(f"{m}[-] {p}Kata sandi salah: {m}{kata_sandi}{r}")
                        continue
        # Jika kata sandi tidak ditemukan
        if not kata_sandi_ditemukan:
            print(f"{p}--------------------------------------------------{r}")
            print(f"{m}[-] {p}Kata sandi tidak ditemukan dalam file wordlist {m}{input_wordlist}{r}")
            print(f"{p}--------------------------------------------------{r}")
    except Exception as e:
        print(f"{m}[-] {p}Kesalahan terjadi: {m}{e}{r}")
