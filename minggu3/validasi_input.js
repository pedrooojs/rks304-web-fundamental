// Validasi input form register (register.html)

const form = document.getElementById("registerForm");

// Tanggal hari ini dalam format YYYY-MM-DD (sama dengan format value input type="date")
function hariIni() {
  const d = new Date();
  const bulan = String(d.getMonth() + 1).padStart(2, "0");
  const tanggal = String(d.getDate()).padStart(2, "0");
  return `${d.getFullYear()}-${bulan}-${tanggal}`;
}

// Kalender di input tanggal lahir tidak bisa memilih tanggal setelah hari ini
document.getElementById("tanggal_lahir").max = hariIni();

// Aturan tiap input: fungsi mengembalikan pesan error, atau "" kalau valid
const aturan = {
  username(nilai) {
    if (nilai === "") return "Username tidak boleh kosong.";
    if (nilai.length < 3) return "Username minimal 3 karakter.";
    return "";
  },
  password(nilai) {
    if (nilai === "") return "Password tidak boleh kosong.";
    if (nilai.length < 8) return "Password minimal 8 karakter.";
    return "";
  },
  nama(nilai) {
    if (nilai === "") return "Nama tidak boleh kosong.";
    return "";
  },
  tanggal_lahir(nilai) {
    if (nilai === "") return "Tanggal lahir tidak boleh kosong.";
    if (nilai > hariIni()) return "Tanggal lahir tidak boleh melebihi hari ini.";
    return "";
  },
  alamat(nilai) {
    if (nilai === "") return "Alamat tidak boleh kosong.";
    return "";
  },
  telepon(nilai) {
    if (nilai === "") return "Nomor telepon tidak boleh kosong.";
    if (!nilai.startsWith("62")) return "Nomor telepon harus berawalan 62.";
    if (!/^\d+$/.test(nilai)) return "Nomor telepon hanya boleh berisi angka.";
    return "";
  },
};

// Tampilkan / sembunyikan pesan error di bawah input, kembalikan true kalau valid
function cekInput(id) {
  const input = document.getElementById(id);
  const error = document.getElementById(id + "-error");
  // Password tidak di-trim supaya spasi tetap dihitung
  const nilai = id === "password" ? input.value : input.value.trim();
  const pesan = aturan[id](nilai);

  error.textContent = pesan;
  error.classList.toggle("hidden", pesan === "");
  input.classList.toggle("ring-2", pesan !== "");
  input.classList.toggle("ring-red-500", pesan !== "");
  return pesan === "";
}

// Event submit: cek semua input, batalkan pengiriman kalau ada yang tidak valid
form.addEventListener("submit", (event) => {
  let semuaValid = true;
  for (const id in aturan) {
    if (!cekInput(id)) semuaValid = false;
  }

  if (!semuaValid) {
    event.preventDefault();
    form.querySelector(".ring-red-500").focus();
  }
  // Kalau valid, form dikirim ke action="dashboard.html"
});

// Event input: error di sebuah input hilang/berubah saat pengguna mulai memperbaikinya
for (const id in aturan) {
  document.getElementById(id).addEventListener("input", () => {
    if (!document.getElementById(id + "-error").classList.contains("hidden")) {
      cekInput(id);
    }
  });
}
