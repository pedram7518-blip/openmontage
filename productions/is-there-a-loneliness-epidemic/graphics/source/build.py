"""Generate HyperFrames stat-card projects for the loneliness video."""
import json, sys
from pathlib import Path

OUT = Path(__file__).parent
CARDS = [
 dict(id="00_title", kind="title", dur=4, kicker="", big="IS THERE A", sub="LONELINESS EPIDEMIC?", src=""),
 dict(id="01_who_one_in_six", kind="ratio", dur=5, kicker="Worldwide", big="1 in 6", sub="people feel lonely", src="World Health Organization, 2025"),
 dict(id="02_young_people", kind="stat", dur=5, kicker="The loneliest age group", big="13–29", sub="year olds", src="World Health Organization, 2025"),
 dict(id="03_deaths", kind="count", dur=5.5, kicker="Linked to loneliness every year", big="871,000", count=871000, sub="deaths  ·  about 100 every hour", src="World Health Organization, 2025"),
 dict(id="04_cigarettes", kind="cigs", dur=5.5, kicker="Health risk comparable to smoking", big="15", count=15, sub="cigarettes a day", src="US Surgeon General Advisory, 2023"),
 dict(id="05_no_close_friends", kind="compare", dur=6, kicker="US men with zero close friends", a_label="1990", a_val=3, b_label="2021", b_val=15, src="Survey Center on American Life, 2021"),
 dict(id="06_single_men", kind="compare", dur=6, kicker="Under 30 and single", a_label="Women", a_val=34, b_label="Men", b_val=63, src="Pew Research Center (survey July 2022)"),
 dict(id="07_reason_1", kind="reason", dur=3.5, kicker="Reason 1", big="There's nowhere to go", src=""),
 dict(id="08_reason_2", kind="reason", dur=3.5, kicker="Reason 2", big="Being alone got comfortable", src=""),
 dict(id="09_reason_3", kind="reason", dur=3.5, kicker="Reason 3", big="Dating became a numbers game", src=""),
 dict(id="10_reason_4", kind="reason", dur=3.5, kicker="Reason 4", big="Remote everything", src=""),
 dict(id="11_reason_5", kind="reason", dur=3.5, kicker="Reason 5", big="The shame spiral", src=""),
 dict(id="12_hours_to_friend", kind="hours", dur=7, kicker="Time it takes to make a friend", steps=[["~50 hrs","casual friend"],["~90 hrs","friend"],["200+ hrs","close friend"]], src="Jeffrey Hall, University of Kansas, 2018"),
]

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#0b0e14;color:#f2efe9;font-family:'Inter','Helvetica Neue',Arial,sans-serif}
#root{position:relative;width:1920px;height:1080px;overflow:hidden}
.bg{position:absolute;inset:0;background:radial-gradient(ellipse 70% 60% at 50% 45%,#1b2333 0%,#0b0e14 70%,#05070a 100%)}
.glow{position:absolute;left:660px;top:240px;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(255,181,71,.16),rgba(255,181,71,0) 65%)}
.scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.kicker{font-size:44px;letter-spacing:.14em;text-transform:uppercase;color:#9aa6b8;font-weight:600;margin-bottom:28px}
.big{font-size:260px;font-weight:900;line-height:1;color:#ffb547;letter-spacing:-.02em}
.sub{font-size:68px;font-weight:700;margin-top:30px;color:#f2efe9}
.src{position:absolute;left:80px;bottom:60px;font-size:28px;color:#6f7b8d;letter-spacing:.04em}
.rule{width:0;height:6px;background:#ffb547;margin-top:40px;border-radius:3px}
.dots{display:flex;gap:40px;margin-top:50px}
.dot{width:110px;height:110px;border-radius:50%;background:#2a3445}
.dot.on{background:#ffb547}
.title1{font-size:110px;font-weight:800;letter-spacing:.06em;color:#f2efe9}
.title2{font-size:124px;font-weight:900;color:#ffb547;letter-spacing:.01em;line-height:1.05;margin-top:10px}
.reasonk{font-size:56px;font-weight:800;color:#ffb547;letter-spacing:.2em;text-transform:uppercase}
.reasonb{font-size:120px;font-weight:900;margin-top:24px;max-width:1600px;line-height:1.05}
.bars{display:flex;gap:120px;align-items:flex-end;height:520px;margin-top:20px}
.barcol{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:520px;width:300px}
.barval{font-size:110px;font-weight:900;margin-bottom:16px}
.bar{width:220px;border-radius:14px 14px 0 0;transform-origin:50% 100%}
.barlbl{font-size:52px;font-weight:700;margin-top:18px;color:#c9d1dc}
.cigs{display:flex;gap:22px;margin-top:40px}
.cig{width:42px;height:200px;border-radius:8px;background:linear-gradient(#ff6a3d 0 10%,#e9e4da 10% 72%,#d08c3e 72% 100%)}
.steps{display:flex;gap:40px;margin-top:30px;align-items:center}
.step{width:450px;padding:44px 20px;white-space:nowrap;border-radius:24px;background:#151c28;border:3px solid #2a3445}
.step.last{border-color:#ffb547}
.stepv{font-size:84px;font-weight:900;color:#ffb547}
.stepl{font-size:48px;font-weight:700;margin-top:10px}
.arrow{font-size:80px;color:#6f7b8d}
"""

def scene(c):
    k = c["kind"]
    src = f'<div id="src" class="src">Source: {c["src"]}</div>' if c["src"] else ""
    if k == "title":
        body = f'<div id="t1" class="title1">{c["big"]}</div><div id="t2" class="title2">{c["sub"]}</div><div id="rule" class="rule"></div>'
        js = """tl.from('#t1',{y:40,opacity:0,duration:.6,ease:'power3.out'},.2)
.from('#t2',{y:60,opacity:0,scale:.92,duration:.8,ease:'power3.out'},.6)
.to('#rule',{width:900,duration:.8,ease:'power2.inOut'},1.2)
.to('#t2',{scale:1.03,duration:2.4,ease:'none'},1.4);"""
    elif k == "ratio":
        dots = "".join(f'<div class="dot{" on" if i==0 else ""}" id="d{i}"></div>' for i in range(6))
        body = f'<div id="kicker" class="kicker">{c["kicker"]}</div><div id="big" class="big">{c["big"]}</div><div class="dots">{dots}</div><div id="sub" class="sub">{c["sub"]}</div>'
        js = """tl.from('#kicker',{y:30,opacity:0,duration:.5},.2)
.from('#big',{y:60,opacity:0,scale:.9,duration:.7,ease:'back.out(1.6)'},.5)
.from('.dot',{scale:0,opacity:0,duration:.35,stagger:.12,ease:'back.out(2)'},1.1)
.from('#d0',{backgroundColor:'#2a3445',duration:.5},2.0)
.from('#sub',{y:30,opacity:0,duration:.5},2.1);"""
    elif k in ("stat",):
        body = f'<div id="kicker" class="kicker">{c["kicker"]}</div><div id="big" class="big">{c["big"]}</div><div id="sub" class="sub">{c["sub"]}</div>'
        js = """tl.from('#kicker',{y:30,opacity:0,duration:.5},.2)
.from('#big',{y:60,opacity:0,scale:.85,duration:.8,ease:'back.out(1.6)'},.5)
.from('#sub',{y:30,opacity:0,duration:.5},1.2)
.to('#big',{scale:1.04,duration:3,ease:'none'},1.4);"""
    elif k in ("count", "cigs"):
        extra = ""
        if k == "cigs":
            extra = '<div class="cigs">' + "".join(f'<div class="cig" id="c{i}"></div>' for i in range(15)) + "</div>"
        body = f'<div id="kicker" class="kicker">{c["kicker"]}</div><div id="big" class="big">0</div>{extra}<div id="sub" class="sub">{c["sub"]}</div>'
        js = f"""const o={{v:0}};const fmt=v=>Math.round(v).toLocaleString('en-US');
tl.from('#kicker',{{y:30,opacity:0,duration:.5}},.2)
.from('#big',{{opacity:0,duration:.3}},.5)
.to(o,{{v:{c['count']},duration:1.8,ease:'power2.out',onUpdate:()=>{{document.getElementById('big').textContent=fmt(o.v)}}}},.5)
.from('#sub',{{y:30,opacity:0,duration:.5}},2.0);
"""
        if k == "cigs":
            js += "tl.from('.cig',{y:80,opacity:0,duration:.3,stagger:.1,ease:'power2.out'},.6);"
    elif k == "compare":
        mx = max(c["a_val"], c["b_val"])
        ha = int(380 * c["a_val"] / mx); hb = int(380 * c["b_val"] / mx)
        body = f'''<div id="kicker" class="kicker">{c["kicker"]}</div><div class="bars">
<div class="barcol"><div id="va" class="barval" style="color:#9aa6b8">{c["a_val"]}%</div><div id="ba" class="bar" style="height:{ha}px;background:#3a4659"></div><div class="barlbl">{c["a_label"]}</div></div>
<div class="barcol"><div id="vb" class="barval" style="color:#ffb547">{c["b_val"]}%</div><div id="bb" class="bar" style="height:{hb}px;background:#ffb547"></div><div class="barlbl">{c["b_label"]}</div></div></div>'''
        js = """tl.from('#kicker',{y:30,opacity:0,duration:.5},.2)
.from('#ba',{scaleY:0,duration:.8,ease:'power3.out'},.6)
.from('#va',{opacity:0,y:20,duration:.4},1.1)
.from('#bb',{scaleY:0,duration:1.0,ease:'power3.out'},1.5)
.from('#vb',{opacity:0,y:20,scale:.8,duration:.5,ease:'back.out(2)'},2.2);"""
    elif k == "reason":
        body = f'<div id="kicker" class="reasonk">{c["kicker"]}</div><div id="big" class="reasonb">{c["big"]}</div><div id="rule" class="rule"></div>'
        js = """tl.from('#kicker',{y:30,opacity:0,duration:.4},.15)
.from('#big',{y:50,opacity:0,duration:.6,ease:'power3.out'},.4)
.to('#rule',{width:500,duration:.6,ease:'power2.inOut'},.8);"""
    elif k == "hours":
        parts = []
        for i, (v, l) in enumerate(c["steps"]):
            if i: parts.append(f'<div class="arrow" id="ar{i}">→</div>')
            parts.append(f'<div class="step{" last" if i==2 else ""}" id="s{i}"><div class="stepv">{v}</div><div class="stepl">{l}</div></div>')
        body = f'<div id="kicker" class="kicker">{c["kicker"]}</div><div class="steps">{"".join(parts)}</div>'
        js = """tl.from('#kicker',{y:30,opacity:0,duration:.5},.2)
.from('#s0',{y:60,opacity:0,duration:.6,ease:'back.out(1.6)'},.7)
.from('#ar1',{opacity:0,x:-20,duration:.3},1.6)
.from('#s1',{y:60,opacity:0,duration:.6,ease:'back.out(1.6)'},1.8)
.from('#ar2',{opacity:0,x:-20,duration:.3},2.8)
.from('#s2',{y:60,opacity:0,scale:.9,duration:.7,ease:'back.out(1.6)'},3.0);"""
    if c["src"]:
        js += "\ntl.from('#src',{opacity:0,duration:.5},1.0);"
    return body + src, js

def html(c):
    body, js = scene(c)
    d = c["dur"]
    return f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1920, height=1080"/>
<title>{c['id']}</title>
<script src="gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-width="1920" data-height="1080" data-duration="{d}">
<div id="bg" class="bg clip" data-start="0" data-duration="{d}" data-track-index="0"></div>
<div id="glow" class="glow clip" data-start="0" data-duration="{d}" data-track-index="1"></div>
<section id="card" class="scene clip" data-start="0" data-duration="{d}" data-track-index="2">{body}</section>
</div>
<script>
window.__timelines=window.__timelines||{{}};
const tl=gsap.timeline({{paused:true}});
{js}
tl.from('#glow',{{opacity:0,scale:.8,duration:1.2,ease:'power2.out'}},0);
tl.to('#card',{{opacity:0,duration:.35}},{d-0.35});
window.__timelines["main"]=tl;
</script></body></html>"""

if __name__ == "__main__":
    only = sys.argv[1:]
    for c in CARDS:
        if only and c["id"] not in only: continue
        d = OUT / c["id"]; d.mkdir(exist_ok=True)
        (d / "index.html").write_text(html(c), encoding="utf-8"); (d / "gsap.min.js").write_bytes((OUT / "gsap.min.js").read_bytes())
        print(d)
