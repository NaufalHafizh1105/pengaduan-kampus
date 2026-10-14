-- =========================================================
--  DATABASE: pengaduan_kampus
--  Aplikasi Pengaduan Fasilitas Kampus
--  Tugas Mata Kuliah Pemrograman Perangkat Bergerak
-- =========================================================

CREATE DATABASE IF NOT EXISTS pengaduan_kampus
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE pengaduan_kampus;

-- ---------------------------------------------------------
--  TABEL: users  (mahasiswa & admin)
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  nama       VARCHAR(100) NOT NULL,
  email      VARCHAR(100) NOT NULL UNIQUE,
  password   VARCHAR(255) NOT NULL,               -- disimpan dalam bentuk hash bcrypt
  role       ENUM('mahasiswa','admin') NOT NULL DEFAULT 'mahasiswa',
  nim        VARCHAR(20),                          -- nomor induk mahasiswa (opsional)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------
--  TABEL: pengaduan  (laporan keluhan fasilitas)
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS pengaduan (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  user_id       INT NOT NULL,
  judul         VARCHAR(150) NOT NULL,
  deskripsi     TEXT NOT NULL,
  kategori      ENUM('Fasilitas','Kebersihan','Keamanan','Akademik','Lainnya')
                NOT NULL DEFAULT 'Lainnya',
  lokasi        VARCHAR(150) NOT NULL,
  foto          VARCHAR(255),                      -- nama file foto (opsional)
  status        ENUM('Menunggu','Diproses','Selesai','Ditolak')
                NOT NULL DEFAULT 'Menunggu',
  catatan_admin TEXT,                              -- tanggapan dari admin
  created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_pengaduan_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ---------------------------------------------------------
--  DATA CONTOH: akun admin default
--  Email    : admin@kampus.ac.id
--  Password : admin123   (hash bcrypt di bawah)
-- ---------------------------------------------------------
INSERT INTO users (nama, email, password, role)
SELECT 'Administrator', 'admin@kampus.ac.id',
       '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'admin'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'admin@kampus.ac.id');
