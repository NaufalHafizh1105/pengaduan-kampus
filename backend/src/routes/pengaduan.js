// =========================================================
//  Route: /api/pengaduan  → CRUD Laporan Pengaduan
// =========================================================
const express = require('express');
const db = require('../config/db');
const { auth, adminOnly } = require('../middleware/auth');
const upload = require('../middleware/upload');

const router = express.Router();

// ---------- DAFTAR LAPORAN ----------
// GET /api/pengaduan?status=Menunggu&kategori=Fasilitas
// Mahasiswa: hanya laporan miliknya sendiri
// Admin    : semua laporan
router.get('/', auth, async (req, res, next) => {
  try {
    const { status, kategori } = req.query;
    const where = [];
    const params = [];

    let sql = `SELECT p.*, u.nama AS pelapor, u.nim
               FROM pengaduan p
               JOIN users u ON p.user_id = u.id`;

    if (req.user.role !== 'admin') {
      where.push('p.user_id = ?');
      params.push(req.user.id);
    }
    if (status) {
      where.push('p.status = ?');
      params.push(status);
    }
    if (kategori) {
      where.push('p.kategori = ?');
      params.push(kategori);
    }
    if (where.length) sql += ' WHERE ' + where.join(' AND ');
    sql += ' ORDER BY p.created_at DESC';

    const [rows] = await db.query(sql, params);
    res.json({ jumlah: rows.length, data: rows });
  } catch (err) {
    next(err);
  }
});

// ---------- DETAIL LAPORAN ----------
// GET /api/pengaduan/:id
router.get('/:id', auth, async (req, res, next) => {
  try {
    const [rows] = await db.query(
      `SELECT p.*, u.nama AS pelapor, u.nim
       FROM pengaduan p
       JOIN users u ON p.user_id = u.id
       WHERE p.id = ?`,
      [req.params.id]
    );
    if (!rows.length) return res.status(404).json({ message: 'Laporan tidak ditemukan' });

    const data = rows[0];
    if (req.user.role !== 'admin' && data.user_id !== req.user.id) {
      return res.status(403).json({ message: 'Tidak berhak melihat laporan ini' });
    }
    res.json({ data });
  } catch (err) {
    next(err);
  }
});

// ---------- BUAT LAPORAN BARU ----------
// POST /api/pengaduan  (multipart/form-data, field foto opsional)
router.post('/', auth, upload.single('foto'), async (req, res, next) => {
  try {
    const { judul, deskripsi, kategori, lokasi } = req.body;

    if (!judul || !deskripsi || !lokasi) {
      return res.status(400).json({ message: 'Judul, deskripsi, dan lokasi wajib diisi' });
    }

    const foto = req.file ? req.file.filename : null;

    const [result] = await db.query(
      `INSERT INTO pengaduan (user_id, judul, deskripsi, kategori, lokasi, foto)
       VALUES (?, ?, ?, ?, ?, ?)`,
      [req.user.id, judul, deskripsi, kategori || 'Lainnya', lokasi, foto]
    );

    res.status(201).json({
      message: 'Laporan berhasil dikirim',
      data: { id: result.insertId },
    });
  } catch (err) {
    next(err);
  }
});

// ---------- UBAH STATUS (ADMIN) ----------
// PUT /api/pengaduan/:id/status
router.put('/:id/status', auth, adminOnly, async (req, res, next) => {
  try {
    const { status, catatan_admin } = req.body;
    const valid = ['Menunggu', 'Diproses', 'Selesai', 'Ditolak'];

    if (!valid.includes(status)) {
      return res.status(400).json({ message: 'Status tidak valid' });
    }

    const [result] = await db.query(
      'UPDATE pengaduan SET status = ?, catatan_admin = ? WHERE id = ?',
      [status, catatan_admin || null, req.params.id]
    );
    if (!result.affectedRows) return res.status(404).json({ message: 'Laporan tidak ditemukan' });

    res.json({ message: 'Status laporan berhasil diperbarui' });
  } catch (err) {
    next(err);
  }
});

// ---------- HAPUS LAPORAN ----------
// DELETE /api/pengaduan/:id
router.delete('/:id', auth, async (req, res, next) => {
  try {
    const [rows] = await db.query('SELECT user_id FROM pengaduan WHERE id = ?', [req.params.id]);
    if (!rows.length) return res.status(404).json({ message: 'Laporan tidak ditemukan' });

    if (req.user.role !== 'admin' && rows[0].user_id !== req.user.id) {
      return res.status(403).json({ message: 'Tidak berhak menghapus laporan ini' });
    }

    await db.query('DELETE FROM pengaduan WHERE id = ?', [req.params.id]);
    res.json({ message: 'Laporan berhasil dihapus' });
  } catch (err) {
    next(err);
  }
});

module.exports = router;
