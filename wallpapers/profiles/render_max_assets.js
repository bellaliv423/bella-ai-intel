// Render all Max-related assets
// Usage: node render_max_assets.js  (or run render_max_assets.bat)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const PROFILES_DIR = __dirname;                                    // .../wallpapers/profiles
const WALLPAPERS_DIR = path.resolve(__dirname, '..');               // .../wallpapers
const INSTA_DIR = path.join(WALLPAPERS_DIR, 'instagram');

const TASKS = [
  // [label, html path, output path, {w, h}]
  ['MAX profile 1080',   path.join(PROFILES_DIR, 'profile_max.html'),                 path.join(PROFILES_DIR, 'profile_max_1080x1080.png'), {w:1080, h:1080}],
  ['MAX thumbnail 320',  path.join(PROFILES_DIR, 'profile_max.html'),                 path.join(PROFILES_DIR, 'max.png'),                   {w:1080, h:1080, resize:320}],
  ['4 Brothers banner',  path.join(PROFILES_DIR, 'leader_profiles_4bros.html'),       path.join(PROFILES_DIR, 'leader_profiles_full.png'),  {w:1920, h:420}],
  ['Wallpaper v8 PC',    path.join(WALLPAPERS_DIR, 'v8_final.html'),                  path.join(WALLPAPERS_DIR, 'dreamteam_pc_1920x1080.png'), {w:1920, h:1080, backup:'dreamteam_pc_1920x1080_v7_backup.png'}],
  ['Insta profile 320',  path.join(INSTA_DIR, 'insta_profile_4bros_320.html'),        path.join(INSTA_DIR, 'insta_profile_4bros_320.png'),  {w:320, h:320}],
  ['Insta post 1080',    path.join(INSTA_DIR, 'insta_post_16_1080.html'),             path.join(INSTA_DIR, 'insta_post_16_1080.png'),       {w:1080, h:1080}],
  ['Insta story 1920',   path.join(INSTA_DIR, 'insta_story_max_1080x1920.html'),      path.join(INSTA_DIR, 'insta_story_max_1080x1920.png'),{w:1080, h:1920}],
];

(async () => {
  console.log('=== MAX Assets Renderer ===');
  const browser = await chromium.launch({ headless: true });

  for (const [label, html, out, opts] of TASKS) {
    if (!fs.existsSync(html)) { console.log(`  [SKIP] ${label} — HTML not found: ${html}`); continue; }
    // Backup existing PNG if requested
    if (opts.backup) {
      const backupPath = path.join(path.dirname(out), opts.backup);
      if (fs.existsSync(out) && !fs.existsSync(backupPath)) {
        fs.copyFileSync(out, backupPath);
        console.log(`  [backup] ${opts.backup}`);
      }
    }
    const page = await browser.newPage({ viewport: { width: opts.w, height: opts.h } });
    await page.goto('file:///' + html.replace(/\\/g, '/'));
    await page.waitForTimeout(1800); // fonts + canvas render
    await page.screenshot({ path: out, fullPage: false });
    await page.close();
    console.log(`  [OK] ${label} -> ${path.basename(out)} (${opts.w}x${opts.h})`);

    // Resize for thumbnail (max.png 320x320) — use a second shot at 320x320 viewport with CSS scaling
    if (opts.resize) {
      const p2 = await browser.newPage({ viewport: { width: opts.resize, height: opts.resize } });
      await p2.goto('file:///' + html.replace(/\\/g, '/'));
      await p2.addStyleTag({ content: `html,body{transform:scale(${opts.resize/opts.w});transform-origin:0 0;width:${opts.w}px;height:${opts.h}px}` });
      await p2.waitForTimeout(1500);
      await p2.screenshot({ path: out, clip: {x:0, y:0, width:opts.resize, height:opts.resize} });
      await p2.close();
      console.log(`      [resize] ${path.basename(out)} -> ${opts.resize}x${opts.resize}`);
    }
  }

  await browser.close();
  console.log('\nAll done! Check the PNGs in:');
  console.log('  ' + PROFILES_DIR);
  console.log('  ' + WALLPAPERS_DIR);
  console.log('  ' + INSTA_DIR);
})().catch(e => { console.error(e); process.exit(1); });
