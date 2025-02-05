from phi.model.openai import OpenAIChat
from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.run.response import RunEvent, RunResponse
from dotenv import load_dotenv
from get_screener_data import get_quaterly_results, get_cash_flow, get_balance_sheet, get_profit_loss, get_analysis
load_dotenv()


def web_get_agent():
    return Agent(
        name="Web Agent",
        description="You are expert who knows to search the internet and obtain information.",
        model=Groq(id="llama-3.3-70b-versatile"),
        # model=OpenAIChat(id="gpt-4o"),
        tools=[DuckDuckGo()],
        instructions=["Always include sources"],
        show_tool_calls=True,
        markdown=True
    )


def yahoo_fin_agent():
    return Agent(
        name="Yahoo Finance Agent",
        description="You are a finance expert specializing in Indian Stock Market. You can effortlessly analyze equity markets and stock data based on Yahoo Finance only.",
        model=Groq(
            id="llama-3.3-70b-versatile"),
        tools=[YFinanceTools(enable_all=True)],
        show_tool_calls=True,
        markdown=True,
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        instructions=[
            "Just provide the summarized data only. Display tables only when necessary."]
    )


def fundamental_agent():
    return Agent(
        name="Fundamental Stock Analyzer Agent",
        description="You are an expert in analyzing the value of a stock by assessing it's fundamentals. You need to analyse the stock based on their balance sheet data, profit-loss data, cash flow data, quaterly results and analyst comments.",
        model=OpenAIChat(id="gpt-4o"),
        tools=[get_quaterly_results, get_cash_flow,
               get_balance_sheet, get_profit_loss, get_analysis],
        show_tool_calls=True,
        markdown=True,
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        instructions=[
            "Just provide the summarized data only. Display tables only when necessary."]

    )


def get_agent_team():
    web_agent = web_get_agent()
    yfin_agent = yahoo_fin_agent()
    f_agent = fundamental_agent()
    return Agent(
        model=OpenAIChat(id="gpt-4o"),
        team=[f_agent, yfin_agent, web_agent],
        instructions=["Always include sources", "Explain the results in detail.",
                      "If you don't know the answer, reply saying you don't know."],
        show_tool_calls=True,
        markdown=True,
    )


def as_stream(response):
    for chunk in response:
        if isinstance(chunk, RunResponse) and isinstance(chunk.content, str):
            if chunk.event == RunEvent.run_response:
                yield chunk.content
