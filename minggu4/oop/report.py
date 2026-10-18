import json
from abc import ABC, abstractmethod
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


class BaseReportExporter(ABC):
    """Kerangka abstrak untuk semua format laporan hasil pemindaian."""

    def __init__(self, data, filename):
        # data adalah objek turunan BaseScanner (agregasi)
        self._data = data
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    @staticmethod
    def _estimate_service(port):
        if port in [80, 443]:
            return "HTTP/HTTPS"
        if port == 22:
            return "SSH"
        if port == 21:
            return "FTP"
        return "Lainnya/Custom"

    @abstractmethod
    def export(self):
        """Menulis laporan ke berkas. Wajib diimplementasikan oleh kelas turunan."""
        pass


class PDFReportExporter(BaseReportExporter):
    """Mengeksport hasil pemindaian ke dokumen PDF."""

    def export(self):
        doc = SimpleDocTemplate(self._filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        # Kustomisasi Gaya Teks
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a365d'),
            spaceAfter=12,
            alignment=1
        )
        normal_style = styles['Normal']

        # Judul Laporan
        story.append(Paragraph("Laporan Hasil Pemindaian Port (Port Scanner)", title_style))
        story.append(Spacer(1, 12))

        # Informasi Target
        summary_data = [
            [Paragraph("<b>Target Host:</b>", normal_style), Paragraph(self._data.target_host, normal_style)],
            [Paragraph("<b>Target IP:</b>", normal_style), Paragraph(self._data.target_ip, normal_style)],
            [Paragraph("<b>Rentang Port:</b>", normal_style),
             Paragraph(f"{self._data.start_port} - {self._data.end_port}", normal_style)],
            [Paragraph("<b>Durasi Pemindaian:</b>", normal_style), Paragraph(self._data.scan_duration, normal_style)],
            [Paragraph("<b>Waktu Eksekusi:</b>", normal_style), Paragraph(str(datetime.now()), normal_style)],
        ]

        summary_table = Table(summary_data, colWidths=[120, 380])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f7fafc')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 15))

        # Tabel Hasil Port Terbuka
        story.append(Paragraph("<b>Daftar Port Terbuka</b>", styles['Heading2']))
        story.append(Spacer(1, 6))

        open_ports = self._data.open_ports
        if open_ports:
            port_table_data = [["Port", "Status", "Layanan Umum (Estimasi)"]]
            for p in open_ports:
                port_table_data.append([str(p), "TERBUKA", self._estimate_service(p)])

            p_table = Table(port_table_data, colWidths=[100, 150, 250])
            p_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(p_table)
        else:
            story.append(Paragraph("Tidak ada port terbuka yang ditemukan pada rentang tersebut.", normal_style))

        # Membangun PDF
        doc.build(story)
        print(f"[+] Laporan berhasil dieksport ke PDF: {self._filename}")


class JSONReportExporter(BaseReportExporter):
    """Mengeksport hasil pemindaian ke dokumen JSON."""

    def export(self):
        open_ports = self._data.open_ports
        data = {
            "target_host": self._data.target_host,
            "target_ip": self._data.target_ip,
            "port_range": {
                "start": self._data.start_port,
                "end": self._data.end_port
            },
            "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "scan_duration": self._data.scan_duration,
            "total_open_ports": len(open_ports),
            "open_ports": [
                {
                    "port": p,
                    "status": "OPEN",
                    "estimated_service": self._estimate_service(p)
                }
                for p in open_ports
            ]
        }

        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"[+] Laporan berhasil dieksport ke JSON: {self._filename}")
