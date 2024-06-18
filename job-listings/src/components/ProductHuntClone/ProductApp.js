// src/App.js

import React from "react";
import PHNavbar from "./PHNavbar";
import MainContent from "./MainContent";

const ProductApp = () => {
  const products = [
    {
      id: 1,
      name: "MARSS TTS",
      description: "Open-source, insanely prosodic text-to-speech model",
      details: "101 · Software Engineering · Artificial Intelligence · GitHub",
      votes: 239,
    },
    {
      id: 2,
      name: "Magic Publish",
      description: "Instantly researched titles for your YouTube videos",
      details: "75 · Social Media · Artificial Intelligence · YouTube",
      votes: 213,
    },
    {
      id: 3,
      name: "AI Top Rank",
      description: "A launchpad for AI tools to get their first backlink",
      details: "74 · Solo maker · Bootstrapped · Marketing",
      votes: 158,
    },
    {
      id: 1,
      name: "MARSS TTS",
      description: "Open-source, insanely prosodic text-to-speech model",
      details: "101 · Software Engineering · Artificial Intelligence · GitHub",
      votes: 239,
    },
    {
      id: 2,
      name: "Magic Publish",
      description: "Instantly researched titles for your YouTube videos",
      details: "75 · Social Media · Artificial Intelligence · YouTube",
      votes: 213,
    },
    {
      id: 3,
      name: "AI Top Rank",
      description: "A launchpad for AI tools to get their first backlink",
      details: "74 · Solo maker · Bootstrapped · Marketing",
      votes: 158,
    },
    // Add more products here...
  ];

  const shoutouts = [
    {
      id: 1,
      title: "CandiView",
      description: "AI CV screener to efficiently find top talent",
      details: "Shouted out MindPal",
    },
    {
      id: 2,
      title: "Humanize AI Text",
      description: "Transform AI writing to be more human like",
      details: "Shouted out SaaS AI",
    },
    {
      id: 3,
      title: "AI Top Rank",
      description: "A launchpad for AI tools to get their first...",
      details: "Shouted out Supabase",
    },
    {
      id: 1,
      title: "CandiView",
      description: "AI CV screener to efficiently find top talent",
      details: "Shouted out MindPal",
    },
    {
      id: 2,
      title: "Humanize AI Text",
      description: "Transform AI writing to be more human like",
      details: "Shouted out SaaS AI",
    },
    {
      id: 3,
      title: "AI Top Rank",
      description: "A launchpad for AI tools to get their first...",
      details: "Shouted out Supabase",
    },
    // Add more shoutouts here...
  ];

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <PHNavbar />
      <MainContent products={products} shoutouts={shoutouts} />
    </div>
  );
};
export default ProductApp;
