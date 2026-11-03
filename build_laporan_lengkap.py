import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import win32com.client

def generate_report():
    doc = docx.Document()

    # 1. Page Setup: A4, Margin 4-4-3-3 cm (Academic Standard)
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(4.0)
    sec.left_margin = Cm(4.0)
    sec.bottom_margin = Cm(3.0)
    sec.right_margin = Cm(3.0)

    # 2. Styling Helpers
    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = tcPr.find(qn('w:shd'))
        if shd is None:
            shd = OxmlElement('w:shd')
            tcPr.append(shd)
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), fill_hex)

    def set_cell_borders(cell, top="CCCCCC", bottom="CCCCCC", left="CCCCCC", right="CCCCCC", sz="4"):
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = tcPr.find(qn('w:tcBorders'))
        if tcBorders is None:
            tcBorders = OxmlElement('w:tcBorders')
            tcPr.append(tcBorders)
        for side, color in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            if color:
                border = OxmlElement(f'w:{side}')
                border.set(qn('w:val'), 'single')
                border.set(qn('w:sz'), sz)
                border.set(qn('w:space'), '0')
                border.set(qn('w:color'), color)
                tcBorders.append(border)

    def format_p(p, space_before=0, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_indent=Cm(1.27)):
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        p.alignment = align
        if first_indent is not None:
            p.paragraph_format.first_line_indent = first_indent

    def add_h1(text):
        p = doc.add_paragraph()
        format_p(p, space_before=16, space_after=8, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT, first_indent=None)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(30, 58, 138) # Navy Blue
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        format_p(p, space_before=12, space_after=6, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT, first_indent=None)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12.5)
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        format_p(p, space_before=8, space_after=4, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT, first_indent=None)
        run = p.add_run(text)
        run.bold = True
        run.italic = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_para(text, bold_prefix=None, first_indent=Cm(1.27)):
        p = doc.add_paragraph()
        format_p(p, space_before=0, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_indent=first_indent)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(12)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        return p

    def add_code_block(sql_code, caption=None):
        if caption:
            cp = doc.add_paragraph()
            format_p(cp, space_before=6, space_after=2, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT, first_indent=None)
            rc = cp.add_run(f"Perintah Console SQL ({caption}):")
            rc.bold = True
            rc.font.name = 'Times New Roman'
            rc.font.size = Pt(10.5)
            rc.font.color.rgb = RGBColor(30, 58, 138)

        tbl = doc.add_table(rows=1, cols=1)
        tbl.style = 'Table Grid'
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        set_cell_background(cell, "0F172A") # Dark slate
        set_cell_borders(cell, top="1E293B", bottom="1E293B", left="3B82F6", right="1E293B", sz="12")
        
        p = cell.paragraphs[0]
        format_p(p, space_before=4, space_after=4, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT, first_indent=None)
        r = p.add_run(sql_code)
        r.font.name = 'Consolas'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(241, 245, 249)

        sp = doc.add_paragraph()
        format_p(sp, space_before=0, space_after=4, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.LEFT, first_indent=None)

    def add_screenshot_box(step_title, command_summary):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.style = 'Table Grid'
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        set_cell_background(cell, "F8FAFC")
        set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="2563EB", right="CBD5E1", sz="10")

        p = cell.paragraphs[0]
        format_p(p, space_before=4, space_after=3, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT, first_indent=None)
        r_tag = p.add_run(f"[TANGKAP LAYAR CONSOLE]: {step_title}\n")
        r_tag.bold = True
        r_tag.font.name = 'Times New Roman'
        r_tag.font.size = Pt(11)
        r_tag.font.color.rgb = RGBColor(37, 99, 235)

        r_desc = p.add_run(f"Instruksi: Jalankan perintah berikut di console MySQL dan lampirkan hasil screenshot tepat di bawah ini:\n")
        r_desc.italic = True
        r_desc.font.name = 'Times New Roman'
        r_desc.font.size = Pt(10)
        r_desc.font.color.rgb = RGBColor(71, 85, 105)

        r_cmd = p.add_run(f"> {command_summary}\n\n")
        r_cmd.bold = True
        r_cmd.font.name = 'Consolas'
        r_cmd.font.size = Pt(9.5)
        r_cmd.font.color.rgb = RGBColor(15, 23, 42)

        r_box = p.add_run("[ --- TEMPELKAN TANGKAP LAYAR / SCREENSHOT CONSOLE DISINI --- ]")
        r_box.bold = True
        r_box.italic = True
        r_box.font.name = 'Times New Roman'
        r_box.font.size = Pt(10)
        r_box.font.color.rgb = RGBColor(148, 163, 184)

        sp = doc.add_paragraph()
        format_p(sp, space_before=0, space_after=6, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.LEFT, first_indent=None)

    def add_custom_table(headers, data_rows, col_widths, font_size=9):
        tbl = doc.add_table(rows=len(data_rows) + 1, cols=len(headers))
        tbl.style = 'Table Grid'
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Header Row
        hdr_row = tbl.rows[0]
        trPr = hdr_row._tr.get_or_add_trPr()
        trPr.append(OxmlElement('w:tblHeader'))
        
        for idx, text in enumerate(headers):
            cell = hdr_row.cells[idx]
            cell.text = text
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_background(cell, "1E3A8A")
            p = cell.paragraphs[0]
            format_p(p, space_before=3, space_after=3, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=None)
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(font_size)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)

        # Data Rows
        for r_idx, row_vals in enumerate(data_rows):
            row = tbl.rows[r_idx + 1]
            bg_hex = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_vals):
                cell = row.cells[c_idx]
                cell.text = str(val)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                set_cell_background(cell, bg_hex)
                p = cell.paragraphs[0]
                s_val = str(val).strip()
                align = WD_ALIGN_PARAGRAPH.CENTER if (len(s_val) <= 15 or s_val.isdigit()) else WD_ALIGN_PARAGRAPH.LEFT
                format_p(p, space_before=2, space_after=2, line_spacing=1.05, align=align, first_indent=None)
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(font_size)
                    r.font.color.rgb = RGBColor(30, 41, 59)

        # Set widths
        for row in tbl.rows:
            for idx, w in enumerate(col_widths):
                row.cells[idx].width = Cm(w)

        sp = doc.add_paragraph()
        format_p(sp, space_before=0, space_after=6, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.LEFT, first_indent=None)

    # =========================================================================
    # HALAMAN SAMPUL (COVER PAGE)
    # =========================================================================
    p_cov_top = doc.add_paragraph()
    format_p(p_cov_top, space_before=20, space_after=8, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=None)
    r1 = p_cov_top.add_run("LAPORAN PRAKTIKUM SISTEM BASIS DATA\n")
    r1.bold = True
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(16)
    r1.font.color.rgb = RGBColor(30, 58, 138)

    r2 = p_cov_top.add_run("IMPLEMENTASI DDL, DCL, DML, RELASIONAL, JOIN, DAN FUNGSI AGREGAT MENGGUNAKAN PERINTAH CONSOLE MYSQL\n")
    r2.bold = True
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(13)
    r2.font.color.rgb = RGBColor(15, 23, 42)

    # Logo
    if os.path.exists("logo_untad.jpg"):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_p(p_logo, space_before=15, space_after=18, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=None)
        p_logo.add_run().add_picture("logo_untad.jpg", width=Inches(2.2))

    # Identitas Mahasiswa
    p_bio = doc.add_paragraph()
    format_p(p_bio, space_before=10, space_after=24, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=None)
    
    r_bio_title = p_bio.add_run("Disusun Oleh:\n")
    r_bio_title.bold = True
    r_bio_title.font.name = 'Times New Roman'
    r_bio_title.font.size = Pt(12)

    r_nama = p_bio.add_run("MUHAMMAD ZIKRI ADAM\n")
    r_nama.bold = True
    r_nama.font.name = 'Times New Roman'
    r_nama.font.size = Pt(13)
    r_nama.font.color.rgb = RGBColor(30, 58, 138)

    r_nim = p_bio.add_run("NIM: F5512530117\n")
    r_nim.bold = True
    r_nim.font.name = 'Times New Roman'
    r_nim.font.size = Pt(12)

    r_kat = p_bio.add_run("(Kategori Stambuk: GANJIL - Akhiran 7)\n")
    r_kat.italic = True
    r_kat.font.name = 'Times New Roman'
    r_kat.font.size = Pt(11)
    r_kat.font.color.rgb = RGBColor(185, 28, 28)

    # Identitas Institusi
    p_inst = doc.add_paragraph()
    format_p(p_inst, space_before=20, space_after=0, line_spacing=1.2, align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=None)
    r_inst = p_inst.add_run(
        "PROGRAM STUDI S1 TEKNIK INFORMATIKA\n"
        "JURUSAN TEKNOLOGI INFORMASI\n"
        "FAKULTAS TEKNIK - UNIVERSITAS TADULAKO\n"
        "PALU\n"
        "2026"
    )
    r_inst.bold = True
    r_inst.font.name = 'Times New Roman'
    r_inst.font.size = Pt(12)

    doc.add_page_break()

    # =========================================================================
    # BAB I: PENDAHULUAN & KETENTUAN UMUM
    # =========================================================================
    add_h1("BAB I. PENDAHULUAN DAN KETENTUAN PRAKTIKUM")
    
    add_para("Sistem Manajemen Basis Data (Database Management System atau DBMS) merupakan perangkat lunak inti yang mengelola, menyimpan, memanipulasi, dan mengamankan data secara terstruktur. Dalam praktikum ini, DBMS yang digunakan adalah MySQL Server versi 8.0 dengan pengoperasian berbasis antarmuka baris perintah (Command Line Interface / Console). Penggunaan console bertujuan agar mahasiswa memahami secara mendalam setiap sintaksis query SQL (Structured Query Language) secara native tanpa bergantung pada antarmuka grafis (GUI) seperti phpMyAdmin atau MySQL Workbench.")

    add_para("Seluruh penugasan praktikum ini mencakup tiga bagian modul terintegrasi yang diselesaikan sesuai ketentuan resmi sebagai berikut:")
    
    ketentuan_data = [
        ["1", "Metode Eksekusi", "Seluruh query wajib dibuat dan dieksekusi melalui PERINTAH CONSOLE (MySQL Client)."],
        ["2", "DBMS Resmi", "MySQL Server (InnoDB Storage Engine dengan dukungan integritas relasional)."],
        ["3", "Format Penamaan DB", "Wajib mengikuti format: Stambuk_namadatabase (Contoh: F5512530117_bioskop)."],
        ["4", "Keunikan Tabel", "Dilarang keras memiliki jenis tabel yang sama antar basis data untuk menjamin orisinalitas."],
        ["5", "Kriteria Stambuk", "NIM F5512530117 berakhiran 7 (GANJIL), sehingga operasi modifikasi baris data pada Tugas 2 wajib diterapkan pada Baris Ganjil (baris 1, 3, 5, 7, 9)."],
        ["6", "Bukti Pelaksanaan", "Setiap sintaks SQL wajib disertai hasil tangkap layar (screenshot) console secara mandiri."]
    ]
    add_custom_table(["No", "Komponen Ketentuan", "Uraian Persyaratan Praktikum"], ketentuan_data, [1.2, 3.8, 8.0], font_size=9.5)

    doc.add_page_break()

    # =========================================================================
    # BAB II: TUGAS 1 - DDL, DESAIN RELASI, DCL, & ALTER TABLE
    # =========================================================================
    add_h1("BAB II. TUGAS 1: DDL, DESAIN RELASI, DCL, & ALTER TABLE")

    add_h2("2.1 Pembuatan 3 Basis Data dengan Masing-Masing Minimal 5 Tabel Berbeda")
    add_para("Untuk mematuhi aturan bahwa tidak boleh ada jenis tabel yang sama, dirancang tiga ekosistem basis data dengan domain fungsional yang sepenuhnya berbeda, yaitu Sistem Tiket Bioskop & Cinema, Sistem Logistik Ekspedisi Kargo, dan Sistem Akademi Bimbingan Belajar. Masing-masing basis data dirancang secara normal (3NF) dan memiliki keterhubungan foreign key yang solid.")

    add_h3("A. Basis Data 1: F5512530117_bioskop (Sistem Manajemen Tiket Bioskop)")
    add_para("Basis data ini mengelola alur penayangan film, studio bioskop, data penonton, jadwal penayangan, serta transaksi pemesanan tiket. Terdiri atas 5 tabel: film, studio, penonton, jadwal_tayang, dan transaksi_tiket.")

    add_code_block(
        "CREATE DATABASE F5512530117_bioskop;\n"
        "USE F5512530117_bioskop;\n\n"
        "-- 1. Tabel Film\n"
        "CREATE TABLE film (\n"
        "    id_film INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    judul_film VARCHAR(150) NOT NULL,\n"
        "    genre VARCHAR(50) NOT NULL,\n"
        "    durasi_menit INT NOT NULL,\n"
        "    rating_usia ENUM('SU', '13+', '17+', '21+') NOT NULL,\n"
        "    harga_dasar DECIMAL(10, 2) NOT NULL\n"
        ") ENGINE=InnoDB;\n\n"
        "-- 2. Tabel Studio\n"
        "CREATE TABLE studio (\n"
        "    id_studio INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    nama_studio VARCHAR(50) NOT NULL,\n"
        "    tipe_layar VARCHAR(30) NOT NULL,\n"
        "    kapasitas_kursi INT NOT NULL,\n"
        "    biaya_tambahan DECIMAL(10, 2) NOT NULL\n"
        ") ENGINE=InnoDB;\n\n"
        "-- 3. Tabel Penonton\n"
        "CREATE TABLE penonton (\n"
        "    id_penonton INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    nama_penonton VARCHAR(100) NOT NULL,\n"
        "    email VARCHAR(100) UNIQUE NOT NULL,\n"
        "    no_hp VARCHAR(15) NOT NULL,\n"
        "    kota_domisili VARCHAR(50) NOT NULL,\n"
        "    tgl_lahir DATE NOT NULL\n"
        ") ENGINE=InnoDB;\n\n"
        "-- 4. Tabel Jadwal Tayang (Relasi ke Film & Studio)\n"
        "CREATE TABLE jadwal_tayang (\n"
        "    id_jadwal INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    id_film INT NOT NULL,\n"
        "    id_studio INT NOT NULL,\n"
        "    tgl_tayang DATE NOT NULL,\n"
        "    jam_mulai TIME NOT NULL,\n"
        "    harga_tiket DECIMAL(10, 2) NOT NULL,\n"
        "    CONSTRAINT fk_jadwal_film FOREIGN KEY (id_film) REFERENCES film(id_film) ON DELETE RESTRICT ON UPDATE CASCADE,\n"
        "    CONSTRAINT fk_jadwal_studio FOREIGN KEY (id_studio) REFERENCES studio(id_studio) ON DELETE RESTRICT ON UPDATE CASCADE\n"
        ") ENGINE=InnoDB;\n\n"
        "-- 5. Tabel Transaksi Tiket (Relasi ke Penonton & Jadwal Tayang)\n"
        "CREATE TABLE transaksi_tiket (\n"
        "    id_transaksi INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    id_penonton INT NOT NULL,\n"
        "    id_jadwal INT NOT NULL,\n"
        "    waktu_transaksi DATETIME NOT NULL,\n"
        "    nomor_kursi VARCHAR(10) NOT NULL,\n"
        "    metode_bayar VARCHAR(30) NOT NULL,\n"
        "    total_bayar DECIMAL(10, 2) NOT NULL,\n"
        "    CONSTRAINT fk_tiket_penonton FOREIGN KEY (id_penonton) REFERENCES penonton(id_penonton) ON DELETE CASCADE ON UPDATE CASCADE,\n"
        "    CONSTRAINT fk_tiket_jadwal FOREIGN KEY (id_jadwal) REFERENCES jadwal_tayang(id_jadwal) ON DELETE RESTRICT ON UPDATE CASCADE\n"
        ") ENGINE=InnoDB;",
        caption="DDL Basis Data F5512530117_bioskop"
    )

    add_h3("B. Basis Data 2: F5512530117_ekspedisi (Sistem Logistik Kargo)")
    add_para("Basis data ini mengelola operasi pengiriman paket logistik antar wilayah. Terdiri atas 5 tabel yang sepenuhnya berbeda karakteristiknya: pengirim, penerima, kurir, paket, dan pelacakan_status.")

    add_code_block(
        "CREATE DATABASE F5512530117_ekspedisi;\n"
        "USE F5512530117_ekspedisi;\n\n"
        "CREATE TABLE pengirim (id_pengirim INT AUTO_INCREMENT PRIMARY KEY, nama_pengirim VARCHAR(100) NOT NULL, kota_asal VARCHAR(50) NOT NULL, alamat_asal VARCHAR(255) NOT NULL, no_telp_pengirim VARCHAR(15) NOT NULL) ENGINE=InnoDB;\n"
        "CREATE TABLE penerima (id_penerima INT AUTO_INCREMENT PRIMARY KEY, nama_penerima VARCHAR(100) NOT NULL, kota_tujuan VARCHAR(50) NOT NULL, alamat_tujuan VARCHAR(255) NOT NULL, no_telp_penerima VARCHAR(15) NOT NULL) ENGINE=InnoDB;\n"
        "CREATE TABLE kurir (id_kurir INT AUTO_INCREMENT PRIMARY KEY, nama_kurir VARCHAR(100) NOT NULL, no_plat VARCHAR(15) NOT NULL, jenis_kendaraan VARCHAR(30) NOT NULL, wilayah_tugas VARCHAR(50) NOT NULL) ENGINE=InnoDB;\n"
        "CREATE TABLE paket (\n"
        "    id_paket INT AUTO_INCREMENT PRIMARY KEY, no_resi VARCHAR(25) UNIQUE NOT NULL,\n"
        "    id_pengirim INT NOT NULL, id_penerima INT NOT NULL, id_kurir INT NOT NULL,\n"
        "    jenis_layanan VARCHAR(30) NOT NULL, berat_kg DECIMAL(6,2) NOT NULL, ongkos_kirim DECIMAL(10,2) NOT NULL,\n"
        "    CONSTRAINT fk_pkt_pengirim FOREIGN KEY (id_pengirim) REFERENCES pengirim(id_pengirim) ON DELETE RESTRICT ON UPDATE CASCADE,\n"
        "    CONSTRAINT fk_pkt_penerima FOREIGN KEY (id_penerima) REFERENCES penerima(id_penerima) ON DELETE RESTRICT ON UPDATE CASCADE,\n"
        "    CONSTRAINT fk_pkt_kurir FOREIGN KEY (id_kurir) REFERENCES kurir(id_kurir) ON DELETE RESTRICT ON UPDATE CASCADE\n"
        ") ENGINE=InnoDB;\n"
        "CREATE TABLE pelacakan_status (\n"
        "    id_status INT AUTO_INCREMENT PRIMARY KEY, id_paket INT NOT NULL,\n"
        "    waktu_update DATETIME NOT NULL, lokasi_posisi VARCHAR(100) NOT NULL, status_paket VARCHAR(50) NOT NULL, keterangan VARCHAR(255),\n"
        "    CONSTRAINT fk_tr_paket FOREIGN KEY (id_paket) REFERENCES paket(id_paket) ON DELETE CASCADE ON UPDATE CASCADE\n"
        ") ENGINE=InnoDB;",
        caption="DDL Basis Data F5512530117_ekspedisi"
    )

    add_h3("C. Basis Data 3: F5512530117_kursus (Sistem Akademi Kursus)")
    add_para("Basis data ini mengelola proses registrasi dan perkuliahan non-formal bimbingan belajar. Terdiri atas 5 tabel: siswa, instruktur, materi_kursus, jadwal_kelas, dan pendaftaran.")

    add_code_block(
        "CREATE DATABASE F5512530117_kursus;\n"
        "USE F5512530117_kursus;\n\n"
        "CREATE TABLE materi_kursus (id_kursus INT AUTO_INCREMENT PRIMARY KEY, nama_kursus VARCHAR(100) NOT NULL, tingkat ENUM('Pemula','Menengah','Mahir') NOT NULL, durasi_pertemuan INT NOT NULL, harga_kursus DECIMAL(10,2) NOT NULL) ENGINE=InnoDB;\n"
        "CREATE TABLE instruktur (id_instruktur INT AUTO_INCREMENT PRIMARY KEY, nama_instruktur VARCHAR(100) NOT NULL, bidang_ahli VARCHAR(50) NOT NULL, email_instruktur VARCHAR(100) NOT NULL, honor_per_sesi DECIMAL(10,2) NOT NULL) ENGINE=InnoDB;\n"
        "CREATE TABLE siswa (id_siswa INT AUTO_INCREMENT PRIMARY KEY, nama_siswa VARCHAR(100) NOT NULL, email_siswa VARCHAR(100) UNIQUE NOT NULL, no_wa VARCHAR(15) NOT NULL, kota_asal VARCHAR(50) NOT NULL) ENGINE=InnoDB;\n"
        "CREATE TABLE jadwal_kelas (\n"
        "    id_jadwal INT AUTO_INCREMENT PRIMARY KEY, id_kursus INT NOT NULL, id_instruktur INT NOT NULL,\n"
        "    hari VARCHAR(20) NOT NULL, jam_mulai TIME NOT NULL, ruangan_online VARCHAR(100) NOT NULL,\n"
        "    CONSTRAINT fk_jd_kursus FOREIGN KEY (id_kursus) REFERENCES materi_kursus(id_kursus) ON DELETE RESTRICT ON UPDATE CASCADE,\n"
        "    CONSTRAINT fk_jd_instruktur FOREIGN KEY (id_instruktur) REFERENCES instruktur(id_instruktur) ON DELETE RESTRICT ON UPDATE CASCADE\n"
        ") ENGINE=InnoDB;\n"
        "CREATE TABLE pendaftaran (\n"
        "    id_daftar INT AUTO_INCREMENT PRIMARY KEY, id_siswa INT NOT NULL, id_jadwal INT NOT NULL,\n"
        "    tgl_daftar DATE NOT NULL, metode_bayar VARCHAR(30) NOT NULL, status_bayar ENUM('Lunas','Cicilan','Belum Bayar') NOT NULL,\n"
        "    CONSTRAINT fk_pdf_siswa FOREIGN KEY (id_siswa) REFERENCES siswa(id_siswa) ON DELETE CASCADE ON UPDATE CASCADE,\n"
        "    CONSTRAINT fk_pdf_jadwal FOREIGN KEY (id_jadwal) REFERENCES jadwal_kelas(id_jadwal) ON DELETE RESTRICT ON UPDATE CASCADE\n"
        ") ENGINE=InnoDB;",
        caption="DDL Basis Data F5512530117_kursus"
    )

    add_screenshot_box("Pembuatan 3 Database & Tabel", "SHOW DATABASES; USE F5512530117_bioskop; SHOW TABLES;")

    # 2.2 Desain Relasi
    add_h2("2.2 Desain Relasi Antar Tabel dan Penjelasan Kardinalitas")
    add_para("Relasi antar tabel dirancang untuk menjamin integritas referensial dan mencegah anomali basis data. Gambar diagram relasi untuk masing-masing basis data disajikan di bawah ini:")

    if os.path.exists("erd_database_1_bioskop.png"):
        p_img1 = doc.add_paragraph()
        format_p(p_img1, space_before=6, space_after=2, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=None)
        p_img1.add_run().add_picture("erd_database_1_bioskop.png", width=Inches(6.0))
        p_c1 = doc.add_paragraph()
        format_p(p_c1, space_before=2, space_after=8, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=None)
        rc1 = p_c1.add_run("Gambar 2.1 Desain Relasi Antar Tabel Basis Data F5512530117_bioskop")
        rc1.bold = True
        rc1.italic = True
        rc1.font.size = Pt(10)

    add_para("Penjelasan Relasi Basis Data Bioskop:", bold_prefix="1. Relasi Film ke Jadwal Tayang (1 : N): ")
    add_para("Satu film dapat memiliki banyak sesi penayangan di berbagai jadwal dan jam tayang yang berbeda. Sebaliknya, setiap satu sesi jadwal tayang mereferensikan satu film yang sah. Aturan ON DELETE RESTRICT melindungi data film agar tidak terhapus selama jadwal penayangannya masih aktif.")

    add_para("Relasi Studio ke Jadwal Tayang (1 : N): ", bold_prefix="2. ")
    add_para("Satu studio auditorium dapat dipakai berulang kali untuk banyak sesi pemutaran film sepanjang hari.")

    add_para("Relasi Penonton ke Transaksi Tiket (1 : N): ", bold_prefix="3. ")
    add_para("Satu penonton dapat melakukan banyak kali transaksi pembelian tiket bioskop.")

    add_para("Relasi Jadwal Tayang ke Transaksi Tiket (1 : N): ", bold_prefix="4. ")
    add_para("Satu sesi jadwal penayangan dapat menerbitkan banyak tiket kursi sesuai kapasitas penonton di studio.")

    if os.path.exists("erd_database_2_ekspedisi.png"):
        p_img2 = doc.add_paragraph()
        format_p(p_img2, space_before=6, space_after=2, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=None)
        p_img2.add_run().add_picture("erd_database_2_ekspedisi.png", width=Inches(6.0))
        p_c2 = doc.add_paragraph()
        format_p(p_c2, space_before=2, space_after=8, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=None)
        rc2 = p_c2.add_run("Gambar 2.2 Desain Relasi Antar Tabel Basis Data F5512530117_ekspedisi")
        rc2.bold = True
        rc2.italic = True
        rc2.font.size = Pt(10)

    if os.path.exists("erd_database_3_kursus.png"):
        p_img3 = doc.add_paragraph()
        format_p(p_img3, space_before=6, space_after=2, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=None)
        p_img3.add_run().add_picture("erd_database_3_kursus.png", width=Inches(6.0))
        p_c3 = doc.add_paragraph()
        format_p(p_c3, space_before=2, space_after=8, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=None)
        rc3 = p_c3.add_run("Gambar 2.3 Desain Relasi Antar Tabel Basis Data F5512530117_kursus")
        rc3.bold = True
        rc3.italic = True
        rc3.font.size = Pt(10)

    # 2.3 Manajemen Hak Akses (DCL)
    add_h2("2.3 Pembuatan 4 Pengguna (User) dengan Hak Akses Berbeda")
    add_para("Data Control Language (DCL) digunakan untuk mengontrol hak otorisasi dan privilese terhadap basis data. Dibuat 4 akun pengguna:")
    add_para("User 1: user_admin bertindak sebagai Administrator global dengan hak penuh (ALL PRIVILEGES) ke seluruh basis data di server (*.*) serta dilengkapi klausa WITH GRANT OPTION.", bold_prefix="a. ")
    add_para("User 2: admin_bioskop bertindak sebagai admin pengelola basis data F5512530117_bioskop.*.", bold_prefix="b. ")
    add_para("User 3: admin_ekspedisi bertindak sebagai admin pengelola basis data F5512530117_ekspedisi.*.", bold_prefix="c. ")
    add_para("User 4: admin_kursus bertindak sebagai admin pengelola basis data F5512530117_kursus.*.", bold_prefix="d. ")

    add_code_block(
        "-- Membuat Akun dan Memberikan Hak Akses (DCL)\n"
        "CREATE USER 'user_admin'@'localhost' IDENTIFIED BY 'AdminPass123!';\n"
        "GRANT ALL PRIVILEGES ON *.* TO 'user_admin'@'localhost' WITH GRANT OPTION;\n\n"
        "CREATE USER 'admin_bioskop'@'localhost' IDENTIFIED BY 'BioskopPass123!';\n"
        "GRANT ALL PRIVILEGES ON F5512530117_bioskop.* TO 'admin_bioskop'@'localhost';\n\n"
        "CREATE USER 'admin_ekspedisi'@'localhost' IDENTIFIED BY 'EkspedisiPass123!';\n"
        "GRANT ALL PRIVILEGES ON F5512530117_ekspedisi.* TO 'admin_ekspedisi'@'localhost';\n\n"
        "CREATE USER 'admin_kursus'@'localhost' IDENTIFIED BY 'KursusPass123!';\n"
        "GRANT ALL PRIVILEGES ON F5512530117_kursus.* TO 'admin_kursus'@'localhost';\n\n"
        "FLUSH PRIVILEGES;\n\n"
        "-- Menampilkan Bukti Hak Akses Pengguna\n"
        "SHOW GRANTS FOR 'user_admin'@'localhost';\n"
        "SHOW GRANTS FOR 'admin_bioskop'@'localhost';\n"
        "SHOW GRANTS FOR 'admin_ekspedisi'@'localhost';\n"
        "SHOW GRANTS FOR 'admin_kursus'@'localhost';",
        caption="Perintah Pembuatan 4 User & Hak Akses"
    )

    add_screenshot_box("Pemeriksaan Hak Akses 4 User", "SHOW GRANTS FOR 'user_admin'@'localhost'; SHOW GRANTS FOR 'admin_bioskop'@'localhost';")

    # 2.4 Simulasi Pencabutan Izin Akses (Read Only)
    add_h2("2.4 Simulasi Pencabutan Hak Akses Menjadi Read Only")
    add_para("Simulasi dilakukan pada akun admin_kursus. Pertama-tama, seluruh hak akses dicabut menggunakan perintah REVOKE ALL PRIVILEGES. Selanjutnya, diberikan kembali hanya hak akses SELECT pada basis data F5512530117_kursus sehingga pengguna tersebut berstatus Read Only (hanya dapat membaca data tanpa bisa menulis atau mengubah).")

    add_code_block(
        "-- Mencabut Seluruh Privilese\n"
        "REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'admin_kursus'@'localhost';\n\n"
        "-- Memberikan Hanya Izin SELECT (Read Only)\n"
        "GRANT SELECT ON F5512530117_kursus.* TO 'admin_kursus'@'localhost';\n"
        "FLUSH PRIVILEGES;\n\n"
        "-- Memeriksa Status Hak Akses Terakhir\n"
        "SHOW GRANTS FOR 'admin_kursus'@'localhost';",
        caption="Simulasi Read Only pada User admin_kursus"
    )

    add_screenshot_box("Simulasi Pencabutan Izin Akses & Penolakan Write", "SHOW GRANTS FOR 'admin_kursus'@'localhost';")

    # 2.5 Penambahan Kolom Setelah Kolom Ke-2
    add_h2("2.5 Penambahan 1 Kolom Setelah Kolom Ke-2 (ALTER TABLE)")
    add_para("Perintah ALTER TABLE dengan klausa AFTER digunakan untuk mengatur posisi peletakan kolom baru secara spesifik. Pada tabel penonton, kolom ke-1 adalah id_penonton dan kolom ke-2 adalah nama_penonton. Kolom baru yang ditambahkan adalah nik bertipe data VARCHAR(16) NOT NULL yang diletakkan persis setelah kolom ke-2 (AFTER nama_penonton).")

    add_code_block(
        "USE F5512530117_bioskop;\n\n"
        "-- 1. Menampilkan struktur tabel sebelum modifikasi\n"
        "DESCRIBE penonton;\n\n"
        "-- 2. Menambahkan kolom 'nik' tepat setelah kolom ke-2 (nama_penonton)\n"
        "ALTER TABLE penonton \n"
        "ADD COLUMN nik VARCHAR(16) NOT NULL AFTER nama_penonton;\n\n"
        "-- 3. Menampilkan struktur tabel setelah modifikasi\n"
        "DESCRIBE penonton;",
        caption="Penambahan Kolom NIK Setelah Kolom Ke-2"
    )

    add_screenshot_box("Struktur Tabel Penonton Sebelum dan Sesudah ALTER TABLE", "DESCRIBE penonton;")

    doc.add_page_break()

    # =========================================================================
    # BAB III: TUGAS 2 - DML (INSERT, UPDATE, SELECT, DELETE)
    # =========================================================================
    add_h1("BAB III. TUGAS 2: DML (DATA MANIPULATION LANGUAGE)")

    add_h2("3.1 Penambahan 10 Baris Data pada Masing-Masing Tabel")
    add_para("Data Manipulation Language (DML) digunakan untuk mengelola data di dalam tabel. Perintah INSERT INTO dieksekusi untuk mengisi 10 record data realistis pada seluruh tabel basis data F5512530117_bioskop (film, studio, penonton, jadwal_tayang, dan transaksi_tiket).")

    add_code_block(
        "-- Cuplikan Penambahan 10 Baris pada Tabel Film\n"
        "INSERT INTO film (judul_film, genre, durasi_menit, rating_usia, harga_dasar) VALUES\n"
        "('Avengers: Secret Wars', 'Action / Sci-Fi', 165, '13+', 50000.00),\n"
        "('Interstellar: Odyssey', 'Sci-Fi / Drama', 169, '13+', 45000.00),\n"
        "('The Conjuring: Last Rites', 'Horror / Mystery', 112, '17+', 40000.00),\n"
        "('Spider-Man: Beyond Verse', 'Animation / Action', 140, 'SU', 45000.00),\n"
        "('Oppenheimer: Re-Release', 'Biography / Drama', 180, '17+', 55000.00),\n"
        "('Fast & Furious: Final Lap', 'Action / Crime', 135, '13+', 45000.00),\n"
        "('Detective Conan: Dark Shadow', 'Animation / Mystery', 110, 'SU', 40000.00),\n"
        "('The Batman: Part II', 'Action / Thriller', 155, '17+', 50000.00),\n"
        "('Dune: Part Three', 'Sci-Fi / Adventure', 160, '13+', 55000.00),\n"
        "('John Wick: Chapter 5', 'Action / Thriller', 145, '21+', 50000.00);",
        caption="Insert 10 Baris Tabel Film"
    )

    add_screenshot_box("Verifikasi 10 Baris Data Tabel Film", "SELECT * FROM film;")

    # 3.2 Operasi Perubahan Berdasarkan Stambuk
    add_h2("3.2 Operasi Perubahan (UPDATE) Berdasarkan Kategori Stambuk")
    add_para("Ketentuan penugasan menyatakan bahwa mahasiswa dengan Stambuk Genap memodifikasi baris genap (2, 4, 6, 8, 10), sedangkan mahasiswa dengan Stambuk Ganjil memodifikasi baris ganjil (1, 3, 5, 7, 9). Mengingat NIM penyusun adalah F5512530117 dengan digit terakhir 7 (Ganjil), maka operasi UPDATE wajib dilakukan secara konsisten pada Baris Ganjil.")

    add_code_block(
        "-- Memperbarui Data Domisili pada Baris Ganjil (ID 1, 3, 5, 7, 9) Tabel Penonton\n"
        "UPDATE penonton \n"
        "SET kota_domisili = CONCAT(kota_domisili, ' [MEMBER VIP]') \n"
        "WHERE id_penonton IN (1, 3, 5, 7, 9);\n\n"
        "-- Memperbarui Harga Dasar pada Baris Ganjil Tabel Film\n"
        "UPDATE film \n"
        "SET harga_dasar = harga_dasar + 5000.00 \n"
        "WHERE id_film IN (1, 3, 5, 7, 9);",
        caption="Operasi Perubahan Baris Ganjil (Stambuk Ganjil)"
    )

    add_screenshot_box("Hasil Operasi Perubahan Baris Ganjil", "SELECT id_penonton, nama_penonton, kota_domisili FROM penonton;")

    # 3.3 SELECT 3 Kriteria
    add_h2("3.3 Perintah SELECT dengan 3 (Tiga) Jenis Kriteria")
    add_para("Klausa WHERE digunakan untuk menyaring record data berdasarkan kriteria logika tertentu:")
    add_para("Kriteria 1 (Operator Perbandingan & Logika AND): Menampilkan film dengan durasi >= 140 menit dan rating usia 13+.", bold_prefix="1. ")
    add_para("Kriteria 2 (Rentang BETWEEN & Pola String LIKE): Menampilkan jadwal dengan harga tiket antara Rp 50.000 s/d Rp 85.000 serta mencari penonton di wilayah 'Palu Timur'.", bold_prefix="2. ")
    add_para("Kriteria 3 (Himpunan Nilai IN): Menampilkan jadwal tayang pada studio khusus IMAX dan Premiere (ID 5, 6, 7, 8).", bold_prefix="3. ")

    add_code_block(
        "-- Kriteria 1: Perbandingan Relasional & Logika AND\n"
        "SELECT id_film, judul_film, genre, durasi_menit, rating_usia, harga_dasar \n"
        "FROM film \n"
        "WHERE durasi_menit >= 140 AND rating_usia = '13+' \n"
        "ORDER BY durasi_menit DESC;\n\n"
        "-- Kriteria 2: Rentang Nilai dan Pola String\n"
        "SELECT id_jadwal, id_film, id_studio, tgl_tayang, jam_mulai, harga_tiket \n"
        "FROM jadwal_tayang \n"
        "WHERE harga_tiket BETWEEN 50000.00 AND 85000.00;\n\n"
        "-- Kriteria 3: Himpunan Nilai IN\n"
        "SELECT id_jadwal, id_film, id_studio, tgl_tayang, harga_tiket \n"
        "FROM jadwal_tayang \n"
        "WHERE id_studio IN (5, 6, 7, 8);",
        caption="Implementasi SELECT 3 Jenis Kriteria"
    )

    add_screenshot_box("Eksekusi SELECT 3 Kriteria", "SELECT id_film, judul_film, durasi_menit, rating_usia FROM film WHERE durasi_menit >= 140 AND rating_usia = '13+';")

    # 3.4 SELECT Urutan Baris ke-3 Hingga Baris ke-7 (LIMIT)
    add_h2("3.4 Perintah SELECT Menampilkan Data dari Urutan Baris Ke-3 Hingga Baris Ke-7")
    add_para("Penjelasan Konsep Indeks Nol (Zero-Based Index):", bold_prefix="Teori LIMIT dan OFFSET: ")
    add_para("Dalam standar SQL MySQL, penomoran posisi baris (offset) selalu dimulai dari angka 0 (nol). Artinya: Baris ke-1 memiliki offset 0, baris ke-2 memiliki offset 1, dan baris ke-3 memiliki offset 2. Rentang baris ke-3 hingga ke-7 memuat sebanyak 5 record data (baris 3, 4, 5, 6, dan 7). Oleh karena itu, sintaks yang tepat adalah LIMIT 5 OFFSET 2 atau dalam sintaks ringkas MySQL: LIMIT 2, 5 (parameter pertama = baris yang dilewati, parameter kedua = jumlah baris yang diambil).")

    add_code_block(
        "-- Menampilkan baris ke-3 sampai baris ke-7 pada tabel PENONTON\n"
        "SELECT id_penonton, nama_penonton, nik, email, no_hp, kota_domisili \n"
        "FROM penonton \n"
        "ORDER BY id_penonton ASC \n"
        "LIMIT 5 OFFSET 2;\n\n"
        "-- Sintaks alternatif pada tabel FILM\n"
        "SELECT id_film, judul_film, genre, durasi_menit, rating_usia, harga_dasar \n"
        "FROM film \n"
        "ORDER BY id_film ASC \n"
        "LIMIT 2, 5;",
        caption="Query LIMIT dan OFFSET untuk Baris 3 Hingga 7"
    )

    add_screenshot_box("Hasil SELECT Baris Ke-3 Hingga Ke-7", "SELECT id_penonton, nama_penonton FROM penonton ORDER BY id_penonton ASC LIMIT 5 OFFSET 2;")

    # 3.5 Menghapus Data Ke-9
    add_h2("3.5 Perintah Menghapus Data Ke-9 pada Masing-Masing Tabel")
    add_para("Penghapusan data dilakukan menggunakan pernyataan DELETE dengan klausa pembatas WHERE id = 9. Urutan penghapusan wajib memperhatikan hierarki ketergantungan: tabel anak (child table seperti transaksi_tiket dan jadwal_tayang) harus dihapus terlebih dahulu sebelum data ke-9 pada tabel induk (penonton, film, studio) dapat dihapus tanpa memicu eror integrity constraint.")

    add_code_block(
        "-- Menghapus data baris ke-9 secara teratur\n"
        "DELETE FROM transaksi_tiket WHERE id_transaksi = 9;\n"
        "DELETE FROM jadwal_tayang WHERE id_jadwal = 9;\n"
        "DELETE FROM penonton WHERE id_penonton = 9;\n"
        "DELETE FROM film WHERE id_film = 9;\n"
        "DELETE FROM studio WHERE id_studio = 9;\n\n"
        "-- Verifikasi bahwa data ke-9 telah terhapus\n"
        "SELECT * FROM penonton WHERE id_penonton = 9;",
        caption="Penghapusan Data Ke-9 Mengikuti Aturan Integritas"
    )

    add_screenshot_box("Verifikasi Penghapusan Data Ke-9 (Empty Set)", "SELECT * FROM penonton WHERE id_penonton = 9;")

    doc.add_page_break()

    # =========================================================================
    # BAB IV: TUGAS 3 - RELASIONAL, JOIN, & FUNGSI AGREGAT
    # =========================================================================
    add_h1("BAB IV. TUGAS 3: IMPLEMENTASI JOIN DAN FUNGSI AGREGAT")

    add_h2("4.1 Basis Data Relasional 3 Tabel")
    add_para("Pada bagian ini dibentuk basis data F5512530117_cinema yang secara khusus mendemonstrasikan hubungan antara 3 tabel relasional inti: penonton (tabel master identitas penonton), film (tabel master judul film), dan transaksi_tiket (tabel transaksi penghubung yang mereferensikan primary key dari kedua tabel master).")

    if os.path.exists("erd_relasi_3_tabel_join.png"):
        p_img4 = doc.add_paragraph()
        format_p(p_img4, space_before=6, space_after=2, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=None)
        p_img4.add_run().add_picture("erd_relasi_3_tabel_join.png", width=Inches(6.0))
        p_c4 = doc.add_paragraph()
        format_p(p_c4, space_before=2, space_after=8, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER, first_indent=None)
        rc4 = p_c4.add_run("Gambar 4.1 Desain 3 Tabel Relasional untuk Implementasi Perintah JOIN")
        rc4.bold = True
        rc4.italic = True
        rc4.font.size = Pt(10)

    add_para("Dataset Uji Cerdas:", bold_prefix="Desain Data Uji Khusus: ")
    add_para("Agar perbedaan sifat INNER JOIN, LEFT JOIN, dan RIGHT JOIN terlihat sangat nyata di hasil terminal console, ditambahkan 1 data penonton baru (Gilang Ramadhan, ID 6) yang belum pernah memesan tiket, serta 1 film baru segera tayang (Avatar: The Seed Bearer, ID 5) yang belum memiliki riwayat penjualan tiket. Keberadaan record ini menjadi kunci pembuktian nilai NULL pada operasi Outer Join.")

    # 4.2 Implementasi 3 Perintah JOIN
    add_h2("4.2 Implementasi Tiga Perintah JOIN (INNER, LEFT, RIGHT)")

    add_h3("A. Implementasi INNER JOIN")
    add_para("INNER JOIN hanya mengembalikan baris di mana terdapat kecocokan nilai kunci di antara tabel-tabel yang digabungkan. Penonton yang belum beli tiket dan film yang belum ada penjualan tiket TIDAK AKAN ditampilkan sama sekali.")

    add_code_block(
        "SELECT \n"
        "    t.id_transaksi, p.nama_penonton, f.judul_film, f.genre, \n"
        "    t.nomor_kursi, t.metode_bayar, t.total_bayar\n"
        "FROM transaksi_tiket t\n"
        "INNER JOIN penonton p ON t.id_penonton = p.id_penonton\n"
        "INNER JOIN film f ON t.id_film = f.id_film\n"
        "ORDER BY t.id_transaksi ASC;",
        caption="Query INNER JOIN 3 Tabel"
    )

    add_screenshot_box("Hasil Eksekusi INNER JOIN", "SELECT t.id_transaksi, p.nama_penonton, f.judul_film FROM transaksi_tiket t INNER JOIN penonton p ON t.id_penonton = p.id_penonton INNER JOIN film f ON t.id_film = f.id_film;")

    add_h3("B. Implementasi LEFT JOIN")
    add_para("LEFT JOIN mempertahankan dan menampilkan SELURUH baris dari tabel sebelah kiri (penonton), terlepas dari apakah ada relasi di tabel transaksi tiket. Penonton ID 6 (Gilang Ramadhan) tetap muncul di tabel output, dengan atribut judul_film, nomor_kursi, dan total_bayar terisi nilai NULL.")

    add_code_block(
        "SELECT \n"
        "    p.id_penonton, p.nama_penonton, p.kota_domisili,\n"
        "    t.nomor_kursi, f.judul_film, t.total_bayar\n"
        "FROM penonton p\n"
        "LEFT JOIN transaksi_tiket t ON p.id_penonton = t.id_penonton\n"
        "LEFT JOIN film f ON t.id_film = f.id_film\n"
        "ORDER BY p.id_penonton ASC;",
        caption="Query LEFT JOIN Menampilkan Seluruh Penonton Termasuk Yang Belum Beli Tiket"
    )

    add_screenshot_box("Hasil Eksekusi LEFT JOIN (Perhatikan Baris NULL)", "SELECT p.id_penonton, p.nama_penonton, f.judul_film FROM penonton p LEFT JOIN transaksi_tiket t ON p.id_penonton = t.id_penonton LEFT JOIN film f ON t.id_film = f.id_film;")

    add_h3("C. Implementasi RIGHT JOIN")
    add_para("RIGHT JOIN mempertahankan dan menampilkan SELURUH baris dari tabel sebelah kanan (film), terlepas dari apakah film tersebut pernah terjual tiketnya. Film ID 5 (Avatar: The Seed Bearer) tetap ditampilkan pada terminal, dengan atribut transaksi dan penonton bernilai NULL.")

    add_code_block(
        "SELECT \n"
        "    f.id_film, f.judul_film, f.genre, f.harga_dasar,\n"
        "    t.id_transaksi, p.nama_penonton, t.nomor_kursi\n"
        "FROM transaksi_tiket t\n"
        "RIGHT JOIN film f ON t.id_film = f.id_film\n"
        "LEFT JOIN penonton p ON t.id_penonton = p.id_penonton\n"
        "ORDER BY f.id_film ASC;",
        caption="Query RIGHT JOIN Menampilkan Seluruh Film Termasuk Yang Belum Ada Penjualan Tiket"
    )

    add_screenshot_box("Hasil Eksekusi RIGHT JOIN (Perhatikan Film Tanpa Tiket)", "SELECT f.id_film, f.judul_film, t.id_transaksi FROM transaksi_tiket t RIGHT JOIN film f ON t.id_film = f.id_film;")

    # 4.3 Fungsi Agregat (MAX, MIN, COUNT)
    add_h2("4.3 Nilai MAX, MIN, dan Hitung Jumlah Baris (COUNT) pada Masing-Masing Tabel")
    add_para("Fungsi agregat SQL memproses sekumpulan baris data untuk menghasilkan sebuah nilai skalar ringkasan:")
    add_para("COUNT(*): Menghitung banyaknya jumlah baris record aktual pada tabel.", bold_prefix="1. ")
    add_para("MAX(kolom): Mengembalikan nilai terbesar/tertinggi dalam suatu kolom numerik atau temporal.", bold_prefix="2. ")
    add_para("MIN(kolom): Mengembalikan nilai terkecil/terendah dalam suatu kolom.", bold_prefix="3. ")

    add_code_block(
        "-- A. Agregasi pada Tabel PENONTON\n"
        "SELECT \n"
        "    COUNT(*) AS total_penonton_terdaftar,\n"
        "    MAX(tgl_lahir) AS tgl_lahir_termuda,\n"
        "    MIN(tgl_lahir) AS tgl_lahir_tertua\n"
        "FROM penonton;\n\n"
        "-- B. Agregasi pada Tabel FILM\n"
        "SELECT \n"
        "    COUNT(*) AS total_film,\n"
        "    MAX(harga_dasar) AS harga_film_termahal,\n"
        "    MIN(harga_dasar) AS harga_film_termurah\n"
        "FROM film;\n\n"
        "-- C. Agregasi pada Tabel TRANSAKSI_TIKET\n"
        "SELECT \n"
        "    COUNT(*) AS total_tiket_terjual,\n"
        "    MAX(total_bayar) AS transaksi_tertinggi,\n"
        "    MIN(total_bayar) AS transaksi_terendah\n"
        "FROM transaksi_tiket;",
        caption="Perhitungan MAX, MIN, dan COUNT pada Seluruh Tabel"
    )

    add_screenshot_box("Hasil Eksekusi Fungsi Agregat MAX, MIN, COUNT", "SELECT COUNT(*), MAX(harga_dasar), MIN(harga_dasar) FROM film;")

    doc.add_page_break()

    # =========================================================================
    # BAB V: PANDUAN PRAKTIS EKSEKUSI CONSOLE
    # =========================================================================
    add_h1("BAB V. PANDUAN PRAKTIS EKSEKUSI DI CONSOLE MYSQL")
    
    add_para("Untuk mempermudah pengambilan tangkap layar mandiri pada terminal console MySQL, berikut adalah tahapan praktis yang dapat langsung diikuti:")

    langkah_data = [
        ["1", "Membuka Console", "Buka menu Start Windows > ketik 'MySQL 8.0 Command Line Client' lalu klik, atau buka Command Prompt (cmd) dan jalankan: mysql -u root -p"],
        ["2", "Login ke Server", "Masukkan password root MySQL Anda saat muncul prompt 'Enter password:'."],
        ["3", "Menjalankan Script SQL", "Untuk mengeksekusi script secara otomatis, gunakan perintah SOURCE diikuti path file, contoh: SOURCE D:/Tugas semester 3/DB/BUAT DATABASE/all_in_one_praktikum.sql;"],
        ["4", "Eksekusi Baris per Baris", "Anda juga dapat menyalin (copy-paste) query per bagian untuk mendapatkan tangkapan layar setiap tabel secara terpisah."],
        ["5", "Mengambil Screenshot", "Gunakan kombinasi tombol Windows + Shift + S atau Alt + PrtScn untuk menangkap jendela console secara jernih, lalu tempelkan (Paste) pada placeholder di laporan ini."]
    ]
    add_custom_table(["Langkah", "Kegiatan", "Panduan Eksekusi Terminal Console"], langkah_data, [1.5, 3.5, 8.0], font_size=9.5)

    add_h1("BAB VI. KESIMPULAN")
    add_para("Berdasarkan seluruh rangkaian pengerjaan penugasan praktikum Sistem Basis Data ini, dapat ditarik beberapa kesimpulan penting:")
    add_para("1. Struktur DDL yang dilengkapi aturan primary key dan foreign key menjamin keutuhan relasi antar entitas, mencegah duplikasi data, dan menghindari anomali penyimpanan.", first_indent=Cm(0.75))
    add_para("2. Manajemen privilese DCL memungkinkan pengelola sistem membatasi wewenang setiap akun pengguna secara terisolasi (least privilege principle). Simulasi pencabutan hak akses terbukti membatasi akun menjadi read-only yang aman dari manipulasi data tak berizin.", first_indent=Cm(0.75))
    add_para("3. Operasi DML seperti INSERT, UPDATE baris ganjil sesuai stambuk ganjil F5512530117, SELECT dengan 3 kriteria, pembatasan rentang LIMIT OFFSET, serta penghapusan DELETE berhasil dijalankan sesuai prinsip konsistensi basis data.", first_indent=Cm(0.75))
    add_para("4. Pemahaman terhadap operasi JOIN terbukti krusial dalam integrasi data multi-tabel: INNER JOIN menghasilkan persimpangan data yang valid, sementara LEFT dan RIGHT JOIN memungkinkan pemantauan record yang belum berpasangan melalui representasi nilai NULL.", first_indent=Cm(0.75))

    # Daftar Pustaka
    add_h1("DAFTAR PUSTAKA")
    p_dp1 = doc.add_paragraph()
    format_p(p_dp1, space_before=4, space_after=4, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_indent=-Cm(1.0))
    p_dp1.paragraph_format.left_indent = Cm(1.0)
    p_dp1.add_run("Elmasri, R., & Navathe, S. B. (2020). ").bold = False
    p_dp1.add_run("Fundamentals of Database Systems").italic = True
    p_dp1.add_run(" (7th ed.). Pearson Education.")

    p_dp2 = doc.add_paragraph()
    format_p(p_dp2, space_before=4, space_after=4, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_indent=-Cm(1.0))
    p_dp2.paragraph_format.left_indent = Cm(1.0)
    p_dp2.add_run("Kroenke, D. M., Auer, D. J., Vandenberg, S. L., & Yoder, R. C. (2021). ").bold = False
    p_dp2.add_run("Database Processing: Fundamentals, Design, and Implementation").italic = True
    p_dp2.add_run(" (15th ed.). Pearson.")

    p_dp3 = doc.add_paragraph()
    format_p(p_dp3, space_before=4, space_after=4, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_indent=-Cm(1.0))
    p_dp3.paragraph_format.left_indent = Cm(1.0)
    p_dp3.add_run("Oracle Corporation. (2026). ").bold = False
    p_dp3.add_run("MySQL 8.0 Reference Manual: DDL, DML, DCL, and JOIN Syntax").italic = True
    p_dp3.add_run(". Oracle Documentation.")

    # Save Word Document
    docx_filename = "Laporan_Praktikum_Basis_Data_F5512530117_Muhammad_Zikri_Adam.docx"
    doc.save(docx_filename)
    print(f"Document saved successfully: {docx_filename}")

    # Convert to PDF using Word COM
    pdf_filename = "Laporan_Praktikum_Basis_Data_F5512530117_Muhammad_Zikri_Adam.pdf"
    abs_docx = os.path.abspath(docx_filename)
    abs_pdf = os.path.abspath(pdf_filename)
    
    print("Converting to PDF via Word COM...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        wb = word.Documents.Open(abs_docx)
        wb.SaveAs(abs_pdf, FileFormat=17) # 17 = wdFormatPDF
        wb.Close()
        print(f"PDF saved successfully: {pdf_filename}")
    except Exception as e:
        print(f"Error during PDF conversion: {e}")
    finally:
        word.Quit()

if __name__ == "__main__":
    generate_report()
