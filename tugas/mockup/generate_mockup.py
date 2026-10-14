# -*- coding: utf-8 -*-
"""
Generator Mockup UI Mobile - Aplikasi Pengaduan Fasilitas Kampus
Menghasilkan 6 gambar PNG layar aplikasi (390x844 px) + 1 banner.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))

# ── Warna tema (sama dengan aplikasi Flutter) ──
PRIMARY   = (21, 101, 192)     # #1565C0
PRIMARY_D = (13, 71, 161)      # #0D47A1
SECONDARY = (38, 166, 154)     # #26A69A
BG        = (245, 247, 250)    # #F5F7FA
WHITE     = (255, 255, 255)
TEXT      = (33, 33, 33)
TEXT_GREY = (117, 117, 117)
BORDER    = (224, 224, 224)
ORANGE    = (255, 152, 0)
GREEN     = (76, 175, 80)
RED       = (244, 67, 54)
BLUE_LT   = (33, 150, 243)

W, H = 390, 844

# ── Font ──
def F(size, bold=False):
    cands = []
    if bold:
        cands = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/calibrib.ttf"]
    else:
        cands = ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf"]
    for c in cands:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def draw_megaphone(d, cx, cy, scale=1.0, color=PRIMARY, dot=WHITE):
    """Ikon balon percakapan (aspirasi/keluhan) yang bersih dan rapi."""
    s = scale
    w, h = 46 * s, 38 * s
    top = cy - h / 2 - 3 * s
    bot = cy + h / 2 - 3 * s
    # Badan balon (rounded rectangle)
    d.rounded_rectangle([cx - w/2, top, cx + w/2, bot], radius=11 * s, fill=color)
    # Ekor balon (segitiga di kiri bawah)
    d.polygon([(cx - 12*s, bot - 6*s),
               (cx + 2*s, bot - 6*s),
               (cx - 14*s, bot + 14*s)], fill=color)
    # Titik-titik di dalam balon
    r = 3.2 * s
    for dx in (-12*s, 0, 12*s):
        d.ellipse([cx + dx - r, cy - 3*s - r, cx + dx + r, cy - 3*s + r], fill=dot)

def draw_doc(d, cx, cy, scale=1.0, color=PRIMARY):
    """Ikon dokumen/laporan (persegi panjang dengan garis)."""
    s = scale
    w, h = 18*s, 24*s
    d.rounded_rectangle([cx - w/2, cy - h/2, cx + w/2, cy + h/2], radius=3*s,
                        outline=color, width=max(2, int(2.5*s)))
    for i in range(3):
        yy = cy - 6*s + i * 7*s
        d.line([cx - w/2 + 5*s, yy, cx + w/2 - 5*s, yy], fill=color, width=max(2, int(2*s)))

def draw_camera(d, cx, cy, scale=1.0, color=PRIMARY):
    """Ikon kamera."""
    s = scale
    d.rounded_rectangle([cx - 26*s, cy - 16*s, cx + 26*s, cy + 18*s], radius=6*s,
                        outline=color, width=max(2, int(3*s)))
    d.polygon([(cx - 10*s, cy - 16*s), (cx - 6*s, cy - 24*s),
               (cx + 6*s, cy - 24*s), (cx + 10*s, cy - 16*s)], fill=color)
    d.ellipse([cx - 11*s, cy - 9*s, cx + 11*s, cy + 13*s], outline=color, width=max(2, int(3*s)))
    d.ellipse([cx - 5*s, cy - 3*s, cx + 5*s, cy + 7*s], fill=color)

def draw_photo(d, cx, cy, scale=1.0, color=PRIMARY):
    """Ikon gambar/foto (gunung + matahari)."""
    s = scale
    d.rounded_rectangle([cx - 30*s, cy - 22*s, cx + 30*s, cy + 22*s], radius=5*s,
                        outline=color, width=max(2, int(3*s)))
    d.ellipse([cx - 18*s, cy - 14*s, cx - 6*s, cy - 2*s], fill=color)
    d.polygon([(cx - 26*s, cy + 18*s), (cx - 6*s, cy - 6*s),
               (cx + 8*s, cy + 8*s), (cx + 16*s, cy - 2*s), (cx + 26*s, cy + 18*s)], fill=color)

def text(d, xy, s, font, fill=TEXT, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)

def new_screen():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)

def status_bar(d):
    """Status bar palsu di atas."""
    text(d, (24, 14), "9:41", F(15, True), TEXT)
    # sinyal, wifi, baterai (ikon sederhana)
    x = W - 90
    for i in range(4):
        h = 6 + i * 4
        d.rectangle([x + i * 7, 26 - h, x + i * 7 + 4, 26], fill=TEXT)
    d.rectangle([x + 36, 16, x + 52, 26], outline=TEXT, width=2)
    d.rectangle([x + 38, 18, x + 46, 24], fill=TEXT)
    d.rectangle([x + 53, 19, x + 55, 23], fill=TEXT)

def appbar(d, title, back=False):
    d.rectangle([0, 44, W, 100], fill=PRIMARY)
    if back:
        text(d, (24, 72), "\u2190", F(26, True), WHITE, anchor="lm")
    text(d, (W // 2, 72), title, F(18, True), WHITE, anchor="mm")

def field(d, y, label, value="", password=False, h=52):
    text(d, (28, y - 22), label, F(12, True), TEXT_GREY)
    rrect(d, [24, y, W - 24, y + h], 10, fill=WHITE, outline=BORDER, width=1)
    if value:
        v = "\u2022" * len(value) if password else value
        text(d, (40, y + h // 2), v, F(15), TEXT if value else TEXT_GREY, anchor="lm")
    else:
        text(d, (40, y + h // 2), "Masukkan " + label.lower(), F(14), (170, 170, 170), anchor="lm")

def button(d, y, label, color=PRIMARY, h=54):
    rrect(d, [24, y, W - 24, y + h], 12, fill=color)
    text(d, (W // 2, y + h // 2), label, F(16, True), WHITE, anchor="mm")

def badge(d, x, y, label, color):
    f = F(12, True)
    tw = d.textlength(label, font=f)
    rrect(d, [x, y, x + tw + 24, y + 26], 13, fill=color)
    text(d, (x + 12, y + 13), label, f, WHITE, anchor="lm")

# ══════════════════════════════════════════════════════════
# 1. SPLASH SCREEN
# ══════════════════════════════════════════════════════════
def splash():
    img = Image.new("RGB", (W, H), PRIMARY)
    d = ImageDraw.Draw(img)
    status_bar_white(d)
    # Logo bulat
    cx, cy = W // 2, 330
    d.ellipse([cx - 55, cy - 55, cx + 55, cy + 55], fill=WHITE)
    draw_megaphone(d, cx - 4, cy, scale=1.1, color=PRIMARY)
    text(d, (cx, 430), "Pengaduan Kampus", F(26, True), WHITE, anchor="mm")
    text(d, (cx, 466), "Layanan Aspirasi & Keluhan Fasilitas", F(13), (200, 220, 245), anchor="mm")
    # loading dots
    for i in range(3):
        d.ellipse([cx - 24 + i * 22, 760, cx - 12 + i * 22, 772], fill=WHITE)
    text(d, (cx, 800), "Memuat...", F(12), (200, 220, 245), anchor="mm")
    img.save(f"{OUT}/01_splash.png")
    return img

def status_bar_white(d):
    text(d, (24, 14), "9:41", F(15, True), WHITE)
    x = W - 90
    for i in range(4):
        h = 6 + i * 4
        d.rectangle([x + i * 7, 26 - h, x + i * 7 + 4, 26], fill=WHITE)
    d.rectangle([x + 36, 16, x + 52, 26], outline=WHITE, width=2)
    d.rectangle([x + 38, 18, x + 46, 24], fill=WHITE)

# ══════════════════════════════════════════════════════════
# 2. LOGIN SCREEN
# ══════════════════════════════════════════════════════════
def login():
    img, d = new_screen()
    status_bar(d)
    # header
    d.rectangle([0, 0, W, 300], fill=PRIMARY)
    d.ellipse([W // 2 - 40, 90, W // 2 + 40, 170], fill=WHITE)
    draw_megaphone(d, W // 2 - 3, 130, scale=0.85, color=PRIMARY)
    text(d, (W // 2, 205), "Selamat Datang", F(24, True), WHITE, anchor="mm")
    text(d, (W // 2, 238), "Masuk untuk melanjutkan", F(13), (200, 220, 245), anchor="mm")
    # card
    rrect(d, [20, 270, W - 20, 620], 20, fill=WHITE)
    field(d, 320, "Email", "naufal@mhs.ac.id")
    field(d, 410, "Password", "123456", password=True)
    text(d, (W - 28, 485), "Lupa password?", F(12, True), PRIMARY, anchor="ra")
    button(d, 520, "MASUK")
    text(d, (W // 2, 640), "Belum punya akun?", F(13), TEXT_GREY, anchor="mm")
    text(d, (W // 2, 668), "Daftar Sekarang", F(14, True), PRIMARY, anchor="mm")
    img.save(f"{OUT}/02_login.png")
    return img

# ══════════════════════════════════════════════════════════
# 3. REGISTER SCREEN
# ══════════════════════════════════════════════════════════
def register():
    img, d = new_screen()
    status_bar(d)
    appbar(d, "Daftar Akun", back=True)
    y = 130
    field(d, y, "Nama Lengkap", "Naufal Hafizh Wahdiyat"); y += 88
    field(d, y, "NIM", "240102090"); y += 88
    field(d, y, "Email", "naufal@mhs.ac.id"); y += 88
    field(d, y, "Password", "123456", password=True); y += 88
    button(d, y + 10, "DAFTAR")
    text(d, (W // 2, y + 100), "Sudah punya akun?  Masuk", F(13), TEXT_GREY, anchor="mm")
    img.save(f"{OUT}/03_register.png")
    return img

# ══════════════════════════════════════════════════════════
# 4. HOME SCREEN (daftar laporan)
# ══════════════════════════════════════════════════════════
def home():
    img, d = new_screen()
    status_bar(d)
    appbar(d, "Pengaduan Kampus")
    # sapaan
    text(d, (24, 116), "Halo, Naufal", F(18, True), TEXT)
    text(d, (24, 142), "Ada keluhan fasilitas hari ini?", F(13), TEXT_GREY)
    # filter chips
    chips = [("Semua", True), ("Menunggu", False), ("Diproses", False), ("Selesai", False)]
    x = 24
    for label, active in chips:
        f = F(12, True)
        tw = d.textlength(label, font=f)
        rrect(d, [x, 175, x + tw + 28, 205], 15, fill=PRIMARY if active else WHITE,
              outline=None if active else BORDER, width=1)
        text(d, (x + 14, 190), label, f, WHITE if active else TEXT_GREY, anchor="lm")
        x += tw + 38
    # kartu laporan
    cards = [
        ("Lampu Kelas Rusak", "Fasilitas", "Gedung A - Ruang 201", "Menunggu", ORANGE),
        ("AC Lab Komputer Mati", "Fasilitas", "Gedung B - Lab 3", "Diproses", BLUE_LT),
        ("Sampah Toilet Menumpuk", "Kebersihan", "Gedung C - Lantai 2", "Selesai", GREEN),
    ]
    y = 225
    for judul, kat, lok, st, col in cards:
        rrect(d, [20, y, W - 20, y + 130], 16, fill=WHITE)
        # ikon kategori
        rrect(d, [34, y + 18, 78, y + 62], 10, fill=(230, 240, 252))
        draw_doc(d, 56, y + 40, scale=0.75, color=PRIMARY)
        text(d, (92, y + 28), judul, F(15, True), TEXT)
        text(d, (92, y + 52), kat + "  \u2022  " + lok, F(11), TEXT_GREY)
        # garis
        d.line([34, y + 78, W - 34, y + 78], fill=(240, 240, 240), width=1)
        text(d, (92, y + 100), "Dilaporkan 2 jam lalu", F(11), (150, 150, 150))
        badge(d, W - 130, y + 90, st, col)
        y += 145
    # FAB
    d.ellipse([W - 96, H - 110, W - 24, H - 38], fill=PRIMARY)
    text(d, (W - 60, H - 74), "+", F(36, True), WHITE, anchor="mm")
    img.save(f"{OUT}/04_home.png")
    return img

# ══════════════════════════════════════════════════════════
# 5. BUAT LAPORAN SCREEN
# ══════════════════════════════════════════════════════════
def buat():
    img, d = new_screen()
    status_bar(d)
    appbar(d, "Buat Laporan", back=True)
    y = 120
    field(d, y, "Judul Laporan", "Lampu Kelas Rusak"); y += 82
    # kategori dropdown
    text(d, (28, y - 22), "Kategori", F(12, True), TEXT_GREY)
    rrect(d, [24, y, W - 24, y + 52], 10, fill=WHITE, outline=BORDER, width=1)
    text(d, (40, y + 26), "Fasilitas", F(15), TEXT, anchor="lm")
    text(d, (W - 40, y + 26), "\u25BE", F(14), TEXT_GREY, anchor="mm")
    y += 82
    field(d, y, "Lokasi", "Gedung A - Ruang 201"); y += 82
    # deskripsi
    text(d, (28, y - 22), "Deskripsi", F(12, True), TEXT_GREY)
    rrect(d, [24, y, W - 24, y + 90], 10, fill=WHITE, outline=BORDER, width=1)
    text(d, (40, y + 20), "Lampu di ruang 201 mati sejak", F(13), TEXT)
    text(d, (40, y + 42), "kemarin, mengganggu kegiatan", F(13), TEXT)
    text(d, (40, y + 64), "belajar mengajar...", F(13), TEXT)
    y += 118
    # upload foto
    text(d, (28, y - 22), "Foto Bukti", F(12, True), TEXT_GREY)
    rrect(d, [24, y, W - 24, y + 120], 12, fill=(240, 244, 248), outline=BORDER, width=1)
    draw_camera(d, W // 2, y + 50, scale=0.85, color=PRIMARY)
    text(d, (W // 2, y + 92), "Ketuk untuk pilih foto", F(12), TEXT_GREY, anchor="mm")
    y += 140
    button(d, y, "KIRIM LAPORAN", SECONDARY)
    img.save(f"{OUT}/05_buat_laporan.png")
    return img

# ══════════════════════════════════════════════════════════
# 6. DETAIL SCREEN
# ══════════════════════════════════════════════════════════
def detail():
    img, d = new_screen()
    status_bar(d)
    appbar(d, "Detail Laporan", back=True)
    # foto
    rrect(d, [20, 116, W - 20, 300], 16, fill=(210, 225, 240))
    draw_photo(d, W // 2, 195, scale=0.9, color=PRIMARY)
    text(d, (W // 2, 268), "Foto Bukti Laporan", F(12), TEXT_GREY, anchor="mm")
    # info
    y = 320
    text(d, (24, y), "Lampu Kelas Rusak", F(20, True), TEXT)
    badge(d, 24, y + 34, "Menunggu", ORANGE)
    # detail box
    rrect(d, [20, y + 80, W - 20, y + 300], 16, fill=WHITE)
    rows = [("Kategori", "Fasilitas"), ("Lokasi", "Gedung A - Ruang 201"),
            ("Pelapor", "Naufal Hafizh"), ("Tanggal", "13 Okt 2026")]
    yy = y + 104
    for k, v in rows:
        text(d, (40, yy), k, F(13), TEXT_GREY)
        text(d, (W - 40, yy), v, F(13, True), TEXT, anchor="ra")
        yy += 40
    # deskripsi
    text(d, (24, y + 320), "Deskripsi", F(14, True), TEXT)
    rrect(d, [20, y + 348, W - 20, y + 448], 12, fill=WHITE)
    text(d, (40, y + 368), "Lampu di ruang 201 mati sejak kemarin,", F(12), TEXT)
    text(d, (40, y + 390), "sangat mengganggu kegiatan belajar", F(12), TEXT)
    text(d, (40, y + 412), "mengajar di kelas.", F(12), TEXT)
    # timeline status
    text(d, (24, y + 470), "Status Penanganan", F(14, True), TEXT)
    steps = [("Laporan diterima", GREEN, True), ("Sedang diproses", (200, 200, 200), False),
             ("Selesai", (200, 200, 200), False)]
    yy = y + 500
    for label, col, done in steps:
        d.ellipse([28, yy, 46, yy + 18], fill=col if done else WHITE, outline=col, width=2)
        if done:
            text(d, (37, yy + 9), "\u2713", F(11, True), WHITE, anchor="mm")
        text(d, (58, yy + 9), label, F(12, True) if done else F(12), TEXT if done else TEXT_GREY, anchor="lm")
        yy += 32
    img.save(f"{OUT}/06_detail.png")
    return img

if __name__ == "__main__":
    splash(); login(); register(); home(); buat(); detail()
    print("Mockup selesai dibuat:")
    for f in sorted(os.listdir(OUT)):
        if f.endswith(".png"):
            print("  -", f, os.path.getsize(os.path.join(OUT, f)), "bytes")
