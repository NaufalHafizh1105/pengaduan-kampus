# 🗄️ ERD & Skema Database

## Diagram Relasi (ERD)

```
┌─────────────────────────────┐
│           users             │
├─────────────────────────────┤
│ PK  id          INT         │
│     nama        VARCHAR(100)│
│     email       VARCHAR(100)│ UNIQUE
│     password    VARCHAR(255)│ (hash bcrypt)
│     role        ENUM        │ mahasiswa | admin
│     nim         VARCHAR(20) │
│     created_at  TIMESTAMP   │
└──────────────┬──────────────┘
               │ 1
               │
               │ N   (user_id → users.id)
┌──────────────▼──────────────┐
│         pengaduan           │
├─────────────────────────────┤
│ PK  id            INT       │
│ FK  user_id       INT       │
│     judul         VARCHAR   │
│     deskripsi     TEXT      │
│     kategori      ENUM      │ Fasilitas | Kebersihan | Keamanan | Akademik | Lainnya
│     lokasi        VARCHAR   │
│     foto          VARCHAR   │ (nama file, opsional)
│     status        ENUM      │ Menunggu | Diproses | Selesai | Ditolak
│     catatan_admin TEXT      │
│     created_at    TIMESTAMP │
│     updated_at    TIMESTAMP │
└─────────────────────────────┘
```

## Relasi
- **1 User → N Pengaduan** (One to Many)
- Satu mahasiswa bisa membuat banyak laporan
- Setiap laporan milik tepat satu user
- Jika user dihapus, laporannya ikut terhapus (`ON DELETE CASCADE`)

## Alur Status Laporan
```
  [Mahasiswa buat laporan]
           │
           ▼
      ┌──────────┐
      │ MENUNGGU │
      └────┬─────┘
           │ admin proses
           ▼
      ┌──────────┐
      │ DIPROSES │
      └────┬─────┘
       ┌───┴────┐
       ▼        ▼
  ┌────────┐ ┌────────┐
  │ SELESAI│ │ DITOLAK│
  └────────┘ └────────┘
```

## Contoh Query
```sql
-- Daftar laporan mahasiswa tertentu
SELECT * FROM pengaduan WHERE user_id = 2 ORDER BY created_at DESC;

-- Jumlah laporan per status
SELECT status, COUNT(*) FROM pengaduan GROUP BY status;

-- Laporan dengan nama pelapor
SELECT p.*, u.nama FROM pengaduan p
JOIN users u ON p.user_id = u.id;
```
