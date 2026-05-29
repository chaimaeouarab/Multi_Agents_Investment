from agents.portfolio_agent import read_portfolio, analyze_portfolio
from agents.search_agent import search_market_news
from agents.writer_agent import generate_report

class Supervisor:
    def __init__(self, portfolio_path: str):
        self.portfolio_path = portfolio_path
        self.portfolio_data = None
        self.portfolio_summary = None
        self.market_insights = None
    
    def run(self, user_query: str) -> str:
        """Orchestrate all agents to answer user query"""
        
        print("📊 Step 1: Reading portfolio...")
        self.portfolio_data = read_portfolio(self.portfolio_path)
        self.portfolio_summary = analyze_portfolio(self.portfolio_data)
        
        print("🔍 Step 2: Searching market insights...")
        # Extract tickers for relevant search
        tickers = [h['ticker'] for h in self.portfolio_data['holdings']]
        search_query = f"Recent news and market trends for {', '.join(tickers)} {user_query}"
        self.market_insights = search_market_news(search_query)
        
        print("✍️ Step 3: Generating report...")
        report = generate_report(self.portfolio_summary, self.market_insights, user_query)
        
        print("✅ Analysis complete!")
        return report