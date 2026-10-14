// =========================================================
//  Middleware Upload Foto (multer)
// =========================================================
const multer = require('multer');
const path = require('path');
const fs = require('fs');

// Pastikan folder uploads ada
const uploadDir = path.join(__dirname, '..', '..', 'uploads');
if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });

// Lokasi & nama file penyimpanan
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase();
    cb(null, `laporan_${Date.now()}_${Math.round(Math.random() * 1e6)}${ext}`);
  },
});

// Hanya izinkan gambar
const fileFilter = (req, file, cb) => {
  const allowed = /jpeg|jpg|png|webp/;
  const isValid = allowed.test(file.mimetype);
  if (isValid) return cb(null, true);
  cb(new Error('Format file harus gambar (jpg, jpeg, png, webp)'));
};

module.exports = multer({
  storage,
  fileFilter,
  limits: { fileSize: 5 * 1024 * 1024 }, // maksimal 5 MB
});
