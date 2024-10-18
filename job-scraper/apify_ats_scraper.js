const { ApifyClient } = require("apify-client");
const fs = require('fs');
const path = require('path');
const { scrapeWorkableJob } = require('./workable_scraper');

// Initialize the ApifyClient with API token
const client = new ApifyClient({
    token: 'apify_api_pC4ZbWh2kb7p8EWpmIObMJm2jcUWpW1yNeri',
});

// Prepare Actor input
const input = {
    "customquery": {
        "aulogicalis": "workable",
        // "clickview": "workable",
        // "infosys-singaporeand-australia": "workable",
        "auspayplus": "workable",
        // "archipro-3": "workable",
        "demystdata": "workable",
        "ofload": "workable",
        "datacom1": "workable",
        "compass-education": "workable",
        // "centorrino-technologies": "workable",
        // "bjak-1": "workable",
        // "employment-hero": "workable",
        // "entaingroup": "workable",
        // "onlife": "workable",
        // "blueapache-pty-ltd": "workable",
        // "engflow": "workable",
        // "creditorwatch": "workable",
        // "shopgrok": "workable",
        // "spinfy-jobs": "workable"
    },
    "delay": 10,
    "greenhouse": true,
    "lever": true,
    "maximum": 20,
    "personio": true,
    "proxy": {
        "useApifyProxy": true,
        "apifyProxyGroups": [
            "RESIDENTIAL"
        ],
        "apifyProxyCountry": "AU"
    },
    "recruitee": true,
    "smartrecruiters": true,
    "timeout": 15,
    "workable": true,
    "workday": true
}


// Define the async function
async function runActor() {
    try {
        // Run the Actor and wait for it to finish
        const run = await client.actor("1tyt3GCvjd14p6Ih6").call(input);

        // Fetch Actor results from the run's dataset
        console.log('Fetching results from dataset');
        const { items } = await client.dataset(run.defaultDatasetId).listItems();
        
        // Process and filter the results
        const processedItems = await processScrapedJobs(items);

        // Write processed results to file
        const resultsDir = path.join(__dirname, 'results');
        const outputPath = path.join(resultsDir, 'ats_scraper_results.json');

        if (!fs.existsSync(resultsDir)) {
            fs.mkdirSync(resultsDir, { recursive: true });
        }

        fs.writeFileSync(outputPath, JSON.stringify(processedItems, null, 2), 'utf8');
        console.log('Processed results have been written to ats_scraper_results.json');
    } catch (error) {
        console.error('An error occurred during actor run:', error);
    }
}

const companyDepartments = {
    "aulogicalis": ["Managed Services (MS)"],
    "auspayplus": ["Technology"],
    "demystdata": ["Delivery", "Customer Success", "Engineering"],
    "ofload": ["Technology"],
    "datacom1": ["Technology", "Infrastructure Products"],
    "compass-education": ["Product"],
};

async function processScrapedJobs(items) {
    const processedItems = [];

    for (const company of items) {
        const allowedDepartments = companyDepartments[company.name] || [];

        for (const job of company.result) {
            try {
                if (!job.location.endsWith(", AU") || 
                    (allowedDepartments.length > 0 && !allowedDepartments.includes(job.department))) {
                    continue;
                }

                let processedJob = {
                    title: job.title,
                    company: company.name,
                    location: job.location,
                    url: job.url,
                    department: job.department,
                    remote: job.remote,
                    experience: job.experience,
                    updatedAt: job.updatedAt
                };

                if (company.source === 'workable') {
                    console.log(`Scraping additional details for ${job.title} at ${job.url}`);
                    const workableDetails = await scrapeWorkableJob(job.url);
                    console.log(`Workable details for ${job.title}:`, workableDetails);
                    processedJob = { ...processedJob, ...workableDetails };
                    await delay(3000);
                }

                processedItems.push(processedJob);
                console.log(`Processed job: ${job.title} for ${company.name}`);
            } catch (error) {
                console.error(`Error processing job ${job.title} for ${company.name}:`, error);
            }
        }
    }

    return processedItems;
}

// Call the async function
runActor().catch(error => console.error('Error in runActor:', error));
