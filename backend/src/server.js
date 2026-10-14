// =========================================================
//  Entry point server Express
// =========================================================
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');

const authRoutes = require('./routes/auth');
const pengaduanRoutes = require('./routes/pengaduan');

const app = express();

// ---------- Middleware Global ----------
app.use(cors());                          // izinkan akses dari app Flutter
app.use(express.json());                  // parsing body JSON
app.use(express.urlencoded({ extended: true }));

// Sajikan file foto yang di-upload agar bisa diakses lewat URL
app.use('/uploads', express.static(path.join(__dirname, '..', 'uploads')));

// ---------- Route Dasar ----------
app.get('/', (req, res) => {
  res.json({
    message: '🚀 API Pengaduan Kampus berjalan',
    endpoints: {
      auth: ['POST /api/auth/register', 'POST /api/auth/login', 'GET /api/auth/me'],
      pengaduan: [
        'GET /api/pengaduan',
        'GET /api/pengaduan/:id',
        'POST /api/pengaduan',
        'PUT /api/pengaduan/:id/status (admin)',
        'DELETE /api/pengaduan/:id',
      ],
    },
  });
});

// ---------- Route API ----------
app.use('/api/auth', authRoutes);
app.use('/api/pengaduan', pengaduanRoutes);

// ---------- 404 ----------
app.use((req, res) => {
  res.status(404).json({ message: `Endpoint ${req.method} ${req.url} tidak ditemukan` });
});

// ---------- Error Handler ----------
app.use((err, req, res, next) => {
  console.error('❌ Error:', err.message);
  res.status(err.status || 500).json({ message: err.message || 'Terjadi kesalahan pada server' });
});

// ---------- Jalankan Server ----------
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Server berjalan di http://localhost:${PORT}`);
});
