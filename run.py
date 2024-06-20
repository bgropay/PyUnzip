#!/usr/bin/env python
#
# PyUnzip
# =======
# PyUnzip adalah program Python sederhana 
# yang dirancang untuk meng-crack kata sandi
# file Zip. Program ini menggunakan teknik
# Dictionary Attack dan Brute Force Attack.
#
#
# Jenis Enkripsi yang didukung PyUnzip
#-------------------------------------
# [+] ZipCrypto
# [+] AES-128
# [+] AES-192
# [+] AES-256
#
#
# Pembuat 
# -------
# BgRopay
#
#
# Lisensi 
#--------
# MIT License
#
# Hak Cipta (c) 2024 bgropay
#
# Dengan ini diberikan izin, gratis, kepada siapa pun yang mendapatkan salinan
# perangkat lunak ini dan file dokumentasi terkait (disebut "Perangkat Lunak"), untuk
# berurusan dalam Perangkat Lunak tanpa batasan, termasuk namun tidak terbatas pada hak
# untuk menggunakan, menyalin, memodifikasi, menggabungkan, menerbitkan, mendistribusikan, mensublisensikan, dan/atau menjual
# salinan Perangkat Lunak, dan untuk mengizinkan orang-orang yang kepadanya Perangkat Lunak ini
# diberikan untuk melakukannya, dengan ketentuan berikut:
#
# Pemberitahuan hak cipta di atas dan pemberitahuan izin ini harus disertakan dalam semua
# salinan atau bagian substansial dari Perangkat Lunak.
#
# PERANGKAT LUNAK INI DIBERIKAN "SEBAGAIMANA ADANYA", TANPA JAMINAN APA PUN, BAIK TERSURAT MAUPUN
# TERSELUBUNG, TERMASUK NAMUN TIDAK TERBATAS PADA JAMINAN DAPAT DIPERJUALBELIKAN,
# KESESUAIAN UNTUK TUJUAN TERTENTU DAN NONPELANGGARAN. DALAM HAL APA PUN PENULIS ATAU PEMEGANG HAK CIPTA TIDAK AKAN BERTANGGUNG JAWAB ATAS KLAIM, KERUSAKAN, ATAU KEWAJIBAN LAINNYA, BAIK DALAM TINDAKAN KONTRAK, KESALAHAN, ATAU LAINNYA, YANG TIMBUL DARI,
# KELUAR DARI, ATAU SEHUBUNGAN DENGAN PERANGKAT LUNAK ATAU PENGGUNAAN ATAU URUSAN LAINNYA DALAM
# PERANGKAT LUNAK.

import os
import time
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

# Mengecek jenis sistem operasi
so = os.name

# Membersihkan layar terminal berdasarkan sistem operasi
if so == "nt":
    os.system("cls")
elif so == "posix":
    os.system("clear")
else:
    print(f"{m}[-] {p}Sistem operasi Anda tidak mendukung untuk menjalankan program PyUnzip :({r}")
    exit(1)

# Banner program
print(f"""{p}******************************************************{r}
{p}* {h}[+] {p}Program   : {k}PyUnzip                            {p}*{r}
{p}* {h}[+] {p}Pembuat   : {k}BgRopay                            {p}*{r}
{p}* {h}[+] {p}Deskripsi : {k}Crack Kata Sandi File Zip          {p}*{r}
{p}* {h}[+] {p}Github    : {k}https://github.com/bgropay/pyunzip {p}*{r}
{p}******************************************************{r}

{bm}{p}:: Program ini hanya untuk tujuan Edukasi dan Pembelajaran. ::{r}
{bm}{p}:: Jangan gunakan program ini untuk tujuan ilegal.          ::{r}
""")

# Input file Zip
while True:
    try:
        input_zip = input(f"{c}[»] {p}Masukkan jalur ke file Zip: {c}")
        if not os.path.isfile(input_zip):
            print(f"{m}[-] {p}File Zip {input_zip} tidak ditemukan.{r}")
            continue
        if not input_zip.endswith(".zip"):
            print(f"{m}[-] {p}File {input_zip} bukan file Zip.{r}")
            continue
        print(f"{h}[+] {p}File Zip {input_zip} ditemukan.{r}")
        break
    # Error handling KeyboardInterrupt
    except KeyboardInterrupt:
        print(f"\n{m}[-] {p}Keluar...{k}:({r}")
        exit(1)

# Memilih metode serangan
x = 1
print("\nMetode serangan yang tersedia:\n")
list_metode_serangan = ["Brute Force Attack", "Dictionary Attack"]
for metode in list_metode_serangan:
    print(f"{x}. {metode}")
    x += 1
print("")
while True:
    try:
        metode_serangan = input(f"{c}[»] {p}Pilih metode serangan: {c}")
        if metode_serangan not in ["1", "2"] or metode_serangan not in list_metode_serangan:
            print(f"{m}[-] {p} Metode serangan {m}{metode_serangan} {p}tidak tersedia.{r}")
            continue
        break
    except KeyboardInterrupt:
        print(f"\n{m}[-] {p}Keluar...{k}:({r}")
        exit(1)

kata_sandi_ditemukan = False

if metode_serangan == "1":
    # Input file Wordlist
    while True:
        try:
            input_wordlist = input(f"{c}[»] {p}Masukkan jalur ke file Wordlist: {c}")
            if not os.path.isfile(input_wordlist):
                print(f"{m}[-] {p}File Wordlist {input_wordlist} tidak ditemukan.{r}")
                continue
            print(f"{h}[+] {p}File Wordlist {input_wordlist} ditemukan.{r}")
            print(f"{b}[*] {p}Menghitung jumlah kata sandi yang terdapat dalam file Wordlist {b}{input_wordlist}{p}...{r}")
            time.sleep(3)
            with open(input_wordlist, "r", encoding="latin-1", errors="ignore") as list_kata_sandi:
                jumlah_kata_sandi = sum(1 for baris in list_kata_sandi)
            print(f"{h}[+] {p}Jumlah kata sandi yang terdapat dalam file {h}{input_wordlist} {p}sebanyak: {h}{jumlah_kata_sandi} {p}kata sandi.{r}\n")
            time.sleep(3)
            break
        # Error handling KeyboardInterrupt
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)

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

elif metode_serangan == "2":
    # Input panjang minimal kata sandi
    while True:
        try:
            min_length = int(input(f"{c}[»] {p}Masukkan panjang minimal kata sandi: {c}"))
            if min_length <= 0:
                print(f"{m}[-] {p}Panjang minimal kata sandi harus lebih dari 0.{r}")
                continue
            break
        except ValueError:
            print(f"{m}[-] {p}Masukkan nilai angka yang valid.{r}")
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)

    # Input panjang maksimal kata sandi
    while True:
        try:
            max_length = int(input(f"{c}[»] {p}Masukkan panjang maksimal kata sandi: {c}"))
            if max_length < min_length:
                print(f"{m}[-] {p}Panjang maksimal kata sandi harus lebih dari atau sama dengan panjang minimal kata sandi.{r}")
                continue
            break
        except ValueError:
            print(f"{m}[-] {p}Masukkan nilai angka yang valid.{r}")
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)
            
    # Memilih jenis karakter
    characters = ""
    while True:
        try:
            if input(f"{c}[»] {p}Gunakan huruf kecil? (y/n): {c}").lower() == "y":
                characters += string.ascii_lowercase
            if input(f"{c}[»] {p}Gunakan huruf besar? (y/n): {c}").lower() == "y":
                characters += string.ascii_uppercase
            if input(f"{c}[»] {p}Gunakan angka? (y/n): {c}").lower() == "y":
                characters += string.digits
            if input(f"{c}[»] {p}Gunakan simbol? (y/n): {c}").lower() == "y":
                characters += string.punctuation
            
            if not characters:
                print(f"{m}[-] {p}Anda harus memilih setidaknya satu jenis karakter.{r}")
                continue
            break
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)

    try:
        with pyzipper.AESZipFile(input_zip) as fz:
            for length in range(min_length, max_length + 1):
                for attempt in itertools.product(characters, repeat=length):
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
