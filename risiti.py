"""Utengenezaji wa risiti (PDF kwa reportlab; HTML kama reportlab haipo)."""
import html
import io
from xml.sax.saxutils import escape as _xml_escape

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    _REPORTLAB = True
except Exception:  # reportlab haijasakinishwa
    _REPORTLAB = False


def _safu(r):
    """Safu za risiti kutoka kwenye dict ya malipo."""
    return [
        ("Namba ya risiti (Order)", r.get("order_ref") or "-"),
        ("Namba ya Pesapal (Tracking)", r.get("tracking_id") or "-"),
        ("Namba ya uthibitisho", r.get("confirmation_code") or "-"),
        ("Mteja", r.get("username") or "-"),
        ("Huduma", "Ourworthlinks Business Premium Suite"),
        ("Kiasi", f"{r.get('sarafu', '')} {float(r.get('kiasi') or 0):,.2f}"),
        ("Njia ya malipo", r.get("payment_method") or "-"),
        ("Tarehe ya malipo", r.get("tarehe") or "-"),
        ("Muda wa Premium", f"Siku {r.get('siku_za_premium', 30)}"),
        ("Hali", "IMELIPWA (COMPLETED)"),
    ]


def tengeneza_pdf(r):
    """Hurejesha bytes za PDF, au None kama reportlab haipo."""
    if not _REPORTLAB:
        return None
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=20 * mm, bottomMargin=20 * mm, title="Risiti ya Malipo")
    st = getSampleStyleSheet()
    jina = ParagraphStyle("jina", parent=st["Title"], textColor=colors.HexColor("#D97706"), alignment=0)
    seli = ParagraphStyle("seli", parent=st["BodyText"], fontSize=10, leading=13)
    kidogo = ParagraphStyle("kidogo", parent=st["BodyText"], fontSize=8, textColor=colors.grey)

    data = [
        [Paragraph(_xml_escape(str(k)), seli), Paragraph(f"<b>{_xml_escape(str(v))}</b>", seli)]
        for k, v in _safu(r)
    ]
    jedwali = Table(data, colWidths=[60 * mm, 110 * mm])
    jedwali.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    doc.build([
        Paragraph("OURWORTHLINKS BUSINESS", jina),
        Paragraph("Risiti ya Malipo", st["Heading2"]),
        Spacer(1, 6 * mm),
        jedwali,
        Spacer(1, 8 * mm),
        Paragraph("Asante kwa kulipa. Hifadhi risiti hii kwa kumbukumbu.", kidogo),
    ])
    return buf.getvalue()


def tengeneza_html(r):
    """Risiti ya HTML (mbadala wakati reportlab haipo)."""
    e = html.escape
    mistari = "".join(
        f"<tr><td style='padding:8px;color:#555'>{e(str(k))}</td>"
        f"<td style='padding:8px;font-weight:600'>{e(str(v))}</td></tr>"
        for k, v in _safu(r)
    )
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Risiti</title></head>"
        "<body style='font-family:Arial,sans-serif;max-width:560px;margin:30px auto'>"
        "<h2 style='color:#D97706'>OURWORTHLINKS BUSINESS</h2><h3>Risiti ya Malipo</h3>"
        f"<table style='border-collapse:collapse;width:100%'>{mistari}</table>"
        "<p style='color:#777;font-size:12px'>Asante kwa kulipa. Hifadhi risiti hii kwa kumbukumbu.</p>"
        "</body></html>"
    )
