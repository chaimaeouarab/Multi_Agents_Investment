"""
API wrapper for Streamlit app on Vercel
This creates a FastAPI server that can serve the Streamlit app
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import subprocess
import os
import sys

app = FastAPI()

# This is the top-level 'app' variable that Vercel is looking for
application = app

@app.get("/")
async def root():
    """Root endpoint - serves the Streamlit app"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Portfolio Intelligence - VestigeAI</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #0c1b2a 0%, #091522 48%, #0d2333 100%);
                color: #f8fbff;
            }
            .container {
                text-align: center;
                padding: 2rem;
                max-width: 600px;
            }
            h1 {
                font-size: 2.5rem;
                margin-bottom: 1rem;
                color: #7dd3fc;
            }
            p {
                font-size: 1.1rem;
                color: #bfd1e4;
                margin-bottom: 2rem;
                line-height: 1.6;
            }
            .info {
                background: rgba(13, 28, 44, 0.82);
                border-radius: 12px;
                padding: 1.5rem;
                border: 1px solid rgba(148, 163, 184, 0.16);
                margin-bottom: 2rem;
            }
            .button {
                display: inline-block;
                padding: 0.75rem 1.5rem;
                background: #38bdf8;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                transition: background 0.3s;
            }
            .button:hover {
                background: #0ea5e9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚡ VestigeAI</h1>
            <h2>Portfolio Intelligence</h2>
            <div class="info">
                <p>Welcome to the Portfolio Intelligence platform powered by Multi-Agent AI.</p>
                <p>This application is currently being deployed. For the best experience, we recommend using <strong>Streamlit Cloud</strong>.</p>
            </div>
            <p>To deploy this app locally, run:</p>
            <code style="background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 8px; display: block; margin-bottom: 1.5rem;">
                streamlit run app.py
            </code>
            <a href="https://streamlit.io/cloud" class="button">Deploy with Streamlit Cloud</a>
        </div>
    </body>
    </html>
    """)

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return JSONResponse({"status": "healthy", "service": "VestigeAI Portfolio Intelligence"})

@app.get("/api/info")
async def info():
    """API info endpoint"""
    return JSONResponse({
        "app": "VestigeAI",
        "version": "1.0.0",
        "description": "Portfolio Intelligence powered by Multi-Agent AI",
        "deployment": "Vercel",
        "note": "For Streamlit apps, deployment on Streamlit Cloud is recommended"
    })

# If running locally with 'uvicorn api.index:app'
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
