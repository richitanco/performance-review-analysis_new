
# Performance Review Analysis System

## Overview

This system provides comprehensive performance review analysis with integrated AI-powered text improvement using the Google Gemini API.

### Key Features

- **Bias detection and analysis**
- **Specificity and actionability assessment**
- **Feedback type classification**
- **AI-powered professional text improvement (Google Gemini)**

---

## How the App Works

The Performance Review Analysis System uses advanced AI and NLP (Natural Language Processing) techniques to analyze and improve feedback. Here’s what happens behind the scenes for each main feature:

### 1. Bias Detection

- **Technique Used:** Zero-Shot Text Classification (Transformer Model)  
- **What it does:** Examines each sentence for possible bias (cultural, racial, or none).
- **How:** Uses a large language model that can detect subtle bias in any sentence, even if it’s never seen similar examples before.

### 2. Specificity & Actionability

- **Technique Used:** Rule-Based Pattern Recognition & Heuristic Scoring  
- **What it does:** Checks if feedback is specific (e.g., contains numbers, deadlines, clear results) or too vague to act on.
- **How:** Uses pattern matching to look for concrete details and penalizes vague phrases to promote actionable feedback.

### 3. Feedback Type Classification

- **Technique Used:** Zero-Shot Text Classification (Transformer Model)  
- **What it does:** Identifies whether feedback is positive, constructive criticism, actionable, or vague.
- **How:** AI classifies the nature of the feedback regardless of its writing style.

### 4. Professional Text Improvement (AI Rewriting)

- **Technique Used:** Prompt Engineering + Generative AI (Google Gemini)  
- **What it does:** Rewrites your review text to be clearer, more professional, and constructive.
- **How:** Sends original feedback to Google's Gemini model with a prompt to enhance clarity, grammar, and actionability while preserving intent.

---

## In Summary

Each part of the app uses a modern NLP technique tailored to the specific task:

- **Zero-shot classification** for bias and feedback-type detection  
- **Rule-based heuristics** for specificity analysis  
- **Prompted generative AI** for text improvement

This ensures your feedback is **fair**, **detailed**, and **impactful**.


# Performance Review Analysis - Setup Guide

## Prerequisites

- **Docker Desktop** (Mac or Windows)  
- *(Optional)* Git (for cloning the repository)

---

## Installation (macOS & Windows)

### 1. Install Docker Desktop

- Download and install from [docker.com](https://www.docker.com/products/docker-desktop)
- Start Docker Desktop and verify the installation by running:

```bash
docker --version
docker-compose --version
```

---

### 2. Obtain the Repository

#### Option A: Clone with Git

```bash
https://github.com/richitanco/performance-review-analysis_new.git
cd performance-review-analysis/app
```

#### Option B: Download as ZIP

- Go to the https://github.com/richitanco/performance-review-analysis_new
- Click the **Code** button, then **Download ZIP**
- Extract the ZIP file
- Open a terminal and navigate to the `app` folder

---

### 3. Run the Application

```bash
docker-compose up --build
```

---

### 4. Access the Web Interface

Open your browser and go to:  
[http://localhost:7860](http://localhost:7860)

---

## Testing the Application

1. Open [http://localhost:7860](http://localhost:7860) in your browser.

2. Enter sample review text, for example:

```text
john is okay worker but could be better at presentations
```

3. Click **"Analyze Review"**. You should see three tables:

- **Bias Analysis**
- **Specificity Analysis**
- **Feedback Type Analysis**

4. Click **"Generate AI Recommendation"** to receive a professional, improved version of the input text.

### Example Output

**ORIGINAL TEXT:**

```text
john is okay worker but could be better at presentations
```

**AI IMPROVED VERSION:**

```text
John is a competent employee who consistently fulfills his job responsibilities. However, there are opportunities for improvement in his presentation skills. I recommend providing him with presentation training and practice opportunities in low-stakes environments to build his confidence and effectiveness.
```

---

## Troubleshooting

### Common Issues

| Issue                         | Solution                                                                 |
|------------------------------|--------------------------------------------------------------------------|
| "This site can't be reached" | Ensure Docker Desktop is running. Restart with:<br>`docker-compose down && docker-compose up --build` |
| Port 7860 already in use     | Mac: `sudo lsof -t -i:7860`                                               |
| Docker build fails           | Clean Docker:<br>`docker system prune -f && docker-compose down --volumes && docker-compose up --build` |
| Other issues                 | Check logs:<br>`docker-compose logs`                                     |

### API Key Errors

This should not occur, as the deployment is pre-configured.  
If you experience an AI-related error, contact the repository maintainer.

---

## Success Criteria

- Docker containers start successfully  
- The web interface loads at [http://localhost:7860](http://localhost:7860)  
- Analysis tables are populated with data  
- AI recommendations are generated as expected

---

## Support

- Check logs:

```bash
docker-compose logs
```

- For unresolved issues, create a GitHub Issue in the repository.
