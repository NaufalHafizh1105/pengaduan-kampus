// =========================================================
//  Middleware Autentikasi (JWT) & Otorisasi (role admin)
// =========================================================
const jwt = require('jsonwebtoken');

// Cek apakah request membawa token JWT yang valid
function auth(req, res, next) {
  const header = req.headers.authorization;

  if (!header || !header.startsWith('Bearer ')) {
    return res.status(401).json({ message: 'Token tidak ditemukan, silakan login dulu' });
  }

  try {
    const token = header.split(' ')[1];
    // Hasil decode disimpan di req.user agar bisa dipakai route berikutnya
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch (err) {
    return res.status(401).json({ message: 'Token tidak valid atau sudah kedaluwarsa' });
  }
}

// Hanya boleh diakses oleh admin
function adminOnly(req, res, next) {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ message: 'Akses ditolak, hanya untuk admin' });
  }
  next();
}

module.exports = { auth, adminOnly };
