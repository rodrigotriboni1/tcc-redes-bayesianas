import zipfile, re, sys
z = zipfile.ZipFile(sys.argv[1]); names = z.namelist()
sl = sorted([n for n in names if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)], key=lambda n: int(re.findall(r'\d+', n)[0]))
notes = [n for n in names if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', n)]
print('a) slides', len(sl), 'notesSlides', len(notes))
proib = [r'\bClaude\b', r'intelig[eê]ncia artificial', r'\bagentes?\b', r'factory', r'melhor modelo', r'\bvence', r'\bsuperior', r'assistente']
bad = []; small = []; out = []; titles = []
txt_all = ''
for n in names:
    if n.endswith('.xml') and (n.startswith('ppt/slides/') or n.startswith('ppt/notesSlides/') or n.startswith('ppt/charts/')):
        x = z.read(n).decode('utf8'); t = ' '.join(re.findall(r'<a:t>([^<]*)</a:t>', x))
        for p in proib:
            if re.search(p, t, re.I): bad.append((n, p))
        for sz in re.findall(r'\bsz="(\d+)"', x):
            if int(sz) < 1200: small.append((n, sz))
for i, n in enumerate(sl, 1):
    x = z.read(n).decode('utf8')
    sps = re.findall(r'<p:sp>.*?</p:sp>', x, re.S)
    # título: primeira caixa com sz=2400/2800 em negrito
    for sp in sps:
        if re.search(r'sz="2[48]00"[^>]*b="1"|b="1"[^>]*sz="2[48]00"', sp):
            titles.append((i, ''.join(re.findall(r'<a:t>([^<]*)</a:t>', sp)))); break
    else: titles.append((i, '(sem título)'))
    for sp in sps:
        if '<a:t>' in sp and re.search(r'sz="(\d+)"', sp):
            s = [int(v) for v in re.findall(r'sz="(\d+)"', sp)]
            t = ''.join(re.findall(r'<a:t>([^<]*)</a:t>', sp))
            if i <= 14 and min(s) < 2000 and not re.match(r'^\(|UFU|\d+$', t) : out.append(('corpo<20pt', i, t[:40], min(s)))
    for off, ext in re.findall(r'<a:off x="(-?\d+)" y="(-?\d+)"/>\s*<a:ext cx="(\d+)" cy="(\d+)"/>', x) and [((int(a),int(b)),(int(c),int(d))) for a,b,c,d in re.findall(r'<a:off x="(-?\d+)" y="(-?\d+)"/>\s*<a:ext cx="(\d+)" cy="(\d+)"/>', x)]:
        if off[0] < 0 or off[1] < 0 or off[0]+ext[0] > 12192000 or off[1]+ext[1] > 6858000: out.append(('fora', i, off, ext))
    rels = z.read(n.replace('slides/', 'slides/_rels/') + '.rels').decode()
    for tgt in re.findall(r'Target="\.\./media/([^"]+)"', rels):
        if 'ppt/media/' + tgt not in names: out.append(('img ausente', i, tgt))
print('b) proibidas:', bad or 'nenhuma')
print('c) sz<1200:', small or 'nenhum'); print('c/d) problemas:', out or 'nenhum')
print('e) ghost deck:'); [print(f'  {i:2d}. {t}  [{len(t)} car.]') for i, t in titles]
