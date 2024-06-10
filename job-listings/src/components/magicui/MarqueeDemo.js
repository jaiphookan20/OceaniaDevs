import React from "react";
import Marquee from "./marquee.js";
import { cn } from "/Users/jai/Desktop/aus-job-board/job-listings/src/lib/utils.ts";

const icons = {
  aws: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-original-wordmark.svg",
  docker:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original.svg",
  gcp: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/googlecloud/googlecloud-original.svg",
  kubernetes:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/kubernetes/kubernetes-original-wordmark.svg",
  angular:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/angularjs/angularjs-original.svg",
  grafana:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/grafana/grafana-original.svg",
  terraform:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/terraform/terraform-original.svg",
  prometheus:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/prometheus/prometheus-original.svg",
  azure:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/azure/azure-original.svg",
  java: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original.svg",
  linux:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/linux/linux-original.svg",
  nextjs:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nextjs/nextjs-original-wordmark.svg",
  nestjs:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nestjs/nestjs-original-wordmark.svg",
  nginx:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nginx/nginx-original.svg",
  postgresql:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg",
  kafka:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apachekafka/apachekafka-original-wordmark.svg",
  spring:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/spring/spring-original.svg",
  nodejs:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nodejs/nodejs-original-wordmark.svg",
  typescript:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/typescript/typescript-original.svg",
  javascript:
    "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg",
};

const logos = Object.values(icons);

// Function to get a random logo URL
const getRandomLogo = () => logos[Math.floor(Math.random() * logos.length)];

// Generate a number of reviews dynamically
const generateReviews = (num) => {
  const reviews = [];
  for (let i = 0; i < num; i++) {
    reviews.push({
      img: getRandomLogo(),
    });
  }
  return reviews;
};

// Define the number of reviews you want to generate
const reviews = generateReviews(20); // Generate 20 reviews

const firstRow = reviews.slice(0, reviews.length / 2);
const secondRow = reviews.slice(reviews.length / 2);

const ReviewCard = ({ img, name, username, body }) => {
  return (
    <figure
      className={cn(
        "relative w-40 cursor-pointer overflow-hidden rounded-xl p-4",
        // light styles
        "hover:bg-gray-950/[.05]",
        // dark styles
        "dark:hover:bg-gray-50/[.15] "
      )}
    >
      <div className="flex flex-row items-center gap-2">
        <img className="rounded-full" width="64" height="72" alt="" src={img} />
        <div className="flex flex-col">
          <figcaption className="text-sm font-medium dark:text-white">
            {name}
          </figcaption>
          <p className="text-xs font-medium dark:text-white/40">{username}</p>
        </div>
      </div>
      <blockquote className="mt-2 text-sm">{body}</blockquote>
    </figure>
  );
};

const MarqueeDemo = () => {
  return (
    <div className="relative flex h-full max-w-8xl flex-col items-center justify-center overflow-hidden rounded-lg bg-background  mb-12">
      <Marquee pauseOnHover className="[--duration:20s]">
        {firstRow.map((review, index) => (
          <ReviewCard key={index} {...review} />
        ))}
      </Marquee>
      <Marquee reverse pauseOnHover className="[--duration:20s]">
        {secondRow.map((review, index) => (
          <ReviewCard key={index} {...review} />
        ))}
      </Marquee>
      <div className="pointer-events-none absolute inset-y-0 left-0 w-1/3 bg-gradient-to-r from-white dark:from-background"></div>
      <div className="pointer-events-none absolute inset-y-0 right-0 w-1/3 bg-gradient-to-l from-white dark:from-background"></div>
    </div>
  );
};

export default MarqueeDemo;

// import React from "react";
// import Marquee from "./marquee.js";
// import { cn } from "/Users/jai/Desktop/aus-job-board/job-listings/src/lib/utils.ts";

// const icons = {
//   aws: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-original-wordmark.svg",
//   docker:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original.svg",
//   gcp: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/googlecloud/googlecloud-original.svg",
//   kubernetes:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/kubernetes/kubernetes-original-wordmark.svg",
//   angular:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/angularjs/angularjs-original.svg",
//   grafana:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/grafana/grafana-original.svg",
//   terraform:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/terraform/terraform-original.svg",
//   prometheus:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/prometheus/prometheus-original.svg",
//   azure:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/azure/azure-original.svg",
//   java: "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original.svg",
//   linux:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/linux/linux-original.svg",
//   nextjs:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nextjs/nextjs-original-wordmark.svg",
//   nestjs:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nestjs/nestjs-original-wordmark.svg",
//   nginx:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nginx/nginx-original.svg",
//   postgresql:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg",
//   kafka:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apachekafka/apachekafka-original-wordmark.svg",
//   spring:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/spring/spring-original.svg",
//   nodejs:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nodejs/nodejs-original-wordmark.svg",
//   typescript:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/typescript/typescript-original.svg",
//   javascript:
//     "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg",
// };

// const logos = Object.values(icons);

// // Function to get a random logo URL
// const getRandomLogo = () => logos[Math.floor(Math.random() * logos.length)];

// const reviews = [
//   {
//     // body: "I've never seen anything like this before. It's amazing. I love it.",
//     img: icons.aws,
//   },
//   {
//     // body: "I don't know what to say. I'm speechless. This is amazing.",
//     img: icons.docker,
//   },
//   {
//     // body: "I'm at a loss for words. This is amazing. I love it.",
//     img: icons.linux,
//   },
//   {
//     // body: "I'm at a loss for words. This is amazing. I love it.",
//     img: icons.gcp,
//   },
//   {
//     // body: "I'm at a loss for words. This is amazing. I love it.",
//     img: icons.nginx,
//   },
//   {
//     // body: "I'm at a loss for words. This is amazing. I love it.",
//     img: icons.typescript,
//   },
// ];

// const firstRow = reviews.slice(0, reviews.length / 2);
// const secondRow = reviews.slice(reviews.length / 2);

// const ReviewCard = ({ img, name, username, body }) => {
//   return (
//     <figure
//       className={cn(
//         "relative w-40 cursor-pointer overflow-hidden rounded-xl p-4",
//         // light styles
//         "hover:bg-gray-950/[.05]",
//         // dark styles
//         "dark:hover:bg-gray-50/[.15] "
//       )}
//     >
//       <div className="flex flex-row items-center gap-2">
//         <img className="rounded-full" width="64" height="72" alt="" src={img} />
//         <div className="flex flex-col">
//           <figcaption className="text-sm font-medium dark:text-white">
//             {name}
//           </figcaption>
//           <p className="text-xs font-medium dark:text-white/40">{username}</p>
//         </div>
//       </div>
//       <blockquote className="mt-2 text-sm">{body}</blockquote>
//     </figure>
//   );
// };

// const MarqueeDemo = () => {
//   return (
//     <div className="relative flex h-full w-full flex-col items-center justify-center overflow-hidden rounded-lg bg-background  mb-12">
//       <Marquee pauseOnHover className="[--duration:20s]">
//         {firstRow.map((review) => (
//           <ReviewCard key={review.username} {...review} />
//         ))}
//       </Marquee>
//       <Marquee reverse pauseOnHover className="[--duration:20s]">
//         {secondRow.map((review) => (
//           <ReviewCard key={review.username} {...review} />
//         ))}
//       </Marquee>
//       <div className="pointer-events-none absolute inset-y-0 left-0 w-1/3 bg-gradient-to-r from-white dark:from-background"></div>
//       <div className="pointer-events-none absolute inset-y-0 right-0 w-1/3 bg-gradient-to-l from-white dark:from-background"></div>
//     </div>
//   );
// };

// export default MarqueeDemo;
