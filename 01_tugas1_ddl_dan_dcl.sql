-- ============================================================================
-- PRAKTIKUM SISTEM BASIS DATA - TUGAS 1 (DDL, DESAIN RELASI, DCL, & ALTER TABLE)
-- Nama Mahasiswa : Muhammad Zikri Adam
-- NIM / Stambuk  : F5512530117 (Digit terakhir 7: GANJIL)
-- Program Studi  : S1 Teknik Informatika - Universitas Tadulako
-- DBMS           : MySQL Server 8.0 (Console Command Line)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- BUTIR 1: MEMBUAT 3 (TIGA) DATABASE DENGAN FORMAT: Stambuk_namadatabase
-- DAN MASING-MASING MEMILIKI MINIMAL 5 TABEL YANG BERBEDA
-- ----------------------------------------------------------------------------

-- ============================================================================
-- DATABASE 1: F5512530117_bioskop (Sistem Manajemen Tiket Bioskop & Cinema)
-- ============================================================================
DROP DATABASE IF EXISTS F5512530117_bioskop;
CREATE DATABASE F5512530117_bioskop;
USE F5512530117_bioskop;

-- 1. Tabel Film (Master Data Film yang Tayang)
CREATE TABLE film (
    id_film INT AUTO_INCREMENT PRIMARY KEY,
    judul_film VARCHAR(150) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    durasi_menit INT NOT NULL,
    rating_usia ENUM('SU', '13+', '17+', '21+') NOT NULL,
    harga_dasar DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB;

-- 2. Tabel Studio (Master Data Auditorium / Studio Pemutaran)
CREATE TABLE studio (
    id_studio INT AUTO_INCREMENT PRIMARY KEY,
    nama_studio VARCHAR(50) NOT NULL,
    tipe_layar VARCHAR(30) NOT NULL,
    kapasitas_kursi INT NOT NULL,
    biaya_tambahan DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB;

-- 3. Tabel Penonton (Master Data Pengunjung / Customer Bioskop)
CREATE TABLE penonton (
    id_penonton INT AUTO_INCREMENT PRIMARY KEY,
    nama_penonton VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    no_hp VARCHAR(15) NOT NULL,
    kota_domisili VARCHAR(50) NOT NULL,
    tgl_lahir DATE NOT NULL
) ENGINE=InnoDB;

-- 4. Tabel Jadwal Tayang (Relasi Penjadwalan Film di Studio Tertentu)
CREATE TABLE jadwal_tayang (
    id_jadwal INT AUTO_INCREMENT PRIMARY KEY,
    id_film INT NOT NULL,
    id_studio INT NOT NULL,
    tgl_tayang DATE NOT NULL,
    jam_mulai TIME NOT NULL,
    harga_tiket DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_jadwal_film FOREIGN KEY (id_film) 
        REFERENCES film(id_film) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_jadwal_studio FOREIGN KEY (id_studio) 
        REFERENCES studio(id_studio) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 5. Tabel Transaksi Tiket (Tabel Transaksi Pembelian Tiket oleh Penonton)
CREATE TABLE transaksi_tiket (
    id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
    id_penonton INT NOT NULL,
    id_jadwal INT NOT NULL,
    waktu_transaksi DATETIME NOT NULL,
    nomor_kursi VARCHAR(10) NOT NULL,
    metode_bayar VARCHAR(30) NOT NULL,
    total_bayar DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_tiket_penonton FOREIGN KEY (id_penonton) 
        REFERENCES penonton(id_penonton) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_tiket_jadwal FOREIGN KEY (id_jadwal) 
        REFERENCES jadwal_tayang(id_jadwal) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ============================================================================
-- DATABASE 2: F5512530117_ekspedisi (Sistem Informasi Manajemen Logistik Kargo)
-- ============================================================================
DROP DATABASE IF EXISTS F5512530117_ekspedisi;
CREATE DATABASE F5512530117_ekspedisi;
USE F5512530117_ekspedisi;

-- 1. Tabel Pengirim (Master Pengirim Paket)
CREATE TABLE pengirim (
    id_pengirim INT AUTO_INCREMENT PRIMARY KEY,
    nama_pengirim VARCHAR(100) NOT NULL,
    kota_asal VARCHAR(50) NOT NULL,
    alamat_asal VARCHAR(255) NOT NULL,
    no_telp_pengirim VARCHAR(15) NOT NULL
) ENGINE=InnoDB;

-- 2. Tabel Penerima (Master Penerima Paket)
CREATE TABLE penerima (
    id_penerima INT AUTO_INCREMENT PRIMARY KEY,
    nama_penerima VARCHAR(100) NOT NULL,
    kota_tujuan VARCHAR(50) NOT NULL,
    alamat_tujuan VARCHAR(255) NOT NULL,
    no_telp_penerima VARCHAR(15) NOT NULL
) ENGINE=InnoDB;

-- 3. Tabel Kurir (Master Kurir Ekspedisi)
CREATE TABLE kurir (
    id_kurir INT AUTO_INCREMENT PRIMARY KEY,
    nama_kurir VARCHAR(100) NOT NULL,
    no_plat VARCHAR(15) NOT NULL,
    jenis_kendaraan VARCHAR(30) NOT NULL,
    wilayah_tugas VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- 4. Tabel Paket (Tabel Transaksi Pengiriman Barang)
CREATE TABLE paket (
    id_paket INT AUTO_INCREMENT PRIMARY KEY,
    no_resi VARCHAR(25) UNIQUE NOT NULL,
    id_pengirim INT NOT NULL,
    id_penerima INT NOT NULL,
    id_kurir INT NOT NULL,
    jenis_layanan VARCHAR(30) NOT NULL,
    berat_kg DECIMAL(6, 2) NOT NULL,
    ongkos_kirim DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_paket_pengirim FOREIGN KEY (id_pengirim) 
        REFERENCES pengirim(id_pengirim) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_paket_penerima FOREIGN KEY (id_penerima) 
        REFERENCES penerima(id_penerima) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_paket_kurir FOREIGN KEY (id_kurir) 
        REFERENCES kurir(id_kurir) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 5. Tabel Pelacakan Status (Riwayat Tracking Posisi Paket)
CREATE TABLE pelacakan_status (
    id_status INT AUTO_INCREMENT PRIMARY KEY,
    id_paket INT NOT NULL,
    waktu_update DATETIME NOT NULL,
    lokasi_posisi VARCHAR(100) NOT NULL,
    status_paket VARCHAR(50) NOT NULL,
    keterangan VARCHAR(255),
    CONSTRAINT fk_status_paket FOREIGN KEY (id_paket) 
        REFERENCES paket(id_paket) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ============================================================================
-- DATABASE 3: F5512530117_kursus (Sistem Bimbingan Belajar & Akademi Pelatihan)
-- ============================================================================
DROP DATABASE IF EXISTS F5512530117_kursus;
CREATE DATABASE F5512530117_kursus;
USE F5512530117_kursus;

-- 1. Tabel Materi Kursus (Master Silabus Kursus)
CREATE TABLE materi_kursus (
    id_kursus INT AUTO_INCREMENT PRIMARY KEY,
    nama_kursus VARCHAR(100) NOT NULL,
    tingkat ENUM('Pemula', 'Menengah', 'Mahir') NOT NULL,
    durasi_pertemuan INT NOT NULL,
    harga_kursus DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB;

-- 2. Tabel Instruktur (Master Pengajar / Mentor)
CREATE TABLE instruktur (
    id_instruktur INT AUTO_INCREMENT PRIMARY KEY,
    nama_instruktur VARCHAR(100) NOT NULL,
    bidang_ahli VARCHAR(50) NOT NULL,
    email_instruktur VARCHAR(100) NOT NULL,
    honor_per_sesi DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB;

-- 3. Tabel Siswa (Master Peserta Pelatihan)
CREATE TABLE siswa (
    id_siswa INT AUTO_INCREMENT PRIMARY KEY,
    nama_siswa VARCHAR(100) NOT NULL,
    email_siswa VARCHAR(100) UNIQUE NOT NULL,
    no_wa VARCHAR(15) NOT NULL,
    kota_asal VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- 4. Tabel Jadwal Kelas (Relasi Antara Materi dan Instruktur)
CREATE TABLE jadwal_kelas (
    id_jadwal INT AUTO_INCREMENT PRIMARY KEY,
    id_kursus INT NOT NULL,
    id_instruktur INT NOT NULL,
    hari VARCHAR(20) NOT NULL,
    jam_mulai TIME NOT NULL,
    ruangan_online VARCHAR(100) NOT NULL,
    CONSTRAINT fk_jadwal_kursus FOREIGN KEY (id_kursus) 
        REFERENCES materi_kursus(id_kursus) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_jadwal_instruktur FOREIGN KEY (id_instruktur) 
        REFERENCES instruktur(id_instruktur) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- 5. Tabel Pendaftaran (Transaksi Siswa Mendaftar Kelas)
CREATE TABLE pendaftaran (
    id_daftar INT AUTO_INCREMENT PRIMARY KEY,
    id_siswa INT NOT NULL,
    id_jadwal INT NOT NULL,
    tgl_daftar DATE NOT NULL,
    metode_bayar VARCHAR(30) NOT NULL,
    status_bayar ENUM('Lunas', 'Cicilan', 'Belum Bayar') NOT NULL,
    CONSTRAINT fk_daftar_siswa FOREIGN KEY (id_siswa) 
        REFERENCES siswa(id_siswa) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_daftar_jadwal FOREIGN KEY (id_jadwal) 
        REFERENCES jadwal_kelas(id_jadwal) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ----------------------------------------------------------------------------
-- BUTIR 3: MEMBUAT 4 USER DENGAN HAK AKSES BERBEDA
-- 1 Sebagai Administrator (Superuser/Full Privileges)
-- 3 Sebagai Admin Pengelola pada masing-masing database
-- ----------------------------------------------------------------------------

-- Hapus user lama jika sebelumnya sudah pernah dibuat
DROP USER IF EXISTS 'user_admin'@'localhost';
DROP USER IF EXISTS 'admin_bioskop'@'localhost';
DROP USER IF EXISTS 'admin_ekspedisi'@'localhost';
DROP USER IF EXISTS 'admin_kursus'@'localhost';

-- 1. User Administrator (Hak Akses Penuh ke Seluruh Database di Server)
CREATE USER 'user_admin'@'localhost' IDENTIFIED BY 'AdminPass123!';
GRANT ALL PRIVILEGES ON *.* TO 'user_admin'@'localhost' WITH GRANT OPTION;

-- 2. User Admin Pengelola Database 1 (F5512530117_bioskop)
CREATE USER 'admin_bioskop'@'localhost' IDENTIFIED BY 'BioskopPass123!';
GRANT ALL PRIVILEGES ON F5512530117_bioskop.* TO 'admin_bioskop'@'localhost';

-- 3. User Admin Pengelola Database 2 (F5512530117_ekspedisi)
CREATE USER 'admin_ekspedisi'@'localhost' IDENTIFIED BY 'EkspedisiPass123!';
GRANT ALL PRIVILEGES ON F5512530117_ekspedisi.* TO 'admin_ekspedisi'@'localhost';

-- 4. User Admin Pengelola Database 3 (F5512530117_kursus)
CREATE USER 'admin_kursus'@'localhost' IDENTIFIED BY 'KursusPass123!';
GRANT ALL PRIVILEGES ON F5512530117_kursus.* TO 'admin_kursus'@'localhost';

-- Terapkan perubahan hak akses ke sistem grant tables MySQL
FLUSH PRIVILEGES;

-- Menampilkan hak akses (Grants) masing-masing user untuk bukti screenshot console
SHOW GRANTS FOR 'user_admin'@'localhost';
SHOW GRANTS FOR 'admin_bioskop'@'localhost';
SHOW GRANTS FOR 'admin_ekspedisi'@'localhost';
SHOW GRANTS FOR 'admin_kursus'@'localhost';


-- ----------------------------------------------------------------------------
-- BUTIR 4: SIMULASI PENCABUTAN IZIN AKSES 1 USER MENJADI READ ONLY
-- User yang disimulasikan: admin_kursus
-- ----------------------------------------------------------------------------

-- Langkah 1: Cabut seluruh hak pengelolaan (ALL PRIVILEGES)
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'admin_kursus'@'localhost';

-- Langkah 2: Berikan HANYA izin membaca data (SELECT = Read Only)
GRANT SELECT ON F5512530117_kursus.* TO 'admin_kursus'@'localhost';
FLUSH PRIVILEGES;

-- Langkah 3: Periksa kembali hak akses user setelah diubah menjadi Read Only
SHOW GRANTS FOR 'admin_kursus'@'localhost';

-- Simulasi Verifikasi:
-- Jika 'admin_kursus' menjalankan: SELECT * FROM F5512530117_kursus.siswa; -> DISETUJUI (Success).
-- Jika 'admin_kursus' menjalankan: INSERT INTO F5512530117_kursus.siswa VALUES (...); -> DITOLAK (Error 1142: INSERT command denied).


-- ----------------------------------------------------------------------------
-- BUTIR 5: PENAMBAHAN 1 KOLOM DAN DILETAKKAN SETELAH KOLOM KE-2
-- Contoh diterapkan pada tabel: penonton (di Database F5512530117_bioskop)
-- Kolom ke-1: id_penonton, Kolom ke-2: nama_penonton
-- Kolom baru yang ditambahkan: nik VARCHAR(16) diletakkan AFTER nama_penonton
-- ----------------------------------------------------------------------------

USE F5512530117_bioskop;

-- 1. Lihat struktur tabel awal sebelum penambahan kolom
DESCRIBE penonton;

-- 2. Jalankan perintah ALTER TABLE untuk menambah kolom setelah kolom ke-2
ALTER TABLE penonton 
ADD COLUMN nik VARCHAR(16) NOT NULL AFTER nama_penonton;

-- 3. Tampilkan struktur tabel sesudah perubahan untuk membuktikan posisi kolom ke-3 (setelah kolom ke-2)
DESCRIBE penonton;
