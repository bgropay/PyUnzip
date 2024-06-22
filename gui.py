import os
import time
import itertools
import string
import pyzipper
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class PyUnzip:
    def __init__(self, root):
        self.root = root
        self.root.title("PyUnzip")
        
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.root, text="PyUnzip - Crack Kata Sandi File Zip", font=("Arial", 16)).pack(pady=10)
        
        tk.Button(self.root, text="Pilih File Zip", command=self.choose_zip_file).pack(pady=5)
        self.zip_file_label = tk.Label(self.root, text="File Zip: None")
        self.zip_file_label.pack(pady=5)
        
        tk.Button(self.root, text="Pilih Metode Serangan", command=self.choose_attack_method).pack(pady=5)
        self.method_label = tk.Label(self.root, text="Metode: None")
        self.method_label.pack(pady=5)
        
        self.start_button = tk.Button(self.root, text="Mulai Cracking", command=self.start_cracking)
        self.start_button.pack(pady=20)
        self.start_button.config(state=tk.DISABLED)
        
        self.output_text = tk.Text(self.root, height=10, width=50, state=tk.DISABLED)
        self.output_text.pack(pady=10)
        
    def choose_zip_file(self):
        self.zip_file = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
        if self.zip_file:
            self.zip_file_label.config(text=f"File Zip: {self.zip_file}")
            self.check_start_button()
    
    def choose_attack_method(self):
        self.method_window = tk.Toplevel(self.root)
        self.method_window.title("Pilih Metode Serangan")
        
        tk.Button(self.method_window, text="Brute Force Attack", command=lambda: self.set_method("Brute Force Attack")).pack(pady=5)
        tk.Button(self.method_window, text="Dictionary Attack", command=lambda: self.set_method("Dictionary Attack")).pack(pady=5)
    
    def set_method(self, method):
        self.method = method
        self.method_label.config(text=f"Metode: {method}")
        self.method_window.destroy()
        self.check_start_button()
    
    def check_start_button(self):
        if hasattr(self, 'zip_file') and hasattr(self, 'method'):
            self.start_button.config(state=tk.NORMAL)
    
    def start_cracking(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        
        if self.method == "Brute Force Attack":
            self.brute_force_setup()
        elif self.method == "Dictionary Attack":
            self.dictionary_setup()
    
    def brute_force_setup(self):
        min_length = simpledialog.askinteger("Panjang Minimal", "Masukkan panjang minimal kata sandi:")
        max_length = simpledialog.askinteger("Panjang Maksimal", "Masukkan panjang maksimal kata sandi:")
        
        if min_length and max_length and min_length > 0 and max_length >= min_length:
            kombinasi_karakter = ""
            if messagebox.askyesno("Karakter", "Gunakan huruf kecil?"):
                kombinasi_karakter += string.ascii_lowercase
            if messagebox.askyesno("Karakter", "Gunakan huruf besar?"):
                kombinasi_karakter += string.ascii_uppercase
            if messagebox.askyesno("Karakter", "Gunakan angka?"):
                kombinasi_karakter += string.digits
            if messagebox.askyesno("Karakter", "Gunakan simbol?"):
                kombinasi_karakter += string.punctuation
            
            if kombinasi_karakter:
                self.brute_force_attack(self.zip_file, min_length, max_length, kombinasi_karakter)
            else:
                messagebox.showerror("Error", "Anda harus memilih setidaknya satu jenis karakter.")
        else:
            messagebox.showerror("Error", "Panjang minimal atau maksimal tidak valid.")
    
    def dictionary_setup(self):
        self.wordlist_file = filedialog.askopenfilename(title="Pilih File Wordlist")
        if self.wordlist_file:
            self.dictionary_attack(self.zip_file, self.wordlist_file)
    
    def update_output(self, message):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        
    def brute_force_attack(self, input_zip, min_length, max_length, kombinasi_karakter):
        self.update_output("Memulai Brute Force Attack...")
        
        try:
            with pyzipper.AESZipFile(input_zip) as fz:
                for length in range(min_length, max_length + 1):
                    for attempt in itertools.product(kombinasi_karakter, repeat=length):
                        kata_sandi = ''.join(attempt)
                        try:
                            fz.pwd = kata_sandi.encode("latin-1")
                            if fz.testzip() is None:
                                self.update_output(f"Kata sandi ditemukan: {kata_sandi}")
                                messagebox.showinfo("Sukses", f"Kata sandi ditemukan: {kata_sandi}")
                                return
                        except KeyboardInterrupt:
                            self.update_output("Keluar...")
                            return
                        except Exception:
                            self.update_output(f"Kata sandi salah: {kata_sandi}")
                            continue

            self.update_output("Kata sandi tidak ditemukan dalam rentang panjang dan karakter yang diberikan.")
            messagebox.showinfo("Gagal", "Kata sandi tidak ditemukan.")
        except Exception as e:
            self.update_output(f"Kesalahan terjadi: {e}")
    
    def dictionary_attack(self, input_zip, wordlist):
        self.update_output("Memulai Dictionary Attack...")
        
        try:
            with pyzipper.AESZipFile(input_zip) as fz:
                with open(wordlist, encoding="latin-1", errors="ignore") as fw:
                    for baris_file in fw:
                        kata_sandi = baris_file.strip()
                        try:
                            fz.pwd = kata_sandi.encode("latin-1")
                            if fz.testzip() is None:
                                self.update_output(f"Kata sandi ditemukan: {kata_sandi}")
                                messagebox.showinfo("Sukses", f"Kata sandi ditemukan: {kata_sandi}")
                                return
                        except KeyboardInterrupt:
                            self.update_output("Keluar...")
                            return
                        except Exception:
                            self.update_output(f"Kata sandi salah: {kata_sandi}")
                            continue

            self.update_output(f"Kata sandi tidak ditemukan dalam file wordlist {wordlist}.")
            messagebox.showinfo("Gagal", "Kata sandi tidak ditemukan.")
        except Exception as e:
            self.update_output(f"Kesalahan terjadi: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PyUnzip(root)
    root.mainloop()
      
