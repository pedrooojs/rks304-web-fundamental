import socket
import time
from abc import ABC, abstractmethod
from datetime import datetime


class BaseScanner(ABC):
    """Kerangka abstrak untuk semua jenis pemindai jaringan."""

    def __init__(self, target_host):
        self._target_host = target_host
        self._target_ip = self._resolve_host()
        self._scan_duration = "0.00 detik"

    @property
    def target_host(self):
        return self._target_host

    @property
    def target_ip(self):
        return self._target_ip

    @property
    def scan_duration(self):
        return self._scan_duration

    def _resolve_host(self):
        """Menyelesaikan nama host menjadi alamat IP."""
        try:
            return socket.gethostbyname(self._target_host)
        except socket.gaierror:
            raise ValueError("Host tidak dapat diselesaikan. Periksa kembali nama/IP target.")

    @abstractmethod
    def scan(self):
        """Menjalankan pemindaian. Wajib diimplementasikan oleh kelas turunan."""
        pass


class TCPPortScanner(BaseScanner):
    """Pemindai port berbasis koneksi TCP (connect scan)."""

    def __init__(self, target_host, start_port, end_port, timeout=0.5):
        if not (1 <= start_port <= end_port <= 65535):
            raise ValueError("Rentang port harus 1-65535 dan port awal tidak boleh lebih besar dari port akhir.")

        super().__init__(target_host)
        self.__start_port = start_port
        self.__end_port = end_port
        self.__timeout = timeout
        self.__open_ports = []

    @property
    def start_port(self):
        return self.__start_port

    @property
    def end_port(self):
        return self.__end_port

    @property
    def open_ports(self):
        # Kembalikan salinan agar daftar asli tidak bisa diubah dari luar kelas
        return list(self.__open_ports)

    def scan(self):
        """Melakukan pemindaian port TCP dan menyimpan daftar port yang terbuka."""
        self.__open_ports = []

        print("-" * 50)
        print(f" Memindai Target IP: {self.target_ip}")
        print(f" Rentang Port      : {self.__start_port} - {self.__end_port}")
        print(f" Waktu Mulai       : {str(datetime.now())}")
        print("-" * 50)

        started = time.perf_counter()
        try:
            for port in range(self.__start_port, self.__end_port + 1):
                if self.__is_port_open(port):
                    print(f"[+] Port {port} : TERBUKA")
                    self.__open_ports.append(port)

        except KeyboardInterrupt:
            print("\n[!] Pemindaian dibatalkan oleh pengguna (Ctrl+C).")

        self._scan_duration = f"{time.perf_counter() - started:.2f} detik"

        print("-" * 50)
        print(f" Pemindaian Selesai. Total port terbuka ditemukan: {len(self.__open_ports)}")
        print(f" Durasi Pemindaian : {self._scan_duration}")
        print("-" * 50)

    def __is_port_open(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.__timeout)
            return s.connect_ex((self.target_ip, port)) == 0
