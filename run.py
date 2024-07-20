#!/usr/bin/env python3

import pyzipper

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
            print(f"{m}[-] {p}Kata sandi tidak ditemukan dalam file wordlist {m}{input_wordlist}{r}")
            print(f"{p}--------------------------------------------------{r}")
    except Exception as e:
        print(f"{m}[-] {p}Kesalahan terjadi: {m}{e}{r}")
