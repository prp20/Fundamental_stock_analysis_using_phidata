import sys
import requests
from bs4 import BeautifulSoup
import json
import time
import pandas as pd
# Scrape data from the website
import json

# from agno.tools import Toolkit

# try:
#     import yfinance as yf
# except ImportError:
#     raise ImportError("`yfinance` not installed. Please install using `pip install yfinance`.")


def scrape_data(ticker, section_id):
    url = f"https://www.screener.in/company/{ticker}/consolidated/#{section_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    section = soup.find('section', {'id': section_id})
    if not section:
        return pd.DataFrame()  # Return an empty DataFrame if the section is not found

    table = section.find(
        'table', {'class': 'data-table responsive-text-nowrap'})
    if not table:
        return pd.DataFrame()  # Return an empty DataFrame if the table is not found

    rows = table.find_all('tr')
    data = []

    for row in rows:
        cols = row.find_all('th')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)

    data = [data[0]]  # Add header row
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)

    filtered_lists = [lst for lst in data if lst]
    df = pd.DataFrame(filtered_lists)
    return df


def get_profit_loss(ticker, ret_json=True):
    """
    Use this function to get a company's profit and loss information of last 5 years based on a given symbol.

    Args:
        symbol (str): The stock symbol.

    Returns:
        str: JSON containing company profit and loss information for last 5 years.
    """
    profit_loss_df = scrape_data(ticker, 'profit-loss')
    profit_loss_df = pd.concat(
        [profit_loss_df.iloc[:, [0]], profit_loss_df.iloc[:, -6:-1]], axis=1)
    profit_loss_df = profit_loss_df.T
    profit_loss_df.columns = profit_loss_df.iloc[0]
    profit_loss_df.drop([profit_loss_df.index[0]], inplace=True)
    if not ret_json:
        return profit_loss_df
    else:
        return profit_loss_df.to_json(orient="index")


def get_balance_sheet(ticker, ret_json=True):
    """
    Use this function to get a company's balance-sheet information of last 5 years based on a given symbol.

    Args:
        symbol (str): The stock symbol.

    Returns:
        str: JSON containing company balance-sheet information for last 5 years.
    """
    balance_sheet_df = scrape_data(ticker, 'balance-sheet')
    balance_sheet_df = pd.concat(
        [balance_sheet_df.iloc[:, [0]], balance_sheet_df.iloc[:, -5:]], axis=1)
    balance_sheet_df = balance_sheet_df.T
    balance_sheet_df.columns = balance_sheet_df.iloc[0]
    balance_sheet_df.drop([balance_sheet_df.index[0]], inplace=True)
    if not ret_json:
        return balance_sheet_df
    else:
        return balance_sheet_df.to_json(orient="index")


def get_cash_flow(ticker, ret_json=True):
    """
    Use this function to get a company's cash flow information of last 5 years based on a given symbol.

    Args:
        symbol (str): The stock symbol.

    Returns:
        str: JSON containing company cash flow information for last 5 years.
    """
    cash_flow_df = scrape_data(ticker, 'cash-flow')
    cash_flow_df = pd.concat(
        [cash_flow_df.iloc[:, [0]], cash_flow_df.iloc[:, -5:]], axis=1)
    cash_flow_df = cash_flow_df.T
    cash_flow_df.columns = cash_flow_df.iloc[0]
    cash_flow_df.drop([cash_flow_df.index[0]], inplace=True)
    if not ret_json:
        return cash_flow_df
    else:
        return cash_flow_df.to_json(orient="index")


def get_quaterly_results(ticker, ret_json=True):
    """
    Use this function to get a company's quaterly results information of last 5 quaters based on a given symbol.

    Args:
        symbol (str): The stock symbol.

    Returns:
        str: JSON containing company's quaterly results information of last 5 quaters.
    """
    quaterly_results_df = scrape_data(ticker, 'quarters')
    quaterly_results_df = pd.concat(
        [quaterly_results_df.iloc[:, [0]], quaterly_results_df.iloc[:, -5:]], axis=1)
    quaterly_results_df = quaterly_results_df.T
    quaterly_results_df.columns = quaterly_results_df.iloc[0]
    quaterly_results_df.drop([quaterly_results_df.index[0]], inplace=True)
    if not ret_json:
        return quaterly_results_df
    else:
        return quaterly_results_df.to_json(orient="index")


def get_analysis(ticker, ret_json=True):
    """
    Use this function to get analyst recommendations for a given stock symbol.

    Args:
        symbol (str): The stock symbol.

    Returns:
        str: JSON containing analyst recommendations.
    """
    url = f"https://www.screener.in/company/{ticker}/consolidated/#analysis"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pros_section = soup.find('div', class_='pros')
    pros = [li.get_text() for li in pros_section.find_all('li')]
    cons_section = soup.find('div', class_='cons')
    cons = [li.get_text() for li in cons_section.find_all('li')]

    return json.dumps({"pros": pros, "cons": cons})
