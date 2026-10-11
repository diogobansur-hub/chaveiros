#!/usr/bin/env python3
"""Gera index.html + uma página por chaveiro a partir de chaveiros.json.
Novo chaveiro: adicione um item no JSON (foto em img/, thumb opcional) e rode: python3 gerar.py
Campos vazios (onde/quando/historia) não aparecem na página."""
import json, html, pathlib
D = pathlib.Path(__file__).parent
CSS = """*{box-sizing:border-box}body{margin:0;background:#121214;color:#e9e9ec;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.55}
main{max-width:680px;margin:0 auto;padding:28px 18px 48px}h1{font-weight:600;font-size:1.6rem;margin:8px 0 22px;letter-spacing:.2px}
ul{list-style:none;padding:0;margin:0}li a{display:flex;align-items:center;gap:14px;padding:10px;margin-bottom:10px;border-radius:14px;background:#1c1c20;color:inherit;text-decoration:none;border:1px solid #2a2a30}
li a:active{background:#24242a}li img{width:64px;height:52px;object-fit:cover;border-radius:10px;background:#0d0d0f}li span{font-size:1.05rem}li small,.data{display:block;color:#8b8b93;font-size:.8rem;margin-top:2px}
.hero{width:100%;display:block;background:#0e0e10}.n{color:#7fb0d6;font-size:.95rem;letter-spacing:1px;margin:0}h2{margin:2px 0 18px;font-size:1.5rem;font-weight:600}
dl{margin:0}dt{color:#8b8b93;font-size:.8rem;text-transform:uppercase;letter-spacing:1px;margin-top:14px}dd{margin:2px 0 0}.hist{white-space:pre-line}
.album{display:block;margin-top:26px;padding:14px;border-radius:12px;background:#2a2d33;color:#fff;text-align:center;text-decoration:none;font-weight:600}
.back{display:inline-block;margin-top:30px;color:#7fb0d6;text-decoration:none}"""
def page(title, body):
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#121214"><title>{html.escape(title)}</title><style>{CSS}</style></head><body>{body}</body></html>'
def fname(c): return f"{c['numero']:02d}-{c['slug']}.html"
cs = sorted(json.loads((D/"chaveiros.json").read_text()), key=lambda c: c["numero"])
items = "".join(f'<li><a href="{fname(c)}"><img src="{c.get("thumb") or c["foto"]}" alt="" loading="lazy"><span>{c.get("bandeira","")} {c["emoji"]} {c["numero"]:02d} · {html.escape(c["nome"])}<small>{html.escape(c.get("data",""))}</small></span></a></li>' for c in cs)
(D/"index.html").write_text(page("Minha coleção de chaveiros", f'<main><h1>Minha coleção de chaveiros</h1><ul>{items}</ul></main>'))
for c in cs:
    rows = "".join(f'<dt>{l}</dt><dd{" class=hist" if k=="historia" else ""}>{html.escape(c[k])}</dd>' for k, l in [("onde","Local"),("quando","Quando"),("historia","História")] if c.get(k, "").strip())
    album = f'<a class="album" href="{c["fotos"]}" target="_blank" rel="noopener">📸 Fotos da viagem</a>' if c.get("fotos","").strip() else ''
    body = f'<img class="hero" src="{c["foto"]}" alt="{html.escape(c["nome"])}"><main><p class="n">{c.get("bandeira","")} {c["emoji"]} Nº {c["numero"]:02d}</p><h2>{html.escape(c["nome"])}<small class="data">{html.escape(c.get("data",""))}</small></h2><dl>{rows}</dl>{album}<a class="back" href="index.html">← Coleção</a></main>'
    (D/fname(c)).write_text(page(f'{c["numero"]:02d} · {c["nome"]}', body))
print("ok:", len(cs), "chaveiro(s)")
