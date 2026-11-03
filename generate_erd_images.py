import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_table(ax, x, y, width, header_text, columns, header_color="#1E3A8A"):
    """
    Renders an ERD table node with a header and list of columns (PK, FK, and regular attributes).
    """
    row_height = 0.32
    header_height = 0.42
    total_height = header_height + len(columns) * row_height

    # Shadow
    shadow = patches.FancyBboxPatch((x + 0.05, y - total_height - 0.05), width, total_height,
                                    boxstyle="round,pad=0.04,rounding_size=0.08",
                                    facecolor="#CBD5E1", edgecolor="none", zorder=1)
    ax.add_patch(shadow)

    # Background card
    card = patches.FancyBboxPatch((x, y - total_height), width, total_height,
                                  boxstyle="round,pad=0.04,rounding_size=0.08",
                                  facecolor="#FFFFFF", edgecolor="#94A3B8", linewidth=1.5, zorder=2)
    ax.add_patch(card)

    # Header bar
    header_box = patches.FancyBboxPatch((x, y - header_height), width, header_height,
                                        boxstyle="round,pad=0.04,rounding_size=0.08",
                                        facecolor=header_color, edgecolor=header_color, linewidth=1, zorder=3)
    ax.add_patch(header_box)
    
    # Square bottom of header
    header_bottom = patches.Rectangle((x, y - header_height), width, header_height * 0.4,
                                      facecolor=header_color, edgecolor=header_color, zorder=3)
    ax.add_patch(header_bottom)

    # Header text
    ax.text(x + width / 2.0, y - header_height / 2.0, header_text,
            ha="center", va="center", color="white", fontsize=10.5, fontweight="bold", fontfamily="sans-serif", zorder=4)

    # Draw columns
    curr_y = y - header_height
    for idx, (col_type, col_name, data_type) in enumerate(columns):
        curr_y -= row_height
        # Alternating background
        if idx % 2 == 1:
            row_bg = patches.Rectangle((x, curr_y), width, row_height, facecolor="#F8FAFC", edgecolor="none", zorder=3)
            ax.add_patch(row_bg)

        # Badge / Prefix text
        prefix_color = "#B91C1C" if col_type == "PK" else ("#0D9488" if col_type == "FK" else "#64748B")
        badge_fontweight = "bold" if col_type in ["PK", "FK"] else "normal"
        
        ax.text(x + 0.12, curr_y + row_height / 2.0, col_type,
                ha="left", va="center", color=prefix_color, fontsize=8.5, fontweight=badge_fontweight, fontfamily="monospace", zorder=4)

        ax.text(x + 0.65, curr_y + row_height / 2.0, col_name,
                ha="left", va="center", color="#0F172A", fontsize=9, fontweight=badge_fontweight, fontfamily="sans-serif", zorder=4)

        ax.text(x + width - 0.12, curr_y + row_height / 2.0, data_type,
                ha="right", va="center", color="#64748B", fontsize=8, fontstyle="italic", fontfamily="monospace", zorder=4)

    return (x, y, width, total_height)

def draw_connector(ax, start_pt, end_pt, label="1:N", color="#2563EB", style="arc3,rad=0.0"):
    """
    Draws a relational connector arrow between tables with a label.
    """
    arrow = patches.ConnectionStyle(style)
    ax.annotate("", xy=end_pt, xytext=start_pt,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.8, connectionstyle=style, mutation_scale=14),
                zorder=5)
    
    # Place label at midpoint
    mid_x = (start_pt[0] + end_pt[0]) / 2.0
    mid_y = (start_pt[1] + end_pt[1]) / 2.0
    ax.text(mid_x, mid_y + 0.08, label, ha="center", va="center",
            fontsize=8.5, fontweight="bold", color=color,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#EFF6FF", edgecolor=color, lw=0.8),
            zorder=6)

def generate_database_1_erd():
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9)
    ax.axis("off")
    fig.patch.set_facecolor("#F1F5F9")

    # Title
    ax.text(7.5, 8.55, "DIAGRAM RELASI BASIS DATA: F5512530117_bioskop",
            ha="center", va="center", fontsize=15, fontweight="bold", color="#1E293B", fontfamily="sans-serif")
    ax.text(7.5, 8.25, "Sistem Informasi Manajemen Tiket Bioskop & Penayangan Film (5 Tabel)",
            ha="center", va="center", fontsize=10.5, color="#64748B", fontfamily="sans-serif")

    # Table 1: Film (Top Left)
    draw_table(ax, 0.8, 7.8, 3.4, "film", [
        ("PK", "id_film", "INT"),
        ("  ", "judul_film", "VARCHAR(150)"),
        ("  ", "genre", "VARCHAR(50)"),
        ("  ", "durasi_menit", "INT"),
        ("  ", "rating_usia", "ENUM(...)"),
        ("  ", "harga_dasar", "DECIMAL(10,2)")
    ], header_color="#1E3A8A")

    # Table 2: Studio (Bottom Left)
    draw_table(ax, 0.8, 4.4, 3.4, "studio", [
        ("PK", "id_studio", "INT"),
        ("  ", "nama_studio", "VARCHAR(50)"),
        ("  ", "tipe_layar", "VARCHAR(30)"),
        ("  ", "kapasitas_kursi", "INT"),
        ("  ", "biaya_tambahan", "DECIMAL(10,2)")
    ], header_color="#0F766E")

    # Table 3: Penonton (Bottom Right)
    draw_table(ax, 10.8, 4.4, 3.4, "penonton", [
        ("PK", "id_penonton", "INT"),
        ("  ", "nama_penonton", "VARCHAR(100)"),
        ("  ", "nik", "VARCHAR(16)"),
        ("  ", "email", "VARCHAR(100)"),
        ("  ", "no_hp", "VARCHAR(15)"),
        ("  ", "kota_domisili", "VARCHAR(50)")
    ], header_color="#B45309")

    # Table 4: Jadwal Tayang (Center)
    draw_table(ax, 5.8, 7.8, 3.4, "jadwal_tayang", [
        ("PK", "id_jadwal", "INT"),
        ("FK", "id_film", "INT"),
        ("FK", "id_studio", "INT"),
        ("  ", "tgl_tayang", "DATE"),
        ("  ", "jam_mulai", "TIME"),
        ("  ", "harga_tiket", "DECIMAL(10,2)")
    ], header_color="#4338CA")

    # Table 5: Transaksi Tiket (Top Right)
    draw_table(ax, 10.8, 7.8, 3.4, "transaksi_tiket", [
        ("PK", "id_transaksi", "INT"),
        ("FK", "id_penonton", "INT"),
        ("FK", "id_jadwal", "INT"),
        ("  ", "waktu_transaksi", "DATETIME"),
        ("  ", "nomor_kursi", "VARCHAR(10)"),
        ("  ", "metode_bayar", "VARCHAR(30)"),
        ("  ", "total_bayar", "DECIMAL(10,2)")
    ], header_color="#047857")

    # Relational Connectors
    # Film (1) -> Jadwal Tayang (N)
    draw_connector(ax, (4.2, 6.4), (5.8, 6.4), label="1 : N", color="#2563EB")
    
    # Studio (1) -> Jadwal Tayang (N)
    draw_connector(ax, (4.2, 3.2), (5.8, 5.6), label="1 : N", color="#0F766E", style="arc3,rad=-0.15")

    # Jadwal Tayang (1) -> Transaksi Tiket (N)
    draw_connector(ax, (9.2, 6.4), (10.8, 6.4), label="1 : N", color="#4338CA")

    # Penonton (1) -> Transaksi Tiket (N)
    draw_connector(ax, (12.5, 4.4), (12.5, 5.4), label="1 : N", color="#B45309")

    plt.tight_layout()
    plt.savefig("erd_database_1_bioskop.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("Generated erd_database_1_bioskop.png")

def generate_database_2_erd():
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9)
    ax.axis("off")
    fig.patch.set_facecolor("#F1F5F9")

    # Title
    ax.text(7.5, 8.55, "DIAGRAM RELASI BASIS DATA: F5512530117_ekspedisi",
            ha="center", va="center", fontsize=15, fontweight="bold", color="#1E293B", fontfamily="sans-serif")
    ax.text(7.5, 8.25, "Sistem Informasi Manajemen Ekspedisi & Logistik Pengiriman (5 Tabel)",
            ha="center", va="center", fontsize=10.5, color="#64748B", fontfamily="sans-serif")

    # Table 1: Pengirim
    draw_table(ax, 0.8, 7.8, 3.4, "pengirim", [
        ("PK", "id_pengirim", "INT"),
        ("  ", "nama_pengirim", "VARCHAR(100)"),
        ("  ", "kota_asal", "VARCHAR(50)"),
        ("  ", "alamat_asal", "VARCHAR(255)"),
        ("  ", "no_telp_pengirim", "VARCHAR(15)")
    ], header_color="#1E3A8A")

    # Table 2: Penerima
    draw_table(ax, 0.8, 4.8, 3.4, "penerima", [
        ("PK", "id_penerima", "INT"),
        ("  ", "nama_penerima", "VARCHAR(100)"),
        ("  ", "kota_tujuan", "VARCHAR(50)"),
        ("  ", "alamat_tujuan", "VARCHAR(255)"),
        ("  ", "no_telp_penerima", "VARCHAR(15)")
    ], header_color="#0F766E")

    # Table 3: Kurir
    draw_table(ax, 5.8, 3.8, 3.4, "kurir", [
        ("PK", "id_kurir", "INT"),
        ("  ", "nama_kurir", "VARCHAR(100)"),
        ("  ", "no_plat", "VARCHAR(15)"),
        ("  ", "jenis_kendaraan", "VARCHAR(30)"),
        ("  ", "wilayah_tugas", "VARCHAR(50)")
    ], header_color="#B45309")

    # Table 4: Paket
    draw_table(ax, 5.8, 7.8, 3.4, "paket", [
        ("PK", "id_paket", "INT"),
        ("  ", "no_resi", "VARCHAR(25)"),
        ("FK", "id_pengirim", "INT"),
        ("FK", "id_penerima", "INT"),
        ("FK", "id_kurir", "INT"),
        ("  ", "jenis_layanan", "VARCHAR(30)"),
        ("  ", "berat_kg", "DECIMAL(6,2)"),
        ("  ", "ongkos_kirim", "DECIMAL(10,2)")
    ], header_color="#6366F1")

    # Table 5: Pelacakan Status
    draw_table(ax, 10.8, 7.8, 3.4, "pelacakan_status", [
        ("PK", "id_status", "INT"),
        ("FK", "id_paket", "INT"),
        ("  ", "waktu_update", "DATETIME"),
        ("  ", "lokasi_posisi", "VARCHAR(100)"),
        ("  ", "status_paket", "VARCHAR(50)"),
        ("  ", "keterangan", "VARCHAR(255)")
    ], header_color="#047857")

    # Connectors
    draw_connector(ax, (4.2, 6.5), (5.8, 6.8), label="1 : N", color="#2563EB")
    draw_connector(ax, (4.2, 3.6), (5.8, 5.8), label="1 : N", color="#0F766E", style="arc3,rad=-0.12")
    draw_connector(ax, (7.5, 3.8), (7.5, 4.8), label="1 : N", color="#B45309")
    draw_connector(ax, (9.2, 6.2), (10.8, 6.2), label="1 : N", color="#059669")

    plt.tight_layout()
    plt.savefig("erd_database_2_ekspedisi.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("Generated erd_database_2_ekspedisi.png")

def generate_database_3_erd():
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9)
    ax.axis("off")
    fig.patch.set_facecolor("#F1F5F9")

    # Title
    ax.text(7.5, 8.55, "DIAGRAM RELASI BASIS DATA: F5512530117_kursus",
            ha="center", va="center", fontsize=15, fontweight="bold", color="#1E293B", fontfamily="sans-serif")
    ax.text(7.5, 8.25, "Sistem Informasi Manajemen Akademi Kursus & Pelatihan (5 Tabel)",
            ha="center", va="center", fontsize=10.5, color="#64748B", fontfamily="sans-serif")

    # Table 1: Materi Kursus
    draw_table(ax, 0.8, 7.8, 3.4, "materi_kursus", [
        ("PK", "id_kursus", "INT"),
        ("  ", "nama_kursus", "VARCHAR(100)"),
        ("  ", "tingkat", "ENUM(...)"),
        ("  ", "durasi_pertemuan", "INT"),
        ("  ", "harga_kursus", "DECIMAL(10,2)")
    ], header_color="#1E3A8A")

    # Table 2: Instruktur
    draw_table(ax, 0.8, 4.8, 3.4, "instruktur", [
        ("PK", "id_instruktur", "INT"),
        ("  ", "nama_instruktur", "VARCHAR(100)"),
        ("  ", "bidang_ahli", "VARCHAR(50)"),
        ("  ", "email_instruktur", "VARCHAR(100)"),
        ("  ", "honor_per_sesi", "DECIMAL(10,2)")
    ], header_color="#0F766E")

    # Table 3: Siswa
    draw_table(ax, 10.8, 4.4, 3.4, "siswa", [
        ("PK", "id_siswa", "INT"),
        ("  ", "nama_siswa", "VARCHAR(100)"),
        ("  ", "email_siswa", "VARCHAR(100)"),
        ("  ", "no_wa", "VARCHAR(15)"),
        ("  ", "kota_asal", "VARCHAR(50)")
    ], header_color="#B45309")

    # Table 4: Jadwal Kelas
    draw_table(ax, 5.8, 7.8, 3.4, "jadwal_kelas", [
        ("PK", "id_jadwal", "INT"),
        ("FK", "id_kursus", "INT"),
        ("FK", "id_instruktur", "INT"),
        ("  ", "hari", "VARCHAR(20)"),
        ("  ", "jam_mulai", "TIME"),
        ("  ", "ruangan_online", "VARCHAR(100)")
    ], header_color="#6366F1")

    # Table 5: Pendaftaran
    draw_table(ax, 10.8, 7.8, 3.4, "pendaftaran", [
        ("PK", "id_daftar", "INT"),
        ("FK", "id_siswa", "INT"),
        ("FK", "id_jadwal", "INT"),
        ("  ", "tgl_daftar", "DATE"),
        ("  ", "metode_bayar", "VARCHAR(30)"),
        ("  ", "status_bayar", "ENUM(...)")
    ], header_color="#047857")

    # Connectors
    draw_connector(ax, (4.2, 6.4), (5.8, 6.4), label="1 : N", color="#2563EB")
    draw_connector(ax, (4.2, 3.6), (5.8, 5.8), label="1 : N", color="#0F766E", style="arc3,rad=-0.12")
    draw_connector(ax, (9.2, 6.4), (10.8, 6.4), label="1 : N", color="#6366F1")
    draw_connector(ax, (12.5, 4.4), (12.5, 5.4), label="1 : N", color="#B45309")

    plt.tight_layout()
    plt.savefig("erd_database_3_kursus.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("Generated erd_database_3_kursus.png")

def generate_relasi_3_tabel():
    fig, ax = plt.subplots(figsize=(14, 6.5), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    fig.patch.set_facecolor("#F8FAFC")

    # Title
    ax.text(7.0, 6.0, "DIAGRAM RELASI 3 TABEL (TUGAS 3 - IMPLEMENTASI JOIN BIOSKOP)",
            ha="center", va="center", fontsize=14, fontweight="bold", color="#1E293B", fontfamily="sans-serif")
    ax.text(7.0, 5.65, "Tabel: penonton (Master), transaksi_tiket (Transaksi Relasi), film (Master)",
            ha="center", va="center", fontsize=10, color="#64748B", fontfamily="sans-serif")

    # Table 1: Penonton (Left)
    draw_table(ax, 0.8, 5.1, 3.4, "penonton", [
        ("PK", "id_penonton", "INT"),
        ("  ", "nama_penonton", "VARCHAR(100)"),
        ("  ", "nik", "VARCHAR(16)"),
        ("  ", "email", "VARCHAR(100)"),
        ("  ", "no_hp", "VARCHAR(15)"),
        ("  ", "kota_domisili", "VARCHAR(50)")
    ], header_color="#1E3A8A")

    # Table 2: Transaksi Tiket (Center)
    draw_table(ax, 5.3, 5.1, 3.4, "transaksi_tiket", [
        ("PK", "id_transaksi", "INT"),
        ("FK", "id_penonton", "INT"),
        ("FK", "id_film", "INT"),
        ("  ", "waktu_transaksi", "DATETIME"),
        ("  ", "nomor_kursi", "VARCHAR(10)"),
        ("  ", "total_bayar", "DECIMAL(10,2)")
    ], header_color="#4338CA")

    # Table 3: Film (Right)
    draw_table(ax, 9.8, 5.1, 3.4, "film", [
        ("PK", "id_film", "INT"),
        ("  ", "judul_film", "VARCHAR(150)"),
        ("  ", "genre", "VARCHAR(50)"),
        ("  ", "durasi_menit", "INT"),
        ("  ", "rating_usia", "ENUM(...)"),
        ("  ", "harga_dasar", "DECIMAL(10,2)")
    ], header_color="#0F766E")

    # Connectors
    draw_connector(ax, (4.2, 3.8), (5.3, 3.8), label="penonton.id_penonton = transaksi_tiket.id_penonton", color="#2563EB")
    draw_connector(ax, (9.8, 3.8), (8.7, 3.8), label="film.id_film = transaksi_tiket.id_film", color="#0F766E")

    plt.tight_layout()
    plt.savefig("erd_relasi_3_tabel_join.png", bbox_inches="tight", dpi=300)
    plt.close()
    print("Generated erd_relasi_3_tabel_join.png")

if __name__ == "__main__":
    generate_database_1_erd()
    generate_database_2_erd()
    generate_database_3_erd()
    generate_relasi_3_tabel()
