"""Render English layout references using headless Chromium, for final project assets."""
from pathlib import Path
import json
import base64
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'store-assets'/'references'
OUT.mkdir(parents=True,exist_ok=True)
C=json.loads((ROOT/'manifest.json').read_text('utf-8-sig'))['theme']['colors']
def color(k): return '#%02X%02X%02X'%tuple(C[k])
css=f''':root{{--milk:{color('ntp_background')};--oat:{color('toolbar')};--sand:{color('frame')};--ink:{color('ntp_text')};--taupe:{color('frame_inactive')};}}'''+'''
*{box-sizing:border-box}body{margin:0;color:var(--ink);font-family:Arial,sans-serif;background:var(--milk)}
.browser{width:1280px;height:800px;background:var(--milk);position:relative;overflow:hidden}
.tabs{height:44px;background:var(--sand);display:flex;align-items:end;padding:6px 12px;gap:10px;padding-bottom:0}
.tab{height:37px;width:235px;padding:12px 18px;font-size:13px;border-radius:12px 12px 0 0}.active{background:var(--oat)}.close{float:right}
.tools{height:56px;background:var(--oat);display:flex;align-items:center;padding:0 20px;gap:24px;font-size:20px}.omni{height:36px;border-radius:22px;background:var(--milk);flex:1;font-size:13px;padding:11px 18px}.bookmarks{height:32px;background:var(--oat);font-size:12px;display:flex;gap:30px;padding:6px 22px}
.content{text-align:center;padding-top:118px}.google{font-size:80px;letter-spacing:-4px;color:var(--sand);margin-bottom:26px}.search{width:560px;height:54px;border-radius:30px;background:white;margin:auto;border:1px solid var(--taupe);text-align:left;padding:18px 24px;font-size:14px}.shortcuts{display:flex;justify-content:center;gap:44px;margin-top:35px}.shortcut{font-size:12px;width:66px}.circle{border-radius:50%;width:48px;height:48px;background:var(--oat);font-size:20px;padding-top:12px;margin:0 auto 12px}.label{position:absolute;bottom:22px;left:24px;font-size:12px}.brand{position:absolute;bottom:22px;right:24px;font-size:13px}
.promo{position:relative;overflow:hidden;background:var(--oat)}.promo h1{font-family:Georgia,serif;margin:0;font-weight:normal}.promo .swatches{display:flex;gap:16px}.swatch{width:46px;height:46px;border-radius:50%;border:1px solid var(--taupe)}
.large{width:1400px;height:560px}.large .copy{position:absolute;left:64px;top:62px}.large h1{font-size:60px;margin:44px 0 8px}.large p{font-size:20px;margin:34px 0}.large .right{position:absolute;left:765px;top:0;width:635px;height:560px;background:var(--sand)}.large .mini{position:absolute;left:725px;top:110px;transform:scale(.49);transform-origin:top left;border-radius:18px;overflow:hidden}.small{width:440px;height:280px}.small .copy{padding:35px 29px}.small h1{font-size:35px}.small p{font-size:16px;margin:16px 0 35px}.small .swatch{width:35px;height:35px}.kicker{font-size:12px;letter-spacing:2px}
'''

css += f'''
:root{{--evergreen:{'#677E61'};}}
.tabs{{color:{color('tab_background_text')};}}
.tab.active{{color:var(--ink);}}
.omni{{background:{color('omnibox_background')};}}
.google{{color:#D9A250;}}
.circle{{background:{color('frame_inactive')};}}
.large .copy{{width:650px;}}
'''

def browser(bookmarks=False):
    bm='<div class="bookmarks"><span>▱ Bookmarks</span><span>▱ Reading</span><span>▱ Design</span><span>▱ Inspiration</span></div>' if bookmarks else ''
    return '<div class="browser"><div class="tabs"><div class="tab active">New Tab <span class="close">×</span></div><div class="tab">Reading list <span class="close">×</span></div><span style="padding:10px">+</span><span style="margin-left:auto;padding:10px 12px;letter-spacing:22px">− □ ×</span></div><div class="tools"><span>←</span><span>→</span><span>↻</span><div class="omni">Search or type a URL</div><span>☆</span><span>⋮</span></div>'+bm+'<div class="content"><div class="google">Google</div><div class="search">Search Google or type a URL</div></div><div class="brand">Cozy Christmas Theme</div></div>'

def swatches():return '<div class="swatches">'+''.join(f'<div class="swatch" style="background:var(--{c})"></div>' for c in ('sand','milk','taupe','evergreen'))+'</div>'
def page(body):
    return '<!doctype html><html lang="en"><meta charset="utf-8"><style>'+css+'</style><body>'+body+'</body></html>'
logo='data:image/png;base64,'+base64.b64encode((ROOT/'logo/logo128.png').read_bytes()).decode()
css += """
.greeting{position:relative;background:#DCE6D7;text-align:center;overflow:hidden}
.greeting h1{font-family:Georgia,serif;font-weight:normal;margin:0;color:var(--ink)}
.greeting.small{width:440px;height:280px;padding-top:12px}
.greeting.small img{width:66px;height:66px;display:block;margin:0 auto 4px}
.greeting.small h1{font-size:34px;line-height:1.1}
.greeting.small .subtitle{font-size:22px;margin-top:4px}
.greeting.small p{font-size:14px;margin:14px 0}
.ribbon{position:absolute;bottom:0;left:0;right:0;height:26px;background:#677E61}
.greeting.wide{width:1400px;height:560px;padding-top:28px}
.greeting.wide h1{font-size:47px}
.greeting.wide p{font-size:17px;margin:10px 0}
.greeting .window{position:absolute;left:335px;top:151px;transform:scale(.57);transform-origin:top left;border-radius:18px;overflow:hidden;border:2px solid #B7C5AF}
.greeting .window .browser{height:660px}
.greeting .window .content{padding-top:86px}
.holly{position:absolute;width:150px;height:160px;top:244px}
.holly.left{left:94px;transform:rotate(-24deg)}.holly.right{right:94px;transform:rotate(24deg)}
"""
holly='<svg viewBox="0 0 150 160" width="150" height="160"><path fill="#73976A" d="M76 107Q32 108 18 57L36 58 29 27 56 40 70 9 83 43 109 27 105 56 133 54Q119 104 76 107Z"/><path d="M76 112V40" stroke="#677E61" stroke-width="5"/><g fill="#BD4444"><circle cx="62" cy="117" r="16"/><circle cx="88" cy="117" r="16"/><circle cx="75" cy="140" r="16"/></g></svg>'
small='<div class="greeting small"><img src="'+logo+'"><h1>Cozy Christmas</h1><div class="subtitle">Theme</div><p>A little Christmas, every day.</p><div class="ribbon"></div></div>'
wide='<div class="greeting wide"><h1>Cozy Christmas Theme</h1><p>A little Christmas, every day.</p><div class="holly left">'+holly+'</div><div class="holly right">'+holly+'</div><div class="window">'+browser()+'</div><div class="ribbon" style="height:12px"></div></div>'
jobs=[('screenshot-1-browser',1280,800,browser(True)),('promo-1400x560',1400,560,wide),('promo-440x280',440,280,small)]
palette=[('Pastel Cream','ntp_background','New tab background'),('Warm White','omnibox_background','Address bar'),('Soft Christmas Red','frame','Frame & window controls'),('Soft Evergreen','frame_inactive','Inactive window'),('Deep Fir','ntp_text','Text & icons'),('Soft Cream','toolbar','Toolbar & active tab')]
cards=''.join(f'<div style="background:{color(key)};color:{color("ntp_text") if i in (0,1,3,5) else color("ntp_background")};border:1px solid #D9CFC7;border-radius:20px;padding:26px;height:200px;display:flex;flex-direction:column;justify-content:end"><strong style="font-size:23px">{name}</strong><span style="font-size:15px;margin-top:9px">{color(key).upper()} · {role}</span></div>' for i,(name,key,role) in enumerate(palette))
intro='<div style="width:1280px;height:800px;padding:58px 72px;background:var(--milk)"><div class="kicker">A COZY CHRISTMAS PALETTE</div><h1 style="font:54px Georgia,serif;margin:18px 0 12px">Cozy Christmas Theme</h1><p style="font-size:20px;margin:0">Festive colors for a warm, minimal browser.</p><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:40px">'+cards+'</div><div style="margin-top:32px;font-size:16px;display:flex;gap:48px"><span>Solid colors</span><span>No wallpaper</span><span>No gradients</span><span>No permissions required</span></div></div>'
jobs.append(('screenshot-2-introduction',1280,800,intro))
with sync_playwright() as p:
    browser_engine=p.chromium.launch(headless=True)
    tab=browser_engine.new_page(device_scale_factor=1)
    for name,w,h,body in jobs:
        html=page(body);(OUT/f'{name}.html').write_text(html,'utf-8')
        tab.set_viewport_size({'width':w,'height':h});tab.set_content(html);tab.screenshot(path=str(OUT/f'{name}.png'))
        destination=ROOT/'store-assets'/('promo' if name.startswith('promo-') else 'screenshots/en')/(name.removeprefix('promo-')+'.png')
        destination.parent.mkdir(parents=True,exist_ok=True)
        temp=destination.with_suffix('.new.png')
        with Image.open(OUT/f'{name}.png') as img: img.convert('RGB').save(temp)
        temp.replace(destination)
        print(f'Rendered {name} {w}x{h}')
    browser_engine.close()
