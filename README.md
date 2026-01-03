# 🎓 AI Scholarship Finder

An intelligent scholarship discovery platform that finds and matches international scholarship opportunities tailored to your profile.

## ✨ Features

- **Smart Scholarship Search** - Browse 40+ scholarships from multiple international databases
- **AI-Powered Matching** - Intelligent ranking based on your profile (country, degree, field, GPA)
- **Real-Time Data** - Pulls fresh scholarship listings from live sources (RSS feeds, web scrapers)
- **Multiple Sources** - Combines data from DAAD, Fulbright, Chevening, Erasmus, and more
- **Parallel Processing** - Fast search using concurrent scraping
- **Excel Export** - Download scholarship results in spreadsheet format
- **User-Friendly Interface** - Simple Streamlit web interface

## 🎯 What It Does

1. **Collects Data** - Scrapes and aggregates scholarships from 10+ international databases
2. **Processes Data** - Cleans, deduplicates, and standardizes scholarship records
3. **Matches Profiles** - Uses a rule-based algorithm to rank scholarships by relevance to your profile
4. **Displays Results** - Shows ranked scholarships with match percentage and details

## 🔧 How the Matching Works

Scholarships are scored (0-100%) based on:
- **Country Match** (30%) - Your preferred study destination
- **Degree Level** (25%) - Bachelor's, Master's, PhD, etc.
- **Field of Study** (20%) - Engineering, CS, Business, Medicine, etc.
- **CGPA/GPA** (15%) - Your academic performance
- **Funding Coverage** (10%) - Full, partial, or merit-based scholarships

## 🚀 Live Demo

Visit: **[AI Scholarship Finder on Streamlit Cloud](https://scholarhip-agent.streamlit.app/)**

## 💻 Tech Stack

- **Frontend**: Streamlit
- **Web Scraping**: BeautifulSoup, requests, feedparser
- **Data Processing**: Pandas
- **Matching Algorithm**: Rule-based scoring system
- **Deployment**: Streamlit Cloud

## 📋 Scholarship Sources

- DAAD (Germany)
- Fulbright (USA)
- Chevening (UK)
- Erasmus+ (Europe)
- Commonwealth (UK/Commonwealth)
- HEC Pakistan
- Scholars4Dev
- Opportunities Corners
- Youth Opportunities
- ScholarshipPortal

