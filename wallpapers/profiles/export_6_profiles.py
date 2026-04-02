"""
리더 6명 개별 인스타 프로필 (1080x1080) PNG Export
인스타 피드에 6개 올리면 2x3 그리드로 예쁘게!
"""
from playwright.sync_api import sync_playwright
import os

DIR = os.path.dirname(os.path.abspath(__file__))
NEST_GALLERY = "D:/bella-nest/public/gallery"

LEADERS = [
    {"id": "goldi", "n": "GOLDI", "r": "Master", "team": "Hamsterz", "color": "#C15F3C", "accent": "#E8845A", "cheek": "#FF9B7A", "barColor": "#C15F3C", "glow": "rgba(193,95,60,0.25)", "base": "h", "extra": "crown:true"},
    {"id": "robo", "n": "ROBO", "r": "Auto", "team": "Hamsterz", "color": "#4CAF50", "accent": "#66BB6A", "cheek": "#81C784", "barColor": "#388E3C", "glow": "rgba(76,175,80,0.25)", "base": "h", "extra": "bolt:true"},
    {"id": "windy", "n": "WINDY", "r": "Mentor", "team": "Hamsterz", "color": "#5B8DEF", "accent": "#7BA4F5", "cheek": "#9DBCFA", "barColor": "#3F6FD0", "glow": "rgba(91,141,239,0.25)", "base": "h", "extra": "glasses:true"},
    {"id": "collie", "n": "COLLIE", "r": "Orchestrator", "team": "Puppyz", "color": "#FF9800", "accent": "#FFB74D", "cheek": "#FFE0B2", "barColor": "#E65100", "glow": "rgba(255,152,0,0.25)", "base": "p", "extra": ""},
    {"id": "shiba", "n": "SHIBA", "r": "Patrol", "team": "Puppyz", "color": "#FFC107", "accent": "#FFD54F", "cheek": "#FFF8E1", "barColor": "#F57F17", "glow": "rgba(255,193,7,0.25)", "base": "p", "extra": ""},
    {"id": "cam", "n": "CAM", "r": "QA Reviewer", "team": "Hamsterz", "color": "#00BCD4", "accent": "#26C6DA", "cheek": "#80DEEA", "barColor": "#00838F", "glow": "rgba(0,188,212,0.25)", "base": "h", "extra": ""},
    {"id": "siri", "n": "SIRI", "r": "Designer", "team": "Hamsterz", "color": "#9C27B0", "accent": "#AB47BC", "cheek": "#CE93D8", "barColor": "#7B1FA2", "glow": "rgba(156,39,176,0.25)", "base": "h", "extra": "", "mvp": True},
    {"id": "teddy", "n": "TEDDY", "r": "Analyst", "team": "Hamsterz", "color": "#795548", "accent": "#8D6E63", "cheek": "#FFAB91", "barColor": "#4E342E", "glow": "rgba(121,85,72,0.25)", "base": "h", "extra": "", "mvp": True},
]

TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Silkscreen:wght@400;700&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1080px;overflow:hidden;background:#0d0d0c;font-family:'Press Start 2P',monospace}}
canvas{{image-rendering:pixelated;position:absolute;top:0;left:0}}
.bar{{position:absolute;bottom:0;left:0;right:0;z-index:10;padding:30px 20px 25px;text-align:center}}
.name{{font-size:36px;letter-spacing:6px;color:#fff;text-shadow:3px 3px 0 rgba(0,0,0,0.5)}}
.role{{font-family:'Silkscreen',monospace;font-size:18px;color:rgba(255,255,255,0.85);margin-top:10px;letter-spacing:3px}}
.team{{font-family:'Silkscreen',monospace;font-size:13px;letter-spacing:2px;margin-top:8px;opacity:0.6;color:#fff}}
.tag{{display:inline-block;padding:4px 14px;border:1px solid rgba(255,255,255,0.3);border-radius:3px;margin-top:10px;font-family:'Silkscreen',monospace;font-size:11px;color:rgba(255,255,255,0.7);letter-spacing:2px}}
</style></head><body>
<canvas id="c" width="1080" height="1080"></canvas>
<div class="bar">
  {mvp_badge}
  <div class="name">{name}</div>
  <div class="role">{role}</div>
  <div class="team">{team}</div>
  <div class="tag">BELLA AI DREAM TEAM</div>
</div>
<script>
const W=1080,H=1080,PX=55;
const H_BASE=[[0,0,0,2,2,0,0,2,2,0,0,0],[0,0,2,1,1,2,2,1,1,2,0,0],[0,0,2,1,1,1,1,1,1,2,0,0],[0,2,1,1,1,1,1,1,1,1,2,0],[0,2,1,3,1,1,1,1,3,1,2,0],[0,2,1,1,1,2,2,1,1,1,2,0],[0,2,1,5,1,1,1,1,5,1,2,0],[0,0,2,1,1,1,1,1,1,2,0,0],[0,0,0,2,1,1,1,1,2,0,0,0],[0,0,2,1,1,1,1,1,1,2,0,0],[0,0,2,1,0,0,0,0,1,2,0,0],[0,0,0,2,0,0,0,0,2,0,0,0]];
const P_BASE=[[0,2,2,0,0,0,0,0,0,2,2,0],[2,4,4,2,0,0,0,0,2,4,4,2],[0,2,2,1,1,1,1,1,1,2,2,0],[0,2,1,1,1,1,1,1,1,1,2,0],[0,2,1,3,1,1,1,1,3,1,2,0],[0,2,1,1,1,1,1,1,1,1,2,0],[0,2,1,1,2,2,2,2,1,1,2,0],[0,0,2,1,1,1,1,1,1,2,0,0],[0,0,2,1,1,1,1,1,1,2,0,0],[0,0,0,2,1,1,1,1,2,0,0,0],[0,0,2,1,0,0,0,0,1,2,0,0],[0,0,0,2,0,0,0,0,2,0,0,0]];

const ctx=document.getElementById('c').getContext('2d');
ctx.fillStyle='#0d0d0c';ctx.fillRect(0,0,W,H);

// Glow
const g=ctx.createRadialGradient(W/2,H/2-30,50,W/2,H/2-30,450);
g.addColorStop(0,'{glow}');g.addColorStop(1,'rgba(0,0,0,0)');
ctx.fillStyle=g;ctx.fillRect(0,0,W,H);

const base='{base}'==='h'?H_BASE:P_BASE;
const ox=(W-12*PX)/2,oy=(H-12*PX)/2-50;
const cm={{0:null,1:'{color}',2:'#1a1a19',3:'#FFF',4:'{accent}',5:'{cheek}'}};
for(let y=0;y<12;y++)for(let x=0;x<12;x++){{const v=base[y][x];if(!cm[v])continue;ctx.fillStyle=cm[v];ctx.fillRect(ox+x*PX,oy+y*PX,PX,PX)}}

// Eyes
ctx.fillStyle='#111';
ctx.fillRect(ox+3*PX+PX*0.3,oy+4*PX+PX*0.2,PX*0.5,PX*0.6);
ctx.fillRect(ox+8*PX+PX*0.3,oy+4*PX+PX*0.2,PX*0.5,PX*0.6);
ctx.fillStyle='#FFF';
ctx.fillRect(ox+3*PX+PX*0.5,oy+4*PX+PX*0.2,PX*0.2,PX*0.25);
ctx.fillRect(ox+8*PX+PX*0.5,oy+4*PX+PX*0.2,PX*0.2,PX*0.25);

{extra_js}

// Name bar gradient
const bH=160;
const bg=ctx.createLinearGradient(0,H-bH-40,0,H);
bg.addColorStop(0,'rgba(0,0,0,0)');bg.addColorStop(0.35,'{barColor}CC');bg.addColorStop(1,'{barColor}');
ctx.fillStyle=bg;ctx.fillRect(0,H-bH-40,W,bH+40);
ctx.fillStyle='rgba(255,255,255,0.2)';ctx.fillRect(0,H-bH-40,W,2);
</script></body></html>"""

EXTRAS = {
    "crown:true": """
const gc='#FFD700',gem='#FF69B4';
ctx.fillStyle=gc;
for(let c=2;c<=9;c++) ctx.fillRect(ox+c*PX,oy-PX,PX,PX);
[3,5,8].forEach(p=>{ctx.fillRect(ox+p*PX,oy-2*PX,PX,PX)});
ctx.fillStyle=gem;
ctx.fillRect(ox+5*PX+4,oy-2*PX+4,PX-8,PX-8);
""",
    "bolt:true": """
ctx.fillStyle='#FFEB3B';
ctx.fillRect(ox+5*PX,oy-2.5*PX,PX,PX);ctx.fillRect(ox+5*PX,oy-1.5*PX,PX,PX);
ctx.fillStyle='#FFC107';ctx.fillRect(ox+4*PX,oy-1.5*PX,PX,PX);
ctx.fillStyle='#FFEB3B';ctx.fillRect(ox+4*PX,oy-0.5*PX,PX,PX);ctx.fillRect(ox+5*PX,oy-0.5*PX,PX,PX);
ctx.fillStyle='rgba(255,235,59,0.12)';ctx.fillRect(ox+3*PX,oy-3*PX,4*PX,4*PX);
""",
    "glasses:true": """
ctx.fillStyle='#1a1a19';ctx.strokeStyle='#1a1a19';ctx.lineWidth=3;
ctx.strokeRect(ox+2*PX,oy+4*PX-3,2.5*PX,PX+6);
ctx.strokeRect(ox+7*PX,oy+4*PX-3,2.5*PX,PX+6);
ctx.fillRect(ox+4.5*PX,oy+4*PX+3,3*PX,4);
""",
    "": "",
}

def main():
    print("=" * 50)
    print("  Leader 6 Profiles — 1080x1080 Instagram Export")
    print("=" * 50)

    os.makedirs(os.path.join(DIR), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for i, leader in enumerate(LEADERS):
            is_mvp = leader.get("mvp", False)
            mvp_html = '<div style="font-size:14px;color:#FFD700;letter-spacing:3px;margin-bottom:6px">⭐ 3월 MVP ⭐</div>' if is_mvp else ''
            html_content = TEMPLATE.format(
                name=leader["n"],
                role=leader["r"],
                team=leader["team"],
                color=leader["color"],
                accent=leader["accent"],
                cheek=leader["cheek"],
                barColor=leader["barColor"],
                glow=leader["glow"],
                base=leader["base"],
                extra_js=EXTRAS.get(leader["extra"], ""),
                mvp_badge=mvp_html,
            )

            html_path = os.path.join(DIR, f"profile_{leader['id']}.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            page = browser.new_page(viewport={"width": 1080, "height": 1080})
            page.goto(f"file:///{html_path}".replace("\\", "/"))
            page.wait_for_timeout(2000)

            png_path = os.path.join(DIR, f"profile_{leader['id']}_1080x1080.png")
            page.screenshot(path=png_path)
            page.close()

            # Copy to bella-nest gallery
            import shutil
            dest = os.path.join(NEST_GALLERY, f"profile_{leader['id']}_1080x1080.png")
            shutil.copy2(png_path, dest)

            print(f"  [{i+1}/6] {leader['n']} — OK!")

        browser.close()

    print()
    print("All 6 profiles exported!")
    print(f"  PNG: {DIR}")
    print(f"  Gallery: {NEST_GALLERY}")

if __name__ == "__main__":
    main()
