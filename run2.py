#!/usr/bin/env python
#
# PyUnzip
# =======
# PyUnzip adalah program Python sederhana 
# yang dirancang untuk meng-crack kata sandi
# file Zip. Program ini menggunakan teknik
# Dictionary Attack dan Brute Force Attack.
#
# Jenis Enkripsi yang didukung PyUnzip
#-------------------------------------
# [+] ZipCrypto
# [+] AES-128
# [+] AES-192
# [+] AES-256
#
# Pembuat 
# -------
# BgRopay
#
# Lisensi 
#--------
# MIT License
#
# Hak Cipta (c) 2024 bgropay
#

import os
import itertools
import string
import colorama
import pyzipper

class PyUnzip:
    def __init__(self):
        self.m = colorama.Fore.LIGHTRED_EX
        self.h = colorama.Fore.LIGHTGREEN_EX
        self.b = colorama.Fore.LIGHTBLUE_EX
        self.k = colorama.Fore.LIGHTYELLOW_EX
        self.c = colorama.Fore.LIGHTCYAN_EX
        self.p = colorama.Fore.LIGHTWHITE_EX
        self.r = colorama.Style.RESET_ALL
        self.bm = colorama.Back.LIGHTRED_EX
        self.kata_sandi_ditemukan = False

    def clear_screen(self):
        if os.name == "nt":
            os.system("cls")
        elif os.name == "posix":
            os.system("clear")
        else:
            print(f"{self.m}[-] {self.p}Sistem operasi Anda tidak mendukung untuk menjalankan program PyUnzip :({self.r}")
            exit(1)

    def banner(self):
        print(f"""{self.p}******************************************************{self.r}
{self.p}* {self.h}[+] {self.p}Program   : {self.k}PyUnzip                            {self.p}*{self.r}
{self.p}* {self.h}[+] {self.p}Pembuat   : {self.k}BgRopay                            {self.p}*{self.r}
{self.p}* {self.h}[+] {self.p}Deskripsi : {self.k}Crack Kata Sandi File Zip          {self.p}*{self.r}
{self.p}* {self.h}[+] {self.p}Github    : {self.k}https://github.com/bgropay/pyunzip {self.p}*{self.r}
{self.p}******************************************************{self.r}

{self.bm}{self.p}:: Program ini hanya untuk tujuan Edukasi dan Pembelajaran. ::{self.r}
{self.bm}{self.p}:: Jangan gunakan program ini untuk tujuan ilegal.          ::{self.r}
""")

    def get_zip_file(self):
        while True:
            try:
                input_zip = input(f"{self.c}[»] {self.p}Masukkan jalur ke file Zip: ")
                if not os.path.isfile(input_zip):
                    print(f"{self.m}[-] {self.p}File Zip {input_zip} tidak ditemukan.{self.r}")
                    continue
                if not input_zip.endswith(".zip"):
                    print(f"{self.m}[-] {self.p}File {input_zip} bukan file Zip.{self.r}")
                    continue
                return input_zip
            except KeyboardInterrupt:
                print(f"\n{self.m}[-] {self.p}Keluar...{self.k}:({self.r}")
                exit(1)

    def get_attack_method(self):
        methods = ["Brute Force Attack", "Dictionary Attack"]
        for i, method in enumerate(methods, 1):
            print(f"{i}. {method}")
        while True:
            try:
                choice = input(f"{self.c}[»] {self.p}Pilih metode serangan: ")
                if choice not in ["1", "2"]:
                    print(f"{self.m}[-] {self.p} Metode serangan '{choice}' tidak tersedia.{self.r}")
                    continue
                return choice
            except KeyboardInterrupt:
                print(f"\n{self.m}[-] {self.p}Keluar...{self.k}:({self.r}")
                exit(1)

    def get_min_max_length(self):
        while True:
            try:
                min_length = int(input(f"{self.c}[»] {self.p}Masukkan panjang minimal kata sandi: "))
                if min_length <= 0:
                    print(f"{self.m}[-] {self.p}Panjang minimal kata sandi harus lebih dari 0.{self.r}")
                    continue
                break
            except ValueError:
                print(f"{self.m}[-] {self.p}Masukkan nilai angka yang valid.{self.r}")
            except KeyboardInterrupt:
                print(f"\n{self.m}[-] {self.p}Keluar...{self.k}:({self.r}")
                exit(1)

        while True:
            try:
                max_length = int(input(f"{self.c}[»] {self.p}Masukkan panjang maksimal kata sandi: "))
                if max_length < min_length:
                    print(f"{self.m}[-] {self.p}Panjang maksimal kata sandi harus lebih dari atau sama dengan panjang minimal kata sandi.{self.r}")
                    continue
                return min_length, max_length
            except ValueError:
                print(f"{self.m}[-] {self.p}Masukkan nilai angka yang valid.{self.r}")
            except KeyboardInterrupt:
                print(f"\n{self.m}[-] {self.p}Keluar...{self.k}:({self.r}")
                exit(1)

    def get_character_combinations(self):
        kombinasi_karakter = ""
        options = {
            "huruf kecil": string.ascii_lowercase,
            "huruf besar": string.ascii_uppercase,
            "angka": string.digits,
            "simbol": string.punctuation,
        }
        for desc, chars in options.items():
            while True:
                try:
                    choice = input(f"{self.c}[»] {self.p}Gunakan {desc}? [iya/tidak]: ").lower()
                    if choice in ["iya", "tidak"]:
                        if choice == "iya":
                            kombinasi_karakter += chars
                        break
                    else:
                        print(f"{self.m}[-] {self.p}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{self.r}")
                except KeyboardInterrupt:
                    print(f"\n{self.m}[-] {self.p}Keluar...{self.k}:({self.r}")
                    exit(1)

        if not kombinasi_karakter:
            print(f"{self.m}[-] {self.p}Anda harus memilih setidaknya satu jenis karakter.{self.r}")
            return self.get_character_combinations()

        return kombinasi_karakter

    def brute_force_attack(self, zip_file, min_length, max_length, kombinasi_karakter):
        input(f"\n{self.h}Tekan [Enter] untuk memulai proses Cracking...{self.r}")
        self.clear_screen()

        try:
            with pyzipper.AESZipFile(zip_file) as fz:
                for length in range(min_length, max_length + 1):
                    for attempt in itertools.product(kombinasi_karakter, repeat=length):
                        kata_sandi = ''.join(attempt)
                        try:
                            fz.pwd = kata_sandi.encode("latin-1")
                            if fz.testzip() is None:
                                print(f"{self.p}--------------------------------------------------{self.r}")
                                print(f"{self.h}[+] {self.p}Kata sandi ditemukan: {self.h}{kata_sandi}{self.r}")
                                print(f"{self.p}--------------------------------------------------{self.r}")
                                self.kata_sandi_ditemukan = True
                                return
                        except KeyboardInterrupt:
                            print(f"\n{self.m}[-] {self.p}Keluar...{self.k}:({self.r}")
                            exit(1)
                        except Exception:
                            print(f"{self.m}[-] {self.p}Kata sandi salah: {self.m}{kata_sandi}{self.r}")
                            continue

            if not self.kata_sandi_ditemukan:
                print(f"{self.p}--------------------------------------------------{self.r}")
                print(f"{self.m}[-] {self.p}Kata sandi tidak ditemukan dalam rentang panjang dan karakter yang diberikan.{self.r}")
                print(f"{self.p}--------------------------------------------------{self.r}")
        except Exception as e:
            print(f"{self.m}[-] {self.p}Kesalahan terjadi: {self.m}{e}{self.r}")

    def dictionary_attack(self, zip_file):
        while True:
            try:
                input_wordlist = input(f"{self.c}[»] {self.p}Masukkan jalur ke file Wordlist: ")
                if not os.path.isfile(input_wordlist):
                    print(f"{self.m}[-] {self.p}File Wordlist {input_wordlist} tidak ditemukan.{self.r}")
                    continue
                break
            except KeyboardInterrupt:
                print(f"\n{self.m}[-] {self.p}Keluar...{self.k}:({self.r}")
                exit(1)

        input(f"\n{self.h}Tekan [Enter] untuk memulai proses Cracking...{self.r}")
        self.clear_screen()

        try:
            with pyzipper.AESZipFile(zip_file) as fz:
                with open(input_wordlist, encoding="latin-1", errors="ignore") as fw:
                    for baris_file in fw:
                        kata_sandi = baris_file.strip()
                        try:
                            fz.pwd = kata_sandi.encode("latin-1")
                            if fz.testzip() is None:
                                print(f"{self.p}--------------------------------------------------{self.r}")
                                print(f"{self.h}[+] {self.p}Kata sandi ditemukan: {self.h}{kata_sandi}{self.r}")
                                print(f"{self.p}--------------------------------------------------{self.r}")
                                self.kata_sandi_ditemukan = True
                                return
                        except KeyboardInterrupt:
                            print(f"\n{self.m}[-] {self.p}Keluar...{self.k}:({self.r}")
                            exit(1)
                        except Exception:
                            print(f"{self.m}[-] {self.p}Kata sandi salah: {self.m}{kata_sandi}{self.r}")
                            continue

            if not self.kata_sandi_ditemukan:
                print(f"{self.p}--------------------------------------------------{self.r}")
                print(f"{self.m}[-] {self.p}Kata sandi tidak ditemukan dalam file wordlist {self.m}{input_wordlist}{self.r}")
                print(f"{self.p}--------------------------------------------------{self.r}")
        except Exception as e:
            print(f"{self.m}[-] {self.p}Kesalahan terjadi: {self.m}{e}{self.r}")

    def run(self):
        self.clear_screen()
        self.banner()

        zip_file = self.get_zip_file()
        attack_method = self.get_attack_method()

        if attack_method == "1":
            min_length, max_length = self.get_min_max_length()
            kombinasi_karakter = self.get_character_combinations()
            self.brute_force_attack(zip_file, min_length, max_length, kombinasi_karakter)
        elif attack_method == "2":
            self.dictionary_attack(zip_file)

if __name__ == "__main__":
    PyUnzip().run()
