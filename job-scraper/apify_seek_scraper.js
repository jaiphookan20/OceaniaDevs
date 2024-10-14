const { ApifyClient } = require("apify-client");
const fs = require('fs');
const path = require('path');

// Initialize the ApifyClient with API token
const client = new ApifyClient({
    token: 'apify_api_pC4ZbWh2kb7p8EWpmIObMJm2jcUWpW1yNeri',
});

// Prepare Actor input
const input = {
    "category": [
        "6281"
    ],
    "country": "australia",
    "days": 5,
    "dev_dataset_clear": false,
    "dev_no_strip": false,
    "limit": 5,
    "sort": "date",
    "types.casual": false,
    "types.contract": false,
    "types.full": false,
    "types.part": false
}

// Define the async function
async function runActor() {
    try {
        // Run the Actor and wait for it to finish
        const run = await client.actor("racH8InrI6hwjhzCc").call(input);

        // Fetch Actor results from the run's dataset
        console.log('Results from dataset');
        const { items } = await client.dataset(run.defaultDatasetId).listItems();
        
        // Process and filter the results
        const processedItems = items.map(item => ({
            companyName: item.companyName || (item.advertiser && item.advertiser.description) || "",
            listingDate: item.listingDate,
            workType: item.workType,
            description: item.content,
            companyLogo: (item.branding && item.branding.assets && item.branding.assets.logo && item.branding.assets.logo.strategies && 
                         (item.branding.assets.logo.strategies.jdpLogo || item.branding.assets.logo.strategies.serpLogo)) || "",
            location: item.location,
            teaser: item.teaser,
            title: item.title,
            bulletPoints: item.bulletPoints,
            salary: item.salary,
            workArrangements: (item.workArrangements && item.workArrangements.data) ? 
                              item.workArrangements.data.map(arr => arr.label && arr.label.text).join(", ") : "",
            url: item.url,
            subClassification: item.subClassification ? item.subClassification.description : ""
        }));

        // Call processScrapedJobs to add staged jobs
        await processScrapedJobs(processedItems);

        // Print processed results to console
        processedItems.forEach((item) => {
            console.dir(item);
        });

        // Write processed results to file
        // The current code doesn't handle the case where the 'results' directory doesn't exist
        // We need to create the directory if it doesn't exist before writing the file

        const resultsDir = path.join(__dirname, 'results');
        const outputPath = path.join(resultsDir, 'seek_scraper_results.json');

        // Create the 'results' directory if it doesn't exist
        if (!fs.existsSync(resultsDir)) {
            // Add a comment to highlight the new code
            // Create the 'results' directory
            fs.mkdirSync(resultsDir, { recursive: true });
        }

        // Write the file
        fs.writeFileSync(outputPath, JSON.stringify(processedItems, null, 2), 'utf8');
        console.log('Filtered results have been written to seek_scraper_results.json');
    } catch (error) {
        console.error('An error occurred:', error);
    }
}

// Define processScrapedJobs function
async function processScrapedJobs(jobs) {
    for (const job of jobs) {
        const jobData = {
            title: job.title,
            description: job.description,
            company_name: job.companyName,
            // The following fields are added based on the available data from the scraped job
            listing_date: job.listingDate,
            work_type: job.workType,
            logo_url: job.companyLogo,
            location: job.location,
            teaser: job.teaser,
            bullet_points: job.bulletPoints,
            salary: job.salary,
            work_arrangements: job.workArrangements,
            url: job.url,
            sub_classification: job.subClassification
        };

        try {
            const response = await fetch('http://your-backend-url/api/add_staged_job', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(jobData),
            });

            if (!response.ok) {
                console.error(`Failed to add staged job: ${job.title}`);
            }
        } catch (error) {
            console.error(`Error adding staged job: ${job.title}`, error);
        }
    }
}

// Call the async function
runActor();
