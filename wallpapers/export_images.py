"""
Dream Team Wallpaper → PNG 이미지 변환
PC(1920x1080) + Samsung Galaxy Z Flip 6 (1080x2640 커버: 720x748)
"""
from playwright.sync_api import sync_playwright
import os

WALL_DIR = os.path.dirname(os.path.abspath(__file__))

def export_pc():
    """v7_final.html → PNG (1920x1080)"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(f"file:///{WALL_DIR}/v7_final.html".replace("\\", "/"))
        page.wait_for_timeout(2000)
        out = os.path.join(WALL_DIR, "dreamteam_pc_1920x1080.png")
        page.screenshot(path=out, full_page=False)
        browser.close()
        print(f"[OK] PC wallpaper: {out}")

def export_mobile():
    """v7 모바일 버전 → PNG (1080x2640, Galaxy Z Flip 6 메인)"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Flip 6 메인 화면: 1080x2640
        page = browser.new_page(viewport={"width": 1080, "height": 2640})
        page.goto(f"file:///{WALL_DIR}/v7_mobile.html".replace("\\", "/"))
        page.wait_for_timeout(2000)
        out = os.path.join(WALL_DIR, "dreamteam_flip6_1080x2640.png")
        page.screenshot(path=out, full_page=False)
        browser.close()
        print(f"[OK] Flip6 wallpaper: {out}")

if __name__ == "__main__":
    export_pc()
    print("[NEXT] Creating mobile version...")
    export_mobile()
    print("[DONE] All images exported!")
