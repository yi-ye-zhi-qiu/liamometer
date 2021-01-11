/*
Configure as webapp
*/
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('')
  const price = await page.$eval('.', div => div.textContent);
  console.log(price);
  await page.waitFor(1000);
  await browser.close();
})
