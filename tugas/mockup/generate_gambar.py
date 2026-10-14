# -*- coding: utf-8 -*-
"""
Generator gambar pendukung:
 - 07_arsitektur.png  : diagram arsitektur sistem (client-server)
 - 08_logo.png        : logo aplikasi
 - 09_mockup_grid.png : gabungan 6 mockup dalam satu gambar
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))

PRIMARY   = (21, 101, 192)
PRIMARY_D = (13, 71, 161)
SECONDARY = (38, 166, 154)
ACCENT    = (255, 152, 0)
BG        = (245, 247, 250)
WHITE     = (255, 255, 255)
TEXT      = (33, 33, 33)
TEXT_GREY = (117, 117, 117)
BORDER    = (200, 212, 224)
GREEN     = (76, 175, 80)
PURPLE    = (123, 31, 162)

def F(size, bold=False):
    cands = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"] if bold \
        else ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
    for c in cands:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def text(d, xy, s, font, fill=TEXT, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)

def arrow(d, x1, y1, x2, y2, color=TEXT_GREY, w=3):
    d.line([x1, y1, x2, y2], fill=color, width=w)
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    L = 12
    d.polygon([(x2, y2),
               (x2 - L*math.cos(ang - 0.4), y2 - L*math.sin(ang - 0.4)),
               (x2 - L*math.cos(ang + 0.4), y2 - L*math.sin(ang + 0.4))], fill=color)

# ══════════════════════════════════════════════════════════
# 7. DIAGRAM ARSITEKTUR
# ══════════════════════════════════════════════════════════
def arsitektur():
    W, H = 1400, 900
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    text(d, (W//2, 40), "Arsitektur Sistem Aplikasi Pengaduan Kampus", F(34, True), PRIMARY_D, anchor="mm")
    text(d, (W//2, 82), "Model Client-Server (3-Tier Architecture)", F(19), TEXT_GREY, anchor="mm")

    # ── Tier 1: Client (Mobile) ──
    cx1, cy1, w1, h1 = 230, 320, 300, 450
    d.rounded_rectangle([cx1-w1//2, cy1-h1//2, cx1+w1//2, cy1+h1//2], radius=18,
                        fill=(230, 240, 252), outline=PRIMARY, width=3)
    text(d, (cx1, cy1-h1//2+38), "CLIENT", F(22, True), PRIMARY, anchor="mm")
    text(d, (cx1, cy1-h1//2+70), "Aplikasi Mobile (Flutter)", F(15, True), TEXT, anchor="mm")
    # HP icon
    d.rounded_rectangle([cx1-42, cy1-70, cx1+42, cy1+55], radius=10, fill=WHITE, outline=PRIMARY, width=3)
    d.rectangle([cx1-30, cy1-52, cx1+30, cy1+35], fill=(235, 244, 255))
    d.ellipse([cx1-6, cy1+40, cx1+6, cy1+50], fill=PRIMARY)
    items = ["• Login & Register", "• Buat Laporan + Foto", "• Riwayat & Status", "• Detail Laporan"]
    yy = cy1 + 95
    for it in items:
        text(d, (cx1-w1//2+30, yy), it, F(14), TEXT)
        yy += 30

    # ── Tier 2: Server (Node.js) ──
    cx2, cy2, w2, h2 = 700, 320, 340, 450
    d.rounded_rectangle([cx2-w2//2, cy2-h2//2, cx2+w2//2, cy2+h2//2], radius=18,
                        fill=(232, 245, 243), outline=SECONDARY, width=3)
    text(d, (cx2, cy2-h2//2+38), "SERVER / API", F(22, True), SECONDARY, anchor="mm")
    text(d, (cx2, cy2-h2//2+70), "Node.js + Express", F(15, True), TEXT, anchor="mm")
    # server icon
    d.rounded_rectangle([cx2-52, cy2-55, cx2+52, cy2-18], radius=6, fill=WHITE, outline=SECONDARY, width=3)
    d.rounded_rectangle([cx2-52, cy2-10, cx2+52, cy2+27], radius=6, fill=WHITE, outline=SECONDARY, width=3)
    for yy2 in (cy2-36, cy2+8):
        d.ellipse([cx2-42, yy2-5, cx2-32, yy2+5], fill=GREEN)
        d.line([cx2-24, yy2, cx2+42, yy2], fill=(180, 190, 200), width=3)
    items2 = ["• REST API (JSON)", "• Autentikasi JWT", "• Bcrypt (hash pass)", "• Upload Foto (Multer)", "• Middleware Auth/Admin"]
    yy = cy2 + 70
    for it in items2:
        text(d, (cx2-w2//2+28, yy), it, F(14), TEXT)
        yy += 29

    # ── Tier 3: Database ──
    cx3, cy3, w3, h3 = 1150, 320, 300, 450
    d.rounded_rectangle([cx3-w3//2, cy3-h3//2, cx3+w3//2, cy3+h3//2], radius=18,
                        fill=(248, 240, 252), outline=PURPLE, width=3)
    text(d, (cx3, cy3-h3//2+38), "DATABASE", F(22, True), PURPLE, anchor="mm")
    text(d, (cx3, cy3-h3//2+70), "MySQL / MariaDB", F(15, True), TEXT, anchor="mm")
    # db icon (silinder)
    for i, yy2 in enumerate([cy3-50, cy3-10, cy3+30]):
        d.ellipse([cx3-55, yy2-14, cx3+55, yy2+14], fill=WHITE, outline=PURPLE, width=3)
    d.rectangle([cx3-55, cy3-50, cx3+55, cy3+30], fill=None)
    d.ellipse([cx3-55, cy3-50-14, cx3+55, cy3-50+14], fill=WHITE, outline=PURPLE, width=3)
    items3 = ["• Tabel: users", "• Tabel: pengaduan", "• Relasi 1 : N", "• role: mahasiswa/admin"]
    yy = cy3 + 95
    for it in items3:
        text(d, (cx3-w3//2+30, yy), it, F(14), TEXT)
        yy += 30

    # ── Panah antar tier ──
    arrow(d, cx1+w1//2+8, cy1-40, cx2-w2//2-8, cy2-40, PRIMARY, 4)
    text(d, ((cx1+w1//2+cx2-w2//2)//2, cy1-78), "HTTP Request", F(14, True), PRIMARY, anchor="mm")
    text(d, ((cx1+w1//2+cx2-w2//2)//2, cy1-56), "(JSON + JWT)", F(12), TEXT_GREY, anchor="mm")

    arrow(d, cx2-w2//2-8, cy2+40, cx1+w1//2+8, cy1+40, SECONDARY, 4)
    text(d, ((cx1+w1//2+cx2-w2//2)//2, cy1+62), "HTTP Response", F(14, True), SECONDARY, anchor="mm")

    arrow(d, cx2+w2//2+8, cy2-40, cx3-w3//2-8, cy3-40, PURPLE, 4)
    text(d, ((cx2+w2//2+cx3-w3//2)//2, cy2-78), "SQL Query", F(14, True), PURPLE, anchor="mm")

    arrow(d, cx3-w3//2-8, cy3+40, cx2+w2//2+8, cy2+40, GREEN, 4)
    text(d, ((cx2+w2//2+cx3-w3//2)//2, cy3+62), "Data", F(14, True), GREEN, anchor="mm")

    # ── Keterangan bawah ──
    d.rounded_rectangle([60, 590, W-60, 860], radius=14, fill=BG, outline=BORDER, width=2)
    text(d, (90, 620), "Keterangan Alur:", F(18, True), PRIMARY_D)
    lines = [
        "1.  Pengguna (mahasiswa/admin) membuka aplikasi Flutter dan melakukan login.",
        "2.  Aplikasi mengirim HTTP Request berisi JSON ke REST API (Node.js + Express).",
        "3.  Server memverifikasi token JWT, lalu memproses logika bisnis dan validasi data.",
        "4.  Server menjalankan SQL Query ke database MySQL untuk menyimpan/mengambil data.",
        "5.  Database mengembalikan data, server mengirim HTTP Response (JSON) ke aplikasi.",
        "6.  Aplikasi menampilkan data (daftar laporan, status, detail) kepada pengguna.",
    ]
    yy = 660
    for ln in lines:
        text(d, (90, yy), ln, F(15), TEXT)
        yy += 32

    img.save(f"{OUT}/07_arsitektur.png")
    print("07_arsitektur.png", os.path.getsize(f"{OUT}/07_arsitektur.png"))

# ══════════════════════════════════════════════════════════
# 8. LOGO
# ══════════════════════════════════════════════════════════
def logo():
    S = 600
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # cincin putih luar (agar terbaca di latar biru maupun putih)
    d.ellipse([22, 22, S-22, S-22], fill=WHITE)
    # lingkaran biru
    d.ellipse([40, 40, S-40, S-40], fill=PRIMARY)
    d.ellipse([80, 80, S-80, S-80], fill=(30, 120, 210))
    # balon percakapan putih
    cx, cy = S//2, S//2 - 20
    w, h = 260, 210
    d.rounded_rectangle([cx-w//2, cy-h//2, cx+w//2, cy+h//2], radius=60, fill=WHITE)
    d.polygon([(cx-60, cy+h//2-20), (cx+20, cy+h//2-20), (cx-70, cy+h//2+80)], fill=WHITE)
    # titik
    for dx in (-70, 0, 70):
        d.ellipse([cx+dx-22, cy-22, cx+dx+22, cy+22], fill=PRIMARY)
    text(d, (cx, S-130), "Pengaduan", F(46, True), WHITE, anchor="mm")
    text(d, (cx, S-80), "Kampus", F(46, True), WHITE, anchor="mm")
    img.save(f"{OUT}/08_logo.png")
    print("08_logo.png", os.path.getsize(f"{OUT}/08_logo.png"))

# ══════════════════════════════════════════════════════════
# 9. MOCKUP GRID (gabungan 6 layar)
# ══════════════════════════════════════════════════════════
def grid():
    files = ["01_splash.png", "02_login.png", "03_register.png",
             "04_home.png", "05_buat_laporan.png", "06_detail.png"]
    labels = ["1. Splash Screen", "2. Login", "3. Register",
              "4. Home / Daftar", "5. Buat Laporan", "6. Detail Laporan"]
    imgs = [Image.open(f"{OUT}/{f}") for f in files]
    # skala tiap layar
    tw = 340
    th = int(tw * 844 / 390)
    imgs = [im.resize((tw, th)) for im in imgs]

    pad = 30
    cols = 3
    rows = 2
    label_h = 46
    title_h = 90
    W = pad + cols * (tw + pad)
    H = title_h + pad + rows * (th + label_h + pad)
    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)
    text(d, (W//2, 44), "Mockup UI Aplikasi Pengaduan Kampus", F(30, True), PRIMARY_D, anchor="mm")

    for i, (im, lb) in enumerate(zip(imgs, labels)):
        r = i // cols
        c = i % cols
        x = pad + c * (tw + pad)
        y = title_h + pad + r * (th + label_h + pad)
        # shadow
        d.rounded_rectangle([x+4, y+4, x+tw+4, y+th+4], radius=16, fill=(215, 222, 230))
        # border
        d.rounded_rectangle([x-2, y-2, x+tw+2, y+th+2], radius=18, outline=BORDER, width=2)
        canvas.paste(im, (x, y))
        text(d, (x + tw//2, y + th + 22), lb, F(19, True), PRIMARY, anchor="mm")

    canvas.save(f"{OUT}/09_mockup_grid.png")
    print("09_mockup_grid.png", os.path.getsize(f"{OUT}/09_mockup_grid.png"))

if __name__ == "__main__":
    arsitektur(); logo(); grid()
    print("Selesai.")
