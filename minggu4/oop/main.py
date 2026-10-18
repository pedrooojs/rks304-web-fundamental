import sys

from scanner import TCPPortScanner
from report import PDFReportExporter, JSONReportExporter


def main():
    print("=== APLIKASI PORT SCANNER & EXPORTER (OOP) ===")
    target = input("Masukkan IP atau Domain target (contoh: 127.0.0.1): ").strip()

    try:
        start = int(input("Masukkan port awal (contoh: 1): "))
        end = int(input("Masukkan port akhir (contoh: 1024): "))
    except ValueError:
        print("[!] Masukkan angka port yang valid.")
        sys.exit(1)

    # 1. Buat objek pemindai (resolusi host dilakukan di dalam kelas)
    try:
        scanner = TCPPortScanner(target, start, end, timeout=0.4)
    except ValueError as e:
        print(f"\n[!] {e}")
        sys.exit(1)

    # 2. Jalankan proses pemindaian port
    scanner.scan()

    # 3. Ekspor hasil ke PDF dan JSON
    safe_target = target.replace('.', '_')
    exporters = [
        PDFReportExporter(scanner, f"scan_report_{safe_target}.pdf"),
        JSONReportExporter(scanner, f"scan_report_{safe_target}.json"),
    ]

    for exporter in exporters:
        exporter.export()


if __name__ == "__main__":
    main()
