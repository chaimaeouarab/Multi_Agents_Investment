import json
from typing import Dict, Any

def read_portfolio(file_path: str) -> Dict[str, Any]:
    """Read and parse portfolio JSON file"""
    with open(file_path, 'r') as f:
        portfolio = json.load(f)
    return portfolio

def analyze_portfolio(portfolio: Dict[str, Any]) -> str:
    """Create a summary of the portfolio"""
    holdings = portfolio['holdings']
    total_invested = sum(h['shares'] * h['purchase_price'] for h in holdings)
    total_current = sum(h['shares'] * h['current_price'] for h in holdings)
    total_return = total_current - total_invested
    total_return_pct = (total_return / total_invested) * 100
    
    summary = f"""
PORTFOLIO SUMMARY
=================
User: {portfolio['user']}
Total Value: ${total_current:,.2f}
Total Invested: ${total_invested:,.2f}
Total Return: ${total_return:,.2f} ({total_return_pct:.2f}%)
Risk Tolerance: {portfolio['risk_tolerance']}
Goals: {portfolio['investment_goals']}

HOLDINGS:
"""
    for h in holdings:
        invested = h['shares'] * h['purchase_price']
        current = h['shares'] * h['current_price']
        return_pct = ((h['current_price'] - h['purchase_price']) / h['purchase_price']) * 100
        summary += f"\n  {h['ticker']} ({h['company']}): {h['shares']} shares | Return: {return_pct:.2f}%"
    
    return summary