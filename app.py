from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
os.environ['GROQ_API_KEY'] = "GROQ_API_KEY"

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    temperature=0.7
)

emissions_analysis_agent = Agent(
    role="Emissions Data Analyst",
    goal="Analyze and extract key insights from company emissions data.",
    backstory="Expert in analyzing carbon emissions data to identify key trends and metrics, including scope emissions and baselines.",
    llm=llm,
    verbose=True
)

sustainability_strategy_agent = Agent(
    role="Sustainability Strategy Advisor",
    goal="Generate actionable sustainability strategies and targets based on the emissions analysis.",
    backstory="Experienced in crafting targeted reduction strategies, suggesting actionable policies, and setting realistic emissions targets.",
    llm=llm,
    verbose=True
)

def get_company_data_paragraph():
    st.write("### Enter your company's emissions data")
    st.write(
        "Provide a detailed paragraph describing your company's emissions targets, baseline year, and progress."
        "\nFor example: 'Company A is aiming for net zero emissions by 2050. Their baseline year is 2020. The company is on track to meet its targets with an interim goal of reducing emissions by 20% by 2030.'"
    )
    user_input = st.text_area(
        "Company Data (e.g., name, targets, and status)",
        placeholder="Enter company emissions data here...",
        height=200
    )
    return user_input

st.title("Green Orbit")

company_data = get_company_data_paragraph()

if company_data:
    emissions_analysis_task = Task(
        description=f"""
        Analyze the following emissions data and extract key metrics (scope emissions, baseline year, current emissions, interim targets, etc.):

        {company_data}

        Provide an emissions profile including insights on the company's emissions across different scopes (Scope 1, Scope 2, Scope 3) and baseline years.
        """,
        agent=emissions_analysis_agent,
        expected_output="Emissions profile including key metrics like Scope 1, Scope 2, Scope 3 emissions, baseline year, and targets."
    )

    sustainability_strategy_task = Task(
        description=f"""
        Based on the following emissions profile, suggest actionable sustainability strategies, reduction targets, and policies:

        {company_data}

        Suggest:
        1. Realistic and impactful reduction targets (e.g., percentage reduction by specific years).
        2. Key actionable policies to reduce emissions (e.g., energy efficiency measures, renewable energy adoption).
        """,
        agent=sustainability_strategy_agent,
        expected_output="Recommendations for emissions reduction targets and policies to achieve sustainability goals."
    )

    crew = Crew(
        agents=[emissions_analysis_agent, sustainability_strategy_agent],
        tasks=[emissions_analysis_task, sustainability_strategy_task]
    )

    with st.spinner("🤖 **Agents are working...**"):
        result = crew.kickoff()

    st.subheader("🌍 Emissions Profile & Strategy Recommendations")
    st.markdown(result)
else:
    st.info("Please enter your company emissions data above.")
