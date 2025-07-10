import csv
from datetime import datetime
import os
import shutil

# Fungsi untuk memilih pengguna dan menentukan nama file
def pilih_pengguna():
    nama = input("Masukkan nama pengguna: ").strip().lower()
    return f"keuangan_{nama}.csv"

FILE_NAME = ""

# Inisialisasi file CSV jika belum ada
def inisialisasi_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Tanggal', 'Jenis', 'Kategori', 'Deskripsi', 'Jumlah'])

# Backup otomatis
def backup_file():
    today = datetime.now().strftime('%Y-%m-%d')
    backup_name = f"backup_{FILE_NAME.split('.')[0]}_{today}.csv"
    shutil.copy(FILE_NAME, backup_name)
    print(f"Backup otomatis disimpan sebagai {backup_name}")

# Hitung saldo saat ini
def hitung_saldo():
    saldo = 0
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                jumlah = int(row['Jumlah'])
                if row['Jenis'].lower() == 'pemasukan':
                    saldo += jumlah
                elif row['Jenis'].lower() == 'pengeluaran':
                    saldo -= jumlah
    return saldo

def tambah_catatan():
    tanggal = input("Tanggal (YYYY-MM-DD): ")
    jenis = input("Jenis [Pemasukan/Pengeluaran]: ")
    kategori = input("Kategori: ")
    deskripsi = input("Deskripsi: ")
    jumlah = int(input("Jumlah: "))

    if jenis.lower() == 'pengeluaran':
        saldo = hitung_saldo()
        if jumlah > saldo:
            print(f"Saldo tidak cukup! Sisa saldo: Rp{saldo}")
            return

    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([tanggal, jenis, kategori, deskripsi, jumlah])
    print("Catatan berhasil ditambahkan.")
    print(f"Sisa saldo sekarang: Rp{hitung_saldo()}")
    backup_file()

def tampilkan_catatan():
    if not os.path.exists(FILE_NAME):
        print("Belum ada data.")
        return
    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        print("\nDaftar Catatan Keuangan:")
        for idx, row in enumerate(reader, start=1):
            print(f"{idx}. {row}")

def perbarui_catatan():
    tampilkan_catatan()
    index = int(input("Nomor catatan yang ingin diubah: "))
    with open(FILE_NAME, mode='r') as file:
        data = list(csv.reader(file))
    header, isi = data[0], data[1:]

    if 0 < index <= len(isi):
        baru = []
        for kolom, nilai in zip(header, isi[index-1]):
            val = input(f"{kolom} [{nilai}]: ") or nilai
            baru.append(val)
        isi[index-1] = baru
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(isi)
        print("Catatan berhasil diperbarui.")
        backup_file()
    else:
        print("Index tidak valid.")

def hapus_catatan():
    tampilkan_catatan()
    index = int(input("Nomor catatan yang ingin dihapus: "))
    with open(FILE_NAME, mode='r') as file:
        data = list(csv.reader(file))
    header, isi = data[0], data[1:]

    if 0 < index <= len(isi):
        isi.pop(index - 1)
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(isi)
        print("Catatan berhasil dihapus.")
        backup_file()
    else:
        print("Index tidak valid.")

def ringkasan_bulanan():
    bulan = input("Masukkan bulan (01-12): ")
    tahun = input("Masukkan tahun (YYYY): ")
    masuk, keluar = 0, 0

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Tanggal'][0:7] == f"{tahun}-{bulan}":
                jumlah = int(row['Jumlah'])
                if row['Jenis'].lower() == 'pemasukan':
                    masuk += jumlah
                elif row['Jenis'].lower() == 'pengeluaran':
                    keluar += jumlah
    print(f"\nRingkasan {bulan}/{tahun}:")
    print(f"Total Pemasukan   : Rp{masuk}")
    print(f"Total Pengeluaran : Rp{keluar}")

def ringkasan_tahunan():
    tahun = input("Masukkan tahun (YYYY): ")
    masuk, keluar = 0, 0

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Tanggal'][0:4] == tahun:
                jumlah = int(row['Jumlah'])
                if row['Jenis'].lower() == 'pemasukan':
                    masuk += jumlah
                elif row['Jenis'].lower() == 'pengeluaran':
                    keluar += jumlah
    print(f"\nRingkasan Tahun {tahun}:")
    print(f"Total Pemasukan   : Rp{masuk}")
    print(f"Total Pengeluaran : Rp{keluar}")

def jalankan_aplikasi():
    global FILE_NAME
    FILE_NAME = pilih_pengguna()
    inisialisasi_file()
    while True:
        print("\n=== Aplikasi Keuangan Pribadi ===")
        print("1. Tambah Catatan")
        print("2. Lihat Catatan")
        print("3. Ubah Catatan")
        print("4. Hapus Catatan")
        print("5. Ringkasan Bulanan")
        print("6. Ringkasan Tahunan")
        print("7. Keluar")
        pilihan = input("Pilih menu [1-7]: ")

        if pilihan == '1':
            tambah_catatan()
        elif pilihan == '2':
            tampilkan_catatan()
        elif pilihan == '3':
            perbarui_catatan()
        elif pilihan == '4':
            hapus_catatan()
        elif pilihan == '5':
            ringkasan_bulanan()
        elif pilihan == '6':
            ringkasan_tahunan()
        elif pilihan == '7':
            print("Terima kasih telah menggunakan aplikasi.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    jalankan_aplikasi()