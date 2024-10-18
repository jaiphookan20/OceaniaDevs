const puppeteer = require('puppeteer');

async function scrapeWorkableJob(url) {
    let browser;
    try {
        browser = await puppeteer.launch({ headless: false, slowMo: 50 });  // Non-headless mode and slow down operations
        const page = await browser.newPage();
        console.log(`Navigating to ${url}`);
        await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });

        // Wait for key elements to load
        await page.waitForSelector('body', { timeout: 10000 });
        await page.waitForSelector('section[data-ui="job-description"]', { timeout: 10000 });

        const jobDetails = await page.evaluate(() => {
            const details = {};
            
            const logo = document.querySelector('img[alt][data-object-fit="contain"]');
            console.log("logo element:", logo);
            details.logo = logo ? logo.src : '';
            
            const jobType = document.querySelector('span[data-ui="job-type"]');
            console.log("jobType element:", jobType);
            details.jobType = jobType ? jobType.innerText : '';
            
            const location = document.querySelector('span[data-ellipsis-element="true"]');
            console.log("location element:", location);
            details.location = location ? location.innerText : '';
            
            const description = document.querySelector('section[data-ui="job-description"]');
            console.log("description element:", description);
            details.description = description ? description.innerText : '';
            
            return details;
        });

        console.log(`Scraped details for ${url}:`, jobDetails);
        return jobDetails;
    } catch (error) {
        console.error(`Error scraping Workable job at ${url}:`, error);
        return { logo: '', jobType: '', location: '', description: '' };
    } finally {
        if (browser) {
            console.log("Closing browser...");
            await browser.close();
        }
    }
}

module.exports = { scrapeWorkableJob };

// If called directly from command line
if (require.main === module) {
    const jobUrl = process.argv[2];
    if (jobUrl) {
        scrapeWorkableJob(jobUrl)
            .then(details => {
                console.log("Final scraped details:");
                console.log(JSON.stringify(details, null, 2));
            })
            .catch(error => console.error('Error:', error))
            .finally(() => process.exit());
    } else {
        console.error('Please provide a Workable job URL as an argument.');
        process.exit(1);
    }
}
