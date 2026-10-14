// =========================================================
//  Service: Pengaduan (CRUD laporan + upload foto)
// =========================================================
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api.dart';
import '../models/pengaduan.dart';
import 'auth_service.dart';

class PengaduanService {
  // ── Ambil daftar laporan ──
  static Future<List<Pengaduan>> getDaftar({String? status}) async {
    final token = await AuthService.getToken();
    final url = status != null && status.isNotEmpty
        ? '${ApiConfig.pengaduan}?status=$status'
        : ApiConfig.pengaduan;

    final res = await http.get(
      Uri.parse(url),
      headers: {'Authorization': 'Bearer $token'},
    );

    final data = jsonDecode(res.body);
    if (res.statusCode == 200) {
      final list = (data['data'] as List).map((e) => Pengaduan.fromJson(e)).toList();
      return list;
    }
    throw Exception(data['message'] ?? 'Gagal memuat laporan');
  }

  // ── Ambil detail 1 laporan ──
  static Future<Pengaduan> getDetail(int id) async {
    final token = await AuthService.getToken();
    final res = await http.get(
      Uri.parse('${ApiConfig.pengaduan}/$id'),
      headers: {'Authorization': 'Bearer $token'},
    );

    final data = jsonDecode(res.body);
    if (res.statusCode == 200) return Pengaduan.fromJson(data['data']);
    throw Exception(data['message'] ?? 'Gagal memuat detail');
  }

  // ── Buat laporan baru (dengan foto opsional) ──
  static Future<String> buat({
    required String judul,
    required String deskripsi,
    required String kategori,
    required String lokasi,
    String? fotoPath,
  }) async {
    final token = await AuthService.getToken();
    final req = http.MultipartRequest('POST', Uri.parse(ApiConfig.pengaduan))
      ..headers['Authorization'] = 'Bearer $token'
      ..fields['judul'] = judul
      ..fields['deskripsi'] = deskripsi
      ..fields['kategori'] = kategori
      ..fields['lokasi'] = lokasi;

    if (fotoPath != null) {
      req.files.add(await http.MultipartFile.fromPath('foto', fotoPath));
    }

    final streamed = await req.send();
    final res = await http.Response.fromStream(streamed);
    final data = jsonDecode(res.body);

    if (res.statusCode == 201) return data['message'] ?? 'Laporan terkirim';
    throw Exception(data['message'] ?? 'Gagal mengirim laporan');
  }

  // ── Ubah status (ADMIN) ──
  static Future<String> ubahStatus({
    required int id,
    required String status,
    String? catatan,
  }) async {
    final token = await AuthService.getToken();
    final res = await http.put(
      Uri.parse('${ApiConfig.pengaduan}/$id/status'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({'status': status, 'catatan_admin': catatan}),
    );

    final data = jsonDecode(res.body);
    if (res.statusCode == 200) return data['message'] ?? 'Status diperbarui';
    throw Exception(data['message'] ?? 'Gagal mengubah status');
  }

  // ── Hapus laporan ──
  static Future<String> hapus(int id) async {
    final token = await AuthService.getToken();
    final res = await http.delete(
      Uri.parse('${ApiConfig.pengaduan}/$id'),
      headers: {'Authorization': 'Bearer $token'},
    );

    final data = jsonDecode(res.body);
    if (res.statusCode == 200) return data['message'] ?? 'Laporan dihapus';
    throw Exception(data['message'] ?? 'Gagal menghapus laporan');
  }
}
