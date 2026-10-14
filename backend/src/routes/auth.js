// =========================================================
//  Route: /api/auth  → Register, Login, Profil
// =========================================================
const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('../config/db');
const { auth } = require('../middleware/auth');

const router = express.Router();

// ---------- REGISTER ----------
// POST /api/auth/register
router.post('/register', async (req, res, next) => {
  try {
    const { nama, email, password, nim, role } = req.body;

    if (!nama || !email || !password) {
      return res.status(400).json({ message: 'Nama, email, dan password wajib diisi' });
    }

    // Cek email sudah dipakai atau belum
    const [exist] = await db.query('SELECT id FROM users WHERE email = ?', [email]);
    if (exist.length) {
      return res.status(409).json({ message: 'Email sudah terdaftar' });
    }

    // Hash password (JANGAN simpan password asli!)
    const hash = await bcrypt.hash(password, 10);
    const userRole = role === 'admin' ? 'admin' : 'mahasiswa';

    const [result] = await db.query(
      'INSERT INTO users (nama, email, password, role, nim) VALUES (?, ?, ?, ?, ?)',
      [nama, email, hash, userRole, nim || null]
    );

    res.status(201).json({
      message: 'Registrasi berhasil',
      data: { id: result.insertId, nama, email, role: userRole },
    });
  } catch (err) {
    next(err);
  }
});

// ---------- LOGIN ----------
// POST /api/auth/login
router.post('/login', async (req, res, next) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ message: 'Email dan password wajib diisi' });
    }

    const [rows] = await db.query('SELECT * FROM users WHERE email = ?', [email]);
    if (!rows.length) {
      return res.status(401).json({ message: 'Email atau password salah' });
    }

    const user = rows[0];
    const cocok = await bcrypt.compare(password, user.password);
    if (!cocok) {
      return res.status(401).json({ message: 'Email atau password salah' });
    }

    // Buat token JWT
    const token = jwt.sign(
      { id: user.id, nama: user.nama, email: user.email, role: user.role },
      process.env.JWT_SECRET,
      { expiresIn: '7d' }
    );

    res.json({
      message: 'Login berhasil',
      token,
      user: { id: user.id, nama: user.nama, email: user.email, role: user.role, nim: user.nim },
    });
  } catch (err) {
    next(err);
  }
});

// ---------- PROFIL (butuh token) ----------
// GET /api/auth/me
router.get('/me', auth, async (req, res, next) => {
  try {
    const [rows] = await db.query(
      'SELECT id, nama, email, role, nim FROM users WHERE id = ?',
      [req.user.id]
    );
    if (!rows.length) return res.status(404).json({ message: 'User tidak ditemukan' });
    res.json({ user: rows[0] });
  } catch (err) {
    next(err);
  }
});

module.exports = router;
