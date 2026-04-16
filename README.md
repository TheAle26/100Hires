\# 100Hires - AI-Powered SEO Research Project

This repository contains the initial research phase for developing a high-performance SEO playbook focused on AI automation and programmatic content production.

## 🛠 Tools & Environment
- **IDE:** Cursor
- **AI Extensions:** Claude Code, Codex (setup and troubleshooting)
- **Tech Stack for Research:** Python 3.13, Requests, Supadata API, Dotenv.

## ✅ Steps Completed

### 1. Environment Setup
- Installed and configured Cursor IDE with relevant extensions.
- Configured GitHub repository and established a CI/CD-ready workflow with regular commits.

### 2. Expert Selection & Research (Step 2)
- Identified **10 high-signal experts** in the AI-SEO niche (including Lidia Infante, Jake Ward, and Juan Gómez Manzanero).
- Focused on profiles with a technical approach to automation, n8n workflows, and pSEO (Programmatic SEO).

### 3. Automated Data Collection (YouTube)
- Developed a **Python automation script** (`collect_youtube.py`) to interface with the **Supadata API**.
- Integrated metadata extraction to dynamically organize transcripts into a directory structure based on the content creator's name.

### 4. Curated Content (LinkedIn)
- Performed a **manual collection** of high-signal posts from selected experts.
- Documented each post with technical justifications and relevance to the project's goal of building scalable SEO pipelines.

## 🚀 Challenges & Solutions

### Tooling Constraints
- **Claude Code/API Key:** Encountered credit requirements for the Claude Code terminal extension. 
- **Solution:** Switched to a hybrid approach using Cursor’s native AI capabilities and independent Python scripts to maintain momentum without being blocked by third-party subscription tiers.

### API Integration Hurdles
- **Challenge:** The initial transcript API endpoint lacked metadata (titles/authors), resulting in "Unknown" file naming.
- **Solution:** Refactored the collection script to implement a two-step process: first querying the `/v1/youtube/video` endpoint for metadata and then retrieving the transcript. 
- **Result:** Successfully automated a clean, organized directory structure for the research database.

### LinkedIn Scraping Strategy
- **Challenge:** LinkedIn's aggressive anti-scraping measures.
- **Judgment:** Decided on **Manual Curation** over automated scraping to ensure 100% data quality and "high-signal" relevance. This avoids the noise of mass-scraping and provides a more strategic research base.

## 📂 Project Structure
- `/research/youtube-transcripts/`: Automated transcripts organized by author.
- `/research/linkedin-posts/`: Curated expert insights with technical annotations.
- `collect_youtube.py`: Custom Python script for data gathering.