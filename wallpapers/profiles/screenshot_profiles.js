const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const htmlPath = path.resolve(__dirname, 'leader_profiles.html');
  await page.goto(`file:///${htmlPath.replace(/\\/g, '/')}`);
  await page.waitForTimeout(2000); // wait for fonts + canvas render

  // Full 6-profile strip (1920x320 visible area)
  await page.setViewportSize({ width: 1920, height: 320 });
  await page.screenshot({ path: path.join(__dirname, 'leader_profiles_full.png'), fullPage: false });
  console.log('OK: leader_profiles_full.png (1920x320)');

  // Individual cards (320x320 each)
  const names = ['goldi', 'robo', 'windy', 'collie', 'shiba', 'cam'];
  for (let i = 0; i < 6; i++) {
    const card = (await page.$$('.card'))[i];
    await card.screenshot({ path: path.join(__dirname, `${names[i]}.png`) });
    console.log(`OK: ${names[i]}.png (320x320)`);
  }

  await browser.close();
  console.log('Done!');
})();
