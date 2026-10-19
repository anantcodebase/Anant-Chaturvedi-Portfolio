from __future__ import annotations
import json, os, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
CONFIG = json.loads((ROOT/'site.config.json').read_text())

def site_url():
    explicit=os.getenv('SITE_URL') or CONFIG.get('siteUrl') or ''
    explicit=explicit.rstrip('/')
    repo=os.getenv('GITHUB_REPOSITORY','')
    if explicit: return explicit
    if repo and '/' in repo:
        owner,name=repo.split('/',1)
        return f'https://{owner}.github.io'
    return 'http://localhost:8000'

def base_path():
    explicit=os.getenv('BASE_PATH') or CONFIG.get('basePath') or ''
    explicit=explicit.strip('/')
    if explicit: return explicit
    repo=os.getenv('GITHUB_REPOSITORY','')
    if repo and '/' in repo:
        owner,name=repo.split('/',1)
        return '' if name==f'{owner}.github.io' else name
    return ''

BASE=base_path()
URL=site_url()
PREFIX = f'/{BASE}' if BASE else ''

def public_path(path:str)->str:
    path='/' + path.lstrip('/')
    return f'/{BASE}{path}' if BASE else path

def copy_tree():
    if DIST.exists(): shutil.rmtree(DIST)
    for source in ['assets','css','js','og']:
        shutil.copytree(ROOT/source, DIST/source)
    for f in ['favicon.svg','apple-touch-icon.svg','site.webmanifest']:
        shutil.copy2(ROOT/f, DIST/f)
    # copy HTML/source pages
    for html in ROOT.rglob('*.html'):
        if 'dist' in html.parts: continue
        rel=html.relative_to(ROOT)
        target=DIST/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        text=html.read_text()
        text=text.replace('__SITE_URL__', URL).replace('__BASE_PATH__', PREFIX)
        target.write_text(text)

def write_meta():
    routes=['/','/about/','/skills/','/projects/','/gaming/','/xlamus/','/contact/','/resume/']
    sitemap='''<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'''
    for route in routes:
        sitemap += f'  <url><loc>{URL}{public_path(route)}</loc></url>\n'
    sitemap += '</urlset>\n'
    (DIST/'sitemap.xml').write_text(sitemap)
    (DIST/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {URL}{public_path("/sitemap.xml")}\n')
    llms=(ROOT/'llms.txt').read_text() if (ROOT/'llms.txt').exists() else ''
    (DIST/'llms.txt').write_text(llms)
    manifest = {'name':'Anant Chaturvedi — XlaMus','short_name':'Anant / XlaMus','start_url':public_path('/'),'display':'standalone','background_color':'#050507','theme_color':'#050507','icons':[{'src':public_path('/favicon.svg'),'sizes':'64x64','type':'image/svg+xml'}]}
    (DIST/'site.webmanifest').write_text(json.dumps(manifest,separators=(',',':')))
    (DIST/'.nojekyll').write_text('')

def validate_build():
    unresolved=[]
    for html in DIST.rglob('*.html'):
        text=html.read_text()
        if '__BASE_PATH__' in text or '__SITE_URL__' in text:
            unresolved.append(str(html.relative_to(DIST)))
    if unresolved:
        raise RuntimeError('Unresolved URL templates in build output: '+', '.join(unresolved))

def main():
    copy_tree(); write_meta(); validate_build()
    print(f'Built {DIST}')
    print(f'URL={URL}')
    print(f'BASE_PATH=/{BASE}' if BASE else 'BASE_PATH=/')

if __name__=='__main__': main()
