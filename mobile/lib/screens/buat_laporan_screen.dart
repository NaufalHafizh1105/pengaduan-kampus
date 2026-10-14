// =========================================================
//  Buat Laporan Screen — form + ambil foto
// =========================================================
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../services/pengaduan_service.dart';

class BuatLaporanScreen extends StatefulWidget {
  const BuatLaporanScreen({super.key});

  @override
  State<BuatLaporanScreen> createState() => _BuatLaporanScreenState();
}

class _BuatLaporanScreenState extends State<BuatLaporanScreen> {
  final _judulCtrl = TextEditingController();
  final _deskCtrl = TextEditingController();
  final _lokasiCtrl = TextEditingController();
  final _picker = ImagePicker();

  String _kategori = 'Fasilitas';
  File? _foto;
  bool _loading = false;

  final _kategoris = ['Fasilitas', 'Kebersihan', 'Keamanan', 'Akademik', 'Lainnya'];

  Future<void> _ambilFoto(ImageSource source) async {
    try {
      final x = await _picker.pickImage(source: source, imageQuality: 70, maxWidth: 1280);
      if (x != null) setState(() => _foto = File(x.path));
    } catch (e) {
      _pesan('Gagal mengambil foto: $e');
    }
  }

  void _opsiFoto() {
    showModalBottomSheet(
      context: context,
      builder: (_) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.camera_alt),
              title: const Text('Ambil dari Kamera'),
              onTap: () {
                Navigator.pop(context);
                _ambilFoto(ImageSource.camera);
              },
            ),
            ListTile(
              leading: const Icon(Icons.photo_library),
              title: const Text('Pilih dari Galeri'),
              onTap: () {
                Navigator.pop(context);
                _ambilFoto(ImageSource.gallery);
              },
            ),
            if (_foto != null)
              ListTile(
                leading: const Icon(Icons.delete, color: Colors.red),
                title: const Text('Hapus Foto', style: TextStyle(color: Colors.red)),
                onTap: () {
                  Navigator.pop(context);
                  setState(() => _foto = null);
                },
              ),
          ],
        ),
      ),
    );
  }

  Future<void> _kirim() async {
    if (_judulCtrl.text.isEmpty || _deskCtrl.text.isEmpty || _lokasiCtrl.text.isEmpty) {
      _pesan('Judul, deskripsi, dan lokasi wajib diisi');
      return;
    }
    setState(() => _loading = true);
    try {
      final msg = await PengaduanService.buat(
        judul: _judulCtrl.text.trim(),
        deskripsi: _deskCtrl.text.trim(),
        kategori: _kategori,
        lokasi: _lokasiCtrl.text.trim(),
        fotoPath: _foto?.path,
      );
      if (!mounted) return;
      _pesan(msg);
      Navigator.pop(context, true);
    } catch (e) {
      _pesan(e.toString().replaceAll('Exception: ', ''));
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  void _pesan(String m) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(m)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Buat Laporan')),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Foto
              GestureDetector(
                onTap: _opsiFoto,
                child: Container(
                  height: 180,
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: Colors.grey.shade300),
                  ),
                  child: _foto == null
                      ? Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.add_a_photo_outlined, size: 48, color: Colors.grey[400]),
                            const SizedBox(height: 8),
                            Text('Tambah Foto (opsional)', style: TextStyle(color: Colors.grey[600])),
                          ],
                        )
                      : ClipRRect(
                          borderRadius: BorderRadius.circular(14),
                          child: Image.file(_foto!, fit: BoxFit.cover, width: double.infinity),
                        ),
                ),
              ),
              const SizedBox(height: 20),

              // Judul
              TextField(
                controller: _judulCtrl,
                decoration: const InputDecoration(
                  labelText: 'Judul Laporan',
                  prefixIcon: Icon(Icons.title),
                ),
              ),
              const SizedBox(height: 16),

              // Kategori
              DropdownButtonFormField<String>(
                initialValue: _kategori,
                decoration: const InputDecoration(
                  labelText: 'Kategori',
                  prefixIcon: Icon(Icons.category_outlined),
                ),
                items: _kategoris
                    .map((k) => DropdownMenuItem(value: k, child: Text(k)))
                    .toList(),
                onChanged: (v) => setState(() => _kategori = v!),
              ),
              const SizedBox(height: 16),

              // Lokasi
              TextField(
                controller: _lokasiCtrl,
                decoration: const InputDecoration(
                  labelText: 'Lokasi (gedung / ruangan)',
                  prefixIcon: Icon(Icons.location_on_outlined),
                ),
              ),
              const SizedBox(height: 16),

              // Deskripsi
              TextField(
                controller: _deskCtrl,
                maxLines: 5,
                decoration: const InputDecoration(
                  labelText: 'Deskripsi Keluhan',
                  alignLabelWithHint: true,
                ),
              ),
              const SizedBox(height: 28),

              ElevatedButton.icon(
                onPressed: _loading ? null : _kirim,
                icon: _loading
                    ? const SizedBox(
                        height: 20, width: 20,
                        child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                      )
                    : const Icon(Icons.send),
                label: Text(_loading ? 'Mengirim...' : 'Kirim Laporan'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
