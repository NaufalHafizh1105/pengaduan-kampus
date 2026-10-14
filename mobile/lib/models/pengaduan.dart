// =========================================================
//  Model: Pengaduan (laporan)
// =========================================================
class Pengaduan {
  final int id;
  final int userId;
  final String judul;
  final String deskripsi;
  final String kategori;
  final String lokasi;
  final String? foto;
  final String status; // Menunggu | Diproses | Selesai | Ditolak
  final String? catatanAdmin;
  final String createdAt;
  final String? pelapor;
  final String? nim;

  Pengaduan({
    required this.id,
    required this.userId,
    required this.judul,
    required this.deskripsi,
    required this.kategori,
    required this.lokasi,
    this.foto,
    required this.status,
    this.catatanAdmin,
    required this.createdAt,
    this.pelapor,
    this.nim,
  });

  factory Pengaduan.fromJson(Map<String, dynamic> json) {
    return Pengaduan(
      id: json['id'],
      userId: json['user_id'],
      judul: json['judul'] ?? '',
      deskripsi: json['deskripsi'] ?? '',
      kategori: json['kategori'] ?? 'Lainnya',
      lokasi: json['lokasi'] ?? '',
      foto: json['foto'],
      status: json['status'] ?? 'Menunggu',
      catatanAdmin: json['catatan_admin'],
      createdAt: json['created_at'] ?? '',
      pelapor: json['pelapor'],
      nim: json['nim'],
    );
  }
}
