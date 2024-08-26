const puppeteer = require('puppeteer');
const fs = require('fs');

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

// Function to scrape individual job listing page
async function scrapeJobListing(page, url) {
    await page.goto(url, { waitUntil: 'networkidle0' });
    
    return page.evaluate(() => {
        const jobDetails = {};
        
        // Extract job description
        jobDetails.fullDescription = document.querySelector('div[data-automation="jobAdDetails"]')?.innerText.trim() || '';
        
        // Extract employer questions
        const questions = Array.from(document.querySelectorAll('ul._1ullll03._1cecker0._1cecker5 li'));
        jobDetails.employerQuestions = questions.map(q => q.innerText.trim());
        
        return jobDetails;
    });
}

(async () => {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    // Set a custom user agent
    await page.setUserAgent(getRandomUserAgent());

    // Set a custom viewport
    await page.setViewport({ width: 1366, height: 768 });

    const baseURL = 'https://www.seek.com.au/jobs-in-information-communication-technology/developers-programmers';
    const allJobs = [];
    let currentPage = 2;

    while (true) {
        console.log(`Scraping page ${currentPage}...`);

        // Add a random delay before each page request
        await randomDelay(3000, 7000);

        const url = currentPage === 1 ? baseURL : `${baseURL}?page=${currentPage}`;
        
        try {
            await page.goto(url, { 
                waitUntil: 'networkidle0',
                timeout: 60000 // Increase timeout to 60 seconds
            });
        } catch (error) {
            console.error(`Error navigating to page ${currentPage}:`, error.message);
            break;
        }

        const jobs = await page.evaluate(() => {
            const jobElements = document.querySelectorAll('article[data-automation="normalJob"]');
            return Array.from(jobElements).map(job => {
                const title = job.querySelector('h3 a')?.innerText.trim() || '';
                const url = job.querySelector('h3 a')?.href || '';
                const company = job.querySelector('a[data-automation="jobCompany"]')?.innerText.trim() || '';
                const location = job.querySelector('span[data-automation="jobCardLocation"]')?.innerText.trim() || '';
                const salary = job.querySelector('span[data-automation="jobSalary"]')?.innerText.trim() || '';
                const jobType = job.querySelector('div._1ullll00._13mb3jh5i._13mb3jh0._11dkhbh0 p')?.innerText.trim() || '';
                const classification = job.querySelector('a[data-type="classification"]')?.innerText.trim() || '';
                const subClassification = job.querySelector('a[data-type="subClassification"]')?.innerText.trim() || '';
                const highlights = Array.from(job.querySelectorAll('ul._1ullll03 li')).map(li => li.innerText.trim());
                const description = job.querySelector('span[data-testid="job-card-teaser"]')?.innerText.trim() || '';
                const postedDate = job.querySelector('span[data-automation="jobListingDate"]')?.innerText.trim() || '';

                return {
                    title,
                    url,
                    company,
                    location,
                    salary,
                    jobType,
                    classification,
                    subClassification,
                    highlights,
                    description,
                    postedDate
                };
            });
        });

        console.log(`Found ${jobs.length} jobs on page ${currentPage}.`);

        if (jobs.length === 0) {
            console.log(`No jobs found on page ${currentPage}. Exiting.`);
            break;
        }

        // Scrape full details for each job
        for (const job of jobs) {
            console.log(`Scraping full details for: ${job.title}`);
            await randomDelay(2000, 5000); // Random delay between job scrapes
            const fullDetails = await scrapeJobListing(page, job.url);
            allJobs.push({ ...job, ...fullDetails });
        }

        // Check if there's a "Next" button
        const hasNextPage = await page.evaluate(() => {
            const nextButton = document.querySelector('a[data-automation="page-next"]');
            return nextButton !== null;
        });

        if (!hasNextPage) {
            console.log('No more pages to scrape.');
            break;
        }

        currentPage++;

        // Break after a certain number of pages (e.g., 20) to avoid over-scraping
        if (currentPage > 4) {
            console.log('Reached maximum page limit. Stopping scrape.');
            break;
        }
    }

    fs.writeFileSync('seek_jobs.json', JSON.stringify(allJobs, null, 2));
    console.log('All jobs data with full details has been saved to seek_jobs.json');

    await browser.close();
})();

// const puppeteer = require('puppeteer');
// const fs = require('fs');

// // Function to add a random delay
// const randomDelay = (min, max) => {
//     return new Promise(resolve => {
//         const delay = Math.floor(Math.random() * (max - min + 1) + min);
//         setTimeout(resolve, delay);
//     });
// };

// // Function to rotate user agents
// const userAgents = [
//     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
//     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
//     'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
//     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
// ];

// const getRandomUserAgent = () => {
//     return userAgents[Math.floor(Math.random() * userAgents.length)];
// };

// // Function to scrape individual job listing page
// async function scrapeJobListing(page, url) {
//     await page.goto(url, { waitUntil: 'networkidle0' });
    
//     return page.evaluate(() => {
//         const jobDetails = {};
        
//         // Extract job description
//         jobDetails.fullDescription = document.querySelector('div[data-automation="jobAdDetails"]')?.innerText.trim() || '';
        
//         // Extract employer questions
//         const questions = Array.from(document.querySelectorAll('ul._1ullll03._1cecker0._1cecker5 li'));
//         jobDetails.employerQuestions = questions.map(q => q.innerText.trim());
        
//         // Extract any other relevant information from the full listing
//         // For example, you might want to get more specific details that are only available on the full listing page
        
//         return jobDetails;
//     });
// }

// (async () => {
//     const browser = await puppeteer.launch({ headless: false });
//     const page = await browser.newPage();

//     // Set a custom user agent
//     await page.setUserAgent(getRandomUserAgent());

//     // Set a custom viewport
//     await page.setViewport({ width: 1366, height: 768 });

//     const baseURL = 'https://www.seek.com.au/jobs-in-information-communication-technology';
//     const allJobs = [];
//     let currentPage = 1;

//     while (true) {
//         console.log(`Scraping page ${currentPage}...`);

//         // Add a random delay before each page request
//         await randomDelay(3000, 7000);

//         try {
//             await page.goto(`${baseURL}${currentPage > 1 ? '?page=' + currentPage : ''}`, { 
//                 waitUntil: 'networkidle0',
//                 timeout: 60000 // Increase timeout to 60 seconds
//             });
//         } catch (error) {
//             console.error(`Error navigating to page ${currentPage}:`, error.message);
//             break;
//         }

//         // Take a screenshot only occasionally
//         // if (Math.random() < 0.2) {
//         //     await page.screenshot({ path: `page-${currentPage}.png` });
//         // }

//         const jobs = await page.evaluate(() => {
//             const jobElements = document.querySelectorAll('article[data-automation="normalJob"]');
//             return Array.from(jobElements).map(job => {
//                 const title = job.querySelector('h3 a')?.innerText.trim() || '';
//                 const url = job.querySelector('h3 a')?.href || '';
//                 const company = job.querySelector('a[data-automation="jobCompany"]')?.innerText.trim() || '';
//                 const location = job.querySelector('span[data-automation="jobCardLocation"]')?.innerText.trim() || '';
//                 const salary = job.querySelector('span[data-automation="jobSalary"]')?.innerText.trim() || '';
//                 const jobType = job.querySelector('div._1ullll00._13mb3jh5i._13mb3jh0._11dkhbh0 p')?.innerText.trim() || '';
//                 const classification = job.querySelector('a[data-type="classification"]')?.innerText.trim() || '';
//                 const subClassification = job.querySelector('a[data-type="subClassification"]')?.innerText.trim() || '';
//                 const highlights = Array.from(job.querySelectorAll('ul._1ullll03 li')).map(li => li.innerText.trim());
//                 const description = job.querySelector('span[data-testid="job-card-teaser"]')?.innerText.trim() || '';
//                 const postedDate = job.querySelector('span[data-automation="jobListingDate"]')?.innerText.trim() || '';

//                 return {
//                     title,
//                     url,
//                     company,
//                     location,
//                     salary,
//                     jobType,
//                     classification,
//                     subClassification,
//                     highlights,
//                     description,
//                     postedDate
//                 };
//             });
//         });

//         console.log(`Found ${jobs.length} jobs on page ${currentPage}.`);

//         if (jobs.length === 0) {
//             console.log(`No jobs found on page ${currentPage}. Exiting.`);
//             break;
//         }

//         // Scrape full details for each job
//         for (const job of jobs) {
//             console.log(`Scraping full details for: ${job.title}`);
//             await randomDelay(2000, 5000); // Random delay between job scrapes
//             const fullDetails = await scrapeJobListing(page, job.url);
//             allJobs.push({ ...job, ...fullDetails });
//         }

//         // Check if there's a "Next" button
//         const hasNextPage = await page.evaluate(() => {
//             const nextButton = document.querySelector('a[data-automation="page-next"]');
//             return nextButton !== null;
//         });

//         if (!hasNextPage) {
//             console.log('No more pages to scrape.');
//             break;
//         }

//         currentPage++;

//         // Break after a certain number of pages (e.g., 20) to avoid over-scraping
//         if (currentPage > 20) {
//             console.log('Reached maximum page limit. Stopping scrape.');
//             break;
//         }
//     }

//     fs.writeFileSync('seek_jobs.json', JSON.stringify(allJobs, null, 2));
//     console.log('All jobs data with full details has been saved to seek_jobs.json');

//     await browser.close();
// })();