// =========================================================
//  Home Screen — daftar laporan + filter status
// =========================================================
import 'package:flutter/material.dart';
import '../models/user.dart';
import '../models/pengaduan.dart';
import '../services/auth_service.dart';
import '../services/pengaduan_service.dart';
import '../utils/theme.dart';
import 'buat_laporan_screen.dart';
import 'detail_screen.dart';
import 'login_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  User? _user;
  List<Pengaduan> _list = [];
  bool _loading = true;
  String _filter = ''; // '' = semua

  final _filters = ['', 'Menunggu', 'Diproses', 'Selesai', 'Ditolak'];

  @override
  void initState() {
    super.initState();
    _init();
  }

  Future<void> _init() async {
    _user = await AuthService.getUser();
    await _muat();
  }

  Future<void> _muat() async {
    setState(() => _loading = true);
    try {
      final data = await PengaduanService.getDaftar(status: _filter);
      setState(() => _list = data);
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

  Future<void> _logout() async {
    await AuthService.logout();
    if (!mounted) return;
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => const LoginScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Image.asset('assets/logo_umb.png', height: 30, width: 30, fit: BoxFit.contain),
            const SizedBox(width: 10),
            const Text('Pengaduan Kampus'),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            tooltip: 'Keluar',
            onPressed: _logout,
          ),
        ],
      ),
      body: Column(
        children: [
          // Kartu sapaan
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            color: AppTheme.primary,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Halo, ${_user?.nama ?? 'Pengguna'} 👋',
                  style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                ),
                Text(
                  _user?.isAdmin == true ? 'Masuk sebagai Admin' : 'Masuk sebagai Mahasiswa',
                  style: TextStyle(color: Colors.white.withValues(alpha: 0.85), fontSize: 13),
                ),
              ],
            ),
          ),

          // Filter status
          SizedBox(
            height: 56,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              children: _filters.map((f) {
                final label = f.isEmpty ? 'Semua' : f;
                final aktif = _filter == f;
                return Padding(
                  padding: const EdgeInsets.only(right: 8),
                  child: ChoiceChip(
                    label: Text(label),
                    selected: aktif,
                    selectedColor: AppTheme.primary,
                    labelStyle: TextStyle(color: aktif ? Colors.white : Colors.black87),
                    onSelected: (_) {
                      setState(() => _filter = f);
                      _muat();
                    },
                  ),
                );
              }).toList(),
            ),
          ),

          // Daftar laporan
          Expanded(
            child: _loading
                ? const Center(child: CircularProgressIndicator())
                : _list.isEmpty
                    ? _kosong()
                    : RefreshIndicator(
                        onRefresh: _muat,
                        child: ListView.builder(
                          padding: const EdgeInsets.all(12),
                          itemCount: _list.length,
                          itemBuilder: (_, i) => _kartu(_list[i]),
                        ),
                      ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          await Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const BuatLaporanScreen()),
          );
          _muat();
        },
        icon: const Icon(Icons.add),
        label: const Text('Buat Laporan'),
        backgroundColor: AppTheme.primary,
        foregroundColor: Colors.white,
      ),
    );
  }

  Widget _kosong() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.inbox_outlined, size: 80, color: Colors.grey[400]),
          const SizedBox(height: 12),
          Text('Belum ada laporan', style: TextStyle(color: Colors.grey[600], fontSize: 16)),
        ],
      ),
    );
  }

  Widget _kartu(Pengaduan p) {
    final warna = AppTheme.statusColor(p.status);
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: () async {
          await Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => DetailScreen(id: p.id)),
          );
          _muat();
        },
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Expanded(
                    child: Text(
                      p.judul,
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: warna.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(AppTheme.statusIcon(p.status), size: 14, color: warna),
                        const SizedBox(width: 4),
                        Text(p.status, style: TextStyle(color: warna, fontSize: 12, fontWeight: FontWeight.w600)),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  Icon(Icons.category_outlined, size: 14, color: Colors.grey[600]),
                  const SizedBox(width: 4),
                  Text(p.kategori, style: TextStyle(color: Colors.grey[700], fontSize: 12)),
                  const SizedBox(width: 12),
                  Icon(Icons.location_on_outlined, size: 14, color: Colors.grey[600]),
                  const SizedBox(width: 4),
                  Expanded(
                    child: Text(
                      p.lokasi,
                      style: TextStyle(color: Colors.grey[700], fontSize: 12),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 6),
              Text(
                p.deskripsi,
                style: TextStyle(color: Colors.grey[600], fontSize: 13),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
