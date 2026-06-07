from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

def generate_report(portfolio_summary: str, market_insights: str, user_query: str) -> str:
    """Generate a professional investment report using TinyLlama (free local model)"""
    
    llm = ChatOllama(
        model="tinyllama",  # Utilise le modèle que vous avez déjà
        temperature=0.3,
        num_predict=2048  # TinyLlama a une limite plus petite
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional financial advisor. Write a complete investment report.

The report MUST include these sections:
1. Executive Summary
2. Portfolio Overview
3. Market Landscape & Trends
4. Performance Analysis
5. Risk Assessment
6. Recommendations
7. Conclusion
8. References

Use simple markdown formatting. Be clear and professional."""),
        ("user", f"""
USER QUESTION: {user_query}

PORTFOLIO DATA:
{portfolio_summary}

MARKET INSIGHTS:
{market_insights}

Now write the complete investment report with all 8 sections.
""")
    ])
    
    try:
        response = llm.invoke(prompt.format_messages())
        return response.content
    except Exception as e:
        # Fallback en cas d'erreur
        return f"""
# Investment Portfolio Report

## Executive Summary
Analysis completed for your portfolio.

## Portfolio Overview
{portfolio_summary[:1000]}

## Market Insights
{market_insights[:500]}

## Recommendations
Based on the analysis, maintain current positions and monitor market conditions.

---
*Note: Report generated with TinyLlama*
"""