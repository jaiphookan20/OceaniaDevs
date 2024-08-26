import React, { useState } from 'react';
import { Camera, Briefcase, Code, Award, Upload } from 'lucide-react';
import amazonLogo from "../assets/amazon-logo.png"
import dovetailLogo from "../assets/dovetail-logo.png"
import profileLogo from "../assets/face-3.png"
import oceSS from "../assets/oce-pic.png"
import airbnbPic from "../assets/airbnbproject.png"
import dashboardPic from "../assets/dashboard-pic.png"
import jobpostPic from "../assets/jobpost-pic.png"
import verifiedIcon from "../assets/verified-icon.png"
import reactLogo from "../assets/tech-logos/react.svg"
import nodeLogo from "../assets/tech-logos/nodejs.svg"
// import expressLogo from "../assets/tech-logos/expressjs.svg"
import mongodbLogo from "../assets/tech-logos/mongodb.svg"
import postgresLogo from "../assets/tech-logos/postgres.svg"
import redisLogo from "../assets/tech-logos/redis.svg"
import awsLogo from "../assets/tech-logos/aws.svg"
import dockerLogo from "../assets/tech-logos/docker.svg"
import kubernetesLogo from "../assets/tech-logos/kubernetes.svg"
import jenkinsLogo from "../assets/tech-logos/jenkins.svg"
// import circleCILogo from "../assets/tech-logos/circleci.svg"
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';


const DeveloperProfile = () => {
  const [profilePic, setProfilePic] = useState(profileLogo);
  const [activeStack, setActiveStack] = useState('Frontend');

  

  const handleImageUpload = (setter) => (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setter(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };


  const developer = {
    name: "Jane Cowan",
    title: "Senior Full Stack Developer",
    location: "Sydney, NSW",
    email: "jane.doe@example.com",
    about: "Passionate full stack developer with 8+ years of experience in building scalable web applications. Specialized in React, Node.js, and cloud technologies.",
    projects: [
      { name: "E-commerce Platform", description: "Built a full-featured e-commerce platform using React, Node.js, and MongoDB.", image: oceSS }, 
      { name: "Task Management App", description: "Developed a real-time task management application using Vue.js and Firebase.", image: airbnbPic },
      { name: "Social Media Analytics", description: "Created a dashboard for social media analytics using Python and D3.js.", image: jobpostPic },
      { name: "IoT Home Automation", description: "Designed an IoT system for home automation using Raspberry Pi and React Native.", image: dashboardPic },
    ],
    experience: [
      { 
        company: "Tech Innovators Inc.", 
        role: "Senior Developer", 
        period: "2019 - Present", 
        logo: amazonLogo,
        description: "Lead developer for enterprise-level web applications. Implemented microservices architecture and improved system performance by 40%."
      },
      { 
        company: "Web Solutions LLC", 
        role: "Full Stack Developer", 
        period: "2015 - 2019", 
        logo: dovetailLogo,
        description: "Developed and maintained multiple client websites. Introduced automated testing, reducing bug reports by 60%."
      },
    ],
    education: [
      {
        institution: "University of Melbourne",
        degree: "Master of Information Technology (Distributed Computing)",
        period: "2022 - 2024",
        logo: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQGzmdOafRC9iy_Jk_msnyToMTo3ODw0alKw&s'
      },
    ],
    skills: [
      { name: "JavaScript", level: 90 },
      { name: "React", level: 85 },
      { name: "Node.js", level: 80 },
      { name: "Python", level: 75 },
      { name: "SQL", level: 70 },
    ],
    preferredStack: {
      Frontend: [
        { name: "React", logo: reactLogo, usage: 60 },
        { name: "Vue.js", logo: "https://vuejs.org/images/logo.png", usage: 30 },
        { name: "Angular", logo: "https://angular.io/assets/images/logos/angular/angular.svg", usage: 10 },
      ],
      Backend: [
        { name: "Node.js", logo: nodeLogo, usage: 50 },
        { name: "Express", logo: redisLogo, usage: 30 },
        { name: "Django", logo: "https://www.djangoproject.com/m/img/logos/django-logo-negative.png", usage: 20 },
      ],
      Database: [
        { name: "MongoDB", logo: mongodbLogo, usage: 40 },
        { name: "PostgreSQL", logo: postgresLogo, usage: 40 },
        { name: "Redis", logo: redisLogo, usage: 20 },
      ],
      "DevOps/Cloud": [
        { name: "AWS", logo: awsLogo, usage: 50 },
        { name: "Docker", logo: dockerLogo, usage: 30 },
        { name: "Kubernetes", logo: kubernetesLogo, usage: 20 },
      ],
      "CI/CD": [
        { name: "Jenkins", logo: jenkinsLogo, usage: 40 },
        { name: "GitHub Actions", logo: dockerLogo, usage: 40 },
        { name: "CircleCI", logo: reactLogo, usage: 20 },
      ],
      Testing: [
        { name: "Jest", logo: redisLogo, usage: 50 },
        { name: "Cypress", logo: postgresLogo, usage: 30 },
        { name: "Selenium", logo: awsLogo, usage: 20 },
      ],
      "Other Tools": [
        { name: "Kafka", logo: jenkinsLogo, usage: 40 },
        { name: "Elasticsearch", logo: dockerLogo, usage: 35 },
        { name: "Grafana", logo: mongodbLogo, usage: 25 },
      ],
    },
    certifications: [
      "AWS Certified Developer - Associate",
      "MongoDB Certified Developer",
      "Google Cloud Certified - Professional Cloud Developer",
    ],
  };

  
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28'];

  const TechStackItem = ({ tech, rank }) => (
    <div className="flex items-center bg-white p-4 rounded-lg shadow-sm">
      <span className="text-2xl font-bold text-gray-400 mr-4">#{rank}</span>
      <img src={tech.logo} alt={tech.name} className="w-10 h-10 object-contain mr-4" />
      <span className="text-lg font-semibold text-gray-700 mr-4">{tech.name}</span>
      <span className="text-md text-gray-500">{tech.usage}% usage</span>
    </div>
  );

  const TechStackChart = ({ data }) => (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          outerRadius={80}
          fill="#8884d8"
          dataKey="usage"
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );

  return (
    <div className="bg-slate-50 min-h-screen p-8" style={{fontFamily: "Avenir, san-serif"}}>
      <div className="max-w-6xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden">
        <div className="p-8 flex items-center">
          <div className="flex-shrink-0 mr-8">
            <div className="relative h-48 w-48">
              <img className="h-full w-full object-cover rounded-full border-4 border-gray-200 shadow-lg" src={profilePic} alt={developer.name} />
              <label htmlFor="upload-button" className="absolute bottom-2 right-2 bg-white rounded-full p-2 cursor-pointer shadow-md hover:shadow-lg transition-shadow duration-300">
                <Camera className="h-6 w-6 text-gray-600" />
              </label>
              <input
                type="file"
                id="upload-button"
                className="hidden"
                onChange={handleImageUpload(setProfilePic)}
                accept="image/*"
              />
            </div>
          </div>
          <div className="flex-grow">
            <div className='flex'>
                <h1 className="text-4xl font-bold mb-2 text-gray-800">{developer.name} </h1>
                <img
                    src={verifiedIcon}
                    alt="verified"
                    className="ml-4 w-16 h-16"
                />
            </div>
            <p className="text-xl font-semibold mb-2 text-gray-600">{developer.title}</p>
            <p className="mb-2 text-gray-500">{developer.location} | {developer.email}</p>
            <p className="text-gray-700">{developer.about}</p>
          </div>
        </div>
          <div className="px-8 py-6 bg-gradient-to-r from-purple-50 to-pink-50">
          <h2 className="text-3xl font-bold text-gray-800 flex items-center mb-2">
            <Code className="mr-2" /> Professional Tech Stack
          </h2>
          <p className='text-gray-500 mb-4'>The technologies I use on a daily-basis professionally, in my current role </p>
          <div className="mb-6 flex flex-wrap gap-2">
            {Object.keys(developer.preferredStack).map((stack) => (
              <button
                key={stack}
                onClick={() => setActiveStack(stack)}
                className={`px-4 py-2 rounded-full text-sm font-semibold transition-colors duration-200 ${
                  activeStack === stack
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {stack}
              </button>
            ))}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              {developer.preferredStack[activeStack].map((tech, index) => (
                <TechStackItem key={tech.name} tech={tech} rank={index + 1} />
              ))}
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <TechStackChart data={developer.preferredStack[activeStack]} />
            </div>
          </div>
        </div>
        {/* <div className="px-8 py-6 bg-gradient-to-r from-amber-50 to-pink-50"> */}
        <div className="px-8 py-6 bg-fuchsia-50/60">
          <h2 className="text-3xl font-semibold text-slate-600 flex items-center mb-6">
             Projects
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {developer.projects.map((project, index) => (
              <div key={index} className="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition-shadow duration-300 border border-slate-400 border-2">
                <div className="relative h-48">
                  <img className="h-full w-full object-cover" src={project.image} alt={project.name} />
                  <label htmlFor={`upload-project-${index}`} className="absolute bottom-2 right-2 bg-white rounded-full p-2 cursor-pointer shadow-md">
                    <Upload className="h-5 w-5 text-gray-600" />
                  </label>
                  <input
                    type="file"
                    id={`upload-project-${index}`}
                    className="hidden"
                    onChange={handleImageUpload((newImage) => {
                      developer.projects[index].image = newImage;
                      // In a real app, you'd update state here
                    })}
                    accept="image/*"
                  />
                </div>
                <div className="p-4">
                  <h3 className="font-semibold text-xl mb-2 text-gray-800">{project.name}</h3>
                  <p className="text-gray-600">{project.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="px-8 py-6 bg-teal-50/60">
          <h2 className="text-3xl font-bold text-gray-800 flex items-center mb-6">
             Professional Experience
          </h2>
          <div className="space-y-6">
            {developer.experience.map((exp, index) => (
              <div key={index} className="bg-gray-50/60 p-6 rounded-xl shadow-md">
                <div className="flex items-center mb-4">
                  <img className="h-16 w-16 object-contain rounded-full mr-4" src={exp.logo} alt={exp.company} />
                  <div>
                    <h3 className="font-semibold text-xl text-gray-800">{exp.role}</h3>
                    <p className="text-gray-600">{exp.company}</p>
                    <p className="text-gray-500">{exp.period}</p>
                  </div>
                </div>
                <p className="text-gray-700">{exp.description}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="px-8 py-6 bg-gray-50">
          <h2 className="text-3xl font-bold text-gray-800 flex items-center mb-6">
            <Code className="mr-2" /> Skills
          </h2>
          <div className="space-y-4">
            {developer.skills.map((skill, index) => (
              <div key={index} className="flex items-center">
                <span className="w-24 font-semibold text-gray-700">{skill.name}</span>
                <div className="flex-1 bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-blue-600 h-3 rounded-full"
                    style={{ width: `${skill.level}%` }}
                  ></div>
                </div>
                <span className="ml-4 text-gray-600 font-medium">{skill.level}%</span>
              </div>
            ))}
          </div>
        </div>

          {/* Education Section */}
          <div className="p-8 border-b border-gray-200">
            <h2 className="text-3xl font-bold text-gray-800 flex items-center mb-6">
               Education
            </h2>
            <div className="space-y-6">
              {developer.education.map((edu, index) => (
                <div key={index} className="flex items-center bg-gray-50 p-6 rounded-xl shadow-md">
                  <img className="h-20 w-20 object-contain rounded-lg mr-6" src={edu.logo} alt={edu.institution} />
                  <div>
                    <h3 className="font-semibold text-xl text-gray-800">{edu.institution}</h3>
                    <p className="text-gray-600 text-lg">{edu.degree}</p>
                    <p className="text-gray-500">{edu.period}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        <div className="px-8 py-6 bg-gray-50">
          <h2 className="text-3xl font-bold text-gray-800 flex items-center mb-6">
            <Award className="mr-2" /> Certifications
          </h2>
          <ul className="space-y-3">
            {developer.certifications.map((cert, index) => (
              <li key={index} className="flex items-center bg-white p-3 rounded-lg shadow-sm">
                <Award className="mr-3 text-blue-500" />
                <span className="text-gray-700">{cert}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default DeveloperProfile;