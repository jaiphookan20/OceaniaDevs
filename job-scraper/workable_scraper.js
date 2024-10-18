const puppeteer = require('puppeteer');

// Function to add a random delay
const randomDelay = (min, max) => {
    return new Promise(resolve => {
        const delay = Math.floor(Math.random() * (max - min + 1) + min);
        setTimeout(resolve, delay);
    });
};

// Function to rotate user agents
const userAgents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
];

const getRandomUserAgent = () => {
    return userAgents[Math.floor(Math.random() * userAgents.length)];
};

async function scrapeWorkableJob(url) {
    let browser;
    try {
        browser = await puppeteer.launch({ 
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();

        // Set a random user agent
        await page.setUserAgent(getRandomUserAgent());

        // Set a custom viewport
        await page.setViewport({ width: 1366, height: 768 });

        console.log(`Navigating to ${url}`);
        await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });

        // Add a random delay
        await randomDelay(2000, 5000);

        // Wait for key elements to load
        await page.waitForSelector('body', { timeout: 10000 });
        await page.waitForSelector('section[data-ui="job-description"]', { timeout: 10000 });

        const jobDetails = await page.evaluate(() => {
            const details = {};
            
            const logo = document.querySelector('img[alt][data-object-fit="contain"]');
            details.logo = logo ? logo.src : '';
            
            const jobType = document.querySelector('span[data-ui="job-type"]');
            details.jobType = jobType ? jobType.innerText : '';
            
            const location = document.querySelector('span[data-ellipsis-element="true"]');
            details.location = location ? location.innerText : '';
            
            const description = document.querySelector('section[data-ui="job-description"]');
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
