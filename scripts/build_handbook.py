"""Publisher-only handbook renderer: PDF, static offline HTML and Markdown.

Requires ReportLab only for authoring. All reading and reference checks remain
dependency-free. The JSON narrative explains existing canonical rules.
"""
from pathlib import Path
import argparse
from hashlib import sha256
from html import escape
import json
import math
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Flowable, Table, TableStyle

if __package__:
    from .build_field_guide import WIDTH, BODY, TITLE, HEADING, CELL, CODE, fit_lines
else:
    from build_field_guide import WIDTH, BODY, TITLE, HEADING, CELL, CODE, fit_lines

ROOT = Path(__file__).resolve().parents[1]
PALE = '#f3f3f3'


class Diagram(Flowable):
    """Shared vector primitives for the printable and browser documents."""
    def __init__(self, block):
        super().__init__()
        self.width, self.height, self.parts = WIDTH, 64, []
        kind = block['type']
        if kind == 'flow':
            steps, gap = block['steps'], 12
            width = (WIDTH-gap*(len(steps)-1))/len(steps)
            for i, label in enumerate(steps):
                x = i*(width+gap)
                self.box(x, 8, width, 43, label)
                if i < len(steps)-1:
                    self.line(x+width+1, 29, x+width+gap-1, 29)
        elif kind == 'decision':
            self.height = 188
            mid = WIDTH/2
            self.parts.append(('polygon', [(mid,1),(mid+111,41),(mid,81),(mid-111,41)]))
            lines=fit_lines(block['question'],130,'Helvetica-Bold',8.5)
            self.label(mid,44-(len(lines)-1)*5,block['question'],130,size=8.5,bold=True)
            self.box(8, 82, 236, 38, block['yes'])
            self.box(WIDTH-244, 82, 236, 38, block['no'])
            self.line(mid-111,41,126,82)
            self.line(mid+111,41,WIDTH-126,82)
            self.parts += [('text',(112,66,'Yes',8.5,True,'middle')),('text',(WIDTH-112,66,'No',8.5,True,'middle'))]
            self.line(126,120,mid,147)
            self.line(WIDTH-126,120,mid,147)
            self.box(42, 147, WIDTH-84, 32, block['after'])
        elif kind == 'sequence':
            actors, messages = block['actors'], block['messages']
            self.height = 44+25*len(messages)
            positions = [(i+.5)*WIDTH/len(actors) for i in range(len(actors))]
            for x, actor in zip(positions, actors):
                self.box(x-50, 0, 100, 27, actor, bold=True)
                self.line(x,27,x,self.height-5,arrow=False,dashed=True)
            for i, (a,b,label) in enumerate(messages):
                y = 45+i*25
                x1,x2 = positions[a], positions[b]
                if a == b:
                    self.line(x1,y,x1+35,y,arrow=False)
                    self.line(x1+35,y,x1+35,y+10,arrow=False)
                    self.line(x1+35,y+10,x1,y+10)
                    self.parts.append(('text',(x1+42,y+7,label,7.5,False,'start')))
                else:
                    self.parts.append(('text',((x1+x2)/2,y-5,label,7.6,False,'middle')))
                    self.line(x1,y,x2,y)
        elif kind == 'graph':
            self.height = 154
            pos = {key:(52+x*(WIDTH-104), 20+(1-y)*110) for key,_,x,y in block['nodes']}
            for a,b,evidence in block['edges']:
                x1,y1=pos[a];x2,y2=pos[b]
                dx,dy=x2-x1,y2-y1
                boundary=min(49/abs(dx) if dx else float('inf'),
                             17/abs(dy) if dy else float('inf'))
                self.line(x1+boundary*dx,y1+boundary*dy,
                          x2-boundary*dx,y2-boundary*dy,dashed=evidence=='assumed')
                if evidence == 'assumed':
                    self.parts.append(('text',((x1+x2)/2+28,(y1+y2)/2,'assumed',7.5,False,'start')))
            for key,label,_,_ in block['nodes']:
                x,y=pos[key]
                self.box(x-49,y-17,98,34,label)
        else:
            raise ValueError(kind)

    def line(self,x1,y1,x2,y2,arrow=True,dashed=False):
        self.parts.append(('line',(x1,y1,x2,y2,arrow,dashed)))

    def label(self,x,y,label,width,size=9,bold=False):
        lines = fit_lines(label,width,'Helvetica-Bold' if bold else 'Helvetica',size)
        for i,line in enumerate(lines):
            self.parts.append(('text',(x,y+i*10,line,size,bold,'middle')))

    def box(self,x,y,w,h,label,bold=False):
        self.parts.append(('rect',(x,y,w,h)))
        lines=fit_lines(label,w-12,'Helvetica-Bold' if bold else 'Helvetica',9)
        self.label(x+w/2,y+h/2+3-(len(lines)-1)*5,label,w-12,bold=bold)

    def draw(self):
        c,h=self.canv,self.height
        for kind,args in self.parts:
            c.setStrokeColor(colors.black);c.setFillColor(colors.black);c.setLineWidth(.65);c.setDash()
            if kind == 'rect':
                x,y,w,height=args;c.setFillColor(colors.HexColor(PALE));c.rect(x,h-y-height,w,height,fill=1)
            elif kind == 'polygon':
                path=c.beginPath();path.moveTo(args[0][0],h-args[0][1])
                for x,y in args[1:]:path.lineTo(x,h-y)
                path.close();c.setFillColor(colors.white);c.drawPath(path,fill=1,stroke=1)
            elif kind == 'text':
                x,y,text,size,bold,align=args;c.setFont('Helvetica-Bold' if bold else 'Helvetica',size)
                (c.drawCentredString if align=='middle' else c.drawString)(x,h-y,text)
            elif kind == 'line':
                x1,y1,x2,y2,arrow,dashed=args
                if dashed:c.setDash(3,3)
                c.line(x1,h-y1,x2,h-y2);c.setDash()
                if arrow:
                    angle=math.atan2(y2-y1,x2-x1)
                    for offset in (-.45,.45):
                        c.line(x2,h-y2,x2-5*math.cos(angle+offset),h-y2+5*math.sin(angle+offset))

    def svg(self):
        parts=[f'<svg viewBox="0 0 {WIDTH} {self.height}" role="img" aria-label="Instructional flow diagram" xmlns="http://www.w3.org/2000/svg">']
        for kind,a in self.parts:
            if kind=='rect':
                x,y,w,h=a;parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PALE}" stroke="black"/>')
            elif kind=='polygon':
                points=' '.join(f'{x},{y}' for x,y in a);parts.append(f'<polygon points="{points}" fill="white" stroke="black"/>')
            elif kind=='text':
                x,y,text,size,bold,align=a
                parts.append(f'<text x="{x}" y="{y}" text-anchor="{align}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}">{escape(text)}</text>')
            else:
                x1,y1,x2,y2,arrow,dashed=a
                dash=' stroke-dasharray="3 3"' if dashed else ''
                parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black"{dash}/>')
                if arrow:
                    angle=math.atan2(y2-y1,x2-x1)
                    for offset in (-.45,.45):
                        xx=x2-5*math.cos(angle+offset);yy=y2-5*math.sin(angle+offset)
                        parts.append(f'<line x1="{x2}" y1="{y2}" x2="{xx}" y2="{yy}" stroke="black"/>')
        return ''.join(parts)+'</svg>'


def rich(text, refs):
    text=escape(text).replace('\n','<br/>')
    return re.sub(r'\[(S\d+)\]',lambda m:f'<a href="{escape(refs[m[1]]["url"],quote=True)}">[{m[1]}]</a>',text)


def table_pdf(block):
    style=ParagraphStyle('BookCell',parent=CELL,fontSize=9,leading=11.5)
    head=ParagraphStyle('BookHead',parent=style,fontName='Helvetica-Bold',textColor=colors.white)
    data=[[Paragraph(escape(v),head) for v in block['headers']]]
    data += [[Paragraph(escape(v),style) for v in row] for row in block['rows']]
    weights=block['widths'];widths=[WIDTH*w/sum(weights) for w in weights]
    t=Table(data,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.black),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor(PALE)]),
        ('GRID',(0,0),(-1,-1),.4,colors.HexColor('#d0d0d0')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return t


def mermaid(block):
    kind=block['type']; lines=[]
    q=lambda s:s.replace('"',"'")
    if kind=='sequence':
        lines=['sequenceDiagram']+[f'    participant A{i} as {v}' for i,v in enumerate(block['actors'])]
        lines += [f'    A{a}->>A{b}: {v}' for a,b,v in block['messages']]
    elif kind=='decision':
        lines=['flowchart TD',f'    Q{{"{q(block["question"])}"}}',f'    Y["{q(block["yes"])}"]',f'    N["{q(block["no"])}"]',f'    E["{q(block["after"])}"]','    Q -->|Yes| Y','    Q -->|No| N','    Y --> E','    N --> E']
    elif kind=='graph':
        lines=['flowchart LR']+[f'    {k}["{q(label)}"]' for k,label,_,_ in block['nodes']]
        lines += [f'    {a} {"-.->" if v=="assumed" else "-->"} {b}' for a,b,v in block['edges']]
    else:
        lines=['flowchart LR']+[f'    A{i}["{q(v)}"]' for i,v in enumerate(block['steps'])]
        lines += [f'    A{i} --> A{i+1}' for i in range(len(block['steps'])-1)]
    return '```mermaid\n'+'\n'.join(lines)+'\n```\n'


def build(root,destination):
    raw=(root/'docs/handbook/content.json').read_bytes();book=json.loads(raw);refs=book['references']
    fingerprint=sha256(raw).hexdigest()[:12]
    for page in book['pages']:
        for name in page['local']:
            if not (root/name).exists():raise ValueError(f'Unknown canonical source: {name}')
        if any(k not in refs for k in page['refs']):raise ValueError('Unknown reference')
    destination.mkdir(parents=True,exist_ok=True)
    pdf=destination/'agentic-engineering-handbook.pdf';seen=[];story=[]
    md=[f'# {book["title"]}\n\n{book["subtitle"]}\n\nGenerated from content.json; explanatory, not a second policy source.\n\n## Contents\n']
    html=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(book['title'])+'</title><style>body{margin:0;background:#e6e6e6;color:#111;font:17px/1.55 Arial,sans-serif}main,nav{max-width:850px;margin:28px auto;background:white;padding:44px 52px}h1,h2,h3{line-height:1.2;color:black}h1{font-size:30px}h2{font-size:25px}h3{font-size:18px;margin-top:24px}a{color:black;text-decoration:underline}p{margin:12px 0}table{border-collapse:collapse;width:100%;font-size:14px;margin:18px 0}th{background:black;color:white}td,th{border:1px solid #ccc;padding:9px;text-align:left}tr:nth-child(even){background:#f3f3f3}.callout,pre{border:1px solid #888;background:#f5f5f5;padding:16px}pre{white-space:pre-wrap;font:14px/1.5 monospace}svg{display:block;width:100%;height:auto;margin:20px 0}footer{font-size:12px;color:#555;border-top:1px solid #ccc;margin-top:24px;padding-top:10px}.chapter{scroll-margin-top:15px}nav ol{columns:2;column-gap:36px}nav li{break-inside:avoid;margin-bottom:8px}@media(max-width:650px){main,nav{padding:22px;margin:0 0 14px}nav ol{columns:1}}@media print{body{background:white;font-size:11pt}nav{break-after:page}main{margin:0;padding:0;break-after:page;max-width:none}svg,table,.callout{break-inside:avoid}a{color:black}}</style><nav><h1>'+escape(book['title'])+'</h1><p>'+escape(book['subtitle'])+'</p><p>Static offline document. No JavaScript, remote fonts or network assets. Source '+fingerprint+'.</p><ol>']
    for i,page in enumerate(book['pages']):
        anchor=f'chapter-{i+1}'
        md.append(f'{i+1}. [{page["title"]}](#{anchor})\n')
        html.append(f'<li><a href="#{anchor}">{escape(page["title"])}</a></li>')
    html.append('</ol></nav>')
    def decorate(canvas,doc):
        n=doc.page;seen.append(n);canvas.setTitle(book['title']);canvas.setAuthor('Golden Standard reference project')
        canvas.setFillColor(colors.HexColor('#555555'));canvas.setFont('Helvetica',8)
        canvas.drawString(44,760,'AGENTIC ENGINEERING  |  FOUNDATIONS AND PRACTICE')
        canvas.drawRightString(568,760,'TECHNICAL HANDBOOK')
        if n<=len(book['pages']):
            page=book['pages'][n-1];canvas.bookmarkPage(f'p{n}');canvas.addOutlineEntry(page['title'],f'p{n}',0)
            sources=['Canonical: '+v for v in page['local']]
            if page['refs']:sources+=['Primary references: '+', '.join(page['refs'])+' (bibliography pages 37-38)']
            canvas.setFont('Helvetica',7)
            for i,line in enumerate(sources[:5]):canvas.drawString(44,72-i*9,line)
        canvas.setFont('Helvetica',7.5);canvas.drawString(44,22,f'Reference 2.0.0 | Narrative {fingerprint} | Synthetic examples unless stated')
        canvas.drawRightString(568,22,f'{n:02d} / {len(book["pages"]):02d}')
    for i,page in enumerate(book['pages']):
        if i:story.append(PageBreak())
        story += [Paragraph(escape(page['title']),TITLE),Paragraph(rich(page['intro'],refs),BODY)]
        anchor=f'chapter-{i+1}';md += [f'\n<a id="{anchor}"></a>\n\n## {i+1} {page["title"]}\n\n{page["intro"]}\n']
        html.append(f'<main class="chapter" id="{anchor}"><h2>{i+1:02d} {escape(page["title"])}</h2><p>{rich(page["intro"],refs)}</p>')
        for b in page['blocks']:
            kind=b['type']
            if kind in ('flow','sequence','graph','decision'):
                diagram=Diagram(b);story += [diagram,Spacer(1,9)];html.append(diagram.svg());md.append('\n'+mermaid(b))
            elif kind=='section':
                story += [Paragraph(escape(b['heading']),HEADING),Paragraph(rich(b['body'],refs),BODY)]
                html += [f'<h3>{escape(b["heading"])}</h3><p>{rich(b["body"],refs)}</p>'];md.append(f'\n### {b["heading"]}\n\n{b["body"]}\n')
            elif kind=='code':
                paragraph=Paragraph(escape(b['text']).replace('\n','<br/>'),CODE)
                t=Table([[paragraph]],colWidths=[WIDTH]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor(PALE)),('BOX',(0,0),(-1,-1),.5,colors.black),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),('LEFTPADDING',(0,0),(-1,-1),10)]))
                story += [t,Spacer(1,10)];html.append('<pre>'+escape(b['text'])+'</pre>');md.append('\n```text\n'+b['text']+'\n```\n')
            elif kind=='callout':
                paragraph=Paragraph('<b>'+escape(b['title'])+'</b><br/>'+rich(b['body'],refs),BODY)
                t=Table([[paragraph]],colWidths=[WIDTH]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor(PALE)),('BOX',(0,0),(-1,-1),.5,colors.black),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10)]))
                story += [t,Spacer(1,9)];html.append('<aside class="callout"><strong>'+escape(b['title'])+'</strong><p>'+rich(b['body'],refs)+'</p></aside>');md.append(f'\n**{b["title"]}**\n\n{b["body"]}\n')
            elif kind=='table':
                story += [table_pdf(b),Spacer(1,10)]
                html.append('<table><tr>'+''.join('<th>'+escape(v)+'</th>' for v in b['headers'])+'</tr>')
                for row in b['rows']:html.append('<tr>'+''.join('<td>'+rich(v,refs)+'</td>' for v in row)+'</tr>')
                html.append('</table>');md += ['\n| '+' | '.join(b['headers'])+' |\n','|'+'|'.join('---' for _ in b['headers'])+'|\n']
                md += ['| '+' | '.join(row)+' |\n' for row in b['rows']]
            elif kind=='reference':
                title=f'[{b["id"]}] {b["title"]}'
                small=ParagraphStyle('Reference',parent=BODY,fontSize=8.8,leading=11.5,spaceAfter=5)
                story += [Paragraph(escape(title),HEADING),Paragraph(f'<a href="{escape(b["url"],quote=True)}">{escape(b["url"])}</a>',small),Paragraph(escape(b['note']),small)]
                html.append('<h3>'+escape(title)+'</h3><p><a href="'+escape(b['url'],quote=True)+'">'+escape(b['url'])+'</a><br/>'+escape(b['note'])+'</p>');md.append(f'\n### {title}\n\n{b["url"]}\n\n{b["note"]}\n')
            else:raise ValueError(kind)
        footer='Canonical sources: '+'; '.join(page['local'])+'. Primary references: '+', '.join(page['refs'])+'.'
        html.append('<footer>'+escape(footer)+'<br/>Narrative '+fingerprint+'. <a href="#chapter-1">Return to start</a></footer></main>')
        local_links='; '.join(f'[{name}](../../{name})' for name in page['local'])
        md.append('\nCanonical sources: '+local_links+'. Primary references: '+', '.join(page['refs'])+'.\n')
    html.append('</html>')
    (destination/'agentic-engineering-handbook.html').write_text(''.join(html),encoding='utf-8')
    markdown=''.join(md)
    markdown=re.sub(r'(?<!\[)\[(S\d+)\](?!\()',lambda m:f'[{m[1]}]({refs[m[1]]["url"]})',markdown)
    (destination/'HANDBOOK.md').write_text(markdown,encoding='utf-8')
    doc=SimpleDocTemplate(str(pdf),pagesize=letter,leftMargin=44,rightMargin=44,topMargin=57,bottomMargin=90,pageCompression=1)
    doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
    if len(seen)!=len(book['pages']):raise ValueError(f'Layout overflow: {len(seen)} vs expected {len(book["pages"])} pages; inspect PDF before delivery')
    print(f'Handbook: {len(seen)} pages, narrative {fingerprint}, outputs in {destination}')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'output/pdf/handbook')
    args=parser.parse_args();build(ROOT,args.output)
