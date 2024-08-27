// src/components/TechnologyDropdown.jsx
import React, { useState } from "react";

const icons = {
  aws: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-original-wordmark.svg",
  docker:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original-wordmark.svg",
  gcp: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/googlecloud/googlecloud-original.svg",
  kubernetes:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/kubernetes/kubernetes-original-wordmark.svg",
  angular:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/angularjs/angularjs-original.svg",
  terraform:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/terraform/terraform-original-wordmark.svg",
  prometheus:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/prometheus/prometheus-original-wordmark.svg",
  azure:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/azure/azure-original.svg",
  react:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/react/react-original-wordmark.svg",
  nodejs:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nodejs/nodejs-original-wordmark.svg",
  python:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original-wordmark.svg",
  java: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original-wordmark.svg",
  csharp:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/csharp/csharp-original.svg",
  javascript:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg",
  typescript:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/typescript/typescript-original.svg",
  ruby: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/ruby/ruby-original-wordmark.svg",
  go: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/go/go-original-wordmark.svg",
  rust: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/rust/rust-plain.svg",
  swift:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/swift/swift-original-wordmark.svg",
  django:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/django/django-plain-wordmark.svg",
  flask:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/flask/flask-original-wordmark.svg",
  rails:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/rails/rails-plain-wordmark.svg",
  spring:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/spring/spring-original-wordmark.svg",
  dotnet:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/dotnetcore/dotnetcore-original.svg",
  mysql:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-original-wordmark.svg",
  postgresql:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original-wordmark.svg",
  mongodb:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mongodb/mongodb-original-wordmark.svg",
  redis:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/redis/redis-original-wordmark.svg",
  kafka:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apachekafka/apachekafka-original-wordmark.svg",
  git: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/git/git-original-wordmark.svg",
  github:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/github/github-original-wordmark.svg",
  gitlab:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/gitlab/gitlab-original-wordmark.svg",
  jenkins:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jenkins/jenkins-original.svg",
  travis:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/travis/travis-plain-wordmark.svg",
  vue: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vuejs/vuejs-original-wordmark.svg",
  redux:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/redux/redux-original.svg",
  webpack:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/webpack/webpack-original-wordmark.svg",
  babel:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/babel/babel-original.svg",
  sass: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/sass/sass-original.svg",
  less: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/less/less-plain-wordmark.svg",
  jquery:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jquery/jquery-original-wordmark.svg",
  bootstrap:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/bootstrap/bootstrap-plain-wordmark.svg",
  tailwind:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/tailwindcss/tailwindcss-plain.svg",
  materialui:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/materialui/materialui-original.svg",
  cplusplus:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-original.svg",
  php: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/php/php-original.svg",
  laravel:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/laravel/laravel-plain-wordmark.svg",
  symfony:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/symfony/symfony-original-wordmark.svg",
  codeigniter:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/codeigniter/codeigniter-plain-wordmark.svg",
  ionic:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/ionic/ionic-original-wordmark.svg",
  android:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/android/android-original-wordmark.svg",
  firebase:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/firebase/firebase-plain-wordmark.svg",
  graphql:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/graphql/graphql-plain-wordmark.svg",
  apollostack:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apollostack/apollostack-original.svg",
  elasticsearch:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/elasticsearch/elasticsearch-original-wordmark.svg",
  nginx:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nginx/nginx-original.svg",
  apache:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apache/apache-original-wordmark.svg",
  linux:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/linux/linux-original.svg",
  bash: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/bash/bash-original.svg",
  vim: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vim/vim-original.svg",
  vscode:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vscode/vscode-original-wordmark.svg",
  intellij:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/intellij/intellij-original.svg",
  figma:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/figma/figma-original.svg",
  illustrator:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/illustrator/illustrator-plain.svg",
  photoshop:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/photoshop/photoshop-plain.svg",
  xd: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/xd/xd-plain.svg",
  jira: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jira/jira-original-wordmark.svg",
  confluence:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/confluence/confluence-original-wordmark.svg",
  slack:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/slack/slack-original-wordmark.svg",
  trello:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/trello/trello-plain-wordmark.svg",
};

const technologies = [
  "aws",
  "docker",
  "gcp",
  "kubernetes",
  "angular",
  "terraform",
  "prometheus",
  "azure",
  "react",
  "nodejs",
  "python",
  "java",
  "csharp",
  "javascript",
  "typescript",
  "ruby",
  "go",
  "rust",
  "swift",
  "django",
  "flask",
  "rails",
  "spring",
  "dotnet",
  "mysql",
  "postgresql",
  "mongodb",
  "redis",
  "kafka",
  "git",
  "github",
  "gitlab",
  "jenkins",
  "travis",
  "vue",
  "redux",
  "webpack",
  "babel",
  "sass",
  "less",
  "jquery",
  "bootstrap",
  "tailwind",
  "materialui",
  "cplusplus",
  "php",
  "laravel",
  "symfony",
  "codeigniter",
  "ionic",
  "android",
  "firebase",
  "graphql",
  "apollostack",
  "elasticsearch",
  "nginx",
  "apache",
  "linux",
  "bash",
  "vim",
  "vscode",
  "intellij",
  "figma",
  "illustrator",
  "photoshop",
  "xd",
  "jira",
  "confluence",
  "slack",
  "trello",
];

const TechnologyDropdown = ({ selectedTechnologies, setSelectedTechnologies }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const filteredTechnologies = technologies.filter((tech) =>
    tech.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSelect = (tech) => {
    if (selectedTechnologies.includes(tech)) {
      setSelectedTechnologies(selectedTechnologies.filter(t => t !== tech));
    } else {
      setSelectedTechnologies([...selectedTechnologies, tech]);
    }
  };

  return (
    <div className="relative">
    <button
      onClick={() => setDropdownOpen(!dropdownOpen)}
      className="rounded-lg px-16 py-2 border border-green-300 bg-green-50 text-green-700 hover:bg-lime-200"
    >
      Technologies ({selectedTechnologies.length})
    </button>
    {dropdownOpen && (
      <div className="absolute mt-1 w-60 bg-white border rounded-lg shadow-lg z-50">
        <div className="mt-1 pr-3 text-center">
          <button
            onClick={() => setSelectedTechnologies([])}
            className="text-purple-500 hover:underline"
          >
            Clear All
          </button>
        </div>
        <div className="p-2">
          <input
            type="text"
            placeholder="Search technology"
            className="w-full border rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-purple-500"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="max-h-96 overflow-y-auto" style={{fontFamily: "Avenir, san-serif"}}>
          {filteredTechnologies.map((tech, index) => (
            <div
              key={index}
              className={`flex items-center p-2 hover:bg-gray-100 cursor-pointer ${
                selectedTechnologies.includes(tech) ? "bg-purple-100" : ""
              }`}
              onClick={() => handleSelect(tech)}
            >
              <img
                src={icons[tech.toLowerCase()]}
                alt={tech}
                className="w-6 h-6 ml-4 mr-6"
              />
              <span>{tech}</span>
            </div>
          ))}
        </div>
      </div>
    )}
  </div>
);
};

export default TechnologyDropdown;


// // src/components/TechnologyDropdown.jsx
// import React, { useState } from "react";

// const icons = {
//   aws: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-original-wordmark.svg",
//   docker:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original-wordmark.svg",
//   gcp: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/googlecloud/googlecloud-original.svg",
//   kubernetes:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/kubernetes/kubernetes-original-wordmark.svg",
//   angular:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/angularjs/angularjs-original.svg",
//   terraform:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/terraform/terraform-original-wordmark.svg",
//   prometheus:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/prometheus/prometheus-original-wordmark.svg",
//   azure:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/azure/azure-original.svg",
//   react:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/react/react-original-wordmark.svg",
//   nodejs:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nodejs/nodejs-original-wordmark.svg",
//   python:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original-wordmark.svg",
//   java: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original-wordmark.svg",
//   csharp:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/csharp/csharp-original.svg",
//   javascript:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg",
//   typescript:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/typescript/typescript-original.svg",
//   ruby: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/ruby/ruby-original-wordmark.svg",
//   go: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/go/go-original-wordmark.svg",
//   rust: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/rust/rust-plain.svg",
//   swift:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/swift/swift-original-wordmark.svg",
//   django:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/django/django-plain-wordmark.svg",
//   flask:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/flask/flask-original-wordmark.svg",
//   rails:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/rails/rails-plain-wordmark.svg",
//   spring:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/spring/spring-original-wordmark.svg",
//   dotnet:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/dotnetcore/dotnetcore-original.svg",
//   mysql:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-original-wordmark.svg",
//   postgresql:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original-wordmark.svg",
//   mongodb:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mongodb/mongodb-original-wordmark.svg",
//   redis:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/redis/redis-original-wordmark.svg",
//   kafka:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apachekafka/apachekafka-original-wordmark.svg",
//   git: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/git/git-original-wordmark.svg",
//   github:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/github/github-original-wordmark.svg",
//   gitlab:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/gitlab/gitlab-original-wordmark.svg",
//   jenkins:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jenkins/jenkins-original.svg",
//   travis:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/travis/travis-plain-wordmark.svg",
//   vue: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vuejs/vuejs-original-wordmark.svg",
//   redux:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/redux/redux-original.svg",
//   webpack:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/webpack/webpack-original-wordmark.svg",
//   babel:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/babel/babel-original.svg",
//   sass: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/sass/sass-original.svg",
//   less: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/less/less-plain-wordmark.svg",
//   jquery:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jquery/jquery-original-wordmark.svg",
//   bootstrap:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/bootstrap/bootstrap-plain-wordmark.svg",
//   tailwind:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/tailwindcss/tailwindcss-plain.svg",
//   materialui:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/materialui/materialui-original.svg",
//   cplusplus:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-original.svg",
//   php: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/php/php-original.svg",
//   laravel:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/laravel/laravel-plain-wordmark.svg",
//   symfony:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/symfony/symfony-original-wordmark.svg",
//   codeigniter:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/codeigniter/codeigniter-plain-wordmark.svg",
//   ionic:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/ionic/ionic-original-wordmark.svg",
//   android:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/android/android-original-wordmark.svg",
//   firebase:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/firebase/firebase-plain-wordmark.svg",
//   graphql:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/graphql/graphql-plain-wordmark.svg",
//   apollostack:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apollostack/apollostack-original.svg",
//   elasticsearch:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/elasticsearch/elasticsearch-original-wordmark.svg",
//   nginx:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nginx/nginx-original.svg",
//   apache:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apache/apache-original-wordmark.svg",
//   linux:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/linux/linux-original.svg",
//   bash: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/bash/bash-original.svg",
//   vim: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vim/vim-original.svg",
//   vscode:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vscode/vscode-original-wordmark.svg",
//   intellij:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/intellij/intellij-original.svg",
//   figma:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/figma/figma-original.svg",
//   illustrator:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/illustrator/illustrator-plain.svg",
//   photoshop:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/photoshop/photoshop-plain.svg",
//   xd: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/xd/xd-plain.svg",
//   jira: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jira/jira-original-wordmark.svg",
//   confluence:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/confluence/confluence-original-wordmark.svg",
//   slack:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/slack/slack-original-wordmark.svg",
//   trello:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/trello/trello-plain-wordmark.svg",
// };

// const technologies = [
//   "aws",
//   "docker",
//   "gcp",
//   "kubernetes",
//   "angular",
//   "terraform",
//   "prometheus",
//   "azure",
//   "react",
//   "nodejs",
//   "python",
//   "java",
//   "csharp",
//   "javascript",
//   "typescript",
//   "ruby",
//   "go",
//   "rust",
//   "swift",
//   "django",
//   "flask",
//   "rails",
//   "spring",
//   "dotnet",
//   "mysql",
//   "postgresql",
//   "mongodb",
//   "redis",
//   "kafka",
//   "git",
//   "github",
//   "gitlab",
//   "jenkins",
//   "travis",
//   "vue",
//   "redux",
//   "webpack",
//   "babel",
//   "sass",
//   "less",
//   "jquery",
//   "bootstrap",
//   "tailwind",
//   "materialui",
//   "cplusplus",
//   "php",
//   "laravel",
//   "symfony",
//   "codeigniter",
//   "ionic",
//   "android",
//   "firebase",
//   "graphql",
//   "apollostack",
//   "elasticsearch",
//   "nginx",
//   "apache",
//   "linux",
//   "bash",
//   "vim",
//   "vscode",
//   "intellij",
//   "figma",
//   "illustrator",
//   "photoshop",
//   "xd",
//   "jira",
//   "confluence",
//   "slack",
//   "trello",
// ];

// const TechnologyDropdown = ({ selectedTechnologies, setSelectedTechnologies }) => {
//   const [searchTerm, setSearchTerm] = useState("");
//   const [dropdownOpen, setDropdownOpen] = useState(false);

//   const filteredTechnologies = technologies.filter((tech) =>
//     tech.toLowerCase().includes(searchTerm.toLowerCase())
//   );

//   const handleSelect = (tech) => {
//     if (selectedTechnologies.includes(tech)) {
//       setSelectedTechnologies(selectedTechnologies.filter(t => t !== tech));
//     } else {
//       setSelectedTechnologies([...selectedTechnologies, tech]);
//     }
//   };

//   return (
//     <div className="relative">
//       <button
//         onClick={() => setDropdownOpen(!dropdownOpen)}
//         className="rounded-lg px-16 py-2 border border-green-300 bg-green-50 text-green-700 hover:bg-lime-200"
//       >
//         Technologies ({selectedTechnologies.length})
//       </button>
//       {dropdownOpen && (
//         <div className="absolute mt-1 w-full bg-white border rounded-lg shadow-lg">
//           <div className="mt-1 pr-3 text-center">
//             <button
//               onClick={() => setSelectedTechnologies([])}
//               className="text-purple-500 hover:underline"
//             >
//               Clear All
//             </button>
//           </div>
//           <div className="pl-1 pr-1 pb-2">
//             <input
//               type="text"
//               placeholder="Search technology"
//               className="w-full border rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-purple-500"
//               value={searchTerm}
//               onChange={(e) => setSearchTerm(e.target.value)}
//             />
//           </div>
//           <div className="max-h-60 overflow-y-auto">
//             {filteredTechnologies.map((tech, index) => (
//               <div
//                 key={index}
//                 className={`flex items-center p-2 hover:bg-gray-100 cursor-pointer ${
//                   selectedTechnologies.includes(tech) ? "bg-purple-100" : ""
//                 }`}
//                 onClick={() => handleSelect(tech)}
//               >
//                 <img
//                   src={icons[tech.toLowerCase()]}
//                   alt={tech}
//                   className="w-6 h-6 ml-4 mr-6"
//                 />
//                 <span>{tech}</span>
//               </div>
//             ))}
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default TechnologyDropdown;