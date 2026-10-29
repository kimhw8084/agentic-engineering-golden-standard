"""Publisher-only PDF renderer. Requires ReportLab; target/offline use does not.

Narrative source: docs/field-guide/content.json. This is explanatory material,
not a second policy source. No network, images, fonts or model calls are needed.
"""
from pathlib import Path
from hashlib import sha256
import argparse
from html import escape
import json
import tomllib

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(__file__).resolve().parents[1]
WIDTH = letter[0] - 88
BLACK, GRAY, PALE = colors.black, colors.HexColor('#666666'), colors.HexColor('#f3f3f3')
BODY = ParagraphStyle('Body', fontName='Helvetica', fontSize=10.5, leading=14.5,
                      textColor=BLACK, spaceAfter=9)
TITLE = ParagraphStyle('Title', parent=BODY, fontName='Helvetica-Bold', fontSize=22, leading=26, spaceAfter=12)
HEADING = ParagraphStyle('Heading', parent=BODY, fontName='Helvetica-Bold', fontSize=12, leading=16, spaceBefore=6, spaceAfter=5)
CELL = ParagraphStyle('Cell', parent=BODY, fontSize=9.4, leading=12.4, spaceAfter=0)
CODE = ParagraphStyle('Code', parent=BODY, fontName='Courier', fontSize=9.5, leading=15, spaceAfter=0)


def paragraph(text, style=BODY):
    return Paragraph(escape(text).replace('\n', '<br/>'), style)


def fit_lines(text, width, font='Helvetica', size=9):
    lines, line = [], ''
    for word in text.split():
        candidate = f'{line} {word}'.strip()
        if stringWidth(candidate, font, size) > width and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    return lines + ([line] if line else [])


class Flow(Flowable):
    def __init__(self, steps):
        super().__init__()
        self.steps = steps
        self.width, self.height = WIDTH, 64

    def draw(self):
        c, gap = self.canv, 12
        box = (self.width - gap*(len(self.steps)-1))/len(self.steps)
        for i, label in enumerate(self.steps):
            x = i*(box+gap)
            c.setFillColor(PALE)
            c.setStrokeColor(BLACK)
            c.setLineWidth(.7)
            c.rect(x, 13, box, 40, fill=1)
            c.setFillColor(BLACK)
            c.setFont('Helvetica-Bold', 8.8)
            lines = fit_lines(label, box-10, 'Helvetica-Bold', 8.8)
            for j, line in enumerate(lines):
                c.drawCentredString(x+box/2, 33+(len(lines)-1)*5-j*10, line)
            if i < len(self.steps)-1:
                end = x+box+gap-2
                c.line(x+box+2, 33, end, 33)
                c.line(end-3, 36, end, 33)
                c.line(end-3, 30, end, 33)


class Lanes(Flowable):
    def __init__(self, items):
        super().__init__()
        self.items = items
        self.width, self.height = WIDTH, len(items)*64+2

    def draw(self):
        c = self.canv
        for i, (title, text) in enumerate(self.items):
            y = self.height-(i+1)*64+10
            c.setFillColor(PALE if i % 2 == 0 else colors.white)
            c.setStrokeColor(BLACK)
            c.setLineWidth(.7)
            c.rect(0, y, self.width, 53, fill=1)
            c.setFillColor(BLACK)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(10, y+36, title)
            c.setFont('Helvetica', 9)
            for j, line in enumerate(fit_lines(text, self.width-20)):
                c.drawString(10, y+21-j*11, line)
            if i < len(self.items)-1:
                c.line(self.width/2, y, self.width/2, y-9)


def make_table(block):
    weights = block['widths']
    widths = [WIDTH*w/sum(weights) for w in weights]
    header_style = ParagraphStyle('Header', parent=CELL, fontName='Helvetica-Bold', textColor=colors.white)
    data = [[paragraph(v, header_style) for v in block['headers']]]
    data += [[paragraph(v, CELL) for v in row] for row in block['rows']]
    table = Table(data, colWidths=widths, hAlign='LEFT', repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLACK), ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, PALE]),
        ('GRID', (0,0), (-1,-1), .4, colors.HexColor('#d0d0d0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9), ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    return table


def build(destination):
    source = ROOT/'docs/field-guide/content.json'
    raw = source.read_bytes()
    guide = json.loads(raw)
    version = tomllib.loads((ROOT/'pyproject.toml').read_text())['project']['version']
    fingerprint = sha256(raw).hexdigest()[:12]
    for page in guide['pages']:
        for name in page['sources']:
            if not (ROOT/name).exists():
                raise ValueError(f'Unknown canonical source: {name}')
    destination.parent.mkdir(parents=True, exist_ok=True)
    seen = []
    def decorate(canvas, doc):
        number = doc.page
        seen.append(number)
        canvas.setTitle(guide['title'])
        canvas.setAuthor('Golden Standard reference project')
        canvas.setFillColor(GRAY)
        canvas.setFont('Helvetica', 8)
        canvas.drawString(44, 760, 'AGENTIC ENGINEERING GOLDEN STANDARD')
        canvas.drawRightString(568, 760, 'FIELD GUIDE')
        if number <= len(guide['pages']):
            names = guide['pages'][number-1]['sources']
            canvas.setFont('Helvetica', 7.2)
            for i, name in enumerate(names):
                canvas.drawString(44, 70-i*9, ('Sources  ' if i == 0 else '               ')+name)
        canvas.setFont('Helvetica', 7.5)
        canvas.drawString(44, 22, f'Reference {version}  |  Content {fingerprint}  |  Explanatory guide')
        canvas.drawRightString(568, 22, f'{number:02d} / {len(guide["pages"]):02d}')
    story = []
    for i, page in enumerate(guide['pages']):
        if i:
            story.append(PageBreak())
        story += [paragraph(page['title'], TITLE), paragraph(page['intro'])]
        for block in page['blocks']:
            kind = block['type']
            if kind == 'flow':
                story.append(Flow(block['steps']))
            elif kind == 'lanes':
                story.append(Lanes(block['items']))
            elif kind == 'table':
                story += [make_table(block), Spacer(1, 12)]
            elif kind == 'section':
                story += [paragraph(block['heading'], HEADING), paragraph(block['body'])]
            elif kind in ('callout', 'code'):
                text = (f'<b>{escape(block["title"])}</b><br/>'+escape(block['body'])) if kind == 'callout' else escape(block['text']).replace('\n','<br/>')
                table = Table([[Paragraph(text, BODY if kind == 'callout' else CODE)]], colWidths=[WIDTH])
                table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),
                    ('BOX',(0,0),(-1,-1),.6,BLACK), ('LEFTPADDING',(0,0),(-1,-1),12),
                    ('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),10),
                    ('BOTTOMPADDING',(0,0),(-1,-1),10)]))
                story += [table, Spacer(1, 10)]
            else:
                raise ValueError(f'Unknown block {kind}')
    doc = SimpleDocTemplate(str(destination), pagesize=letter, leftMargin=44, rightMargin=44,
                            topMargin=57, bottomMargin=90, pageCompression=1)
    doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
    if len(seen) != len(guide['pages']):
        raise ValueError(f'Layout overflow: {len(seen)} pages, expected {len(guide["pages"])}; inspect and revise')
    print(f'Field guide: {destination} ({len(seen)} pages, content {fingerprint})')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT/'output/pdf/agentic-engineering-field-guide.pdf')
    build(parser.parse_args().output)
