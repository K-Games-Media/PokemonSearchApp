const puppeteer = require('puppeteer');

async function scrapeFaceToFaceGames(query) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(`https://facetofacegames.com/search?q=${query}`);
    const results = await page.evaluate(() => {
        let items = [];
        document.querySelectorAll('div.product-grid-item').forEach((item) => {
            const title = item.querySelector('h4.card-title') ? item.querySelector('h4.card-title').innerText : '';
            const price = item.querySelector('span.price') ? item.querySelector('span.price').innerText : '';
            if (title && price) {
                items.push(`${title} - ${price}`);
            }
        });
        return items;
    });
    await browser.close();
    return results;
}

async function scrapeHobbiesville(query) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(`https://hobbiesville.com/search/?q=${query}`);
    const results = await page.evaluate(() => {
        let items = [];
        document.querySelectorAll('div.product-grid-item').forEach((item) => {
            const title = item.querySelector('h4.card-title') ? item.querySelector('h4.card-title').innerText : '';
            const price = item.querySelector('span.price') ? item.querySelector('span.price').innerText : '';
            if (title && price) {
                items.push(`${title} - ${price}`);
            }
        });
        return items;
    });
    await browser.close();
    return results;
}

async function scrapeKGamesCollectables(query) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(`https://kgamesncollectables.com/search?q=${query}`);
    const results = await page.evaluate(() => {
        let items = [];
        document.querySelectorAll('div.product-grid-item').forEach((item) => {
            const title = item.querySelector('h4.card-title') ? item.querySelector('h4.card-title').innerText : '';
            const price = item.querySelector('span.price') ? item.querySelector('span.price').innerText : '';
            if (title && price) {
                items.push(`${title} - ${price}`);
            }
        });
        return items;
    });
    await browser.close();
    return results;
}

async function main() {
    const site = process.argv[2];
    const query = process.argv[3];

    let results;
    switch (site) {
        case 'facetofacegames':
            results = await scrapeFaceToFaceGames(query);
            break;
        case 'hobbiesville':
            results = await scrapeHobbiesville(query);
            break;
        case 'kgamescollectables':
            results = await scrapeKGamesCollectables(query);
            break;
        default:
            console.error('Unknown site');
            return;
    }

    console.log(JSON.stringify(results));
}

main().catch(error => {
    console.error('Error in main function:', error);
});