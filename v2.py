#!/usr/bin/env python3

import os
import sys
import itertools
import string
import colorama
import pyzipper
import multiprocessing

# Mengubah output warna teks
class Color:
    RED = colorama.Fore.LIGHTRED_EX
    GREEN = colorama.Fore.LIGHTGREEN_EX
    BLUE = colorama.Fore.LIGHTBLUE_EX
    YELLOW = colorama.Fore.LIGHTYELLOW_EX
    CYAN = colorama.Fore.LIGHTCYAN_EX
    WHITE = colorama.Fore.LIGHTWHITE_EX
    RESET = colorama.Style.RESET_ALL
    BRED = colorama.Back.LIGHTRED_EX

class ZipCracker:
    def __init__(self):
        self.so = os.name
        self.kata_sandi_ditemukan = False
        self.input_zip = None
        self.metode_serangan = None
        self.input_wordlist = None
        self.min_length = None
        self.max_length = None
        self.kombinasi_karakter = ""
        self.pool = None
        self.results = []

    def clear_screen(self):
        if self.so == "nt":
            os.system("cls")
        elif self.so == "posix":
            os.system("clear")
        else:
            print(f"{Color.RED}[-] {Color.WHITE}Sistem operasi Anda tidak mendukung untuk menjalankan program PyUnzip :({Color.RESET}")
            exit(1)

    def banner(self):
        print(f"""{Color.WHITE}******************************************************{Color.RESET}
{Color.WHITE}* {Color.GREEN}[+] {Color.WHITE}Program   : {Color.YELLOW}PyUnzip                            {Color.WHITE}*{Color.RESET}
{Color.WHITE}* {Color.GREEN}[+] {Color.WHITE}Pembuat   : {Color.YELLOW}BgRopay                            {Color.WHITE}*{Color.RESET}
{Color.WHITE}* {Color.GREEN}[+] {Color.WHITE}Deskripsi : {Color.YELLOW}Crack Kata Sandi File Zip          {Color.WHITE}*{Color.RESET}
{Color.WHITE}* {Color.GREEN}[+] {Color.WHITE}Github    : {Color.YELLOW}https://github.com/bgropay/pyunzip {Color.WHITE}*{Color.RESET}
{Color.WHITE}******************************************************{Color.RESET}

{Color.BRED}{Color.WHITE}:: Program ini hanya untuk tujuan Edukasi dan Pembelajaran. ::{Color.RESET}
{Color.BRED}{Color.WHITE}:: Jangan gunakan program ini untuk tujuan ilegal.          ::{Color.RESET}
""")

    def input_zip_file(self):
        while True:
            try:
                self.input_zip = input(f"{Color.CYAN}[»] {Color.WHITE}Masukkan jalur ke file Zip: ")
                if not os.path.isfile(self.input_zip):
                    print(f"{Color.RED}[-] {Color.WHITE}File Zip '{self.input_zip}' tidak ditemukan.{Color.RESET}")
                    continue
                if not self.input_zip.endswith(".zip"):
                    print(f"{Color.RED}[-] {Color.WHITE}File '{self.input_zip}' bukan file Zip.{Color.RESET}")
                    continue
                break
            except KeyboardInterrupt:
                print(f"\n{Color.RED}[-] {Color.WHITE}Keluar...{Color.YELLOW}:({Color.RESET}")
                exit(1)

    def select_attack_method(self):
        x = 1
        print("\nMetode serangan yang tersedia:\n")
        list_metode_serangan = ["Brute Force Attack", "Dictionary Attack"]
        for metode in list_metode_serangan:
            print(f"{x}. {metode}")
            x += 1
        print("")
        while True:
            try:
                self.metode_serangan = input(f"{Color.CYAN}[»] {Color.WHITE}Pilih metode serangan: ")
                if self.metode_serangan not in ["1", "2"]:
                    print(f"{Color.RED}[-] {Color.WHITE}Metode serangan '{self.metode_serangan}' tidak tersedia.{Color.RESET}")
                    continue
                break
            except KeyboardInterrupt:
                print(f"\n{Color.RED}[-] {Color.WHITE}Keluar...{Color.YELLOW}:({Color.RESET}")
                exit(1)

    def brute_force_setup(self):
        while True:
            try:
                self.min_length = int(input(f"{Color.CYAN}[»] {Color.WHITE}Masukkan panjang minimal kata sandi: "))
                if self.min_length <= 0:
                    print(f"{Color.RED}[-] {Color.WHITE}Panjang minimal kata sandi harus lebih dari 0.{Color.RESET}")
                    continue
                break
            except ValueError:
                print(f"{Color.RED}[-] {Color.WHITE}Masukkan nilai angka yang valid.{Color.RESET}")
            except KeyboardInterrupt:
                print(f"\n{Color.RED}[-] {Color.WHITE}Keluar...{Color.YELLOW}:({Color.RESET}")
                exit(1)

        while True:
            try:
                self.max_length = int(input(f"{Color.CYAN}[»] {Color.WHITE}Masukkan panjang maksimal kata sandi: "))
                if self.max_length < self.min_length:
                    print(f"{Color.RED}[-] {Color.WHITE}Panjang maksimal kata sandi harus lebih dari atau sama dengan panjang minimal kata sandi.{Color.RESET}")
                    continue
                break
            except ValueError:
                print(f"{Color.RED}[-] {Color.WHITE}Masukkan nilai angka yang valid.{Color.RESET}")
            except KeyboardInterrupt:
                print(f"\n{Color.RED}[-] {Color.WHITE}Keluar...{Color.YELLOW}:({Color.RESET}")
                exit(1)

        while True:
            try:
                while True:
                    pilih_huruf_kecil = input(f"{Color.CYAN}[»] {Color.WHITE}Gunakan huruf kecil? [iya/tidak]: ").lower()
                    if pilih_huruf_kecil in ["iya", "tidak"]:
                        if pilih_huruf_kecil == "iya":
                            self.kombinasi_karakter += string.ascii_lowercase
                        break
                    else:
                        print(f"{Color.RED}[-] {Color.WHITE}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{Color.RESET}")

                while True:
                    pilih_huruf_besar = input(f"{Color.CYAN}[»] {Color.WHITE}Gunakan huruf besar? [iya/tidak]: ").lower()
                    if pilih_huruf_besar in ["iya", "tidak"]:
                        if pilih_huruf_besar == "iya":
                            self.kombinasi_karakter += string.ascii_uppercase
                        break
                    else:
                        print(f"{Color.RED}[-] {Color.WHITE}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{Color.RESET}")

                while True:
                    pilih_angka = input(f"{Color.CYAN}[»] {Color.WHITE}Gunakan angka? [iya/tidak]: ").lower()
                    if pilih_angka in ["iya", "tidak"]:
                        if pilih_angka == "iya":
                            self.kombinasi_karakter += string.digits
                        break
                    else:
                        print(f"{Color.RED}[-] {Color.WHITE}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{Color.RESET}")

                while True:
                    pilih_simbol = input(f"{Color.CYAN}[»] {Color.WHITE}Gunakan simbol? [iya/tidak]: ").lower()
                    if pilih_simbol in ["iya", "tidak"]:
                        if pilih_simbol == "iya":
                            self.kombinasi_karakter += string.punctuation
                        break
                    else:
                        print(f"{Color.RED}[-] {Color.WHITE}Input tidak valid. Harap masukkan 'iya' atau 'tidak'.{Color.RESET}")

                if not self.kombinasi_karakter:
                    print(f"{Color.RED}[-] {Color.WHITE}Anda harus memilih setidaknya satu jenis karakter.{Color.RESET}")
                    continue
                break
            except KeyboardInterrupt:
                print(f"\n{Color.RED}[-] {Color.WHITE}Keluar...{Color.YELLOW}:({Color.RESET}")
                exit(1)

    def start_cracking(self):
        input(f"\n{Color.GREEN}Tekan [Enter] untuk memulai proses Cracking...{Color.RESET}")

        self.clear_screen()

        try:
            if self.metode_serangan == "1":
                self.brute_force_attack()
            elif self.metode_serangan == "2":
                self.dictionary_attack()
        except Exception as e:
            print(f"{Color.RED}[-] {Color.WHITE}Kesalahan terjadi: {Color.RED}{e}{Color.RESET}")

    def brute_force_attack(self):
        try:
            def crack_password(length_range):
                with pyzipper.AESZipFile(self.input_zip) as fz:
                    for length in range(length_range[0], length_range[1] + 1):
                        for attempt in itertools.product(self.kombinasi_karakter, repeat=length):
                            kata_sandi = ''.join(attempt)
                            try:
                                fz.pwd = kata_sandi.encode("latin-1")
                                if fz.testzip() is None:
                                    print(f"{Color.BLUE}--------------------------------------------------{Color.RESET}")
                                    print(f"{Color.GREEN}[+] {Color.WHITE}Kata sandi ditemukan: {Color.GREEN}{kata_sandi}{Color.RESET}")
                                    print(f"{Color.BLUE}--------------------------------------------------{Color.RESET}")
                                    self.kata_sandi_ditemukan = True
                                    return kata_sandi
                            except KeyboardInterrupt:
                                print(f"\n{Color.RED}[-] {Color.WHITE}Keluar...{Color.YELLOW}:({Color.RESET}")
                                exit(1)
                            except Exception:
                                print(f"{Color.RED}[-] {Color.WHITE}Kata sandi salah: {Color.RED}{kata_sandi}{Color.RESET}")
                                continue
                    return None

            def chunk_range(start, end, num_chunks):
                chunk_size = (end - start + 1) // num_chunks
                chunks = []
                for i in range(num_chunks):
                    if i == num_chunks - 1:
                        chunks.append((start + i * chunk_size, end))
                    else:
                        chunks.append((start + i * chunk_size, start + (i + 1) * chunk_size - 1))
                return chunks

            # Calculate the range of password lengths to attempt
            range_chunks = chunk_range(self.min_length, self.max_length, multiprocessing.cpu_count())

            # Set up multiprocessing pool
            self.pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
            results = self.pool.map(crack_password, range_chunks)

            # Check results for password found
            for result in results:
                if result:
                    self.kata_sandi_ditemukan = True
                    break

            # Close multiprocessing pool
            self.pool.close()
            self.pool.join()

            # If password not found
            if not self.kata_sandi_ditemukan:
                print(f"{Color.BLUE}--------------------------------------------------{Color.RESET}")
                print(f"{Color.RED}[-] {Color.WHITE}Kata sandi tidak ditemukan dalam rentang panjang dan karakter yang diberikan.{Color.RESET}")
                print(f"{Color.BLUE}--------------------------------------------------{Color.RESET}")

        except Exception as e:
            print(f"{Color.RED}[-] {Color.WHITE}Kesalahan terjadi: {Color.RED}{e}{Color.RESET}")

    def dictionary_attack(self):
        try:
            with pyzipper.AESZipFile(self.input_zip) as fz:
                with open(self.input_wordlist, encoding="latin-1", errors="ignore") as fw:
                    for baris_file in fw:
                        kata_sandi = baris_file.strip()
                        try:
                            fz.pwd = kata_sandi.encode("latin-1")
                            if fz.testzip() is None:
                                print(f"{Color.BLUE}--------------------------------------------------{Color.RESET}")
                                print(f"{Color.GREEN}[+] {Color.WHITE}Kata sandi ditemukan: {Color.GREEN}{kata_sandi}{Color.RESET}")
                                print(f"{Color.BLUE}--------------------------------------------------{Color.RESET}")
                                self.kata_sandi_ditemukan = True
                                break
                        except KeyboardInterrupt:
                            print(f"\n{Color.RED}[-] {Color.WHITE}Keluar...{Color.YELLOW}:({Color.RESET}")
                            exit(1)
                        except Exception:
                            print(f"{Color.RED}[-] {Color.WHITE}Kata sandi salah: {Color.RED}{kata_sandi}{Color.RESET}")
                            continue

            # If password not found
            if not self.kata_sandi_ditemukan:
                print(f"{Color.BLUE}--------------------------------------------------{Color.RESET}")
                print(f"{Color.RED}[-] {Color.WHITE}Kata sandi tidak ditemukan dalam file wordlist {Color.RED}{self.input_wordlist}{Color.RESET}")
                print(f"{Color.BLUE}--------------------------------------------------{Color.RESET}")

        except Exception as e:
            print(f"{Color.RED}[-] {Color.WHITE}Kesalahan terjadi: {Color.RED}{e}{Color.RESET}")

def main():
    try:
        zip_cracker = ZipCracker()
        zip_cracker.banner()
        zip_cracker.input_zip_file()
        zip_cracker.select_attack_method()

        if zip_cracker.metode_serangan == "1":
            zip_cracker.brute_force_setup()
        elif zip_cracker.metode_serangan == "2":
            zip_cracker.input_wordlist = input(f"{Color.CYAN}[»] {Color.WHITE}Masukkan jalur ke file Wordlist: ")

        zip_cracker.start_cracking()

    except KeyboardInterrupt:
        print(f"\n{Color.RED}[-] {Color.WHITE}Keluar...{Color.YELLOW}:({Color.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
