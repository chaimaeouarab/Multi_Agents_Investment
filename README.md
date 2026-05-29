# VestigeAI - Portfolio Intelligence

A multi-agent AI application for intelligent portfolio analysis and investment insights using LangChain and OpenAI.

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Recommended)
The best and simplest way to deploy this Streamlit app:

1. Push your code to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "New app" and select your repository
4. Set the main file to `app.py`
5. Deploy!

### Option 2: Vercel
This project includes configuration for Vercel deployment:

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repository
4. Vercel will auto-detect the FastAPI app in `api/index.py`
5. Add environment variables (if needed)
6. Deploy!

**Note:** Vercel serves a landing page for the API. The full Streamlit experience is best on Streamlit Cloud.

### Option 3: Local Deployment
Run the app locally with Streamlit:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📋 Requirements

- Python 3.8+
- OpenAI API key (set in `.env` file)
- Tavily API key (for search capabilities)

## 🔧 Setup

1. Clone the repository:
```bash
git clone https://github.com/chaimaeouarab/Multi_Agents_Investment.git
cd portfolio_agent_project
```

2. Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run locally:
```bash
streamlit run app.py
```

## 📁 Project Structure

- `app.py` - Main Streamlit application
- `agents/` - Multi-agent components
  - `portfolio_agent.py` - Portfolio analysis agent
  - `search_agent.py` - Web search agent
  - `writer_agent.py` - Report writing agent
  - `supervisor.py` - Agent supervisor/orchestrator
- `utils/` - Utility functions
  - `pdf_generator.py` - PDF report generation
- `api/` - FastAPI wrapper for Vercel compatibility
- `portfolio_sample.json` - Sample portfolio data

## 🤖 Features

- Multi-agent AI system for portfolio analysis
- Real-time market data integration
- PDF report generation
- Interactive web interface

## 📝 License

MIT

## 👤 Author

Chaimae Ouarab

---

**Deployment Status:** Ready for production on Streamlit Cloud or Vercel
