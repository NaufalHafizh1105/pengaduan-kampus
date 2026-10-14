// =========================================================
//  Koneksi Database (MySQL / MariaDB) menggunakan connection pool
// =========================================================
const mysql = require('mysql2/promise');
require('dotenv').config();

// Pool = kumpulan koneksi yang dipakai ulang, lebih efisien
// daripada buka-tutup koneksi tiap request.
const pool = mysql.createPool({
  host: process.env.DB_HOST || '127.0.0.1',
  port: Number(process.env.DB_PORT) || 3306,
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  database: process.env.DB_NAME || 'pengaduan_kampus',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

// Uji koneksi saat aplikasi dijalankan
(async () => {
  try {
    const conn = await pool.getConnection();
    await conn.ping();
    conn.release();
    console.log('✅ Database terhubung:', process.env.DB_NAME);
  } catch (err) {
    console.error('❌ Gagal koneksi ke database:', err.message);
    console.error('   Pastikan MySQL XAMPP sudah Start dan database sudah dibuat.');
  }
})();

module.exports = pool;
