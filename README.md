# 🔬 Multi-Agent Research System

An AI-powered research assistant that automates information gathering, web research, and content summarization using multiple intelligent agents. The system helps users quickly collect, analyze, and summarize information from various online sources in a structured format.

## 🚀 Live Demo

🌐 Live App: https://research-system-bfje94vwx7rn9csrp2jsyx.streamlit.app/

---

## 📌 Features

- 🤖 Multi-Agent Architecture
- 🔍 Web Search Integration
- 🌐 Website Content Extraction
- 📄 Automated Research Summaries
- 🧠 LLM-Powered Analysis
- ⚡ Fast and Interactive Streamlit Interface
- 📚 Context-Aware Information Retrieval
- 🔄 End-to-End Research Workflow

---

## 🏗️ System Architecture

User Query
↓
Research Agent
↓
Search Tool (Tavily)
↓
Web Scraping Tool (BeautifulSoup)
↓
LLM Analysis
↓
Structured Research Report

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### AI & LLM
- LangChain
- Mistral AI

### Search & Retrieval
- Tavily Search API

### Web Scraping
- BeautifulSoup4
- Requests

### Programming Language
- Python

---

## 📂 Project Structure

```bash
research-system/
│
├── app.py
├── agents/
├── tools/
├── chains/
├── requirements.txt
├── README.md
└── assets/
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/research-system.git
cd research-system
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file and add:

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## ▶️ Run Locally

```bash
streamlit run app.py
```

---

## 💡 How It Works

1. User enters a research query.
2. Tavily searches the web for relevant information.
3. BeautifulSoup extracts content from selected websites.
4. The LLM analyzes and combines the gathered information.
5. A structured research report is generated and displayed.

---

## 🎯 Use Cases

- Academic Research
- Market Research
- Technology Trends Analysis
- Competitive Analysis
- Quick Topic Exploration
- Content Creation Support

---

## 📸 Demo

Live Application:

https://research-system-bfje94vwx7rn9csrp2jsyx.streamlit.app/

---

## 🔮 Future Improvements

- PDF Report Generation
- Multi-Source Citation Support
- RAG-Based Knowledge Storage
- Export to DOCX/PDF
- Advanced Agent Collaboration
- Research History Tracking

---

## 👨‍💻 Author

**Aayush Sharma**

- AI/ML Enthusiast
- Generative AI Developer
- Machine Learning Practitioner

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

## 📜 License

This project is licensed under the MIT License.
