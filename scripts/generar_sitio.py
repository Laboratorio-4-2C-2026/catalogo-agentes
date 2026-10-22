"""Genera sitio/index.html: el explorador de piezas y el avance por alumno en
una sola página, con las dos vistas conectadas. No necesita servidor ni
internet: se abre con doble clic o se publica con GitHub Pages.

Corre solo, después de aceptar un PR.
"""
import json

from common import RAIZ, archivo_ficha, cargar_yaml, como_lista, leer_ficha, piezas, texto_ejemplo

META = 10


def persona(p):
    if not isinstance(p, dict):
        return None
    return {"nombre": str(p.get("nombre", "")), "github": str(p.get("github", ""))}


def datos_piezas():
    datos = []
    for tipo, carpeta in piezas():
        ruta, es_yml = archivo_ficha(carpeta)
        if not ruta:
            continue
        ficha, _ = leer_ficha(ruta, es_yml)
        if not ficha:
            continue
        meta = ficha.get("metadata") or {}
        datos.append({
            "name": ficha.get("name", carpeta.name),
            "description": str(ficha.get("description", "")).strip(),
            "tipo": tipo,
            "grupo": str(meta.get("grupo", "")),
            "autor": persona(meta.get("autor")),
            "colaboradores": [c for c in map(persona, como_lista(meta.get("colaboradores"))) if c],
            "area": como_lista(meta.get("area")),
            "fase": como_lista(meta.get("fase")),
            "tecnologias": como_lista(meta.get("tecnologias")),
            "herramientas": como_lista(meta.get("herramientas")),
            "requiere": como_lista(meta.get("requiere")),
            "madurez": meta.get("madurez", ""),
            "relacionados": como_lista(meta.get("relacionados")),
            "ejemplo": texto_ejemplo(carpeta, ruta, es_yml) or "",
            "ruta": carpeta.relative_to(RAIZ).as_posix(),
        })
    return datos


def datos_alumnos():
    alumnos = []
    for grupo, lista in cargar_yaml(RAIZ / "integrantes.yml").items():
        if grupo == "catedra":
            continue
        for p in lista or []:
            alumnos.append({"grupo": grupo.replace("grupo-", ""), "nombre": str(p.get("nombre", "")),
                            "github": str(p.get("github", ""))})
    return alumnos


PLANTILLA = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catálogo Común de Agentes</title>
<style>
:root{--bg:#f5f6f8;--card:#fff;--fg:#1a2130;--muted:#5b6577;--line:#dde1e8;--acc:#2e55c8;--soft:#e7ecfb;--on:#fff;
--tag:#8a5a00;--tagbg:#fbf1dc;--ok:#1f7a4d;--okbg:#e2f3ea}
@media (prefers-color-scheme:dark){:root{--bg:#12161e;--card:#1a1f2a;--fg:#e4e8f0;--muted:#9aa4b6;--line:#2c3342;--acc:#8ea8ff;
--soft:#1f2a48;--on:#10141b;--tag:#f0c56a;--tagbg:#3a2f17;--ok:#6fd3a0;--okbg:#17342a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
.w{max-width:1160px;margin:0 auto;padding:20px 16px 48px}
header{display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:12px;border-bottom:1px solid var(--line);padding-bottom:12px}
h1{margin:0;font-size:1.6rem}.m{color:var(--muted)}.s{font-size:14px}
nav{display:flex;gap:6px}nav a{text-decoration:none;color:var(--fg);padding:7px 14px;border-radius:8px;border:1px solid var(--line);background:var(--card);font-weight:600}
nav a.on{background:var(--acc);border-color:var(--acc);color:var(--on)}
a{color:var(--acc)}
input{width:100%;font:inherit;padding:9px 12px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg);margin:16px 0 8px}
.row{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0;align-items:center}.row b{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);min-width:100px}
.chip{font:inherit;font-size:14px;padding:3px 10px;border-radius:99px;border:1px solid var(--line);background:var(--card);color:var(--fg);cursor:pointer}
.chip.on{background:var(--acc);border-color:var(--acc);color:var(--on)}
.g{display:grid;grid-template-columns:1fr;gap:14px;margin-top:12px}@media(min-width:880px){.g{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.list{display:grid;gap:8px;align-content:start}
.c{display:block;text-decoration:none;color:var(--fg);background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.c.on{border-color:var(--acc);box-shadow:inset 0 0 0 1px var(--acc)}
.n{font-family:ui-monospace,Consolas,monospace;font-weight:600;font-size:14px;word-break:break-word}
.t{display:inline-block;font-size:12px;padding:0 7px;border-radius:99px;background:var(--tagbg);color:var(--tag);margin:3px 3px 0 0}
.t.b{background:var(--soft);color:var(--acc)}
.d{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;align-self:start;position:sticky;top:12px;min-width:0}
dl{display:grid;grid-template-columns:120px minmax(0,1fr);gap:4px 10px;font-size:14.5px}dt{color:var(--muted)}dd{margin:0}
pre{white-space:pre-wrap;background:var(--soft);border-radius:8px;padding:10px 12px;font:14px/1.5 system-ui,sans-serif}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:16px 0}
.st{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}.st .v{font-size:1.6rem;font-weight:700;font-variant-numeric:tabular-nums}
.tw{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:15px}th,td{text-align:left;padding:8px 10px;border-top:1px solid var(--line);vertical-align:middle}
th{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);border-top:0;white-space:nowrap}
td.r{text-align:right;font-variant-numeric:tabular-nums}tr.on td{background:var(--soft)}
.bar{width:110px;height:8px;border-radius:4px;background:var(--bg);border:1px solid var(--line);overflow:hidden}.bar span{display:block;height:100%;background:var(--acc)}.bar span.full{background:var(--ok)}
.pill{font-size:12px;font-weight:700;padding:1px 8px;border-radius:99px;white-space:nowrap;background:var(--tagbg);color:var(--tag)}.pill.ok{background:var(--okbg);color:var(--ok)}
h2{font-size:1.15rem;margin:22px 0 8px}h3{font-size:1rem;margin:14px 0 6px}
ul.p{padding-left:1.1em;margin:4px 0}
</style></head><body><div class="w">
<header><div><h1>Catálogo Común de Agentes</h1><div class="m s" id="sub"></div></div>
<nav><a href="#explorar" id="tab-explorar">Explorador</a><a href="#avance" id="tab-avance">Avance por alumno</a></nav></header>
<main id="main"></main>
</div>
<script>
const P = __PIEZAS__, A = __ALUMNOS__, META = __META__;
const low = s => String(s||"").toLowerCase();
const alumno = gh => A.find(a => low(a.github) === low(gh));
const comoAutor = gh => P.filter(p => p.autor && low(p.autor.github) === low(gh) && p.grupo !== "00");
const comoColab = gh => P.filter(p => p.colaboradores.some(c => low(c.github) === low(gh)) && p.grupo !== "00");
const st = {q:"", area:new Set(), fase:new Set(), herramientas:new Set(), grupo:new Set(), gAv:new Set()};
const $ = id => document.getElementById(id);
function e(t,c,x){const n=document.createElement(t);if(c)n.className=c;if(x!=null)n.textContent=x;return n}
function a(href,txt,c){const n=e("a",c,txt);n.href=href;return n}
function linkPersona(p){if(!p)return e("span",null,"—");return alumno(p.github)?a("#alumno/"+encodeURIComponent(p.github),p.nombre||p.github):e("span",null,p.nombre||p.github)}

function ruta(){const h=decodeURIComponent(location.hash.slice(1));const i=h.indexOf("/");
  return i<0?{v:h||"explorar",id:null}:{v:h.slice(0,i),id:h.slice(i+1)}}
function render(){const r=ruta();const av=r.v==="avance"||r.v==="alumno";
  $("tab-explorar").className=av?"":"on";$("tab-avance").className=av?"on":"";
  $("sub").textContent=P.length+" piezas · "+A.length+" alumnos · "+new Set(P.map(p=>p.grupo)).size+" grupos con piezas";
  const m=$("main");m.innerHTML="";av?vistaAvance(m,r.v==="alumno"?r.id:null):vistaExplorar(m,r.v==="pieza"?r.id:null);
  if(r.v==="pieza"||r.v==="alumno"){const s=document.querySelector(".on[data-k]");if(s)s.scrollIntoView({block:"nearest"})}}

function chips(box,campo,valores,etq){valores.forEach(v=>{const b=e("button","chip"+(st[campo].has(v)?" on":""),etq?etq(v):v);
  b.onclick=()=>{st[campo].has(v)?st[campo].delete(v):st[campo].add(v);render()};box.append(b)})}
function ok(p){const q=low(st.q);
  if(q&&!low(p.name+" "+p.description+" "+p.tecnologias.join(" ")+" "+(p.autor?p.autor.nombre:"")).includes(q))return false;
  for(const c of ["area","fase","herramientas","grupo"]){if(st[c].size&&![].concat(p[c]).some(v=>st[c].has(v)))return false}return true}

function vistaExplorar(m,sel){
  const q=e("input");q.type="search";q.placeholder="Buscar por nombre, descripción, tecnología o autor…";q.value=st.q;
  q.oninput=()=>{st.q=q.value;const pos=q.selectionStart;render();const n=document.querySelector("input");n.focus();n.setSelectionRange(pos,pos)};m.append(q);
  for(const [campo,et] of [["area","Área"],["fase","Fase"],["herramientas","Herramienta"],["grupo","Grupo"]]){
    const r=e("div","row");r.append(e("b",null,et));chips(r,campo,[...new Set(P.flatMap(p=>[].concat(p[campo])))].sort(),campo==="grupo"?v=>"g"+v:null);m.append(r)}
  const l=P.filter(ok);if(!sel||!l.some(p=>p.name===sel))sel=l.length?l[0].name:null;
  const g=e("div","g"),list=e("div","list"),d=e("div","d");g.append(list,d);m.append(g);
  list.append(e("div","m s",l.length+" de "+P.length+" piezas"));
  l.forEach(p=>{const c=a("#pieza/"+encodeURIComponent(p.name),null,"c"+(p.name===sel?" on":""));c.dataset.k=1;
    c.append(e("div","n",p.name),e("div","m s",p.description));const t=e("div");
    p.area.forEach(v=>t.append(e("span","t",v)));p.herramientas.forEach(v=>t.append(e("span","t b",v)));c.append(t);list.append(c)});
  const p=P.find(x=>x.name===sel);
  if(!p){d.append(e("div","m",P.length?"Ninguna pieza coincide con los filtros.":"Todavía no hay piezas en el catálogo."));return}
  d.append(e("div","n",p.name),e("p",null,p.description));const dl=e("dl");
  const fila=(k,v)=>{dl.append(e("dt",null,k));const dd=e("dd");typeof v==="string"?dd.textContent=v||"—":dd.append(v);dl.append(dd)};
  fila("Tipo",p.tipo);fila("Grupo","g"+p.grupo);fila("Autor",linkPersona(p.autor));
  const col=e("span");p.colaboradores.forEach((c,i)=>{if(i)col.append(", ");col.append(linkPersona(c))});fila("Colaboradores",p.colaboradores.length?col:"—");
  fila("Área",p.area.join(", "));fila("Fase",p.fase.join(", "));fila("Tecnologías",p.tecnologias.join(", "));
  fila("Funciona en",p.herramientas.join(", "));fila("Requiere",p.requiere.join(", ")||"nada externo");fila("Madurez",p.madurez);fila("Carpeta",p.ruta);
  d.append(dl,e("h3",null,"Ejemplo de uso"),e("pre",null,p.ejemplo||"—"));
  if(p.relacionados.length){d.append(e("h3",null,"Relacionadas"));const u=e("ul","p");
    p.relacionados.forEach(n=>{const li=e("li");li.append(P.some(x=>x.name===n)?a("#pieza/"+encodeURIComponent(n),n):e("span",null,n));u.append(li)});d.append(u)}}

function vistaAvance(m,sel){
  const grupos=[...new Set(A.map(x=>x.grupo))].sort();const r=e("div","row");r.style.marginTop="16px";r.append(e("b",null,"Grupo"));
  grupos.forEach(gr=>{const b=e("button","chip"+(st.gAv.has(gr)?" on":""),"g"+gr);b.onclick=()=>{st.gAv.has(gr)?st.gAv.delete(gr):st.gAv.add(gr);render()};r.append(b)});m.append(r);
  const vis=A.filter(x=>!st.gAv.size||st.gAv.has(x.grupo));const n=x=>comoAutor(x.github).length;
  const s=e("div","stats");[[vis.filter(x=>n(x)>=META).length+" de "+vis.length,"alumnos con "+META+" o más"],
    [vis.reduce((t,x)=>t+n(x),0),"piezas como autor"],[vis.reduce((t,x)=>t+comoColab(x.github).length,0),"colaboraciones"]]
    .forEach(([v,k])=>{const c=e("div","st");c.append(e("div","v",String(v)),e("div","m s",k));s.append(c)});m.append(s);
  const g=e("div","g"),izq=e("div"),d=e("div","d");g.append(izq,d);m.append(g);
  const tw=e("div","tw"),tb=e("table");tb.innerHTML="<tr><th>Alumno</th><th>Grupo</th><th>Autor</th><th>Avance</th><th>Colab.</th><th>Estado</th></tr>";
  vis.slice().sort((x,y)=>x.grupo.localeCompare(y.grupo)||x.nombre.localeCompare(y.nombre)).forEach(x=>{
    const k=n(x),tr=e("tr",low(x.github)===low(sel)?"on":"");tr.dataset.k=low(x.github)===low(sel)?1:"";
    const td=e("td");td.append(a("#alumno/"+encodeURIComponent(x.github),x.nombre||x.github));tr.append(td,e("td",null,"g"+x.grupo),e("td","r",String(k)));
    const tb2=e("td"),bar=e("div","bar"),sp=e("span",k>=META?"full":"");sp.style.width=Math.min(100,k*100/META)+"%";bar.append(sp);tb2.append(bar);tr.append(tb2);
    tr.append(e("td","r",String(comoColab(x.github).length)));const te=e("td");te.append(e("span","pill"+(k>=META?" ok":""),k>=META?"Completo":"Faltan "+(META-k)));tr.append(te);tb.append(tr)});
  tw.append(tb);izq.append(tw);
  const x=sel&&alumno(sel);
  if(!x){d.append(e("div","m","Elegí un alumno para ver sus piezas."));return}
  d.append(e("h2",null,x.nombre||x.github),e("div","m s","@"+x.github+" · grupo "+x.grupo));
  for(const [tit,l] of [["Como autor ("+comoAutor(x.github).length+")",comoAutor(x.github)],["Como colaborador ("+comoColab(x.github).length+")",comoColab(x.github)]]){
    d.append(e("h3",null,tit));if(!l.length){d.append(e("div","m s","Ninguna todavía."));continue}
    const u=e("ul","p");l.forEach(p=>{const li=e("li");li.append(a("#pieza/"+encodeURIComponent(p.name),p.name));u.append(li)});d.append(u)}}

addEventListener("hashchange",render);render();
</script></body></html>
"""


def main():
    def js(v):
        return json.dumps(v, ensure_ascii=False).replace("</", "<\\/")
    pagina = (PLANTILLA.replace("__PIEZAS__", js(datos_piezas()))
              .replace("__ALUMNOS__", js(datos_alumnos())).replace("__META__", str(META)))
    salida = RAIZ / "sitio" / "index.html"
    salida.parent.mkdir(exist_ok=True)
    salida.write_text(pagina, encoding="utf-8")
    print(f"Sitio generado: {salida.relative_to(RAIZ).as_posix()}")


if __name__ == "__main__":
    main()
