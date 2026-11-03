-- ============================================================================
-- PRAKTIKUM SISTEM BASIS DATA - TUGAS 3 (RELASIONAL, JOIN, & FUNGSI AGREGAT)
-- Nama Mahasiswa : Muhammad Zikri Adam
-- NIM / Stambuk  : F5512530117
-- Program Studi  : S1 Teknik Informatika - Universitas Tadulako
-- DBMS           : MySQL Server 8.0 (Console Command Line)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- BUTIR 1: MEMBUAT 1 DATABASE DENGAN MINIMAL 3 TABEL RELASIONAL
-- Database: F5512530117_cinema
-- 3 Tabel Relasional: penonton (Master), film (Master), transaksi_tiket (Transaksi)
-- ----------------------------------------------------------------------------

DROP DATABASE IF EXISTS F5512530117_cinema;
CREATE DATABASE F5512530117_cinema;
USE F5512530117_cinema;

-- 1. Tabel PENONTON (Tabel Master 1)
CREATE TABLE penonton (
    id_penonton INT AUTO_INCREMENT PRIMARY KEY,
    nama_penonton VARCHAR(100) NOT NULL,
    nik VARCHAR(16) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    no_hp VARCHAR(15) NOT NULL,
    kota_domisili VARCHAR(50) NOT NULL,
    tgl_lahir DATE NOT NULL
) ENGINE=InnoDB;

-- 2. Tabel FILM (Tabel Master 2)
CREATE TABLE film (
    id_film INT AUTO_INCREMENT PRIMARY KEY,
    judul_film VARCHAR(150) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    durasi_menit INT NOT NULL,
    rating_usia ENUM('SU', '13+', '17+', '21+') NOT NULL,
    harga_dasar DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB;

-- 3. Tabel TRANSAKSI_TIKET (Tabel Transaksi Relasional Menghubungkan Penonton & Film)
CREATE TABLE transaksi_tiket (
    id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
    id_penonton INT NOT NULL,
    id_film INT NOT NULL,
    waktu_transaksi DATETIME NOT NULL,
    nomor_kursi VARCHAR(10) NOT NULL,
    metode_bayar VARCHAR(30) NOT NULL,
    total_bayar DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_relasi_penonton FOREIGN KEY (id_penonton) 
        REFERENCES penonton(id_penonton) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_relasi_film FOREIGN KEY (id_film) 
        REFERENCES film(id_film) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Pengisian Data Sampel (Dataset Edukatif untuk Mendemonstrasikan INNER, LEFT, dan RIGHT JOIN)
-- Penonton ID 1 - 5: Penonton yang telah membeli tiket film
-- Penonton ID 6: Penonton Baru (BELUM PERNAH beli tiket) -> Untuk menguji LEFT JOIN
INSERT INTO penonton (nama_penonton, nik, email, no_hp, kota_domisili, tgl_lahir) VALUES
('Ahmad Fauzan', '7271011203950001', 'ahmad.fauzan@gmail.com', '081234567801', 'Palu Timur', '1995-03-12'),
('Siti Nurhaliza', '7271024508980002', 'siti.nurhaliza@gmail.com', '081234567802', 'Palu Timur', '1998-08-25'),
('Budi Santoso', '7271031705880003', 'budi.santoso@yahoo.com', '081234567803', 'Palu Selatan', '1988-05-17'),
('Rina Marlina', '7271046201010004', 'rina.marlina@gmail.com', '081234567804', 'Palu Barat', '2001-01-22'),
('Dedi Setiawan', '7271010911920005', 'dedi.setiawan@gmail.com', '081234567805', 'Palu Utara', '1992-11-09'),
('Gilang Ramadhan', '7271051104020006', 'gilang.ramadhan@gmail.com', '081234567806', 'Palu Selatan', '2002-04-11');

-- Film ID 1 - 4: Film aktif yang ditonton
-- Film ID 5: Film Baru Segera Tayang (BELUM ADA penjualan tiket) -> Untuk menguji RIGHT JOIN
INSERT INTO film (judul_film, genre, durasi_menit, rating_usia, harga_dasar) VALUES
('Avengers: Secret Wars', 'Action / Sci-Fi', 165, '13+', 50000.00),
('Interstellar: Odyssey', 'Sci-Fi / Drama', 169, '13+', 45000.00),
('The Conjuring: Last Rites', 'Horror / Mystery', 112, '17+', 40000.00),
('Spider-Man: Beyond Verse', 'Animation / Action', 140, 'SU', 45000.00),
('Avatar: The Seed Bearer', 'Sci-Fi / Adventure', 190, '13+', 60000.00);

-- Data Transaksi Tiket (Menghubungkan Penonton 1-5 dengan Film 1-4)
INSERT INTO transaksi_tiket (id_penonton, id_film, waktu_transaksi, nomor_kursi, metode_bayar, total_bayar) VALUES
(1, 1, '2026-03-20 13:00:00', 'F-12', 'QRIS', 50000.00),
(2, 2, '2026-03-20 14:15:00', 'G-08', 'Debit BCA', 45000.00),
(3, 3, '2026-03-20 15:30:00', 'H-10', 'E-Wallet Dana', 40000.00),
(4, 4, '2026-03-20 16:45:00', 'E-05', 'Cash', 45000.00),
(5, 1, '2026-03-20 19:00:00', 'F-14', 'QRIS', 50000.00);


-- ----------------------------------------------------------------------------
-- BUTIR 2: IMPLEMENTASI 3 PERINTAH JOIN (INNER JOIN, LEFT JOIN, RIGHT JOIN)
-- ----------------------------------------------------------------------------

-- A. IMPLEMENTASI INNER JOIN
-- Konsep: Hanya menampilkan baris yang memiliki kecocokan (match) di kedua belah tabel.
-- Penonton yang belum beli tiket dan film yang belum ada penjualan TIDAK AKAN ditampilkan.
SELECT 
    t.id_transaksi,
    p.nama_penonton,
    f.judul_film,
    f.genre,
    t.nomor_kursi,
    t.metode_bayar,
    t.total_bayar
FROM transaksi_tiket t
INNER JOIN penonton p ON t.id_penonton = p.id_penonton
INNER JOIN film f ON t.id_film = f.id_film
ORDER BY t.id_transaksi ASC;


-- B. IMPLEMENTASI LEFT JOIN
-- Konsep: Menampilkan SEMUA baris dari tabel sebelah kiri (penonton), meskipun tidak
-- memiliki pasangan data di tabel transaksi tiket.
-- Perhatikan: Penonton 'Gilang Ramadhan' (id 6) akan tetap tampil, namun kolom
-- judul_film, nomor_kursi, dan total_bayar bernilai NULL. Ini membuktikan fungsi LEFT JOIN!
SELECT 
    p.id_penonton,
    p.nama_penonton,
    p.kota_domisili,
    t.nomor_kursi,
    f.judul_film,
    t.total_bayar
FROM penonton p
LEFT JOIN transaksi_tiket t ON p.id_penonton = t.id_penonton
LEFT JOIN film f ON t.id_film = f.id_film
ORDER BY p.id_penonton ASC;


-- C. IMPLEMENTASI RIGHT JOIN
-- Konsep: Menampilkan SEMUA baris dari tabel sebelah kanan (film), meskipun belum
-- memiliki transaksi penjualan tiket.
-- Perhatikan: Film 'Avatar: The Seed Bearer' (id 5) yang belum pernah terjual tiketnya
-- akan tetap tampil, dengan kolom id_transaksi, nama_penonton, dan nomor_kursi bernilai NULL!
SELECT 
    f.id_film,
    f.judul_film,
    f.genre,
    f.harga_dasar,
    t.id_transaksi,
    p.nama_penonton,
    t.nomor_kursi
FROM transaksi_tiket t
RIGHT JOIN film f ON t.id_film = f.id_film
LEFT JOIN penonton p ON t.id_penonton = p.id_penonton
ORDER BY f.id_film ASC;


-- ----------------------------------------------------------------------------
-- BUTIR 3: CARI NILAI MAX, MIN, DAN HITUNG JUMLAH BARIS (COUNT)
-- PADA MASING-MASING TABEL
-- ----------------------------------------------------------------------------

-- A. Fungsi Agregat pada Tabel PENONTON
-- Menghitung jumlah total penonton, tanggal lahir termuda (MAX), dan tertua (MIN)
SELECT 
    COUNT(*) AS total_penonton_terdaftar,
    MAX(tgl_lahir) AS tgl_lahir_termuda,
    MIN(tgl_lahir) AS tgl_lahir_tertua
FROM penonton;

-- B. Fungsi Agregat pada Tabel FILM
-- Menghitung total film, harga tiket dasar tertinggi (MAX), dan terendah (MIN)
SELECT 
    COUNT(*) AS total_film,
    MAX(harga_dasar) AS harga_film_termahal,
    MIN(harga_dasar) AS harga_film_termurah
FROM film;

-- C. Fungsi Agregat pada Tabel TRANSAKSI_TIKET
-- Menghitung total transaksi tiket terjual, pembayaran tertinggi (MAX), dan terendah (MIN)
SELECT 
    COUNT(*) AS total_tiket_terjual,
    MAX(total_bayar) AS transaksi_tertinggi,
    MIN(total_bayar) AS transaksi_terendah
FROM transaksi_tiket;
