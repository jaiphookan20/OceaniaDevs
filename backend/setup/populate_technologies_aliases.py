from app import create_app
from extensions import db
from models import Technology, TechnologyAlias
from flask import current_app

def populate_technologies_and_aliases():
    technologies = {
        "html": ["html"],
        "css": ["css"],
        "selenium": ["selenium"],
        "sap": ["sap"],
        "syniti": ["syniti"],
        "puppeteer": ["puppeteer"],
        "aws": ["aws", "amazon web services"],
        "docker": ["docker"],
        "gcp": ["gcp", "google cloud platform"],
        "kubernetes": ["kubernetes", "k8s"],
        "angular": ["angular", "angularjs"],
        "terraform": ["terraform"],
        "prometheus": ["prometheus"],
        "azure": ["azure", "microsoft azure"],
        "reactjs": ["reactjs", "react", "react.js"],
        "nodejs": ["nodejs", "node.js", "node"],
        "python": ["python"],
        "pydantic": ["pydantic"],
        "java": ["java"],
        "csharp": ["csharp", "c#", "c sharp"],
        "javascript": ["javascript", "js"],
        "typescript": ["typescript", "ts"],
        "ruby": ["ruby"],
        "golang": ["golang", "go"],
        "kotlin": ["kotlin"],
        "tensorflow": ["tensorflow"],
        "rust": ["rust"],
        "swift": ["swift"],
        "django": ["django"],
        "flask": ["flask"],
        "fastapi": ["fastapi"],
        "jest": ["jest"],
        "rubyonrails": ["rubyonrails", "ruby on rails", "rails"],
        "spring": ["spring", "spring boot"],
        "dotnet": ["dotnet", ".net", "asp.net"],
        "mysql": ["mysql"],
        "postgresql": ["postgresql", "postgres"],
        "mongodb": ["mongodb"],
        "redis": ["redis"],
        "kafka": ["kafka"],
        "git": ["git"],
        "github": ["github"],
        "gitlab": ["gitlab"],
        "jenkins": ["jenkins"],
        "travisci": ["travisci", "travis ci"],
        "vuejs": ["vuejs", "vue", "vue.js"],
        "redux": ["redux"],
        "webpack": ["webpack"],
        "babel": ["babel"],
        "sass": ["sass"],
        "less": ["less"],
        "jquery": ["jquery"],
        "bootstrap": ["bootstrap"],
        "materialui": ["materialui", "material-ui"],
        "cplusplus": ["cplusplus", "c++"],
        "php": ["php"],
        "laravel": ["laravel"],
        "symfony": ["symfony"],
        "codeigniter": ["codeigniter"],
        "ionic": ["ionic"],
        "android": ["android"],
        "firebase": ["firebase"],
        "graphql": ["graphql"],
        "elasticsearch": ["elasticsearch", "elastic search"],
        "nginx": ["nginx"],
        "apache": ["apache"],
        "linux": ["linux"],
        "bash": ["bash"],
        "vim": ["vim"],
        "vscode": ["vscode", "visual studio code"],
        "intellij": ["intellij", "intellij idea"],
        "figma": ["figma"],
        "adobeillustrator": ["adobeillustrator", "illustrator"],
        "adobephotoshop": ["adobephotoshop", "photoshop"],
        "adobexd": ["adobexd", "xd"],
        "jira": ["jira"],
        "confluence": ["confluence"],
        "slack": ["slack"],
        "trello": ["trello"],
        "apacheairflow": ["apacheairflow", "airflow"],
        "looker": ["looker"],
        "snowflake": ["snowflake"],
        "dbt": ["dbt"],
        "oracle": ["oracle"],
        "mobx": ["mobx"],
        "cloudflare": ["cloudflare"]
    }

    for tech_name, aliases in technologies.items():
        # Create the Technology entry
        technology = Technology.query.filter_by(name=tech_name).first()
        if not technology:
            technology = Technology(name=tech_name)
            db.session.add(technology)
            db.session.flush()  # This will assign an ID to the new technology

        # Create TechnologyAlias entries
        for alias in aliases:
            existing_alias = TechnologyAlias.query.filter_by(alias=alias).first()
            if not existing_alias:
                new_alias = TechnologyAlias(alias=alias, technology_id=technology.id)
                db.session.add(new_alias)

    db.session.commit()
    current_app.logger.info("Technologies and aliases have been populated successfully.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        populate_technologies_and_aliases()