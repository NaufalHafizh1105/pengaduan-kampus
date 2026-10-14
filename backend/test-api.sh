#!/bin/bash
# =========================================================
#  Script Tes Otomatis API Pengaduan Kampus
#  Jalankan: bash test-api.sh   (server harus sudah jalan)
# =========================================================
BASE="http://127.0.0.1:3000"
PASS=0
FAIL=0

cek() {
  # $1 = nama tes, $2 = kondisi (0 = lolos)
  if [ "$2" = "0" ]; then
    echo "  ✅ $1"; PASS=$((PASS+1))
  else
    echo "  ❌ $1"; FAIL=$((FAIL+1))
  fi
}

echo "========================================"
echo " TES API PENGADUAN KAMPUS"
echo "========================================"

echo; echo "[1] Server hidup?"
curl -s "$BASE/" | grep -q "berjalan" && cek "Server merespons" 0 || cek "Server merespons" 1

echo; echo "[2] Register mahasiswa baru"
R=$(curl -s -X POST "$BASE/api/auth/register" -H "Content-Type: application/json" \
  -d '{"nama":"Tes User","email":"tes'$RANDOM'@mhs.ac.id","password":"123456","nim":"2021099"}')
echo "$R" | grep -q "berhasil" && cek "Register sukses" 0 || cek "Register sukses" 1

echo; echo "[3] Login"
EMAIL="tes$RANDOM@mhs.ac.id"
curl -s -X POST "$BASE/api/auth/register" -H "Content-Type: application/json" \
  -d "{\"nama\":\"Tes\",\"email\":\"$EMAIL\",\"password\":\"123456\"}" > /dev/null
LOGIN=$(curl -s -X POST "$BASE/api/auth/login" -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"123456\"}")
TOKEN=$(echo "$LOGIN" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
[ -n "$TOKEN" ] && cek "Dapat token JWT" 0 || cek "Dapat token JWT" 1

echo; echo "[4] Buat laporan"
C=$(curl -s -X POST "$BASE/api/pengaduan" -H "Authorization: Bearer $TOKEN" \
  -F "judul=Test laporan" -F "deskripsi=Deskripsi test" -F "kategori=Fasilitas" -F "lokasi=Gedung Test")
echo "$C" | grep -q "berhasil dikirim" && cek "Buat laporan sukses" 0 || cek "Buat laporan sukses" 1

echo; echo "[5] Daftar laporan"
curl -s "$BASE/api/pengaduan" -H "Authorization: Bearer $TOKEN" | grep -q '"jumlah"' \
  && cek "Ambil daftar laporan" 0 || cek "Ambil daftar laporan" 1

echo; echo "[6] Login admin"
ALOGIN=$(curl -s -X POST "$BASE/api/auth/login" -H "Content-Type: application/json" \
  -d '{"email":"admin@kampus.ac.id","password":"admin123"}')
ATOKEN=$(echo "$ALOGIN" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
[ -n "$ATOKEN" ] && cek "Login admin sukses" 0 || cek "Login admin sukses" 1

echo; echo "[7] Mahasiswa ditolak saat ubah status"
S=$(curl -s -X PUT "$BASE/api/pengaduan/1/status" -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" -d '{"status":"Selesai"}')
echo "$S" | grep -q "ditolak" && cek "Otorisasi admin bekerja" 0 || cek "Otorisasi admin bekerja" 1

echo; echo "[8] Tanpa token ditolak"
CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/api/pengaduan")
[ "$CODE" = "401" ] && cek "Proteksi token bekerja" 0 || cek "Proteksi token bekerja" 1

echo; echo "========================================"
echo " HASIL: $PASS lolos, $FAIL gagal"
echo "========================================"
