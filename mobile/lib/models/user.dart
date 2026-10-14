// =========================================================
//  Model: User
// =========================================================
class User {
  final int id;
  final String nama;
  final String email;
  final String role; // 'mahasiswa' | 'admin'
  final String? nim;

  User({
    required this.id,
    required this.nama,
    required this.email,
    required this.role,
    this.nim,
  });

  bool get isAdmin => role == 'admin';

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      nama: json['nama'] ?? '',
      email: json['email'] ?? '',
      role: json['role'] ?? 'mahasiswa',
      nim: json['nim'],
    );
  }
}
