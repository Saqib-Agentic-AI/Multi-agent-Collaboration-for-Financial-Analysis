import os
from crewai import Agent, Crew, Task, LLM, Process
from crewai_tools import ScrapeWebsiteTool

# 1. Initialize the local LLM for BOTH the agents and the manager
local_llm = LLM(
    model="ollama/qwen2.5-coder:3b",
    base_url="http://localhost:11434"
)

# 2. Initialize tools
scrape_tool = ScrapeWebsiteTool()

# 3. Create Agents
data_analyst_agent = Agent(
    role="Data Analyst",
    goal="Monitor and analyze market data in real-time to identify trends and predict market movements.",
    backstory="Specializing in financial markets, this agent uses statistical modeling to provide crucial insights.",
    verbose=True,
    tools=[scrape_tool],
    llm=local_llm
)

trading_strategy_agent = Agent(
    role="Trading Strategy Developer",
    goal="Develop and test various trading strategies based on insights from the Data Analyst Agent.",
    backstory="Equipped with a deep understanding of financial markets, this agent devises profitable and risk-averse options.",
    verbose=True,
    tools=[scrape_tool],
    llm=local_llm
)

execution_agent = Agent(
    role="Trade Advisor",
    goal="Suggest optimal trade execution strategies based on approved trading strategies.",
    backstory="Analyzes timing, price, and logistical details to maximize efficiency and adherence to strategy.",
    verbose=True,
    tools=[scrape_tool],
    llm=local_llm
)

risk_management_agent = Agent(
    role="Risk Advisor",
    goal="Evaluate and provide insights on the risks associated with potential trading activities.",
    backstory="Scrutinizes potential risks and suggests safeguards to ensure alignment with the firm's risk tolerance.",
    verbose=True,
    tools=[scrape_tool],
    llm=local_llm
)

# 4. Create Tasks
data_analysis_task = Task(
    description="Continuously monitor and analyze market data for the selected stock ({stock_selection}).",
    expected_output="Insights and alerts about significant market opportunities or threats for {stock_selection}.",
    agent=data_analyst_agent
)

strategy_development_task = Task(
    description="Develop and refine trading strategies based on insights and user risk tolerance ({risk_tolerance}). Consider trading preferences ({trading_strategy_preference}).",
    expected_output="A set of potential trading strategies for {stock_selection} that align with risk tolerance.",
    agent=trading_strategy_agent
)

execution_planning_task = Task(
    description="Analyze approved strategies to determine the best execution methods for {stock_selection}, considering current market conditions.",
    expected_output="Detailed execution plans suggesting how and when to execute trades for {stock_selection}.",
    agent=execution_agent
)

risk_assessment_task = Task(
    description="Evaluate risks associated with the proposed trading strategies and execution plans for {stock_selection}.",
    expected_output="A comprehensive risk analysis report detailing potential risks and mitigation recommendations for {stock_selection}.",
    agent=risk_management_agent
)

# 5. Create Crew (HIERARCHICAL SETUP)
financial_trading_crew = Crew(
    agents=[
        data_analyst_agent, 
        trading_strategy_agent, 
        execution_agent, 
        risk_management_agent
    ],
    tasks=[
        data_analysis_task, 
        strategy_development_task, 
        execution_planning_task, 
        risk_assessment_task
    ],
    verbose=True,
    process=Process.hierarchical,  # Tell CrewAI to use a manager structure
    manager_llm=local_llm          # CRITICAL: Forces manager to use local Qwen model!
)

# 6. Define Inputs
financial_trading_inputs = {
    'stock_selection': 'AAPL',
    'initial_capital': '100000',
    'risk_tolerance': 'Medium',
    'trading_strategy_preference': 'Day Trading',
    'news_impact_consideration': True
}

# 7. Run the Crew
print("Starting the Financial Analysis Crew (Hierarchical Mode)...")
result = financial_trading_crew.kickoff(inputs=financial_trading_inputs)

print("\n=== FINANCIAL ANALYSIS REPORT ===\n")
print(result)