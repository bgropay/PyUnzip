import json
import os
import time
import getpass
import colorama
import pyzipper
from datetime import datetime, timedelta

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
        print(f"{b}[*] {p}Menghitung jumlah kata sandi yang terdapat dalam file Wordlist {input_wordlist}...{r}")
        time.sleep(3)
        with open(input_wordlist, "r", encoding="latin-1", errors="ignore") as list_kata_sandi:
            jumlah_kata_sandi = sum(1 for baris in list_kata_sandi)
        print(f"{h}[+] {p}Jumlah kata sandi yang terdapat dalam file {h}{input_wordlist} {p}sebanyak: {h}{jumlah_kata_sandi} {p}kata sandi.{r}\n")
        time.sleep(3)
        break
    except KeyboardInterrupt:
        print(f"\n{m}[-] {p}Keluar...{k}:({r}")
        exit(1)

# Variabel untuk pencatatan hasil cracking
found_password = False
mulai = datetime.now()
jumlah_kata_sandi_dicoba = 0

try:
    with pyzipper.AESZipFile(input_zip) as fz:
        with open(input_wordlist, encoding="latin-1", errors="ignore") as fw:
            for baris_file in fw:
                kata_sandi = baris_file.strip()
                jumlah_kata_sandi_dicoba += 1

                try:
                    fz.pwd = kata_sandi.encode("latin-1")
                    if fz.testzip() is None:
                        print(f"{p}--------------------------------------------------{r}")
                        print(f"{h}[+] {p}Kata sandi ditemukan: {h}{kata_sandi}{r}")
                        print(f"{p}--------------------------------------------------{r}")
                        found_password = True

                        # Menyimpan hasil dalam format JSON
                        selesai = datetime.now()
                        durasi_detik = (selesai - mulai).total_seconds()
                        durasi_formatted = str(timedelta(seconds=durasi_detik))
                        hasil_cracking = {
                            "Waktu Mulai": mulai.strftime('%d-%m-%Y %H:%M:%S'),
                            "Waktu Selesai": selesai.strftime('%d-%m-%Y %H:%M:%S'),
                            "Durasi": durasi_formatted,
                            "Nama File Zip": input_zip,
                            "Nama File Wordlist": input_wordlist,
                            "Jumlah kata sandi file Wordlist": jumlah_kata_sandi,
                            "Kata Sandi": kata_sandi,
                            "Jumlah kata sandi yang dicoba": jumlah_kata_sandi_dicoba
                        }
                        if os.path.exists("hasil_cracking.json"):
                            with open("hasil_cracking.json", "r+") as file_json:
                                data = json.load(file_json)
                                data.append(hasil_cracking)
                                file_json.seek(0)
                                json.dump(data, file_json, indent=4)
                        else:
                            with open("hasil_cracking.json", "w") as file_json:
                                json.dump([hasil_cracking], file_json, indent=4)

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

        # Menyimpan hasil dalam format JSON
        selesai = datetime.now()
        durasi_detik = (selesai - mulai).total_seconds()
        durasi_formatted = str(timedelta(seconds=durasi_detik))
        hasil_cracking = {
            "Waktu Mulai": mulai.strftime('%d-%m-%Y %H:%M:%S'),
            "Waktu Selesai": selesai.strftime('%d-%m-%Y %H:%M:%S'),
            "Durasi": durasi_formatted,
            "Nama File Zip": input_zip,
            "Nama File Wordlist": input_wordlist,
            "Jumlah kata sandi file Wordlist": jumlah_kata_sandi,
            "Kata Sandi": False,  # Menandakan kata sandi tidak ditemukan
            "Jumlah kata sandi yang dicoba": jumlah_kata_sandi_dicoba
        }
        if os.path.exists("hasil_cracking.json"):
            with open("hasil_cracking.json", "r+") as file_json:
                data = json.load(file_json)
                data.append(hasil_cracking)
                file_json.seek(0)
                json.dump(data, file_json, indent=4)
        else:
            with open("hasil_cracking.json", "w") as file_json:
                json.dump([hasil_cracking], file_json, indent=4)

except Exception as e:
    print(f"{m}[-] {p}Kesalahan terjadi: {m}{e}{r}")
