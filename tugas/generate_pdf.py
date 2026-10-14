# -*- coding: utf-8 -*-
"""
Generator Dokumen PDF - Tugas Pemrograman Perangkat Bergerak
Aplikasi Pengaduan Fasilitas Kampus (Flutter + Node.js + MySQL)
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Image, Table, TableStyle, PageBreak,
                                KeepTogether, NextPageTemplate)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = os.path.dirname(os.path.abspath(__file__))
MOCK = os.path.join(BASE, "mockup")
ASSETS = os.path.join(BASE, "assets")

# ── Warna ──
PRIMARY = colors.HexColor("#1565C0")
PRIMARY_D = colors.HexColor("#0D47A1")
SECONDARY = colors.HexColor("#26A69A")
GREY = colors.HexColor("#555555")
LIGHT = colors.HexColor("#F5F7FA")
BORDER = colors.HexColor("#D0D8E0")

# ── Font (Calibri jika ada) ──
def reg_font(name, path):
    if os.path.exists(path):
        pdfmetrics.registerFont(TTFont(name, path))
        return True
    return False

FONT = "Helvetica"
FONT_B = "Helvetica-Bold"
if reg_font("Calibri", "C:/Windows/Fonts/calibri.ttf"):
    reg_font("Calibri-Bold", "C:/Windows/Fonts/calibrib.ttf")
    FONT = "Calibri"; FONT_B = "Calibri-Bold"

# ── Styles ──
ss = getSampleStyleSheet()
def style(name, **kw):
    base = dict(fontName=FONT, fontSize=11.5, leading=18, textColor=colors.HexColor("#212121"))
    base.update(kw)
    return ParagraphStyle(name, **base)

S_TITLE   = style("T", fontName=FONT_B, fontSize=26, leading=32, textColor=PRIMARY_D, alignment=TA_CENTER)
S_SUB     = style("ST", fontSize=14, leading=20, textColor=GREY, alignment=TA_CENTER)
S_H1      = style("H1", fontName=FONT_B, fontSize=17, leading=22, textColor=colors.white)
S_H2      = style("H2", fontName=FONT_B, fontSize=14, leading=19, textColor=PRIMARY_D, spaceBefore=6, spaceAfter=4)
S_BODY    = style("B", alignment=TA_JUSTIFY, spaceAfter=8)
S_BULLET  = style("BU", alignment=TA_JUSTIFY, leftIndent=18, bulletIndent=6, spaceAfter=5)
S_CENTER  = style("C", alignment=TA_CENTER)
S_SMALL   = style("SM", fontSize=10, textColor=GREY, alignment=TA_CENTER)
S_CELL    = style("CE", fontSize=10.5, leading=15)
S_CELLB   = style("CEB", fontName=FONT_B, fontSize=10.5, leading=15)

def h1_box(num, title):
    """Heading kotak berwarna."""
    t = Table([[Paragraph(f"{num}.&nbsp;&nbsp;{title}", S_H1)]],
              colWidths=[17*cm], rowHeights=[0.95*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PRIMARY),
        ("LEFTPADDING", (0,0), (-1,-1), 14),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROUNDEDCORNERS", [6,6,6,6]),
    ]))
    return t

def P(txt, st=S_BODY): return Paragraph(txt, st)
def bullet(txt): return Paragraph(txt, S_BULLET, bulletText="•")

# ══════════════════════════════════════════════════════════
#  HALAMAN JUDUL (Cover)
# ══════════════════════════════════════════════════════════
def cover():
    el = []
    el.append(Spacer(1, 0.3*cm))
    # Logo UMB
    logo_path = os.path.join(ASSETS, "logo_umb.png")
    if os.path.exists(logo_path):
        img = Image(logo_path, width=3.4*cm, height=3.4*cm)
        img.hAlign = "CENTER"
        el.append(img)
    el.append(Spacer(1, 0.5*cm))
    el.append(P("LAPORAN TUGAS MATA KULIAH", style("c1", fontName=FONT_B, fontSize=13, textColor=SECONDARY, alignment=TA_CENTER)))
    el.append(P("PEMROGRAMAN PERANGKAT BERGERAK", style("c2", fontName=FONT_B, fontSize=13, textColor=SECONDARY, alignment=TA_CENTER)))
    el.append(Spacer(1, 0.6*cm))
    el.append(P("APLIKASI PENGADUAN<br/>FASILITAS KAMPUS", S_TITLE))
    el.append(Spacer(1, 0.2*cm))
    el.append(P("Aplikasi Mobile Berbasis Client-Server untuk Pelaporan<br/>Keluhan Fasilitas Kampus", S_SUB))
    el.append(Spacer(1, 0.5*cm))

    # garis
    line = Table([[""]], colWidths=[10*cm], rowHeights=[2])
    line.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),SECONDARY)]))
    el.append(line)
    el.append(Spacer(1, 0.6*cm))

    # Anggota
    el.append(P("Disusun oleh:", style("c3", fontName=FONT_B, fontSize=12, alignment=TA_CENTER, textColor=PRIMARY_D)))
    el.append(Spacer(1, 0.2*cm))
    anggota = [
        ["No", "Nama", "NIM"],
        ["1", "Syamil Imaddudin Sinan Erhaff", "240102125"],
        ["2", "Naufal Hafizh Wahdiyat", "240102090"],
        ["3", "Adithya Putra Pangestu CW", "240102003"],
        ["4", "Ahmad Ikhwal Fauzan", "240102010"],
    ]
    data = [[Paragraph(c, S_CELLB if i==0 else S_CELL) for c in row] for i, row in enumerate(anggota)]
    t = Table(data, colWidths=[1.2*cm, 9.3*cm, 3.5*cm], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    el.append(t)
    el.append(Spacer(1, 1.0*cm))

    # Universitas
    el.append(P("PROGRAM STUDI TEKNIK INFORMATIKA", style("c4", fontName=FONT_B, fontSize=14, alignment=TA_CENTER, textColor=PRIMARY_D)))
    el.append(P("FAKULTAS SAINS DAN TEKNOLOGI", style("c5", fontName=FONT_B, fontSize=13, alignment=TA_CENTER, textColor=PRIMARY_D)))
    el.append(P("UNIVERSITAS MUHAMMADIYAH BANDUNG", style("c6", fontName=FONT_B, fontSize=14, alignment=TA_CENTER, textColor=PRIMARY_D)))
    el.append(Spacer(1, 0.2*cm))
    el.append(P("2026", style("c7", fontName=FONT_B, fontSize=13, alignment=TA_CENTER, textColor=GREY)))
    return el

# ══════════════════════════════════════════════════════════
#  1. TOPIK
# ══════════════════════════════════════════════════════════
def bab_topik():
    el = [h1_box("1", "TOPIK"), Spacer(1, 0.4*cm)]
    el.append(P("<b>Topik Tugas Akhir:</b>", S_H2))
    el.append(P('"Perancangan dan Pembangunan Aplikasi Pengaduan Fasilitas Kampus Berbasis Mobile '
                'dengan Arsitektur Client-Server"'))
    el.append(Spacer(1, 0.2*cm))
    el.append(P("Aplikasi ini merupakan sebuah layanan digital yang memungkinkan mahasiswa dan civitas "
                "akademika untuk melaporkan berbagai permasalahan fasilitas kampus — seperti kerusakan "
                "lampu, pendingin ruangan (AC), kebersihan, keamanan, hingga sarana akademik — secara "
                "langsung melalui perangkat mobile. Laporan yang dikirim akan diterima oleh pihak "
                "administrator kampus dan diproses dengan alur status yang jelas, mulai dari "
                "<b>Menunggu</b>, <b>Diproses</b>, hingga <b>Selesai</b>."))
    el.append(Spacer(1, 0.3*cm))

    # Kotak ringkas
    ringkas = [
        [Paragraph("<b>Nama Aplikasi</b>", S_CELLB), Paragraph("Pengaduan Kampus", S_CELL)],
        [Paragraph("<b>Platform</b>", S_CELLB), Paragraph("Android (Mobile) — dibangun dengan Flutter", S_CELL)],
        [Paragraph("<b>Arsitektur</b>", S_CELLB), Paragraph("Client-Server (3-Tier Architecture)", S_CELL)],
        [Paragraph("<b>Teknologi</b>", S_CELLB), Paragraph("Flutter (client), Node.js + Express (server), MySQL (database)", S_CELL)],
        [Paragraph("<b>Pengguna</b>", S_CELLB), Paragraph("Mahasiswa (pelapor) dan Admin (pengelola)", S_CELL)],
        [Paragraph("<b>Fitur Utama</b>", S_CELLB), Paragraph("Login/Register, Buat Laporan + Foto, Riwayat, Detail & Status, Kelola Laporan (admin)", S_CELL)],
    ]
    t = Table(ringkas, colWidths=[3.5*cm, 13.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), LIGHT),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
    ]))
    el.append(t)
    return el

# ══════════════════════════════════════════════════════════
#  2. LATAR BELAKANG
# ══════════════════════════════════════════════════════════
def bab_latar():
    el = [h1_box("2", "LATAR BELAKANG"), Spacer(1, 0.4*cm)]
    par = [
        "Kampus merupakan lingkungan akademik yang menuntut tersedianya fasilitas yang layak dan "
        "berfungsi dengan baik untuk menunjang kegiatan belajar mengajar. Namun, dalam praktiknya, "
        "kerusakan atau ketidaklayakan fasilitas sering kali terjadi — mulai dari lampu kelas yang "
        "mati, AC yang tidak dingin, kebocoran, sampah yang menumpuk, hingga fasilitas keamanan yang "
        "kurang memadai. Permasalahan seperti ini jika dibiarkan akan mengganggu kenyamanan dan "
        "produktivitas seluruh civitas akademika.",

        "Selama ini, mekanisme pelaporan keluhan fasilitas di banyak kampus masih dilakukan secara "
        "konvensional, misalnya melalui penyampaian lisan kepada petugas, pencatatan di buku, atau "
        "penyampaian pesan melalui grup pesan instan. Cara-cara tersebut memiliki beberapa kelemahan: "
        "laporan mudah hilang atau terlewat, tidak ada rekam jejak (tracking) yang jelas mengenai "
        "status penanganan, sulitnya memantau laporan mana yang sudah ditindaklanjuti, serta tidak "
        "adanya data terpusat yang dapat digunakan pihak kampus untuk evaluasi.",

        "Perkembangan teknologi mobile memberikan peluang untuk mengatasi permasalahan tersebut. "
        "Hampir seluruh mahasiswa kini memiliki smartphone, sehingga sebuah aplikasi mobile menjadi "
        "media yang efektif dan mudah diakses untuk melaporkan keluhan fasilitas kapan saja dan di "
        "mana saja. Dengan aplikasi ini, mahasiswa dapat mengirim laporan beserta foto bukti secara "
        "cepat, sementara pihak pengelola kampus memperoleh data yang terstruktur dan dapat dipantau "
        "perkembangannya secara real-time.",

        "Oleh karena itu, pada tugas mata kuliah Pemrograman Perangkat Bergerak ini, penulis "
        "mengusulkan pembangunan sebuah aplikasi mobile bernama <b>Pengaduan Kampus</b>. Aplikasi ini "
        "dibangun dengan arsitektur client-server, di mana aplikasi mobile (client) berkomunikasi "
        "dengan sebuah server melalui REST API. Diharapkan aplikasi ini dapat menjadi solusi nyata "
        "dalam meningkatkan kualitas pelayanan dan pengelolaan fasilitas kampus, sekaligus menjadi "
        "sarana pembelajaran penerapan konsep client-server pada perangkat bergerak.",
    ]
    for p in par:
        el.append(P(p))
    return el

# ══════════════════════════════════════════════════════════
#  3. RUMUSAN MASALAH
# ══════════════════════════════════════════════════════════
def bab_rumusan():
    el = [h1_box("3", "RUMUSAN MASALAH"), Spacer(1, 0.4*cm)]
    el.append(P("Berdasarkan latar belakang di atas, dapat dirumuskan beberapa permasalahan sebagai berikut:"))
    items = [
        "Bagaimana merancang dan membangun aplikasi mobile yang dapat memudahkan mahasiswa dalam melaporkan keluhan fasilitas kampus secara cepat dan terdokumentasi?",
        "Bagaimana menerapkan arsitektur client-server sehingga aplikasi mobile (client) dapat berkomunikasi dengan server untuk mengirim dan mengambil data laporan?",
        "Bagaimana merancang sistem autentikasi dan hak akses yang membedakan peran antara mahasiswa sebagai pelapor dan admin sebagai pengelola laporan?",
        "Bagaimana membangun mekanisme pelaporan yang menyertakan bukti foto serta penelusuran status penanganan laporan (Menunggu, Diproses, Selesai)?",
        "Bagaimana merancang struktur basis data dan API yang mampu menyimpan serta mengelola data laporan secara terpusat dan terstruktur?",
    ]
    for i, it in enumerate(items, 1):
        el.append(Paragraph(f"{i}.&nbsp; {it}", S_BULLET))
    return el

# ══════════════════════════════════════════════════════════
#  4. TUJUAN
# ══════════════════════════════════════════════════════════
def bab_tujuan():
    el = [h1_box("4", "TUJUAN"), Spacer(1, 0.4*cm)]
    el.append(P("Adapun tujuan dari pembuatan aplikasi ini adalah:"))
    items = [
        "<b>Tujuan Umum:</b> Merancang dan membangun aplikasi mobile layanan pengaduan fasilitas kampus sebagai solusi digital untuk mempercepat dan mempermudah proses pelaporan keluhan di lingkungan kampus.",
        "<b>Menerapkan arsitektur client-server:</b> Membangun sistem di mana aplikasi mobile berkomunikasi dengan server melalui REST API sehingga data tersimpan terpusat.",
        "<b>Menyediakan sistem autentikasi &amp; hak akses:</b> Menerapkan login/register dengan token (JWT) serta pembedaan peran antara mahasiswa dan admin.",
        "<b>Memfasilitasi pelaporan berbasis bukti:</b> Memungkinkan mahasiswa mengirim laporan lengkap dengan kategori, lokasi, deskripsi, dan foto bukti.",
        "<b>Menyediakan penelusuran status:</b> Memberi kejelasan kepada pelapor mengenai status penanganan laporan secara transparan.",
        "<b>Memenuhi tugas mata kuliah:</b> Menjadi implementasi nyata dari materi Pemrograman Perangkat Bergerak, khususnya konsep koneksi server ke client.",
    ]
    for it in items:
        el.append(bullet(it))
    return el

# ══════════════════════════════════════════════════════════
#  5. METODE
# ══════════════════════════════════════════════════════════
def bab_metode():
    el = [h1_box("5", "METODE"), Spacer(1, 0.4*cm)]
    el.append(P("Metode pengembangan yang digunakan adalah <b>Waterfall (Sekuensial)</b>, yaitu pendekatan "
                "pengembangan perangkat lunak yang dilakukan secara bertahap dan berurutan. Metode ini dipilih "
                "karena alur pengerjaannya jelas dan sesuai untuk proyek berskala tugas kuliah. Tahapan-tahapannya "
                "adalah sebagai berikut:"))
    el.append(Spacer(1, 0.15*cm))
    tahap = [
        ["Tahap", "Kegiatan"],
        ["1. Analisis Kebutuhan", "Mengidentifikasi kebutuhan pengguna (mahasiswa & admin), fitur yang diperlukan, serta menentukan teknologi yang akan digunakan."],
        ["2. Perancangan (Design)", "Merancang arsitektur sistem client-server, struktur basis data (ERD), alur sistem, serta desain antarmuka (mockup UI) aplikasi mobile."],
        ["3. Implementasi", "Menulis kode program: membangun server REST API (Node.js + Express), basis data (MySQL), dan aplikasi mobile (Flutter)."],
        ["4. Pengujian (Testing)", "Menguji setiap endpoint API dan alur aplikasi, mulai dari login, pembuatan laporan, upload foto, hingga perubahan status oleh admin."],
        ["5. Pemeliharaan (Maintenance)", "Melakukan perbaikan bug, penyempurnaan fitur, dan dokumentasi agar aplikasi dapat dikembangkan lebih lanjut."],
    ]
    data = [[Paragraph(c, S_CELLB if i==0 else S_CELL) for c in row] for i, row in enumerate(tahap)]
    t = Table(data, colWidths=[4.0*cm, 13.0*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 9),
    ]))
    el.append(t)
    el.append(Spacer(1, 0.4*cm))
    el.append(P("<b>Teknologi yang Digunakan</b>", S_H2))
    tech = [
        ["Komponen", "Teknologi", "Keterangan"],
        ["Aplikasi Mobile (Client)", "Flutter (Dart)", "Framework cross-platform untuk membangun aplikasi Android."],
        ["Server (Backend)", "Node.js + Express", "Menyediakan REST API dan logika bisnis aplikasi."],
        ["Basis Data", "MySQL / MariaDB", "Menyimpan data pengguna dan laporan secara terpusat."],
        ["Autentikasi", "JWT + Bcrypt", "Token sesi login dan enkripsi (hash) password."],
        ["Upload File", "Multer", "Menangani unggahan foto bukti laporan."],
        ["Pengujian API", "cURL / Postman", "Menguji seluruh endpoint sebelum integrasi ke aplikasi."],
    ]
    data2 = [[Paragraph(c, S_CELLB if i==0 else S_CELL) for c in row] for i, row in enumerate(tech)]
    t2 = Table(data2, colWidths=[4.0*cm, 4.0*cm, 9.0*cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), SECONDARY),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 9),
    ]))
    el.append(t2)
    return el

# ══════════════════════════════════════════════════════════
#  6. ARSITEKTUR SISTEM
# ══════════════════════════════════════════════════════════
def bab_arsitektur():
    el = [h1_box("6", "ARSITEKTUR SISTEM"), Spacer(1, 0.4*cm)]
    el.append(P("Aplikasi ini dibangun menggunakan arsitektur <b>Client-Server</b> dengan pola "
                "<b>3-Tier Architecture</b>, yang terdiri dari tiga lapisan utama yang saling terhubung:"))
    el.append(Spacer(1, 0.15*cm))
    tier = [
        ["Lapisan", "Komponen", "Tugas"],
        ["Presentation Tier", "Aplikasi Mobile (Flutter)", "Menampilkan antarmuka kepada pengguna dan mengirim permintaan ke server."],
        ["Application Tier", "Server REST API (Node.js + Express)", "Memproses logika bisnis, autentikasi, validasi data, dan menjembatani client dengan database."],
        ["Data Tier", "Basis Data (MySQL)", "Menyimpan dan mengelola data pengguna serta data laporan secara permanen."],
    ]
    data = [[Paragraph(c, S_CELLB if i==0 else S_CELL) for c in row] for i, row in enumerate(tier)]
    t = Table(data, colWidths=[3.6*cm, 5.4*cm, 8.0*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 9),
    ]))
    el.append(t)
    el.append(Spacer(1, 0.5*cm))

    # Gambar arsitektur
    ars = os.path.join(MOCK, "07_arsitektur.png")
    if os.path.exists(ars):
        from PIL import Image as PILImage
        aw, ah = PILImage.open(ars).size
        aw_cm = 16.0
        el.append(Image(ars, width=aw_cm*cm, height=aw_cm*cm*ah/aw))
        el.append(P("Gambar 1. Diagram Arsitektur Sistem Client-Server", S_SMALL))
    el.append(PageBreak())

    el.append(P("<b>Penjelasan Alur Sistem</b>", S_H2))
    alur = [
        "Pengguna (mahasiswa atau admin) membuka aplikasi dan melakukan login. Server memverifikasi kredensial dan mengembalikan token JWT.",
        "Untuk membuat laporan, aplikasi mengirim data (judul, kategori, lokasi, deskripsi) beserta foto bukti ke server melalui endpoint REST API.",
        "Server memvalidasi token JWT terlebih dahulu melalui middleware. Jika valid, server memproses data dan menyimpannya ke basis data.",
        "Foto yang diunggah disimpan di server (folder <i>uploads</i>) dan nama filenya dicatat di basis data.",
        "Saat pengguna membuka daftar laporan, aplikasi meminta data ke server; server mengambil data dari MySQL dan mengirimkannya kembali dalam format JSON.",
        "Admin dapat mengubah status laporan (Menunggu → Diproses → Selesai); perubahan ini tersimpan di basis data dan langsung terlihat oleh pelapor.",
    ]
    for i, a in enumerate(alur, 1):
        el.append(Paragraph(f"{i}.&nbsp; {a}", S_BULLET))

    el.append(Spacer(1, 0.4*cm))
    el.append(P("<b>Rancangan Basis Data (ERD)</b>", S_H2))
    el.append(P("Basis data terdiri dari dua tabel utama dengan relasi satu-ke-banyak (1:N), yaitu satu "
                "pengguna dapat membuat banyak laporan."))
    el.append(Spacer(1, 0.15*cm))

    # Tabel users
    el.append(P("<b>Tabel: users</b>", style("t1", fontName=FONT_B, fontSize=11, textColor=PRIMARY)))
    users = [
        ["Field", "Tipe", "Keterangan"],
        ["id", "INT (PK, AI)", "Primary key, auto increment"],
        ["nama", "VARCHAR(100)", "Nama lengkap pengguna"],
        ["email", "VARCHAR(100) UNIQUE", "Email untuk login (unik)"],
        ["password", "VARCHAR(255)", "Password ter-hash dengan Bcrypt"],
        ["role", "ENUM", "Peran: 'mahasiswa' atau 'admin'"],
        ["nim", "VARCHAR(20)", "Nomor Induk Mahasiswa"],
        ["created_at", "TIMESTAMP", "Waktu pendaftaran akun"],
    ]
    du = [[Paragraph(c, S_CELLB if i==0 else S_CELL) for c in row] for i, row in enumerate(users)]
    tu = Table(du, colWidths=[3.5*cm, 4.5*cm, 9.0*cm])
    tu.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), SECONDARY),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 9),
    ]))
    el.append(tu)
    el.append(Spacer(1, 0.35*cm))

    el.append(P("<b>Tabel: pengaduan</b>", style("t2b", fontName=FONT_B, fontSize=11, textColor=PRIMARY)))
    peng = [
        ["Field", "Tipe", "Keterangan"],
        ["id", "INT (PK, AI)", "Primary key, auto increment"],
        ["user_id", "INT (FK)", "Relasi ke tabel users (pelapor)"],
        ["judul", "VARCHAR(150)", "Judul singkat laporan"],
        ["kategori", "VARCHAR(50)", "Fasilitas / Kebersihan / Keamanan / Akademik / Lainnya"],
        ["lokasi", "VARCHAR(150)", "Lokasi kejadian di kampus"],
        ["deskripsi", "TEXT", "Penjelasan rinci keluhan"],
        ["foto", "VARCHAR(255)", "Nama file foto bukti (di folder uploads)"],
        ["status", "ENUM", "Menunggu / Diproses / Selesai / Ditolak"],
        ["created_at", "TIMESTAMP", "Waktu laporan dibuat"],
    ]
    dp = [[Paragraph(c, S_CELLB if i==0 else S_CELL) for c in row] for i, row in enumerate(peng)]
    tp = Table(dp, colWidths=[3.5*cm, 4.5*cm, 9.0*cm])
    tp.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), SECONDARY),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 9),
    ]))
    el.append(tp)
    el.append(Spacer(1, 0.3*cm))
    el.append(P("<b>Relasi:</b> <font color='#1565C0'><b>users (1) ——&lt; pengaduan (N)</b></font> — "
                "satu pengguna (mahasiswa) dapat membuat banyak laporan pengaduan, sedangkan setiap "
                "laporan hanya dimiliki oleh satu pengguna.", S_BODY))
    return el

# ══════════════════════════════════════════════════════════
#  7. RENCANA
# ══════════════════════════════════════════════════════════
def bab_rencana():
    el = [h1_box("7", "RENCANA"), Spacer(1, 0.4*cm)]
    el.append(P("Berikut adalah rencana pelaksanaan (timeline) pembangunan aplikasi Pengaduan Kampus "
                "yang disusun dalam beberapa tahapan:"))
    el.append(Spacer(1, 0.15*cm))
    rencana = [
        ["Pertemuan", "Tahapan", "Target / Output"],
        ["Minggu 1", "Analisis kebutuhan & studi pustaka", "Daftar kebutuhan sistem dan teknologi yang dipilih."],
        ["Minggu 2", "Perancangan sistem", "Arsitektur client-server, ERD, dan mockup UI mobile."],
        ["Minggu 3", "Pembangunan Backend & Database", "REST API (auth & pengaduan) berjalan, basis data MySQL siap, diuji dengan cURL."],
        ["Minggu 4", "Pembangunan aplikasi mobile", "Aplikasi Flutter: halaman login, register, home, buat laporan, detail."],
        ["Minggu 5", "Integrasi & Pengujian", "Aplikasi terhubung dengan server, seluruh fitur diuji end-to-end."],
        ["Minggu 6", "Penyempurnaan & Dokumentasi", "Perbaikan bug, penyusunan laporan tugas, dan presentasi."],
    ]
    data = [[Paragraph(c, S_CELLB if i==0 else S_CELL) for c in row] for i, row in enumerate(rencana)]
    t = Table(data, colWidths=[2.6*cm, 6.0*cm, 8.4*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 9),
    ]))
    el.append(t)
    el.append(Spacer(1, 0.4*cm))
    el.append(P("<b>Rencana Pengembangan Selanjutnya (Future Work)</b>", S_H2))
    for it in [
        "Menambahkan notifikasi (push notification) ketika status laporan berubah.",
        "Menambahkan fitur peta lokasi (maps) untuk menandai titik kerusakan fasilitas.",
        "Menambahkan fitur komentar/balasan antara admin dan pelapor.",
        "Menambahkan dashboard statistik laporan untuk pihak pengelola kampus.",
        "Menambahkan fitur pencarian dan filter lanjutan pada daftar laporan.",
    ]:
        el.append(bullet(it))
    return el

# ══════════════════════════════════════════════════════════
#  8. MOCKUP UI MOBILE
# ══════════════════════════════════════════════════════════
def bab_mockup():
    el = [h1_box("8", "MOCKUP UI MOBILE"), Spacer(1, 0.4*cm)]
    el.append(P("Berikut adalah rancangan antarmuka (mockup) aplikasi mobile Pengaduan Kampus. "
                "Aplikasi terdiri dari enam halaman utama yang dirancang dengan tema warna biru "
                "yang bersih, modern, dan mudah digunakan."))
    el.append(Spacer(1, 0.3*cm))

    # Grid semua mockup
    grid = os.path.join(MOCK, "09_mockup_grid.png")
    if os.path.exists(grid):
        from PIL import Image as PILImage
        gw, gh = PILImage.open(grid).size
        gw_cm = 14.0
        el.append(Image(grid, width=gw_cm*cm, height=gw_cm*cm*gh/gw))
        el.append(P("Gambar 2. Mockup Antarmuka Aplikasi Pengaduan Kampus", S_SMALL))
    el.append(PageBreak())

    # Penjelasan tiap halaman
    el.append(P("<b>Penjelasan Setiap Halaman</b>", S_H2))
    el.append(Spacer(1, 0.1*cm))
    hal = [
        ["No", "Halaman", "Fungsi"],
        ["1", "Splash Screen", "Halaman pembuka yang menampilkan logo aplikasi saat pertama kali dibuka, sekaligus memeriksa status login pengguna."],
        ["2", "Login", "Halaman untuk masuk menggunakan email dan password. Terdapat tautan menuju halaman pendaftaran."],
        ["3", "Register", "Halaman pendaftaran akun baru bagi mahasiswa dengan mengisi nama, NIM, email, dan password."],
        ["4", "Home / Daftar Laporan", "Menampilkan daftar laporan yang pernah dibuat, lengkap dengan filter status dan tombol untuk membuat laporan baru."],
        ["5", "Buat Laporan", "Form untuk membuat laporan baru: judul, kategori, lokasi, deskripsi, dan unggah foto bukti."],
        ["6", "Detail Laporan", "Menampilkan rincian satu laporan beserta status penanganannya. Admin dapat mengubah status dari halaman ini."],
    ]
    data = [[Paragraph(c, S_CELLB if i==0 else S_CELL) for c in row] for i, row in enumerate(hal)]
    t = Table(data, colWidths=[1.0*cm, 4.2*cm, 11.8*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 9),
    ]))
    el.append(t)
    el.append(Spacer(1, 0.4*cm))

    # Mockup besar tiap layar (2 per baris)
    el.append(P("<b>Tampilan Detail Setiap Halaman</b>", S_H2))
    pairs = [
        ("01_splash.png", "Splash Screen", "02_login.png", "Login"),
        ("03_register.png", "Register", "04_home.png", "Home / Daftar Laporan"),
        ("05_buat_laporan.png", "Buat Laporan", "06_detail.png", "Detail Laporan"),
    ]
    for f1, l1, f2, l2 in pairs:
        p1 = os.path.join(MOCK, f1); p2 = os.path.join(MOCK, f2)
        imgs = []
        for p in (p1, p2):
            if os.path.exists(p):
                imgs.append(Image(p, width=5.6*cm, height=5.6*cm*844/390))
            else:
                imgs.append(Spacer(5.6*cm, 1))
        row = Table([[imgs[0], imgs[1]]], colWidths=[8.2*cm, 8.2*cm], hAlign="CENTER")
        row.setStyle(TableStyle([("ALIGN",(0,0),(-1,-1),"CENTER"), ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        el.append(row)
        cap = Table([[Paragraph(l1, S_SMALL), Paragraph(l2, S_SMALL)]],
                    colWidths=[8.2*cm, 8.2*cm], hAlign="CENTER")
        cap.setStyle(TableStyle([("ALIGN",(0,0),(-1,-1),"CENTER")]))
        el.append(cap)
        el.append(Spacer(1, 0.35*cm))
    return el

# ══════════════════════════════════════════════════════════
#  BUILD
# ══════════════════════════════════════════════════════════
def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(2.2*cm, 1.6*cm, A4[0]-2.2*cm, 1.6*cm)
    canvas.setFont(FONT, 9)
    canvas.setFillColor(GREY)
    canvas.drawString(2.2*cm, 1.15*cm, "Aplikasi Pengaduan Fasilitas Kampus — Pemrograman Perangkat Bergerak")
    canvas.drawRightString(A4[0]-2.2*cm, 1.15*cm, f"Halaman {doc.page}")
    canvas.restoreState()

def build():
    out = os.path.join(BASE, "Laporan_Tugas_Pengaduan_Kampus.pdf")
    doc = BaseDocTemplate(out, pagesize=A4,
                          leftMargin=2.2*cm, rightMargin=2.2*cm,
                          topMargin=2.0*cm, bottomMargin=2.2*cm,
                          title="Laporan Tugas - Aplikasi Pengaduan Fasilitas Kampus")
    frame_cover = Frame(2.2*cm, 2.2*cm, A4[0]-4.4*cm, A4[1]-4.4*cm, id="cover")
    frame_body  = Frame(2.2*cm, 2.2*cm, A4[0]-4.4*cm, A4[1]-4.2*cm, id="body")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame_cover]),
        PageTemplate(id="body", frames=[frame_body], onPage=footer),
    ])

    story = []
    story += cover()
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())
    story += bab_topik()
    story.append(PageBreak())
    story += bab_latar()
    story.append(PageBreak())
    story += bab_rumusan()
    story.append(PageBreak())
    story += bab_tujuan()
    story.append(PageBreak())
    story += bab_metode()
    story.append(PageBreak())
    story += bab_arsitektur()
    story.append(PageBreak())
    story += bab_rencana()
    story.append(PageBreak())
    story += bab_mockup()

    doc.build(story)
    print("PDF dibuat:", out, os.path.getsize(out), "bytes")

if __name__ == "__main__":
    build()
