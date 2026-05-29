from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def generate_report(portfolio_summary: str, market_insights: str, user_query: str) -> str:
    """Generate a professional investment report in English - CUSTOMIZED PER QUESTION TYPE"""
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
    
    # Determine report type and create COMPLETELY DIFFERENT reports for each
    query_lower = user_query.lower()
    
    print(f"📝 Query received: {user_query}")  # Debug
    print(f"📝 Query type check: risk={('risk' in query_lower)}, perform={('perform' in query_lower)}, recommend={('recommend' in query_lower)}")  # Debug
    
    if "risk" in query_lower:
        print("✅ Detected: RISK REPORT")  # Debug
        # ===== RISK REPORT =====
        report_title = "Investment - Risk - Portfolio Report"
        system_prompt = """You are a risk management specialist. Write ONLY about portfolio RISKS.

CRITICAL: DO NOT add any title or main heading to your response. Just start with the sections.

MANDATORY SECTIONS:
## Critical Risk Areas
## Concentration Risk Analysis
## Sector Risk Exposure
## Individual Position Risk
## Volatility & Downside Risk
## Risk Rating & Score
## Risk Mitigation Actions

- DO NOT discuss performance or recommendations unless directly related to risk
- DO NOT include general portfolio composition unless it affects risk
- FOCUS 100% on identifying, measuring, and mitigating risks
- Use specific percentages, ratios, and risk metrics
- Be direct and prescriptive about which positions are risky"""

        user_prompt = f"""PORTFOLIO DATA:
{portfolio_summary}

MARKET CONTEXT:
{market_insights}

Write a RISK-FOCUSED report. Analyze every concentration risk, sector risk, volatility risk. What are the biggest dangers in this portfolio? Rate the overall portfolio risk. Suggest specific risk mitigation actions. Do NOT discuss general performance or non-risk topics."""

    elif "perform" in query_lower:
        print("✅ Detected: PERFORMANCE REPORT")  # Debug
        # ===== PERFORMANCE REPORT =====
        report_title = "Investment - Performance - Portfolio Report"
        system_prompt = """You are a performance analyst. Write ONLY about portfolio PERFORMANCE metrics.

CRITICAL: DO NOT add any title or main heading to your response. Just start with the sections.

MANDATORY SECTIONS:
## Overall Performance Summary
## Return Analysis
## Best Performing Assets
## Worst Performing Assets
## Benchmark Comparison
## Performance Drivers
## Performance Trend & Outlook

- DO NOT discuss risks unless specifically caused by the performance strategy
- DO NOT include recommendations unless directly related to performance improvement
- FOCUS 100% on measuring, analyzing, and comparing performance
- Use specific returns, percentages, YTD/YTM data
- Compare to relevant benchmarks (S&P 500, sector indices)"""

        user_prompt = f"""PORTFOLIO DATA:
{portfolio_summary}

MARKET CONTEXT:
{market_insights}

Write a PERFORMANCE-FOCUSED report. What are the returns? Which assets are winning and which are losing? How does this compare to the market? What drove the performance? What's the performance trend? Do NOT discuss risks or general recommendations."""

    elif "recommend" in query_lower:
        print("✅ Detected: RECOMMENDATIONS REPORT")  # Debug
        # ===== RECOMMENDATIONS REPORT =====
        report_title = "Investment - Recommendations - Portfolio Report"
        system_prompt = """You are an investment advisor. Write ONLY actionable RECOMMENDATIONS.

CRITICAL: DO NOT add any title or main heading to your response. Just start with the sections.

MANDATORY SECTIONS:
## Executive Recommendations Summary
## SELL Recommendations
## HOLD Recommendations  
## BUY Recommendations
## Rebalancing Actions
## Portfolio Optimization Strategy
## Implementation Timeline

- DO NOT analyze historical performance unless needed for recommendation
- DO NOT discuss risks unless they justify a recommendation change
- FOCUS 100% on specific, actionable advice
- Each recommendation must be specific: "SELL 30% of XYZ", "BUY QQQ", etc.
- Include rationale and expected benefits for each action"""

        user_prompt = f"""PORTFOLIO DATA:
{portfolio_summary}

MARKET CONTEXT:
{market_insights}

Write a RECOMMENDATION-FOCUSED report. What should be SOLD, HELD, or BOUGHT? What rebalancing is needed? What specific actions should be taken? Include the rationale for each recommendation. Be prescriptive and actionable. Do NOT discuss historical performance analysis or general risk assessment."""

    else:
        print("✅ Detected: FULL ANALYSIS REPORT")  # Debug
        # ===== FULL ANALYSIS REPORT =====
        report_title = "Investment - Full Analysis - Portfolio Report"
        system_prompt = """You are a comprehensive investment advisor. Write a COMPLETE portfolio analysis covering all aspects.

CRITICAL: DO NOT add any title or main heading to your response. Just start with the sections.

MANDATORY SECTIONS:
## Executive Summary
## Portfolio Overview & Composition
## Performance Analysis
## Risk Assessment  
## Market Context & Trends
## Key Findings & Insights
## Recommendations
## Conclusion & Action Items

- Cover all major aspects: composition, performance, risk, market context
- Balance detail across all sections
- Include specific metrics, percentages, and data
- End with clear action items
- Professional, comprehensive tone"""

        user_prompt = f"""PORTFOLIO DATA:
{portfolio_summary}

MARKET CONTEXT:
{market_insights}

Write a COMPLETE portfolio analysis covering: composition, performance, risk assessment, market trends, and recommendations. This is a comprehensive report that addresses all major aspects of the portfolio."""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt)
    ])
    
    response = llm.invoke(prompt.format_messages())
    
    # Clean the response - remove any duplicate titles the LLM might have added
    content = response.content
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip "Investment Portfolio Report" or other generic titles
        if 'Investment Portfolio Report' in line:
            continue
        # Skip lines that look like a report title
        if line.strip().startswith('# ') and line.strip() in ['# Investment Portfolio Report', '# Portfolio Report', '# Analysis Report']:
            continue
        cleaned_lines.append(line)
    
    cleaned_content = '\n'.join(cleaned_lines).strip()
    
    # Add our title at the beginning
    final_report = f"# {report_title}\n\n{cleaned_content}"
    return final_report