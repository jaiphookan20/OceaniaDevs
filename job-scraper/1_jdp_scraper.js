const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch({ headless: false, slowMo: 100 });  // Non-headless mode and slow down operations
    const page = await browser.newPage();

    const baseURL = 'https://www.justdigitalpeople.com.au/jobs';
    const allJobs = [];
    let currentPage = 1;

    while (true) {
        console.log(`Scraping page ${currentPage}...`);

        // Navigate to the job listings page
        await page.goto(`${baseURL}?page=${currentPage}`, { waitUntil: 'domcontentloaded' });

        // Extract job links from the current page
        const jobs = await page.evaluate(() => {
            const jobElements = document.querySelectorAll('.job-listing__item-container a');
            const jobsData = [];

            jobElements.forEach(job => {
                const title = job.querySelector('.job-listing__item__title')?.innerText || '';
                const url = job.href || '';
                const jobDetails = job.querySelectorAll('.job-listing__item__text');

                const category = jobDetails[1]?.innerText || '';
                const location = jobDetails[2]?.innerText || '';
                const jobType = jobDetails[3]?.innerText || '';
                const postedDate = jobDetails[4]?.innerText || '';

                jobsData.push({
                    title,
                    url,
                    category,
                    location,
                    jobType,
                    postedDate
                });
            });

            return jobsData;
        });

        console.log(`Found ${jobs.length} jobs on page ${currentPage}.`);  // Log number of jobs found

        // If no jobs are found, break out of the loop
        if (jobs.length === 0) {
            console.log(`No jobs found on page ${currentPage}. Exiting.`);
            break;
        }

        // Collect job details from individual job pages
        for (const job of jobs) {
            console.log(`Scraping details for job: ${job.title}`);
            await page.goto(job.url, { waitUntil: 'domcontentloaded' });

            const jobDetails = await page.evaluate(() => {
                const jobHighlights = {};
                const detailContainers = document.querySelectorAll('.job-detail__highlight__detail-container');
                
                detailContainers.forEach(container => {
                    const label = container.querySelector('.job-detail__highlight__label')?.innerText || '';
                    const detail = container.querySelector('.job-detail__highlight__detail')?.innerText || '';

                    if (label.includes('Salary Period')) jobHighlights.salaryPeriod = detail;
                    if (label.includes('Posted On')) jobHighlights.postedDate = detail;
                });

                // Additional details from job page
                jobHighlights.technology = document.querySelector('.job-detail__highlight__detail-container:nth-child(1) .job-detail__highlight__detail')?.innerText || '';
                jobHighlights.category = document.querySelector('.job-detail__highlight__detail-container:nth-child(2) .job-detail__highlight__detail')?.innerText || '';
                jobHighlights.location = document.querySelector('.job-detail__highlight__detail-container:nth-child(3) .job-detail__highlight__detail')?.innerText || '';
                jobHighlights.jobType = document.querySelector('.job-detail__highlight__detail-container:nth-child(4) .job-detail__highlight__detail')?.innerText || '';

                const description = document.querySelector('.job-detail__section__content')?.innerText || '';
                const contactEmail = document.querySelector('.job-detail__section__email')?.innerText || '';
                const applyLink = document.querySelector('.job-detail__button')?.href || '';

                return {
                    jobHighlights,
                    description,
                    contactEmail,
                    applyLink
                };
            });

            console.log(`Finished scraping details for job: ${job.title}`);  // Log after scraping job details

            // Combine basic job info with details
            allJobs.push({
                ...job,
                ...jobDetails
            });

            // Add a delay between job page navigations
            await new Promise(r => setTimeout(r, 2000)); // Use this instead of waitForTimeout
        }

        // Try to navigate to the next page
        currentPage++;

        // Assuming there are only 9 pages based on your example; change if there are more
        if (currentPage > 9) {
            console.log('All pages scraped.');
            break;
        }
    }

    // Write the jobs data to a JSON file
    fs.writeFileSync('jobs.json', JSON.stringify(allJobs, null, 2));
    console.log('All jobs data has been saved to jobs.json');

    // Prevent automatic browser closure
    // await browser.close();
})();
