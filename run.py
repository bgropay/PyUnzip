#!/usr/bin/env python
#
# PyUnzip
# =======
# PyUnzip adalah program Python sederhana 
# yang dirancang untuk meng-crack kata sandi
# file Zip. Program ini menggunakan teknik
# Dictionary Attack, yaitu teknik yang mencoba
# semua kemungkinan kata sandi yang terdapat
# dalam file Wordlist.
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
import colorama
import pyzipper

# Mengubah output warna teks
m = colorama.Fore.LIGHTRED_EX    # merah
h = colorama.Fore.LIGHTGREEN_EX  # hijau
b = colorama.Fore.LIGHTBLUE_EX   # biru
k = colorama.Fore.LIGHTYELLOW_EX # kuning
c = colorama.Fore.LIGHTCYAN_EX   # cyan
p = colorama.Fore.LIGHTWHITE_EX  # putih
r = colorama.Style.RESET_ALL      # reset
bm = colorama.Back.LIGHTRED_EX    # background merah

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

{bm}{p}:: Program ini hanya untuk tujuan edukasi dan Pembelajaran. ::{r}
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
    except KeyboardInterrupt:
        print(f"\n{m}[-] {p}Keluar...{k}:({r}")
        exit(1)

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
    except KeyboardInterrupt:
        print(f"\n{m}[-] {p}Keluar...{k}:({r}")
        exit(1)

found_password = False

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
                        found_password = True
                        exit(0)
                except KeyboardInterrupt:
                    print(f"\n{m}[-] {p}Keluar...{k}:({r}")
                    exit(1)
                except Exception:
                    print(f"{m}[-] {p}Kata sandi salah: {m}{kata_sandi}{r}")
                    continue
    # Jika kata sandi tidak ditemukan
    if not found_password:
        print(f"{p}--------------------------------------------------{r}")
        print(f"{m}[-] {p}Kata sandi tidak ditemukan dalam file wordlist {m}{input_wordlist}{r}")
        print(f"{p}--------------------------------------------------{r}")
except Exception as e:
    print(f"{m}[-] {p}Kesalahan terjadi: {m}{e}{r}")
