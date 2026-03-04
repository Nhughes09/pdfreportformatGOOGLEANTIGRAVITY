#!/usr/bin/env python3
"""
Anti-Vibecode PDF Report Generator
Rebuilds the Grid-Scale Energy Storage report using professional formatting.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ─── COLOR PALETTE ───────────────────────────────────────────
NAVY = HexColor("#1e3a8a")
DARK_SLATE = HexColor("#334155")
MEDIUM_SLATE = HexColor("#64748b")
LIGHT_SLATE = HexColor("#94a3b8")
SKY = HexColor("#0ea5e9")
VIOLET = HexColor("#8b5cf6")
EMERALD = HexColor("#10b981")
AMBER = HexColor("#f59e0b")
ROSE = HexColor("#f43f5e")
WHITE = HexColor("#ffffff")
BG_ALT = HexColor("#f8fafc")
BG_CALLOUT_SKY = HexColor("#f0f9ff")
BG_CALLOUT_VIOLET = HexColor("#faf5ff")
BORDER = HexColor("#e2e8f0")
BORDER_NAVY_LIGHT = HexColor("#1e3a8a")

REPORT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(REPORT_DIR, "..", "reports", "2025-11_grid-scale-energy-storage")

# ─── STYLES ──────────────────────────────────────────────────
def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'CoverTitle', fontName='Helvetica-Bold', fontSize=32,
        textColor=NAVY, leading=38, spaceAfter=8, alignment=TA_LEFT,
        letterSpacing=-0.5
    ))
    styles.add(ParagraphStyle(
        'CoverSubtitle', fontName='Helvetica', fontSize=16,
        textColor=MEDIUM_SLATE, leading=22, spaceAfter=14
    ))
    styles.add(ParagraphStyle(
        'CoverDesc', fontName='Helvetica', fontSize=11,
        textColor=DARK_SLATE, leading=17, spaceAfter=30
    ))
    styles.add(ParagraphStyle(
        'SectionNumber', fontName='Helvetica-Bold', fontSize=42,
        textColor=SKY, leading=48, spaceAfter=0
    ))
    styles.add(ParagraphStyle(
        'SectionTitle', fontName='Helvetica-Bold', fontSize=22,
        textColor=NAVY, leading=28, spaceAfter=6, letterSpacing=-0.3
    ))
    styles.add(ParagraphStyle(
        'SectionDesc', fontName='Helvetica', fontSize=11,
        textColor=MEDIUM_SLATE, leading=16, spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        'HHHeading2', fontName='Helvetica-Bold', fontSize=16,
        textColor=NAVY, leading=22, spaceAfter=8, spaceBefore=16,
        letterSpacing=-0.2
    ))
    styles.add(ParagraphStyle(
        'HHHeading3', fontName='Helvetica-Bold', fontSize=13,
        textColor=DARK_SLATE, leading=18, spaceAfter=6, spaceBefore=12
    ))
    styles.add(ParagraphStyle(
        'BodyText2', fontName='Helvetica', fontSize=10.5,
        textColor=DARK_SLATE, leading=17, spaceAfter=8,
        alignment=TA_JUSTIFY
    ))
    styles.add(ParagraphStyle(
        'Eyebrow', fontName='Helvetica-Bold', fontSize=9,
        textColor=SKY, leading=12, spaceAfter=4,
        tracking=200
    ))
    styles.add(ParagraphStyle(
        'ExhibitLabel', fontName='Helvetica-Bold', fontSize=9,
        textColor=SKY, leading=14, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        'SourceLine', fontName='Helvetica-Oblique', fontSize=8,
        textColor=LIGHT_SLATE, leading=12, spaceBefore=4, spaceAfter=16
    ))
    styles.add(ParagraphStyle(
        'BulletBody', fontName='Helvetica', fontSize=10.5,
        textColor=DARK_SLATE, leading=17, spaceAfter=6,
        bulletIndent=20, leftIndent=30
    ))
    styles.add(ParagraphStyle(
        'CalloutHead', fontName='Helvetica-Bold', fontSize=9,
        textColor=SKY, leading=14, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'CalloutBody', fontName='Helvetica', fontSize=10,
        textColor=DARK_SLATE, leading=16, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'TOCEntry', fontName='Helvetica', fontSize=11,
        textColor=DARK_SLATE, leading=20, leftIndent=20
    ))
    styles.add(ParagraphStyle(
        'TOCSection', fontName='Helvetica-Bold', fontSize=11,
        textColor=NAVY, leading=22
    ))
    styles.add(ParagraphStyle(
        'MetaLabel', fontName='Helvetica-Bold', fontSize=8,
        textColor=MEDIUM_SLATE, leading=12
    ))
    styles.add(ParagraphStyle(
        'MetaValue', fontName='Helvetica', fontSize=10,
        textColor=DARK_SLATE, leading=14
    ))
    styles.add(ParagraphStyle(
        'Footer', fontName='Helvetica', fontSize=8,
        textColor=LIGHT_SLATE, leading=11
    ))
    return styles


# ─── HELPER FUNCTIONS ────────────────────────────────────────
def zebra_table(data, col_widths=None, has_total=False):
    """Create a professional zebra-striped table."""
    style_cmds = [
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('TEXTCOLOR', (0, 0), (-1, 0), NAVY),
        ('BACKGROUND', (0, 0), (-1, 0), BG_ALT),
        ('LINEBELOW', (0, 0), (-1, 0), 2, NAVY),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9.5),
        ('TEXTCOLOR', (0, 1), (-1, -1), DARK_SLATE),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 1), (-1, -2), 0.5, BORDER),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]
    # Zebra striping
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), BG_ALT))
        else:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), WHITE))

    if has_total:
        last = len(data) - 1
        style_cmds.append(('LINEABOVE', (0, last), (-1, last), 2, NAVY))
        style_cmds.append(('BACKGROUND', (0, last), (-1, last), BG_CALLOUT_SKY))
        style_cmds.append(('FONTNAME', (0, last), (-1, last), 'Helvetica-Bold'))
        style_cmds.append(('TEXTCOLOR', (0, last), (-1, last), NAVY))

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(style_cmds))
    return t


def callout_box(title, body, border_color=SKY, bg_color=BG_CALLOUT_SKY):
    """Create a callout box with colored left border."""
    data = [[Paragraph(f'<b>{title}</b>', ParagraphStyle(
        'cb_title', fontName='Helvetica-Bold', fontSize=9,
        textColor=border_color, leading=14
    )), ''],
    [Paragraph(body, ParagraphStyle(
        'cb_body', fontName='Helvetica', fontSize=10,
        textColor=DARK_SLATE, leading=16
    )), '']]

    t = Table(data, colWidths=[6*inch, 0])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
        ('TOPPADDING', (0, 0), (0, 0), 12),
        ('BOTTOMPADDING', (-1, -1), (-1, -1), 12),
        ('LINEBELOW', (0, 0), (-1, -1), 0, bg_color),
        ('LINEBEFORE', (0, 0), (0, -1), 3, border_color),
    ]))
    return t


def section_page(number, title, desc, styles):
    """Create a section title page."""
    elements = [
        PageBreak(),
        Spacer(1, 1.5*inch),
        Paragraph(f'{number:02d}.', styles['SectionNumber']),
        Paragraph(title, styles['SectionTitle']),
        HRFlowable(width="100%", thickness=1, color=BORDER, spaceAfter=12),
        Paragraph(desc, styles['SectionDesc']),
    ]
    return elements


# ─── HEADER / FOOTER ────────────────────────────────────────
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(LIGHT_SLATE)
    canvas.drawRightString(7.5*inch, 0.5*inch, f"{doc.page}")
    canvas.drawString(1.25*inch, 0.5*inch, "HHeuristics  •  Grid-Scale Energy Storage Systems")
    # Top line
    if doc.page > 1:
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.5)
        canvas.line(1.25*inch, 10.2*inch, 7.5*inch, 10.2*inch)
    canvas.restoreState()


# ─── BUILD THE REPORT ────────────────────────────────────────
def build_report():
    output_path = os.path.join(ASSETS_DIR, "Grid_Scale_Energy_Storage_REFORMATTED.pdf")
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=1*inch,
        bottomMargin=1*inch,
        leftMargin=1.25*inch,
        rightMargin=1*inch
    )

    styles = get_styles()
    story = []

    # ════════════════════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.5*inch))

    # Cover image if it exists
    cover_img = os.path.join(ASSETS_DIR, "cover.png")
    if os.path.exists(cover_img):
        story.append(Image(cover_img, width=5.5*inch, height=7.1*inch))
    else:
        story.append(Paragraph("Grid-Scale Energy<br/>Storage Systems", styles['CoverTitle']))
        story.append(Paragraph("Market Outlook 2025–2030", styles['CoverSubtitle']))
        story.append(Spacer(1, 20))
        story.append(Paragraph(
            "Comprehensive analysis of battery storage technologies, market dynamics, "
            "competitive landscape, and strategic opportunities in the global energy transition.",
            styles['CoverDesc']
        ))
        story.append(Spacer(1, 30))
        story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=16))

        meta_data = [
            ['PUBLICATION DATE', 'REPORT LENGTH', 'REPORT ID'],
            ['November 2025', '38 Pages', 'HH-ER-2025-047'],
        ]
        meta_table = Table(meta_data, colWidths=[2*inch, 2*inch, 2*inch])
        meta_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('TEXTCOLOR', (0, 0), (-1, 0), MEDIUM_SLATE),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, 1), 11),
            ('TEXTCOLOR', (0, 1), (-1, 1), DARK_SLATE),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LINEBELOW', (0, 0), (-1, 0), 0, WHITE),
        ]))
        story.append(meta_table)

        story.append(Spacer(1, 2*inch))
        story.append(Paragraph("www.hheuristics.com", styles['Footer']))
        story.append(Paragraph("© 2025 HHeuristics. All Rights Reserved.", styles['Footer']))

    # ════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Table of Contents", styles['SectionTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER, spaceAfter=20))

    toc_entries = [
        ("1.", "Executive Summary", "3"),
        ("2.", "Market Size & Growth Forecast", "5"),
        ("3.", "Technology Analysis", "12"),
        ("4.", "Competitive Landscape", "18"),
        ("5.", "Market Dynamics & Business Models", "22"),
        ("6.", "Regional Deep Dives", "26"),
        ("7.", "Regulatory & Policy Environment", "30"),
        ("8.", "Strategic Recommendations", "34"),
        ("9.", "Methodology & Sources", "37"),
    ]
    for num, title, page in toc_entries:
        toc_text = f'<b><font color="#1e3a8a">{num}</font></b>  {title}'
        row = Table(
            [[Paragraph(toc_text, styles['TOCEntry']),
              Paragraph(page, ParagraphStyle('tocpage', fontName='Helvetica',
                  fontSize=11, textColor=LIGHT_SLATE, alignment=TA_RIGHT))]],
            colWidths=[5*inch, 1.25*inch]
        )
        row.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, BORDER),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ]))
        story.append(row)

    story.append(Spacer(1, 30))
    story.append(Paragraph("EXHIBITS", styles['Eyebrow']))
    story.append(Spacer(1, 8))

    exhibits = [
        ("Exhibit 1:", "Global Grid-Scale Storage Capacity & Revenue (2020–2030F)", "6"),
        ("Exhibit 2:", "Market Revenue by Technology Segment", "8"),
        ("Exhibit 3:", "Annual Deployment by Region (GW)", "10"),
        ("Exhibit 4:", "Battery Technology Comparison Matrix", "12"),
        ("Exhibit 5:", "Lithium-ion Battery Pack Cost Decline", "14"),
        ("Exhibit 6:", "Competitive Market Share Analysis (2024)", "19"),
        ("Exhibit 7:", "Revenue Stream Analysis", "22"),
        ("Exhibit 8:", "Revenue Stack by Market", "24"),
        ("Exhibit 9:", "Investment Decision Framework", "34"),
    ]
    for label, title, page in exhibits:
        row = Table(
            [[Paragraph(f'<font color="#0ea5e9"><b>{label}</b></font> {title}',
                styles['TOCEntry']),
              Paragraph(page, ParagraphStyle('tocpage2', fontName='Helvetica',
                  fontSize=11, textColor=LIGHT_SLATE, alignment=TA_RIGHT))]],
            colWidths=[5*inch, 1.25*inch]
        )
        row.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, BORDER),
            ('TOPPADDING', (0, 0), (-1, 0), 4),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ]))
        story.append(row)

    # ════════════════════════════════════════════════════════
    # 1. EXECUTIVE SUMMARY
    # ════════════════════════════════════════════════════════
    story.extend(section_page(1, "Executive Summary",
        "Key findings and strategic implications from our analysis of the global grid-scale energy storage market.", styles))

    story.append(Paragraph(
        "The global grid-scale energy storage market is entering a transformative period of "
        "mainstream adoption, driven by accelerating renewable energy deployment, declining "
        "battery costs, and increasingly supportive policy frameworks. This report provides "
        "a comprehensive analysis of the market's trajectory through 2030.",
        styles['BodyText2']
    ))
    story.append(Spacer(1, 12))

    # Key findings as bold lead-in bullets
    findings = [
        ("<b>Market Scale:</b> The global grid-scale storage market reached an estimated $15.8 billion "
         "in revenue in 2024, with cumulative installed capacity surpassing 110 GW. We project the "
         "market to reach $47.2 billion by 2030, representing a compound annual growth rate (CAGR) of 20.1%."),
        ("<b>Technology Leadership:</b> Lithium iron phosphate (LFP) chemistry has emerged as the dominant "
         "technology for utility-scale applications, capturing 70% of market revenue in 2024. LFP's "
         "superior safety profile, longer cycle life (6,000+ cycles), and lower cost have driven this transition."),
        ("<b>Regional Dynamics:</b> China leads global deployment with 45% of annual installations, followed "
         "by the United States (28%) and Europe (15%). The U.S. market has accelerated dramatically "
         "following the Inflation Reduction Act (IRA)."),
        ("<b>Emerging Technologies:</b> Sodium-ion batteries entered commercial deployment in 2024 and are "
         "projected to capture 8–12% of the grid-scale market by 2030. Long-duration energy storage (LDES) "
         "technologies are attracting significant investment."),
        ("<b>Competitive Landscape:</b> CATL maintains market leadership with 34% share, followed by BYD (18%) "
         "and Tesla (13%). Software capabilities have emerged as a critical source of competitive differentiation."),
    ]

    for finding in findings:
        story.append(Paragraph(f"•  {finding}", styles['BulletBody']))

    story.append(Spacer(1, 16))
    story.append(callout_box(
        "KEY FINDING",
        "Battery pack costs have declined approximately 90% since 2010 — from over $1,100/kWh to ~$139/kWh "
        "in 2024 — making storage economically competitive with conventional peaking generation across an "
        "expanding range of applications and geographies."
    ))

    # ════════════════════════════════════════════════════════
    # 2. MARKET SIZE & GROWTH
    # ════════════════════════════════════════════════════════
    story.extend(section_page(2, "Market Size & Growth Forecast",
        "Global market overview, technology segmentation, and regional deployment analysis.", styles))

    story.append(Paragraph("2.1 Global Market Overview", styles['HHHeading2']))
    story.append(Paragraph(
        "The global grid-scale energy storage market has experienced exceptional growth over the "
        "past five years, with installed capacity expanding from approximately 17 GW in 2020 to over "
        "85 GW by end of 2024 — a compound annual growth rate of 49.6% in capacity terms. Market "
        "revenues have grown commensurately, rising from $4.8 billion in 2020 to an estimated "
        "$15.8 billion in 2024.",
        styles['BodyText2']
    ))

    # Revenue chart
    chart_img = os.path.join(ASSETS_DIR, "chart_revenue.png")
    if os.path.exists(chart_img):
        story.append(Spacer(1, 8))
        story.append(Paragraph("EXHIBIT 1: GLOBAL GRID-SCALE STORAGE REVENUE", styles['ExhibitLabel']))
        story.append(Image(chart_img, width=5.5*inch, height=4.2*inch))
        story.append(Paragraph("Source: HHeuristics analysis; BloombergNEF; Wood Mackenzie", styles['SourceLine']))

    # Main data table
    story.append(Paragraph("EXHIBIT 1: GLOBAL GRID-SCALE STORAGE CAPACITY & REVENUE (2020–2030F)", styles['ExhibitLabel']))

    market_data = [
        ['YEAR', 'CUMULATIVE\nCAPACITY (GW)', 'ANNUAL\nADDITIONS (GW)', 'MARKET\nREVENUE ($B)', 'YoY\nGROWTH'],
        ['2020', '17.4', '4.7', '$4.8', '—'],
        ['2021', '27.2', '9.8', '$6.9', '44%'],
        ['2022', '43.4', '16.2', '$9.4', '36%'],
        ['2023', '68.7', '25.3', '$12.1', '29%'],
        ['2024E', '110.5', '41.8', '$15.8', '31%'],
        ['2025F', '163.2', '52.7', '$20.2', '28%'],
        ['2026F', '225.8', '62.6', '$25.4', '26%'],
        ['2027F', '299.1', '73.3', '$31.2', '23%'],
        ['2028F', '383.7', '84.6', '$37.8', '21%'],
        ['2029F', '478.4', '94.7', '$42.4', '12%'],
        ['2030F', '585.0', '106.6', '$47.2', '11%'],
    ]
    story.append(zebra_table(market_data, col_widths=[0.9*inch, 1.3*inch, 1.3*inch, 1.2*inch, 0.8*inch]))
    story.append(Paragraph("Source: HHeuristics analysis; BloombergNEF; Wood Mackenzie; company disclosures", styles['SourceLine']))

    # Forecast scenarios callout
    story.append(callout_box(
        "FORECAST SCENARIOS",
        "• <b>Bull Case ($58B by 2030):</b> Accelerated policy support, faster cost declines, breakthrough in LDES technologies<br/>"
        "• <b>Base Case ($47B by 2030):</b> Continued policy support, gradual cost reductions, moderate supply chain constraints<br/>"
        "• <b>Bear Case ($38B by 2030):</b> Policy reversals, persistent supply chain disruptions, slower renewable deployment"
    ))

    story.append(Spacer(1, 16))
    story.append(Paragraph("2.2 Market Segmentation by Technology", styles['HHHeading2']))
    story.append(Paragraph(
        "Lithium-ion technology continues to dominate the grid-scale storage market, accounting for "
        "92% of new capacity additions in 2024. However, the technology mix is evolving as sodium-ion "
        "and long-duration storage technologies gain traction.",
        styles['BodyText2']
    ))

    # Technology pie chart
    tech_img = os.path.join(ASSETS_DIR, "chart_technology.png")
    if os.path.exists(tech_img):
        story.append(Paragraph("EXHIBIT 2: MARKET SHARE BY TECHNOLOGY (2024)", styles['ExhibitLabel']))
        story.append(Image(tech_img, width=4.5*inch, height=4.2*inch))
        story.append(Paragraph("Source: HHeuristics analysis", styles['SourceLine']))

    # Technology table
    story.append(Paragraph("EXHIBIT 2: MARKET REVENUE BY TECHNOLOGY SEGMENT (2024 VS. 2030F)", styles['ExhibitLabel']))
    tech_data = [
        ['TECHNOLOGY', '2024\nREVENUE', '2024\nSHARE', '2030F\nREVENUE', '2030F\nSHARE', 'CAGR'],
        ['Lithium-ion (LFP)', '$11.1B', '70%', '$28.3B', '60%', '16.9%'],
        ['Lithium-ion (NMC)', '$2.8B', '18%', '$5.2B', '11%', '10.8%'],
        ['Sodium-ion', '$0.3B', '2%', '$4.2B', '9%', '54.8%'],
        ['Flow Batteries', '$0.6B', '4%', '$3.3B', '7%', '32.7%'],
        ['Other LDES', '$0.2B', '1%', '$2.8B', '6%', '55.2%'],
        ['Pumped Hydro', '$0.8B', '5%', '$3.4B', '7%', '27.3%'],
        ['Total', '$15.8B', '100%', '$47.2B', '100%', '20.1%'],
    ]
    story.append(zebra_table(tech_data,
        col_widths=[1.4*inch, 0.85*inch, 0.7*inch, 0.85*inch, 0.7*inch, 0.7*inch], has_total=True))
    story.append(Paragraph("Source: HHeuristics analysis; BloombergNEF", styles['SourceLine']))

    story.append(callout_box(
        "TECHNOLOGY OUTLOOK",
        "Sodium-ion batteries are projected to capture 8–12% of the grid-scale storage market by 2030, "
        "primarily displacing LFP in cost-sensitive applications. The technology is particularly "
        "attractive in markets seeking to reduce dependence on lithium supply chains.",
        border_color=VIOLET, bg_color=BG_CALLOUT_VIOLET
    ))

    # ════════════════════════════════════════════════════════
    # 3. TECHNOLOGY ANALYSIS
    # ════════════════════════════════════════════════════════
    story.extend(section_page(3, "Technology Analysis",
        "Comprehensive assessment of current and emerging storage technologies.", styles))

    story.append(Paragraph("3.1 Technology Overview", styles['HHHeading2']))
    story.append(Paragraph(
        "Grid-scale energy storage encompasses a diverse range of technologies, each with distinct "
        "performance characteristics, cost structures, and optimal applications.",
        styles['BodyText2']
    ))

    story.append(Paragraph("EXHIBIT 4: BATTERY TECHNOLOGY COMPARISON MATRIX", styles['ExhibitLabel']))
    battery_data = [
        ['PARAMETER', 'Li-ion\n(LFP)', 'Li-ion\n(NMC)', 'SODIUM-\nION', 'VANADIUM\nFLOW', 'IRON-AIR'],
        ['Energy Density (Wh/L)', '250–350', '400–600', '150–250', '25–35', '750–1,000'],
        ['Cycle Life', '4,000–\n8,000', '2,000–\n4,000', '3,000–\n6,000', '15,000–\n20,000', '3,000–\n5,000'],
        ['Round-trip Efficiency', '92–96%', '90–94%', '88–92%', '70–80%', '45–55%'],
        ['Duration Sweet Spot', '2–4 hrs', '2–4 hrs', '2–6 hrs', '4–12 hrs', '24–100 hrs'],
        ['Capital Cost ($/kWh)', '$150–200', '$180–250', '$100–150', '$350–500', '$50–100\n(target)'],
        ['Commercial Maturity', 'Mature', 'Mature', 'Early\ncommercial', 'Commercial', 'Demo'],
        ['Safety Profile', 'Good', 'Moderate', 'Excellent', 'Excellent', 'Excellent'],
    ]
    story.append(zebra_table(battery_data,
        col_widths=[1.3*inch, 0.85*inch, 0.85*inch, 0.85*inch, 0.92*inch, 0.85*inch]))
    story.append(Paragraph("Source: HHeuristics analysis; BNEF; NREL; manufacturer specifications", styles['SourceLine']))

    story.append(Paragraph("3.2 Lithium-Ion Technologies", styles['HHHeading2']))
    story.append(Paragraph("Lithium Iron Phosphate (LFP)", styles['HHHeading3']))
    story.append(Paragraph(
        "LFP chemistry has become the dominant technology for grid-scale storage applications, "
        "capturing 78% of utility-scale deployments in 2024. Key advantages include:",
        styles['BodyText2']
    ))

    lfp_points = [
        "<b>Superior safety:</b> Inherently stable chemistry with minimal thermal runaway risk",
        "<b>Longer cycle life:</b> 6,000+ cycles at 80% depth of discharge, enabling 15–20 year project lifetimes",
        "<b>Lower cost:</b> Freedom from cobalt and nickel supply constraints; costs approaching $130/kWh at pack level",
        "<b>Supply chain security:</b> Mature manufacturing base, primarily in China",
    ]
    for pt in lfp_points:
        story.append(Paragraph(f"•  {pt}", styles['BulletBody']))

    # Cost decline table
    story.append(Spacer(1, 12))
    story.append(Paragraph("EXHIBIT 5: LITHIUM-ION BATTERY PACK COST DECLINE ($/KWH)", styles['ExhibitLabel']))
    cost_data = [
        ['YEAR', 'LFP PACK PRICE', 'NMC PACK PRICE', 'LFP YoY CHANGE'],
        ['2018', '$176', '$185', '—'],
        ['2019', '$156', '$161', '-11%'],
        ['2020', '$137', '$140', '-12%'],
        ['2021', '$132', '$138', '-4%'],
        ['2022', '$153', '$165', '+16%'],
        ['2023', '$130', '$149', '-15%'],
        ['2024E', '$115', '$139', '-12%'],
        ['2026F', '$98', '$118', '—'],
        ['2028F', '$89', '$108', '—'],
        ['2030F', '$82', '$98', '—'],
    ]
    story.append(zebra_table(cost_data, col_widths=[1*inch, 1.4*inch, 1.4*inch, 1.4*inch]))
    story.append(Paragraph("Source: BloombergNEF; BNEF Battery Price Survey; HHeuristics analysis", styles['SourceLine']))

    # ════════════════════════════════════════════════════════
    # 4. COMPETITIVE LANDSCAPE
    # ════════════════════════════════════════════════════════
    story.extend(section_page(4, "Competitive Landscape",
        "Market structure, leading competitors, and competitive dynamics.", styles))

    story.append(Paragraph("4.1 Market Structure", styles['HHHeading2']))
    story.append(Paragraph(
        "The grid-scale energy storage market features a complex competitive landscape with "
        "participants across multiple segments of the value chain. The market exhibits increasing "
        "vertical integration, with leading cell manufacturers expanding into system integration and "
        "software capabilities emerging as a critical source of competitive differentiation.",
        styles['BodyText2']
    ))

    story.append(Paragraph("EXHIBIT 6: COMPETITIVE MARKET SHARE ANALYSIS (2024)", styles['ExhibitLabel']))
    comp_data = [
        ['COMPANY', 'HQ', 'PRIMARY POSITION', '2024 REV ($B)', 'MARKET SHARE'],
        ['CATL', 'China', 'Cell Manufacturer', '$5.4', '34%'],
        ['BYD', 'China', 'Integrated', '$2.8', '18%'],
        ['Tesla', 'United States', 'System Integrator', '$2.1', '13%'],
        ['Fluence', 'United States', 'System Integrator', '$1.4', '9%'],
        ['Samsung SDI', 'South Korea', 'Cell Manufacturer', '$0.8', '5%'],
        ['LG Energy Sol.', 'South Korea', 'Cell Manufacturer', '$0.7', '4%'],
        ['Sungrow', 'China', 'Integrated', '$0.9', '6%'],
        ['Others', 'Various', 'Various', '$1.7', '11%'],
        ['Total', '', '', '$15.8', '100%'],
    ]
    story.append(zebra_table(comp_data,
        col_widths=[1.2*inch, 0.9*inch, 1.3*inch, 1.0*inch, 1.0*inch], has_total=True))
    story.append(Paragraph("Source: Company filings; HHeuristics analysis", styles['SourceLine']))

    # ════════════════════════════════════════════════════════
    # 8. STRATEGIC RECOMMENDATIONS
    # ════════════════════════════════════════════════════════
    story.extend(section_page(8, "Strategic Recommendations",
        "Investment framework and market entry prioritization for key stakeholders.", styles))

    story.append(Paragraph("8.1 Market Entry Prioritization", styles['HHHeading2']))
    story.append(Paragraph(
        "For organizations considering geographic expansion, HHeuristics recommends prioritizing "
        "markets based on the following criteria:",
        styles['BodyText2']
    ))

    priority_data = [
        ['PRIORITY', 'MARKET', 'RATIONALE'],
        ['1 (Highest)', 'United States\n(ERCOT, CAISO)', 'IRA incentives; large pipeline;\nsophisticated markets'],
        ['2', 'United Kingdom', 'Mature market; strong revenue\nopportunities; clear policy'],
        ['3', 'Australia', 'High renewables; price volatility;\nsupportive state policies'],
        ['4', 'Germany / Italy', 'Growing markets; EU policy support;\ngrid needs'],
        ['5', 'India', 'High growth potential; scale\nopportunity; execution risk'],
    ]
    story.append(zebra_table(priority_data, col_widths=[1*inch, 1.6*inch, 2.8*inch]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("8.2 Risk Factors", styles['HHHeading2']))
    risks = [
        "<b>Policy risk:</b> Changes to incentive programs or market rules",
        "<b>Supply chain disruption:</b> Raw material shortages; geopolitical tensions",
        "<b>Technology risk:</b> Faster-than-expected obsolescence; safety incidents",
        "<b>Market saturation:</b> Oversupply in certain markets reducing revenue",
        "<b>Execution risk:</b> Interconnection delays; cost overruns; operational issues",
    ]
    for r in risks:
        story.append(Paragraph(f"•  {r}", styles['BulletBody']))

    # ════════════════════════════════════════════════════════
    # 9. METHODOLOGY
    # ════════════════════════════════════════════════════════
    story.extend(section_page(9, "Methodology & Sources",
        "Research methodology, data sources, and limitations.", styles))

    story.append(Paragraph("9.1 Research Methodology", styles['HHHeading2']))
    story.append(Paragraph(
        "This report was developed using HHeuristics' proprietary research methodology, "
        "integrating multiple data sources and analytical approaches.",
        styles['BodyText2']
    ))

    story.append(Paragraph("Primary Research", styles['HHHeading3']))
    primary = [
        "In-depth interviews with 18 industry executives spanning manufacturers, developers, utilities, and investors",
        "Survey of 45 project developers on market conditions and investment priorities",
        "Site visits to manufacturing facilities and operational storage projects",
    ]
    for p in primary:
        story.append(Paragraph(f"•  {p}", styles['BulletBody']))

    story.append(Paragraph("Data Sources", styles['HHHeading3']))
    sources = [
        "BloombergNEF Energy Storage Outlook and Battery Price Survey",
        "Wood Mackenzie Global Energy Storage Service",
        "International Energy Agency (IEA) World Energy Outlook",
        "U.S. Energy Information Administration (EIA)",
        "National laboratory reports (NREL, Sandia, PNNL)",
    ]
    for s in sources:
        story.append(Paragraph(f"•  {s}", styles['BulletBody']))

    # ════════════════════════════════════════════════════════
    # DISCLAIMER
    # ════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Spacer(1, 2*inch))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER, spaceAfter=20))
    story.append(Paragraph(
        "<i>Disclaimer: This report is provided for informational purposes only and does not constitute "
        "investment advice. HHeuristics makes no representations or warranties regarding the accuracy "
        "or completeness of the information contained herein. Readers should conduct their own due "
        "diligence before making investment decisions. Past performance is not indicative of future "
        "results. © 2025 HHeuristics. All rights reserved. No part of this publication may be reproduced "
        "without prior written permission.</i>",
        ParagraphStyle('disclaimer', fontName='Helvetica', fontSize=9,
            textColor=LIGHT_SLATE, leading=14, alignment=TA_JUSTIFY)
    ))
    story.append(Spacer(1, 30))
    story.append(Paragraph("9.4 About HHeuristics", styles['HHHeading3']))
    story.append(Paragraph(
        "HHeuristics provides in-depth, data-driven market research reports across a wide range of "
        "industries, offering actionable insights for investors, executives, policymakers, and analysts.",
        styles['BodyText2']
    ))
    story.append(Spacer(1, 16))

    contact = [
        ['Website:', 'www.hheuristics.com'],
        ['Email:', 'research@hheuristics.com'],
        ['Reports:', 'Available at MarketResearch.com'],
    ]
    ct = Table(contact, colWidths=[1.2*inch, 3*inch])
    ct.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_SLATE),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(ct)

    # ─── BUILD ───
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"✅ Report generated: {output_path}")
    return output_path


if __name__ == "__main__":
    build_report()
