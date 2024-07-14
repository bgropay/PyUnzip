#!/usr/bin/env python3
#
# PyUnzip 
#
# PyUnzip adalah program yang dirancang oleh BgRopay 
# untuk melakukan peretasan terhadap kata sandi file
# ZIP. PyUnzip menggunakan tiga teknik serangan yaitu
# Brute Force Attack, Dictionary Attack, dan Combinator
# Attack.

import os
import time
import sys
import itertools
import string
import colorama
import pyzipper
import getpass

# Mengubah output warna teks
m = colorama.Fore.LIGHTRED_EX    # merah
h = colorama.Fore.LIGHTGREEN_EX  # hijau
b = colorama.Fore.LIGHTBLUE_EX   # biru
k = colorama.Fore.LIGHTYELLOW_EX # kuning
c = colorama.Fore.LIGHTCYAN_EX   # cyan
p = colorama.Fore.LIGHTWHITE_EX  # putih
r = colorama.Style.RESET_ALL     # reset
bm = colorama.Back.LIGHTRED_EX   # background merah

# Sistem operasi 
so = os.name
    
if so == "nt":
    os.system("cls")
elif so == "posix":
    os.system("clear")
else:
    print(f"{m}[-] {p}Sistem operasi Anda tidak mendukung untuk menjalankan program PyUnzip {k}:({r}")
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
            print(f"{m}[-] {p}File Zip '{input_zip}' tidak ditemukan.{r}")
            continue
        if not input_zip.endswith(".zip"):
            print(f"{m}[-] {p}File '{input_zip}' bukan file Zip.{r}")
            continue
        break
    # Error handling KeyboardInterrupt
    except KeyboardInterrupt:
        print(f"\n{m}[-] {p}Keluar...{k}:({r}")
        exit(1)

# *************** MEMILIH METODE SERANGAN ***************
x = 1
print("\nMetode serangan yang tersedia:\n")
list_metode_serangan = ["Brute Force Attack", "Dictionary Attack", "Combinator Attack"]
for metode in list_metode_serangan:
    print(f"{x}. {metode}")
    x += 1
print("")
while True:
    try:
        metode_serangan = input(f"{c}[»] {p}Pilih metode serangan: ")
        if metode_serangan not in ["1", "2", "3"]:
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

    # Input mau menggunakan verbose atau tidak 
    while True:
        try:
            verbose = input(f"{c}[»] {p}Gunakan mode verbose? [iya/tidak]: ").lower()
            if verbose in ["iya", "tidak"]:
                break
            else:
                print(f"{m}[-] {p}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{r}")
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)
    
    input(f"\n{h}Tekan [Enter] untuk memulai proses Cracking...{r}")
    print("")
    
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
                        if verbose == "iya":
                            print(f"{m}[-] {p}Kata sandi salah: {m}{kata_sandi}{r}")
                            continue
                        continue 
        # Jika kata sandi tidak ditemukan
        if not kata_sandi_ditemukan:
            print(f"{p}--------------------------------------------------{r}")
            print(f"{m}[-] {p}Kata sandi tidak ditemukan.{r}")
            print(f"{p}--------------------------------------------------{r}")
    except Exception as e:
        print(f"{m}[-] {p}Kesalahan terjadi: {m}{e}{r}")

# *************** DICTIONARY ATTACK ***************
elif metode_serangan == "2":
    # input file Wordlist
    while True:
        try:
            input_wordlist = input(f"{c}[»] {p}Masukkan jalur ke file Wordlist: ")
            if not os.path.isfile(input_wordlist):
                print(f"{m}[-] {p}File Wordlist '{input_wordlist}' tidak ditemukan.{r}")
                continue
            break
        # Error handling KeyboardInterrupt
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)
    # Input mau menggunakan verbose atau tidak 
    while True:
        try:
            verbose = input(f"{c}[»] {p}Gunakan mode verbose? [iya/tidak]: ").lower()
            if verbose in ["iya", "tidak"]:
                break
            else:
                print(f"{m}[-] {p}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{r}")
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)
    
    input(f"\n{h}Tekan [Enter] untuk memulai proses Cracking...{r}")
    print("")
    
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
                        if verbose == "iya":
                            print(f"{m}[-] {p}Kata sandi salah: {m}{kata_sandi}{r}")
                            continue
                        continue         
        # Jika kata sandi tidak ditemukan
        if not kata_sandi_ditemukan:
            print(f"{p}--------------------------------------------------{r}")
            print(f"{m}[-] {p}Kata sandi tidak ditemukan.{r}")
            print(f"{p}--------------------------------------------------{r}")
    except Exception as e:
        print(f"{m}[-] {p}Kesalahan terjadi: {m}{e}{r}")

# *************** COMBINATOR ATTACK ***************
if metode_serangan == "3":
    # Input file Wordlist 1
    while True:
        try:
            input_wordlist1 = input(f"{c}[»] {p}Masukkan jalur ke file Wordlist 1: ")
            if not os.path.isfile(input_wordlist1):
                print(f"{m}[-] {p}File Wordlist 1 '{input_wordlist1}' tidak ditemukan.{r}")
                continue
            break
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)

    # Input file Wordlist 2
    while True:
        try:
            input_wordlist2 = input(f"{c}[»] {p}Masukkan jalur ke file Wordlist 2: ")
            if not os.path.isfile(input_wordlist2):
                print(f"{m}[-] {p}File Wordlist 2 '{input_wordlist2}' tidak ditemukan.{r}")
                continue
            break
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)

    # Input mau menggunakan rules atau tidak
    while True:
        try:
            rules_wordlist = input(f"{c}[»] {p}Gunakan rules ke file Wordlist? [iya/tidak]: ").lower()
            if rules_wordlist in  ["iya", "tidak"]:
                break
            else:
                print(f"{m}[-] {p}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{r}")
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)

    if rules_wordlist == "iya":
        while True:
            try:
                rules_kombinasi_karakter = input(f"{c}[»] {p}Gunakan rules kombinasi katarater? [iya/tidak]: ").lower()
                if rules_kombinasi_karakter in  ["iya", "tidak"]:
                    break
                else:
                    print(f"{m}[-] {p}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{r}")
            except KeyboardInterrupt:
                print(f"\n{m}[-] {p}Keluar...{k}:({r}")
                exit(1)
                
    elif rules_wordlist == "tidak":
        while True:
            try:
                rules_kombinasi_karakter = input(f"{c}[»] {p}Gunakan rules kombinasi katarater? [iya/tidak]: ").lower()
                if rules_kombinasi_karakter in  ["iya", "tidak"]:
                    break
                else:
                    print(f"{m}[-] {p}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{r}")
            except KeyboardInterrupt:
                print(f"\n{m}[-] {p}Keluar...{k}:({r}")
                exit(1)

    if rules_kombinasi_karakter == "iya":
        kombinasirules = []
        daftar_rules = ["Huruf Besar", "Huruf Kecil", "Angka", "Simbol"]

        counter = 1
        x = 1
        
        while True:
            try:
                panjang_rules = int(input(f"{c}[»] {p}Masukkan panjang rules kombinasi karakter: "))
                if panjang_rules <= 0:
                    print(f"{m}[-] {p}Panjang rules kombinasi karakter harus lebih dari 0.{r}")
                    continue
                break
            except ValueError:
                print(f"{m}[-] {p}Masukkan nilai angka yang valid.{r}")
            except KeyboardInterrupt:
                print(f"\n{m}[-] {p}Keluar...{k}:({r}")
                exit(1)

        print("\nJenis kombinasi karakter yang tersedia:\n")
        for menu_rules in daftar_rules:
            print(f"{x}. {menu_rules}")
            x += 1
        print("")
        
        while counter <= panjang_rules:
            try:
                rules = input(f"{c}[»] {p}Masukkan rules ke-{counter}: ")
                if rules == "1" or rules == daftar_rules[0]:
                    kombinasirules += string.ascii_uppercase
                elif rules == "2" or rules == daftar_rules[2]:
                    kombinasirules += string.ascii_lowercase
                elif rules == "3" or rules == daftar_rules[2]:
                    kombinasirules += string.digits
                elif rules == "4" or rules == daftar_rules[2]:
                    kombinasirules += string.punctuation
                
            except KeyboardInterrupt:
                print(f"\n{m}[-] {p}Keluar...{k}:({r}")
                exit(1)
            counter += 1

    elif rules_kombinasi_karakter == "tidak":
        pass
    
    # Input mau menggunakan verbose atau tidak
    while True:
        try:
            verbose = input(f"{c}[»] {p}Gunakan mode verbose? [iya/tidak]: ").lower()
            if verbose in ["iya", "tidak"]:
                break
            else:
                print(f"{m}[-] {p}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{r}")
        except KeyboardInterrupt:
            print(f"\n{m}[-] {p}Keluar...{k}:({r}")
            exit(1)

    input(f"\n{h}Tekan [Enter] untuk memulai proses Cracking...{r}")
    print("")
    # *************** CRACK KATA SANDI FILE ZIP DENGAN METODE SERANGAN COMBINATOR ATTACK ***************
    try:
        with pyzipper.AESZipFile(input_zip) as fz:
            with open(input_wordlist1, encoding="latin-1", errors="ignore") as fw1:
                # Ambil baris pertama dari Wordlist 2
                with open(input_wordlist2, encoding="latin-1", errors="ignore") as fw2:
                    words2 = fw2.readlines()
                    for word1 in fw1:
                        word1 = word1.strip()
                        for word2 in words2:
                            word2 = word2.strip()
                            for word3 in itertools.product(kombinasirules, repeat=panjang_rules):
                                word3 = "".join(coba_rules)
                                if rules_wordlist == "iya":
                                    if rules_kombinasi_karakter == "iya":
                                        kata_sandi = (word2 + word1 + word3)
                                elif rules_wordlist == "tidak":
                                    kata_sandi = (word1 + word2)
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
                                    if verbose == "iya":
                                        print(f"{m}[-] {p}Kata sandi salah: {m}{kata_sandi}{r}")
                                        continue
                                    continue
        # Jika kata sandi tidak ditemukan
        if not kata_sandi_ditemukan:
            print(f"{p}--------------------------------------------------{r}")
            print(f"{m}[-] {p}Kata sandi tidak ditemukan.{r}")
            print(f"{p}--------------------------------------------------{r}")
    except Exception as e:
        print(f"{m}[-] {p}Kesalahan terjadi: {m}{e}{r}")
