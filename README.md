# Tugas Praktikum Sistem Basis Data (MySQL Console)

**Nama**: Muhammad Zikri Adam  
**NIM**: F5512530117 (Kategori Stambuk: **GANJIL** - Akhiran 7)  
**Program Studi**: S1 Teknik Informatika  
**Jurusan**: Teknologi Informasi  
**Fakultas**: Teknik, Universitas Tadulako  
**Mata Kuliah**: Sistem Basis Data  
**DBMS**: MySQL Server 8.0 (*Command Line / Console Interface*)

---

## 📌 Ringkasan Proyek

Repository ini berisi seluruh berkas implementasi dan dokumentasi penugasan praktikum Sistem Basis Data yang mencakup DDL, DCL, DML, Relasi Entitas (ERD), operasi JOIN (INNER, LEFT, RIGHT), serta fungsi agregat (MAX, MIN, COUNT) yang seluruhnya dikerjakan menggunakan perintah terminal/konsol MySQL sesuai ketentuan akademik.

---

## 🗄️ Struktur Basis Data

Sesuai ketentuan tugas, dibuat 3 (tiga) basis data terpisah dengan format `Stambuk_namadatabase` yang masing-masing memiliki minimal 5 tabel relasional dengan jenis entitas yang 100% berbeda satu sama lain:

### 1. `F5512530117_bioskop` (Sistem Informasi Tiket Bioskop & Cinema)
Mengelola penayangan film, studio auditorium, data penonton, jadwal tayang, serta transaksi pembelian tiket.
- **Tabel**:
  1. `film` (Master film: judul, genre, durasi, rating usia, harga dasar)
  2. `studio` (Master auditorium: tipe layar, kapasitas kursi, biaya tambahan)
  3. `penonton` (Master pengunjung: nama, nik, email, no_hp, domisili, tgl_lahir)
  4. `jadwal_tayang` (Relasi penjadwalan film di studio)
  5. `transaksi_tiket` (Transaksi pemesanan tiket kursi oleh penonton)

### 2. `F5512530117_ekspedisi` (Sistem Manajemen Logistik & Pengiriman Kargo)
Mengelola transaksi pengiriman paket kargo antar wilayah dan tracking posisi barang.
- **Tabel**:
  1. `pengirim` (Master pihak pengirim)
  2. `penerima` (Master pihak penerima)
  3. `kurir` (Master armada kurir)
  4. `paket` (Transaksi pengiriman paket)
  5. `pelacakan_status` (Riwayat log tracking posisi paket)

### 3. `F5512530117_kursus` (Sistem Akademi Bimbingan Belajar)
Mengelola silabus kursus, instruktur pengajar, peserta siswa, jadwal kelas, dan pendaftaran.
- **Tabel**:
  1. `materi_kursus` (Master materi kursus)
  2. `instruktur` (Master pengajar)
  3. `siswa` (Master peserta kursus)
  4. `jadwal_kelas` (Slot waktu dan ruang kelas online)
  5. `pendaftaran` (Transaksi registrasi kelas)

---

## 📂 Struktur Berkas Repository

```text
├── 01_tugas1_ddl_dan_dcl.sql       # Script DDL 3 DB, DCL 4 user, simulasi read-only, ALTER TABLE
├── 02_tugas2_dml.sql               # Script INSERT 10 baris, UPDATE baris ganjil, SELECT 3 kriteria, LIMIT, DELETE
├── 03_tugas3_join_dan_agregat.sql  # Script relasional 3 tabel, INNER/LEFT/RIGHT JOIN, fungsi agregat
├── all_in_one_praktikum.sql        # Master script SQL untuk eksekusi sekali jalan di console MySQL
├── generate_erd_images.py          # Script python penghasil diagram ERD resolusi tinggi (300 DPI)
├── build_laporan_lengkap.py        # Script generator laporan resmi DOCX & PDF berstandar akademik
├── erd_database_1_bioskop.png      # Diagram ERD Basis Data Bioskop
├── erd_database_2_ekspedisi.png    # Diagram ERD Basis Data Ekspedisi
├── erd_database_3_kursus.png       # Diagram ERD Basis Data Kursus
├── erd_relasi_3_tabel_join.png     # Diagram ERD 3 Tabel Relasi untuk Pembuktian JOIN
├── Laporan_Praktikum_Basis_Data_F5512530117_Muhammad_Zikri_Adam.docx # Laporan akademik editable
├── Laporan_Praktikum_Basis_Data_F5512530117_Muhammad_Zikri_Adam.pdf  # Dokumen laporan siap kumpul LMS
└── README.md                       # Dokumentasi repositori
```

---

## 💻 Panduan Menjalankan Script di Console MySQL

1. Buka **MySQL 8.0 Command Line Client** atau buka `cmd` lalu login:
   ```cmd
   mysql -u root -p
   ```
2. Jalankan file SQL master secara langsung menggunakan perintah `SOURCE`:
   ```sql
   SOURCE all_in_one_praktikum.sql;
   ```
   *(Atau jalankan file per bagian secara berurutan: `01_tugas1_ddl_dan_dcl.sql`, `02_tugas2_dml.sql`, dan `03_tugas3_join_dan_agregat.sql`).*

---

## 🧠 Catatan Penting Implementasi

1. **Aturan Stambuk Ganjil (NIM: F5512530117 - Akhiran 7)**:
   Operasi modifikasi data (`UPDATE`) pada Tugas 2 secara konsisten diterapkan pada **Baris Ganjil (baris ke-1, 3, 5, 7, dan 9)** menggunakan klausa `WHERE id IN (1, 3, 5, 7, 9)`.
2. **Klausa LIMIT Baris 3 hingga 7**:
   Menggunakan konsep zero-based index di MySQL: baris ke-3 berposisi pada offset 2, sehingga sintaks resmi yang digunakan adalah:
   ```sql
   SELECT * FROM penonton ORDER BY id_penonton ASC LIMIT 5 OFFSET 2;
   -- atau sintaks ringkas: LIMIT 2, 5;
   ```
3. **Pembuktian INNER, LEFT, dan RIGHT JOIN**:
   Menyertakan dataset khusus (penonton baru tanpa tiket dan film baru tanpa tiket terjual) sehingga hasil `LEFT JOIN` dan `RIGHT JOIN` secara akurat menampilkan baris dengan nilai `NULL` untuk baris yang tidak berpasangan.
