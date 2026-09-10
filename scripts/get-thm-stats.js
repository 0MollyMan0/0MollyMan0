const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
    const context = await chromium.launchPersistentContext('./browser-profile', {
        headless: true,
        viewport: {
            width: 1440,
            height: 1000
        }
    });

    const page = context.pages()[0] || await context.newPage();

    const response = await page.goto(
        'https://tryhackme.com/api/v2/public-profile?username=Mollyman',
        {
            waitUntil: 'domcontentloaded'
        }
    );

    if (response.status() !== 200)
        throw new Error(`HTTP status: ${response.status()}`);

    const json = await response.json();

    if (json.status !== 'success')
        throw new Error('TryHackMe API returned an error');

    const data = json.data;

    const stats = {
        username: data.username,
        level: data.level,
        totalPoints: data.totalPoints,
        badgesNumber: data.badgesNumber,
        completedRoomsNumber: data.completedRoomsNumber,
        rank: data.rank,
        topPercentage: data.topPercentage,
        leagueTier: data.leagueTier,
        capabilityScore: data.capabilityScore.value,
        capabilityPov: data.capabilityScore.pov
    };

    fs.writeFileSync(
        'stats.json',
        JSON.stringify(stats, null, 2) + '\n'
    );

    console.log('THM stats saved to stats.json');

    await context.close();
})();