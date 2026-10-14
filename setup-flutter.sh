#!/bin/bash
# =========================================================
#  Script Setup Flutter Otomatis
#  Jalankan sekali saja setelah flutter_windows.zip terunduh
# =========================================================
set -e

ZIP="/c/Users/Naufal Hafizh/Downloads/flutter_windows.zip"
DEST="/c/Users/Naufal Hafizh/develop"
FLUTTER_DIR="$DEST/flutter"

echo "========================================"
echo " SETUP FLUTTER SDK"
echo "========================================"

# 1. Buat folder tujuan
mkdir -p "$DEST"
echo "📁 Folder tujuan: $DEST"

# 2. Extract kalau belum ada
if [ -d "$FLUTTER_DIR" ]; then
  echo "ℹ️  Flutter sudah pernah di-extract, lewati."
else
  echo "📦 Meng-extract Flutter (mohon tunggu, agak lama)..."
  cd "$DEST"
  unzip -q "$ZIP"
  echo "✅ Extract selesai."
fi

# 3. Tambahkan ke PATH (untuk sesi ini)
export PATH="$FLUTTER_DIR/bin:$PATH"

# 4. Verifikasi
echo
echo "🔍 Versi Flutter:"
"$FLUTTER_DIR/bin/flutter" --version

echo
echo "========================================"
echo " ✅ SETUP SELESAI"
echo "========================================"
echo
echo "⚠️  PENTING: Tambahkan Flutter ke PATH permanen."
echo "   Buka: Windows Settings → Environment Variables"
echo "   Tambahkan ke 'Path':"
echo "      $FLUTTER_DIR\\bin"
echo
echo "   Atau jalankan di PowerShell (sekali):"
echo "      setx PATH \"\$env:PATH;$FLUTTER_DIR\\bin\""
