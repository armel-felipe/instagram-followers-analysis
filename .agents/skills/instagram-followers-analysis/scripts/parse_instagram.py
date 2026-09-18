#!/usr/bin/env python3
"""Parse Instagram export and generate a self-contained HTML dashboard.

Usage:
    python3 parse_instagram.py <path-to-instagram-export-folder> [-o output.html]

Requires: Python 3.6+, standard library only.
"""
import argparse, json, os, re, sys
from collections import Counter

BLOCK = '<div class="pam _3-95 _2ph- _a6-g uiBoxWhite noborder">'
MONTHS = 'jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez'
FOLLOWERS_DIR = os.path.join("connections", "followers_and_following")

def parse_entries(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"<main.*?</main>", content, re.S)
    if not m:
        return []
    main = m.group(0)
    parts = main.split(BLOCK)[1:]
    entries = []
    for part in parts:
        a = re.search(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', part, re.S)
        if not a:
            continue
        u = re.search(r"instagram\.com/(?:_u/)?([^/?\"']+)", a.group(1))
        username = u.group(1) if u else None
        if not username:
            continue
        date = None
        dm = re.search(rf"({MONTHS})\s+\d+,\s+\d{{4}}[^<]*", part, re.I)
        if dm:
            date = dm.group(0).strip()
        entries.append({"username": username, "date": date})
    return entries

def build_data(followers, following):
    fol_map = {e["username"]: e for e in followers}
    fng_map = {e["username"]: e for e in following}
    all_users = sorted(set(fol_map) | set(fng_map), key=str.lower)
    rows = []
    for username in all_users:
        rows.append({
            "username": username,
            "following": username in fng_map,
            "follower": username in fol_map,
            "fng_date": fng_map[username]["date"] if username in fng_map else None,
            "fol_date": fol_map[username]["date"] if username in fol_map else None,
        })
    return rows

def categorize(rows):
    cats = Counter()
    for r in rows:
        if r["following"] and r["follower"]:
            cats["mutual"] += 1
        elif r["following"]:
            cats["churner"] += 1
        else:
            cats["onboarding"] += 1
    return cats

CSS = ":root{--bg:#fafafa;--card:#fff;--text:#1a1a1a;--muted:#888;--border:#e0e0e0;--accent:#e1306c;--green:#22c55e;--red:#ef4444;--amber:#f59e0b}\n"
CSS += "*{box-sizing:border-box;margin:0;padding:0}\n"
CSS += "body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);font-size:14px;line-height:1.5;padding:20px;max-width:960px;margin:0 auto}\n"
CSS += "h1{font-size:20px;font-weight:600;margin-bottom:4px}\n"
CSS += ".sub{color:var(--muted);font-size:13px;margin-bottom:16px}\n"
CSS += ".cards{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px}\n"
CSS += ".card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px 18px;min-width:130px;cursor:pointer;transition:box-shadow .15s,border-color .15s;user-select:none}\n"
CSS += ".card:hover{box-shadow:0 2px 8px rgba(0,0,0,.08)}\n"
CSS += ".card.active{border-color:var(--accent);box-shadow:0 0 0 2px rgba(225,48,108,.15)}\n"
CSS += ".card .n{font-size:26px;font-weight:700}\n"
CSS += ".card .l{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px}\n"
CSS += ".card.mutual .n{color:var(--green)}\n"
CSS += ".card.churner .n{color:var(--red)}\n"
CSS += ".card.onboarding .n{color:var(--amber)}\n"
CSS += ".card.all .n{color:var(--text)}\n"
CSS += ".search{width:100%;padding:10px 14px;border:1px solid var(--border);border-radius:8px;font-size:14px;outline:none;background:var(--card);margin-bottom:12px}\n"
CSS += ".search:focus{border-color:var(--accent)}\n"
CSS += "table{width:100%;border-collapse:collapse;background:var(--card);border-radius:10px;overflow:hidden;border:1px solid var(--border)}\n"
CSS += "thead th{text-align:left;padding:10px 12px;background:#f5f5f5;font-size:12px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);border-bottom:1px solid var(--border);cursor:pointer;user-select:none;white-space:nowrap}\n"
CSS += "thead th:hover{background:#eee}\n"
CSS += "tbody td{padding:9px 12px;border-bottom:1px solid #f0f0f0}\n"
CSS += "tbody tr:hover{background:#fafafa}\n"
CSS += ".badge{display:inline-block;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:600}\n"
CSS += ".badge.y{background:#dcfce7;color:#16a34a}\n"
CSS += ".badge.n{background:#fee2e2;color:#dc2626}\n"
CSS += ".tag{display:inline-block;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600}\n"
CSS += ".tag.mutual{background:#dcfce7;color:#16a34a}\n"
CSS += ".tag.churner{background:#fee2e2;color:#dc2626}\n"
CSS += ".tag.onboarding{background:#fef3c7;color:#d97706}\n"
CSS += "a{color:var(--accent);text-decoration:none}\n"
CSS += "a:hover{text-decoration:underline}\n"
CSS += ".date{color:var(--muted);font-size:12px;white-space:nowrap}\n"
CSS += ".count-row{color:var(--muted);font-size:13px;margin-bottom:8px}\n"
CSS += ".empty{text-align:center;padding:40px;color:var(--muted)}\n"
CSS += "@media(max-width:640px){.date{display:none}}\n"

JS = "let filter='all', sortKey='username', sortAsc=true, query='';\n"
JS += "const cats={all:DATA.length,mutual:0,churner:0,onboarding:0};\n"
JS += "DATA.forEach(r=>{const c=r.following&&r.follower?'mutual':r.following?'churner':'onboarding';cats[c]++});\n"
JS += "const cardsEl=document.getElementById('cards');\n"
JS += "const cardDefs=[['all','Todos'],['mutual','Mutuo'],['churner','Churners'],['onboarding','Onboarding']];\n"
JS += "cardDefs.forEach(function(kl){\n"
JS += " var k=kl[0],l=kl[1];\n"
JS += " var d=document.createElement('div');\n"
JS += " d.className='card '+k+(k==='all'?' active':'');\n"
JS += " d.innerHTML='<div class=\"n\">'+cats[k]+'</div><div class=\"l\">'+l+'</div>';\n"
JS += " d.onclick=function(){filter=k;document.querySelectorAll('.card').forEach(function(c){c.classList.remove('active')});d.classList.add('active');render()};\n"
JS += " cardsEl.appendChild(d);\n"
JS += "});\n"
JS += "var qEl=document.getElementById('q');\n"
JS += "qEl.addEventListener('input',function(){query=qEl.value.toLowerCase();render()});\n"
JS += "document.querySelectorAll('th[data-k]').forEach(function(th){\n"
JS += " th.addEventListener('click',function(){\n"
JS += "  var k=th.dataset.k;\n"
JS += "  if(sortKey===k)sortAsc=!sortAsc;else{sortKey=k;sortAsc=true}\n"
JS += "  document.querySelectorAll('th[data-k]').forEach(function(t){t.textContent=t.textContent.replace(/\\s*[\\u2191\\u2193]\\s*$/,'')});\n"
JS += "  th.textContent=th.textContent.replace(/\\s*[\\u2191\\u2193]\\s*$/,'')+(sortAsc?' \\u2191':' \\u2193');\n"
JS += "  render();\n"
JS += " });\n"
JS += "});\n"
JS += "function status(r){return r.following&&r.follower?'mutual':r.following?'churner':'onboarding'}\n"
JS += "function statusLabel(s){return s==='mutual'?'Mutuo':s==='churner'?'Churner':'Onboarding'}\n"
JS += "function esc(s){var d=document.createElement('div');d.textContent=s||'';return d.innerHTML}\n"
JS += "function render(){\n"
JS += " var filtered=DATA.filter(function(r){\n"
JS += "  if(filter!=='all'){if(status(r)!==filter)return false}\n"
JS += "  if(query&&r.username.toLowerCase().indexOf(query)<0)return false;\n"
JS += "  return true;\n"
JS += " });\n"
JS += " filtered.sort(function(a,b){\n"
JS += "  var va,vb;\n"
JS += "  if(sortKey==='status'){va=status(a);vb=status(b)}\n"
JS += "  else{va=a[sortKey];vb=b[sortKey]}\n"
JS += "  if(va===null||va===undefined)return 1;\n"
JS += "  if(vb===null||vb===undefined)return -1;\n"
JS += "  va=String(va).toLowerCase();vb=String(vb).toLowerCase();\n"
JS += "  return sortAsc?va.localeCompare(vb):vb.localeCompare(va);\n"
JS += " });\n"
JS += " var tb=document.getElementById('tb');\n"
JS += " var h='';\n"
JS += " for(var i=0;i<filtered.length;i++){\n"
JS += "  var r=filtered[i],s=status(r);\n"
JS += "  h+='<tr>'\n"
JS += "   +'<td><a href=\"https://www.instagram.com/'+esc(r.username)+'\" target=\"_blank\">'+esc(r.username)+'</a></td>'\n"
JS += "   +'<td><span class=\"badge '+(r.following?'y':'n')+'\">'+(r.following?'Sim':'Nao')+'</span></td>'\n"
JS += "   +'<td><span class=\"badge '+(r.follower?'y':'n')+'\">'+(r.follower?'Sim':'Nao')+'</span></td>'\n"
JS += "   +'<td><span class=\"tag '+s+'\">'+statusLabel(s)+'</span></td>'\n"
JS += "   +'<td class=\"date\">'+(r.fng_date?esc(r.fng_date):'\\u2014')+'</td>'\n"
JS += "   +'<td class=\"date\">'+(r.fol_date?esc(r.fol_date):'\\u2014')+'</td>'\n"
JS += "   +'</tr>';\n"
JS += " }\n"
JS += " tb.innerHTML=h;\n"
JS += " document.getElementById('count').textContent=filtered.length+' de '+DATA.length+' perfis';\n"
JS += " document.getElementById('empty').style.display=filtered.length?'none':'block';\n"
JS += "}\n"
JS += "render();\n"

def generate_html(data_js, cats, total):
    h = "<!doctype html>\n<html lang=\"pt-BR\">\n<head>\n"
    h += '<meta charset="utf-8">\n'
    h += '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
    h += "<title>Instagram \u2014 Following vs Followers</title>\n"
    h += "<style>\n" + CSS + "</style>\n</head>\n<body>\n"
    h += "<h1>Instagram \u2014 Following vs Followers</h1>\n"
    h += '<p class="sub">Gerado a partir do export do Instagram \u00b7 ' + str(total) + " perfis \u00fanicos \u00b7 " + str(cats["mutual"]) + " m\u00fatuo \u00b7 " + str(cats["churner"]) + " churners \u00b7 " + str(cats["onboarding"]) + " onboarding</p>\n"
    h += '<div class="cards" id="cards"></div>\n'
    h += '<input class="search" id="q" type="text" placeholder="Buscar perfil...">\n'
    h += '<p class="count-row" id="count"></p>\n<table>\n<thead><tr>\n'
    h += '<th data-k="username">Perfil</th>\n'
    h += '<th data-k="following">Seguindo</th>\n'
    h += '<th data-k="follower">Seguidor</th>\n'
    h += '<th data-k="status">Status</th>\n'
    h += '<th class="date" data-k="fng_date">Desde que sigo</th>\n'
    h += '<th class="date" data-k="fol_date">Desde que me segue</th>\n'
    h += "</tr></thead>\n"
    h += '<tbody id="tb"></tbody>\n</table>\n'
    h += '<p class="empty" id="empty" style="display:none">Nenhum perfil encontrado.</p>\n'
    h += "<script>\nconst DATA=" + data_js + ";\n" + JS + "</script>\n</body>\n</html>"
    return h

def main():
    ap = argparse.ArgumentParser(description="Parse Instagram export and generate followers/following dashboard")
    ap.add_argument("path", help="Path to the Instagram export folder")
    ap.add_argument("-o", "--output", default="instagram_followers_following.html", help="Output HTML filename")
    args = ap.parse_args()
    base = args.path
    fng_path = os.path.join(base, FOLLOWERS_DIR, "following.html")
    fol_path = os.path.join(base, FOLLOWERS_DIR, "followers_1.html")
    if not os.path.isfile(fng_path):
        sys.exit("Error: following.html not found at " + fng_path)
    if not os.path.isfile(fol_path):
        sys.exit("Error: followers_1.html not found at " + fol_path)
    following = parse_entries(fng_path)
    followers = parse_entries(fol_path)
    rows = build_data(followers, following)
    cats = categorize(rows)
    data_js = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    total = len(rows)
    out = generate_html(data_js, cats, total)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Parsed {len(following)} following, {len(followers)} followers")
    print(f"Total unique: {total} | Mutual: {cats['mutual']} | Churners: {cats['churner']} | Onboarding: {cats['onboarding']}")
    print(f"Wrote {args.output} ({len(out)} bytes)")

if __name__ == "__main__":
    main()
