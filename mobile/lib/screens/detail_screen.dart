// =========================================================
//  Detail Screen — detail laporan + (admin) ubah status
// =========================================================
import 'package:flutter/material.dart';
import '../config/api.dart';
import '../models/pengaduan.dart';
import '../models/user.dart';
import '../services/auth_service.dart';
import '../services/pengaduan_service.dart';
import '../utils/theme.dart';

class DetailScreen extends StatefulWidget {
  final int id;
  const DetailScreen({super.key, required this.id});

  @override
  State<DetailScreen> createState() => _DetailScreenState();
}

class _DetailScreenState extends State<DetailScreen> {
  Pengaduan? _data;
  User? _user;
  bool _loading = true;

  final _statusList = ['Menunggu', 'Diproses', 'Selesai', 'Ditolak'];

  @override
  void initState() {
    super.initState();
    _muat();
  }

  Future<void> _muat() async {
    setState(() => _loading = true);
    try {
      _user = await AuthService.getUser();
      final d = await PengaduanService.getDetail(widget.id);
      setState(() => _data = d);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.toString().replaceAll('Exception: ', ''))),
        );
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  // Dialog ubah status (khusus admin)
  Future<void> _ubahStatus() async {
    if (_data == null) return;
    String statusBaru = _data!.status;
    final catatanCtrl = TextEditingController(text: _data!.catatanAdmin ?? '');

    await showDialog(
      context: context,
      builder: (_) => StatefulBuilder(
        builder: (context, setD) => AlertDialog(
          title: const Text('Ubah Status Laporan'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              DropdownButtonFormField<String>(
                initialValue: statusBaru,
                decoration: const InputDecoration(labelText: 'Status'),
                items: _statusList
                    .map((s) => DropdownMenuItem(value: s, child: Text(s)))
                    .toList(),
                onChanged: (v) => setD(() => statusBaru = v!),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: catatanCtrl,
                maxLines: 3,
                decoration: const InputDecoration(
                  labelText: 'Catatan untuk pelapor',
                  alignLabelWithHint: true,
                ),
              ),
            ],
          ),
          actions: [
            TextButton(onPressed: () => Navigator.pop(context), child: const Text('Batal')),
            ElevatedButton(
              onPressed: () async {
                try {
                  await PengaduanService.ubahStatus(
                    id: widget.id,
                    status: statusBaru,
                    catatan: catatanCtrl.text.trim(),
                  );
                  if (context.mounted) Navigator.pop(context);
                  _pesan('Status berhasil diperbarui');
                  _muat();
                } catch (e) {
                  _pesan(e.toString().replaceAll('Exception: ', ''));
                }
              },
              child: const Text('Simpan'),
            ),
          ],
        ),
      ),
    );
  }

  void _pesan(String m) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(m)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Detail Laporan')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _data == null
              ? const Center(child: Text('Data tidak ditemukan'))
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      // Foto
                      if (_data!.foto != null)
                        ClipRRect(
                          borderRadius: BorderRadius.circular(14),
                          child: Image.network(
                            ApiConfig.fotoUrl(_data!.foto!),
                            height: 220,
                            fit: BoxFit.cover,
                            errorBuilder: (_, __, ___) => Container(
                              height: 220,
                              color: Colors.grey.shade200,
                              child: const Center(child: Icon(Icons.broken_image, size: 48)),
                            ),
                          ),
                        ),
                      if (_data!.foto != null) const SizedBox(height: 20),

                      // Judul
                      Text(
                        _data!.judul,
                        style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 12),

                      // Badge status
                      Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                            decoration: BoxDecoration(
                              color: AppTheme.statusColor(_data!.status).withValues(alpha: 0.15),
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(AppTheme.statusIcon(_data!.status),
                                    size: 16, color: AppTheme.statusColor(_data!.status)),
                                const SizedBox(width: 6),
                                Text(
                                  _data!.status,
                                  style: TextStyle(
                                    color: AppTheme.statusColor(_data!.status),
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(width: 10),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                            decoration: BoxDecoration(
                              color: Colors.grey.shade200,
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Text(_data!.kategori, style: const TextStyle(fontSize: 13)),
                          ),
                        ],
                      ),
                      const SizedBox(height: 20),

                      _baris(Icons.person_outline, 'Pelapor',
                          '${_data!.pelapor ?? '-'}${_data!.nim != null ? ' (${_data!.nim})' : ''}'),
                      _baris(Icons.location_on_outlined, 'Lokasi', _data!.lokasi),
                      _baris(Icons.calendar_today_outlined, 'Tanggal',
                          _data!.createdAt.substring(0, 10)),
                      const SizedBox(height: 16),

                      const Text('Deskripsi', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                      const SizedBox(height: 6),
                      Text(_data!.deskripsi, style: TextStyle(color: Colors.grey[800], height: 1.5)),
                      const SizedBox(height: 20),

                      // Catatan admin
                      if (_data!.catatanAdmin != null && _data!.catatanAdmin!.isNotEmpty)
                        Container(
                          padding: const EdgeInsets.all(14),
                          decoration: BoxDecoration(
                            color: Colors.green.shade50,
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: Colors.green.shade200),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  Icon(Icons.admin_panel_settings, size: 18, color: Colors.green.shade800),
                                  const SizedBox(width: 6),
                                  Text('Tanggapan Admin',
                                      style: TextStyle(fontWeight: FontWeight.bold, color: Colors.green.shade800)),
                                ],
                              ),
                              const SizedBox(height: 6),
                              Text(_data!.catatanAdmin!, style: TextStyle(color: Colors.green.shade900)),
                            ],
                          ),
                        ),

                      // Tombol ubah status (admin)
                      if (_user?.isAdmin == true) ...[
                        const SizedBox(height: 24),
                        ElevatedButton.icon(
                          onPressed: _ubahStatus,
                          icon: const Icon(Icons.edit),
                          label: const Text('Ubah Status'),
                        ),
                      ],
                    ],
                  ),
                ),
    );
  }

  Widget _baris(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        children: [
          Icon(icon, size: 18, color: Colors.grey[600]),
          const SizedBox(width: 10),
          SizedBox(width: 70, child: Text(label, style: TextStyle(color: Colors.grey[600]))),
          const SizedBox(width: 8),
          Expanded(child: Text(value, style: const TextStyle(fontWeight: FontWeight.w500))),
        ],
      ),
    );
  }
}
