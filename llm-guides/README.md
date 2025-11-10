# Using LLMs to Generate Blueshift Trading Strategies

This directory contains specialized guides designed to be used as context for Large Language Models (LLMs) like ChatGPT, Claude, and Gemini. By providing these guides along with your prompts, you can enable LLMs to generate accurate, functional, and well-structured trading strategy code for the Blueshift platform.

## Available Guides

1.  **`llm-context.md` (General Strategy Guide):**
    *   **Purpose:** The primary guide for most trading strategies.
    *   **Use Cases:** Ideal for strategies involving a small, fixed set of assets (e.g., single-stock, pairs trading), technical indicators, or specific event-driven logic. Covers the core Blueshift API for orders, scheduling, and data access.

2.  **`llm-context-pipeline.md` (Pipeline Strategy Guide):**
    *   **Purpose:** An extension of the general guide, focusing on the Pipeline API.
    *   **Use Cases:** Essential for strategies that require dynamic screening, ranking, and filtering of a large universe of assets. For these complex cases, it is recommended to provide **both** this guide and the general `llm-context.md` guide to the LLM.

## How to Use the Guides

The process is straightforward:

1.  **Select the Guide(s):**
    *   For most strategies, use `llm-context.md`.
    *   For strategies involving large universe screening and ranking, it is highly recommended to use both `llm-context.md` and `llm-context-pipeline.md`.

2.  **Provide Context to the LLM:** Upload the selected guide file(s) directly to your LLM interface (e.g., ChatGPT, Gemini). This is more reliable than copy-pasting the content.

3.  **Write Your Prompt:** Clearly describe the trading strategy you want the LLM to create. Follow the prompt engineering guidelines below for the best results.

---

## Prompt Engineering Guidelines for Trading Strategies

Crafting a good prompt is crucial for getting high-quality code from an LLM. A well-structured prompt reduces errors and minimizes the need for follow-up corrections.

### 1. Be Specific and Unambiguous

Clarity is key. Avoid vague terms and clearly define every aspect of your logic.

*   **Vague:** "Create a momentum strategy."
*   **Specific:** "Write a strategy that buys the 10 stocks with the highest 3-month rate of change (63 trading days)."

### 2. Assign a Role and State the Goal

Always start your prompt by assigning an expert role to the LLM. This focuses the model on producing high-quality, domain-specific code. Then, state the goal and the context (the guides) it should use.

*   **Good Example:** "You are an expert Python developer specializing in creating algorithmic trading strategies for the Blueshift platform. Using the uploaded `Blueshift LLM Strategy Developer Guide`, your task is to generate a complete Python trading strategy that..."

### 3. Structure Your Prompt

A structured prompt helps the LLM understand the different components of your request. A recommended structure is:

1.  **Role Assignment & Context:** "You are an expert... Using the uploaded [Guide Name(s)]..."
2.  **Strategy Summary:** A one-sentence summary of the logic.
3.  **Asset Universe:** Define the assets to be traded (e.g., specific stocks, a dynamic universe).
4.  **Entry Logic:** The exact conditions for entering a long or short position.
5.  **Exit Logic:** The exact conditions for closing a position.
6.  **Risk Management:** Specify stop-loss, take-profit, or position sizing rules.
7.  **Rebalancing/Scheduling:** Define how often the logic should run (e.g., daily, weekly, at a specific time).
8.  **Parameters:** List all numerical inputs in one place (e.g., lookback periods, indicator settings, number of stocks).

### 4. Define All Parameters

Quantify everything. Don't let the LLM guess the numbers.

*   **Incomplete:** "Use a fast and a slow moving average."
*   **Complete:** "Use a 20-period Simple Moving Average (SMA) for the fast MA and a 50-period SMA for the slow MA."

### 5. Iterate and Refine

If the LLM generates incorrect or incomplete code, don't just say "it's wrong." Instead, guide it by:
*   Pointing out the specific error (e.g., "The `schedule_function` is used in the wrong place.").
*   Referencing the relevant section from the guide you provided (e.g., "According to the guide, `schedule_function` should only be called in `initialize`.").
*   Providing the corrected code snippet yourself.

---

## Example Prompts

### Example for General Guide (`llm-context.md`)

```
You are an expert Python developer specializing in creating algorithmic trading strategies for the Blueshift platform. Using the uploaded 'Blueshift LLM Strategy Developer Guide', write a complete Python strategy for the following logic:

**Strategy:** A simple RSI-based strategy for the stock 'RELIANCE'.

**Universe:**
- 'RELIANCE'

**Entry Logic:**
- Go long (buy) with 100% of the portfolio value when the 14-day RSI crosses below 30.

**Exit Logic:**
- Exit the long position (sell) when the 14-day RSI crosses above 70.

**Scheduling:**
- The logic should be checked once every day at market open.

**Parameters:**
- RSI Period: 14 days
- RSI Oversold Level: 30
- RSI Overbought Level: 70
```

### Example for Pipeline Guide (using both guides)

```
You are an expert Python developer specializing in creating algorithmic trading strategies for the Blueshift platform. Using the uploaded 'Blueshift LLM Strategy Developer Guide' and 'Blueshift LLM Pipeline Strategy Developer Guide', write a complete Python strategy for the following logic:

**Strategy:** A long-only momentum strategy that invests in the top 5 performing stocks from the NIFTY 50 universe, filtered by liquidity.

**Universe:**
- All stocks in the NSE.

**Pipeline Screening & Ranking:**
1.  **Liquidity Filter:** First, filter the universe to include only stocks with an average daily dollar volume over the last 20 days greater than 10,000,000.
2.  **Momentum Factor:** Calculate the 6-month (126 trading days) rate of change (ROC) for the remaining stocks.
3.  **Ranking:** Select the top 5 stocks with the highest 6-month ROC.

**Trading Logic:**
- At the beginning of each month, rebalance the portfolio to hold the 5 selected stocks in equal-weighted positions (20% each).
- Sell any stocks that are no longer in the top 5 list.

**Scheduling:**
- The pipeline and rebalancing logic should run on the first trading day of each month, 30 minutes before the market closes.
```
