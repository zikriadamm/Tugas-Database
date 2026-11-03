-- ============================================================================
-- PRAKTIKUM SISTEM BASIS DATA - TUGAS 2 (DML: INSERT, UPDATE, SELECT, DELETE)
-- Nama Mahasiswa : Muhammad Zikri Adam
-- NIM / Stambuk  : F5512530117 (Digit terakhir 7: GANJIL)
-- Program Studi  : S1 Teknik Informatika - Universitas Tadulako
-- DBMS           : MySQL Server 8.0 (Console Command Line)
-- ============================================================================

USE F5512530117_bioskop;

-- ----------------------------------------------------------------------------
-- BUTIR 1: PERINTAH MENAMBAH 10 (SEPULUH) BARIS PADA MASING-MASING TABEL
-- ----------------------------------------------------------------------------

-- A. Menambah 10 Baris Data pada Tabel FILM
INSERT INTO film (judul_film, genre, durasi_menit, rating_usia, harga_dasar) VALUES
('Avengers: Secret Wars', 'Action / Sci-Fi', 165, '13+', 50000.00),
('Interstellar: Odyssey', 'Sci-Fi / Drama', 169, '13+', 45000.00),
('The Conjuring: Last Rites', 'Horror / Mystery', 112, '17+', 40000.00),
('Spider-Man: Beyond Verse', 'Animation / Action', 140, 'SU', 45000.00),
('Oppenheimer: Re-Release', 'Biography / Drama', 180, '17+', 55000.00),
('Fast & Furious: Final Lap', 'Action / Crime', 135, '13+', 45000.00),
('Detective Conan: Dark Shadow', 'Animation / Mystery', 110, 'SU', 40000.00),
('The Batman: Part II', 'Action / Thriller', 155, '17+', 50000.00),
('Dune: Part Three', 'Sci-Fi / Adventure', 160, '13+', 55000.00),
('John Wick: Chapter 5', 'Action / Thriller', 145, '21+', 50000.00);

-- B. Menambah 10 Baris Data pada Tabel STUDIO
INSERT INTO studio (nama_studio, tipe_layar, kapasitas_kursi, biaya_tambahan) VALUES
('Studio 1 Regular', 'Standard 2D', 150, 0.00),
('Studio 2 Regular', 'Standard 2D', 150, 0.00),
('Studio 3 Atmos', 'Dolby Atmos 2D', 120, 10000.00),
('Studio 4 Atmos', 'Dolby Atmos 2D', 120, 10000.00),
('Studio IMAX Laser', 'IMAX 3D Laser', 200, 25000.00),
('Studio IMAX GT', 'IMAX 70mm Dual', 250, 30000.00),
('The Premiere 1', 'VIP Recliner Suite', 40, 50000.00),
('The Premiere 2', 'VIP Recliner Suite', 40, 50000.00),
('Studio 4DX Dynamic', '4DX Motion & Wind', 80, 35000.00),
('ScreenX Panoramic', '270 Degree ScreenX', 100, 20000.00);

-- C. Menambah 10 Baris Data pada Tabel PENONTON
-- Catatan: Tabel penonton telah memiliki kolom 'nik' (disisipkan setelah nama_penonton)
INSERT INTO penonton (nama_penonton, nik, email, no_hp, kota_domisili, tgl_lahir) VALUES
('Ahmad Fauzan', '7271011203950001', 'ahmad.fauzan@gmail.com', '081234567801', 'Palu Timur', '1995-03-12'),
('Siti Nurhaliza', '7271024508980002', 'siti.nurhaliza@gmail.com', '081234567802', 'Palu Timur', '1998-08-25'),
('Budi Santoso', '7271031705880003', 'budi.santoso@yahoo.com', '081234567803', 'Palu Selatan', '1988-05-17'),
('Rina Marlina', '7271046201010004', 'rina.marlina@gmail.com', '081234567804', 'Palu Barat', '2001-01-22'),
('Dedi Setiawan', '7271010911920005', 'dedi.setiawan@gmail.com', '081234567805', 'Palu Utara', '1992-11-09'),
('Eka Wahyuni', '7271025804960006', 'eka.wahyuni@yahoo.com', '081234567806', 'Palu Timur', '1996-04-18'),
('Hendra Gunawan', '7271032307840007', 'hendra.gunawan@gmail.com', '081234567807', 'Palu Barat', '1984-07-23'),
('Nurul Hidayah', '7271044410990008', 'nurul.hidayah@gmail.com', '081234567808', 'Palu Selatan', '1999-10-14'),
('Fajar Pratama', '7271011512900009', 'fajar.pratama@yahoo.com', '081234567809', 'Mantikulore', '1990-12-15'),
('Dewi Lestari', '7271026002000010', 'dewi.lestari@gmail.com', '081234567810', 'Palu Utara', '2000-02-20');

-- D. Menambah 10 Baris Data pada Tabel JADWAL_TAYANG
INSERT INTO jadwal_tayang (id_film, id_studio, tgl_tayang, jam_mulai, harga_tiket) VALUES
(1, 5, '2026-03-20', '13:00:00', 75000.00),
(2, 3, '2026-03-20', '13:30:00', 55000.00),
(3, 1, '2026-03-20', '14:00:00', 40000.00),
(4, 2, '2026-03-20', '15:00:00', 45000.00),
(5, 6, '2026-03-20', '16:00:00', 85000.00),
(6, 4, '2026-03-21', '13:15:00', 55000.00),
(7, 1, '2026-03-21', '14:30:00', 40000.00),
(8, 7, '2026-03-21', '16:30:00', 100000.00),
(9, 5, '2026-03-21', '19:00:00', 80000.00),
(10, 9, '2026-03-21', '21:00:00', 85000.00);

-- E. Menambah 10 Baris Data pada Tabel TRANSAKSI_TIKET
INSERT INTO transaksi_tiket (id_penonton, id_jadwal, waktu_transaksi, nomor_kursi, metode_bayar, total_bayar) VALUES
(1, 1, '2026-03-19 10:15:00', 'F-12', 'QRIS', 75000.00),
(2, 2, '2026-03-19 11:20:00', 'G-08', 'Debit BCA', 55000.00),
(3, 3, '2026-03-19 14:05:00', 'H-10', 'E-Wallet Dana', 40000.00),
(4, 4, '2026-03-19 16:30:00', 'E-05', 'Cash', 45000.00),
(5, 5, '2026-03-19 18:45:00', 'C-14', 'QRIS', 85000.00),
(6, 6, '2026-03-20 09:10:00', 'D-07', 'Transfer Bank', 55000.00),
(7, 7, '2026-03-20 10:40:00', 'F-09', 'QRIS', 40000.00),
(8, 8, '2026-03-20 12:00:00', 'A-02', 'Kartu Kredit', 100000.00),
(9, 9, '2026-03-20 15:25:00', 'B-11', 'E-Wallet GoPay', 80000.00),
(10, 10, '2026-03-20 17:50:00', 'G-04', 'Cash', 85000.00);

-- Verifikasi hasil penambahan seluruh data
SELECT * FROM film;
SELECT * FROM studio;
SELECT * FROM penonton;
SELECT * FROM jadwal_tayang;
SELECT * FROM transaksi_tiket;


-- ----------------------------------------------------------------------------
-- BUTIR 2: OPERASI PERUBAHAN (UPDATE) PADA BARIS GANJIL / GENAP
-- Aturan Soal:
-- - Stambuk Genap  : Update baris 2, 4, 6, 8, dan 10
-- - Stambuk Ganjil : Update baris 1, 3, 5, 7, dan 9
--
-- Karena Stambuk Mahasiswa adalah F5512530117 (Digit terakhir 7 = GANJIL),
-- maka operasi UPDATE dilakukan pada BARIS GANJIL (Baris 1, 3, 5, 7, dan 9).
-- ----------------------------------------------------------------------------

-- A. Perubahan pada Tabel PENONTON (Baris Ganjil: 1, 3, 5, 7, 9)
-- Buktikan data sebelum perubahan
SELECT id_penonton, nama_penonton, kota_domisili FROM penonton WHERE id_penonton IN (1, 3, 5, 7, 9);

-- Jalankan perintah UPDATE untuk baris ganjil
UPDATE penonton 
SET kota_domisili = CONCAT(kota_domisili, ' [MEMBER VIP]') 
WHERE id_penonton IN (1, 3, 5, 7, 9);

-- Tampilkan data setelah perubahan (Buktikan hanya baris 1, 3, 5, 7, 9 yang berubah)
SELECT id_penonton, nama_penonton, kota_domisili FROM penonton;

-- B. Perubahan pada Tabel FILM (Baris Ganjil: 1, 3, 5, 7, 9)
-- Penyesuaian harga dasar film naik Rp 5.000 untuk baris ganjil
UPDATE film 
SET harga_dasar = harga_dasar + 5000.00 
WHERE id_film IN (1, 3, 5, 7, 9);

-- C. Perubahan pada Tabel STUDIO (Baris Ganjil: 1, 3, 5, 7, 9)
-- Pembaruan nama studio dengan label 'Upgraded Sound'
UPDATE studio 
SET nama_studio = CONCAT(nama_studio, ' (Dolby Enhanced)') 
WHERE id_studio IN (1, 3, 5, 7, 9);

-- D. Perubahan pada Tabel JADWAL_TAYANG (Baris Ganjil: 1, 3, 5, 7, 9)
UPDATE jadwal_tayang 
SET harga_tiket = harga_tiket + 5000.00 
WHERE id_jadwal IN (1, 3, 5, 7, 9);

-- E. Perubahan pada Tabel TRANSAKSI_TIKET (Baris Ganjil: 1, 3, 5, 7, 9)
UPDATE transaksi_tiket 
SET metode_bayar = CONCAT(metode_bayar, ' - Promo Cashback') 
WHERE id_transaksi IN (1, 3, 5, 7, 9);


-- ----------------------------------------------------------------------------
-- BUTIR 3: PERINTAH SELECT DENGAN 3 (TIGA) JENIS KRITERIA
-- ----------------------------------------------------------------------------

-- Kriteria 1: Filter Relasional & Gerbang Logika (AND / OR)
-- Menampilkan film dengan durasi tayang di atas 140 menit dan rating usia 13+
SELECT id_film, judul_film, genre, durasi_menit, rating_usia, harga_dasar 
FROM film 
WHERE durasi_menit >= 140 AND rating_usia = '13+' 
ORDER BY durasi_menit DESC;

-- Kriteria 2: Filter Rentang Nilai (BETWEEN) & Pola Karakter (LIKE)
-- Menampilkan jadwal tayang dengan harga tiket antara Rp 50.000 hingga Rp 85.000
SELECT id_jadwal, id_film, id_studio, tgl_tayang, jam_mulai, harga_tiket 
FROM jadwal_tayang 
WHERE harga_tiket BETWEEN 50000.00 AND 85000.00;

-- Serta filter pencarian penonton dengan domisili di wilayah 'Palu Timur'
SELECT id_penonton, nama_penonton, nik, email, kota_domisili 
FROM penonton 
WHERE kota_domisili LIKE '%Palu Timur%';

-- Kriteria 3: Filter Keanggotaan Nilai Himpunan (IN / NOT IN)
-- Menampilkan jadwal film yang ditayangkan di Studio khusus IMAX dan Premiere (ID 5, 6, 7, 8)
SELECT id_jadwal, id_film, id_studio, tgl_tayang, harga_tiket 
FROM jadwal_tayang 
WHERE id_studio IN (5, 6, 7, 8);


-- ----------------------------------------------------------------------------
-- BUTIR 4: PERINTAH SELECT MENAMPILKAN DATA DARI BARIS KE-3 HINGGA BARIS KE-7
-- Teori:
-- MySQL menggunakan 0-based offset pada klausa LIMIT.
-- Baris ke-1 = offset 0
-- Baris ke-2 = offset 1
-- Baris ke-3 = offset 2
-- Dari baris ke-3 sampai baris ke-7 ada total 5 baris (3, 4, 5, 6, 7).
-- Sintaks: LIMIT 5 OFFSET 2 (atau sintaks alternatif: LIMIT 2, 5)
-- ----------------------------------------------------------------------------

-- Implementasi pada tabel PENONTON:
SELECT id_penonton, nama_penonton, nik, email, no_hp, kota_domisili 
FROM penonton 
ORDER BY id_penonton ASC 
LIMIT 5 OFFSET 2;

-- Implementasi alternatif pada tabel FILM:
SELECT id_film, judul_film, genre, durasi_menit, rating_usia, harga_dasar 
FROM film 
ORDER BY id_film ASC 
LIMIT 2, 5;


-- ----------------------------------------------------------------------------
-- BUTIR 5: PERINTAH MENGHAPUS DATA KE-9 PADA MASING-MASING TABEL
-- Catatan Integritas Referensial (Foreign Key):
-- Untuk menghindari pelanggaran Foreign Key Constraint (RESTRICT), urutan
-- penghapusan data ke-9 dilakukan dari tabel anak (child table) ke tabel induk (parent table).
-- ----------------------------------------------------------------------------

-- A. Hapus data ke-9 pada tabel TRANSAKSI_TIKET (Tabel Anak)
SELECT * FROM transaksi_tiket WHERE id_transaksi = 9;
DELETE FROM transaksi_tiket WHERE id_transaksi = 9;
SELECT * FROM transaksi_tiket WHERE id_transaksi = 9; -- Verifikasi: Hasil kosong (Empty set)

-- B. Hapus data ke-9 pada tabel JADWAL_TAYANG
SELECT * FROM jadwal_tayang WHERE id_jadwal = 9;
DELETE FROM jadwal_tayang WHERE id_jadwal = 9;
SELECT * FROM jadwal_tayang WHERE id_jadwal = 9;

-- C. Hapus data ke-9 pada tabel PENONTON
SELECT * FROM penonton WHERE id_penonton = 9;
DELETE FROM penonton WHERE id_penonton = 9;
SELECT * FROM penonton WHERE id_penonton = 9;

-- D. Hapus data ke-9 pada tabel FILM
SELECT * FROM film WHERE id_film = 9;
DELETE FROM film WHERE id_film = 9;
SELECT * FROM film WHERE id_film = 9;

-- E. Hapus data ke-9 pada tabel STUDIO
SELECT * FROM studio WHERE id_studio = 9;
DELETE FROM studio WHERE id_studio = 9;
SELECT * FROM studio WHERE id_studio = 9;
