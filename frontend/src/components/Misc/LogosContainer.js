import React from "react";

const CompanyLogo = ({ src, alt }) => {
  return (
    <div className="w-64 h-32 rounded2xl flex justify-center items-center rounded-md ml-4 p-4">
      <img src={src} alt={alt} className="max-w-full max-h-full" />
    </div>
  );
};

const CompanyLogosContainer = () => {
  const logos = [
    // {
    //   src: "https://logowik.com/content/uploads/images/linktree-new-20226266.logowik.com.webp",
    //   alt: "Linktree Logo",
    // },
    {
      src: "https://buildkite.com/_next/static/assets/assets/images/brand-assets/buildkite-logo-portrait-on-light-f7f1af58.png",
      alt: "Buildkite Logo",
    },
    {
      src: "https://www.freshcare.com.au/wp-content/uploads/2023/03/SafetyCulture-Logo-Full-colour.png",
      alt: "Safety Culture Logo",
    },
    {
      src: "https://images.g2crowd.com/uploads/product/image/large_detail/large_detail_729bc0d8b36107f81b46d45695003a37/go1-content-hub.png",
      alt: "Go1 Logo",
    },
    //https://www.janison.com/wp-content/uploads/2021/04/go1-logo-1024x1024-.jpg - circular GO1 logo
    // GO1 neon https://mms.businesswire.com/media/20200722005588/en/807300/23/GO1_Logo_Petrol_Green_RGB.jpg
    {
      src: "https://logos-world.net/wp-content/uploads/2023/03/Atlassian-Logo.png",
      alt: "Atlassian Logo",
    },
    {
      src: "https://dka575ofm4ao0.cloudfront.net/pages-transactional_logos/retina/259922/immutable-logo-horiz-noreg-BLK-RGB.png",
      alt: "Immutable Logo",
    },
    {
      src: "https://builtin.com/sites/www.builtin.com/files/2021-11/CIRCLE%20LOGO%20-%20GRADIENT%20-%20RGB_0.png",
      alt: "Canva Logo",
      //https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEk3H5TIZHDP9cuDtiqF5upuGW61cqSsCoZw&s
    },

    {
      src: "https://lever-client-logos.s3.us-west-2.amazonaws.com/d20056fd-6295-4ec6-b809-a6477a1d79f0-1615158495863.png",
      alt: "Deputy Logo",
    },
    {
      src: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Xero-logo-hires-RGB.png/600px-Xero-logo-hires-RGB.png",
      alt: "Octopus Deploy Logo",
    },
    // https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9QIkaSxXIOnwzTArejNxEIsaWqn7cngamUA&s
  ];

  return (
    <div>
      <div className="flex flex-wrap space-between items-center mb-12 rounded-md w-7/10 space-x-8">
        {logos.map((logo, index) => (
          <CompanyLogo key={index} src={logo.src} alt={logo.alt} />
        ))}
      </div>
      <div className="pb-32 mb-12">
        <center>
          <p
            className="font-bold text-4xl rounded-3xl p-4 mw-1/3"
            style={{ fontFamily: "HK Nova" }}
          >
            Jobs from Oceania's Brightest Companies!
          </p>
        </center>
      </div>
    </div>
  );
};

export default CompanyLogosContainer;
