const puppeteer = require('puppeteer');

async function scrapeWorkableJob(url) {
    let browser;
    try {
        browser = await puppeteer.launch({ headless: true });
        const page = await browser.newPage();
        console.log(`Navigating to ${url}`);
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });

        const jobDetails = await page.evaluate(() => {
            const details = {};
            const logo = document.querySelector('a[data-ui="company-logo"] img');
            console.log("logo", logo);
            details.logo = logo ? logo.src : '';
            const jobType = document.querySelector('span[data-ui="job-type"]');
            console.log("jobType", jobType);
            details.jobType = jobType ? jobType.innerText : '';
            const description = document.querySelector('section[data-ui="job-description"]');
            console.log("description", description);
            details.description = description ? description.innerText : '';
            return details;
        });

        console.log(`Scraped details for ${url}:`, jobDetails);
        return jobDetails;
    } catch (error) {
        console.error(`Error scraping Workable job at ${url}:`, error);
        return { logo: '', jobType: '', description: '' };
    } finally {
        if (browser) await browser.close();
    }
}

module.exports = { scrapeWorkableJob };

// If called directly from command line
if (require.main === module) {
    const jobUrl = process.argv[2];
    if (jobUrl) {
        scrapeWorkableJob(jobUrl)
            .then(details => console.log(JSON.stringify(details)))
            .catch(error => console.error('Error:', error))
            .finally(() => process.exit());
    } else {
        console.error('Please provide a Workable job URL as an argument.');
        process.exit(1);
    }
}
