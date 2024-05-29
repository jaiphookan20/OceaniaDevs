import string

# Define a dictionary to store the categories and their corresponding keywords
categories = {
    'Programming Languages': ['typescript','javascript', 'python', 'java', 'c++', 'c#', 'php', 'swift', 'ruby', 'kotlin', 'go', 'r', 'rust', 'scala', 'dart', 'perl', 'clojure', 'haskell', 'erlang', 'elixir', 'groovy', 'objective-c', 'assembly', 'fortran', 'cobol', 'bash', 'shell', 'sql'],
    'Web Development': ['html', 'css', 'react', 'angular', 'vue.js', 'jquery', 'bootstrap', 'sass', 'less', 'node.js', 'express.js', 'django', 'flask', 'ruby on rails', 'asp.net', 'spring', 'laravel'],
    'Mobile App Development': ['react native', 'flutter', 'xamarin', 'ionic', 'nativescript', 'cordova'],
    'Game Development': ['unity', 'unreal engine', 'godot', 'cocos2d', 'libgdx'],
    'Databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'oracle', 'sql server', 'firebase'],
    'Cloud Computing': ['aws', 'amazon web services', 'azure', 'microsoft azure', 'google cloud platform', 'gcp','heroku', 'digitalocean'],
    'DevOps': ['docker', 'kubernetes', 'jenkins', 'ansible', 'terraform', 'vagrant', 'grafana', 'terraform', 'prometheus', 'zscaler'],
    # Add more categories as needed
}

icons = {
    'aws': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" />',
    "Docker": '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original-wordmark.svg" />',
    "GCP": '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/googlecloud/googlecloud-original.svg" />',
    "Kubernetes": '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/kubernetes/kubernetes-original-wordmark.svg" />',
    'Angular': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/angularjs/angularjs-original.svg" />',
    'Terraform': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/terraform/terraform-original-wordmark.svg" />',
    'Prometheus': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/prometheus/prometheus-original-wordmark.svg" />',
    'Azure': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/azure/azure-original.svg" />'                   
}


def categorize_words(description):
    categorized_words = {}

    # Initialize the categorized_words dictionary with empty lists for each category
    for category in categories:
        categorized_words[category] = []

    # Split the job description into words and categorize them
    words = description.split()
    for word in words:
        # Remove any trailing punctuation marks from the word
        word_stripped = word.strip(string.punctuation)
        word_lower = word_stripped.lower()
        for category, keywords in categories.items():
            if word_lower in keywords:
                categorized_words[category].append(word)

    # Update the tech_stack column with the categorized words
    tech_stack = []
    # Update the tech_stack column with the deduplicated categorized words
    tech_stack = list(set([word for words in categorized_words.values() for word in words]))
    print(f"tech_stack: {tech_stack}")
    return tech_stack