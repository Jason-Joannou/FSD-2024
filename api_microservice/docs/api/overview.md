# API Overview

Welcome to the FSD API documentation. This guide offers a comprehensive overview of the available endpoints and how to use them. You can access the root API endpoint at [fsd-api.axh0cuaybfezfjdp.uksouth.azurecontainer.io](http://fsd-api.axh0cuaybfezfjdp.uksouth.azurecontainer.io)


## Plotting Endpoints

These endpoints are designed for generic use, allowing users to plot their own data in various formats.

- [GET /](endpoints.md#api-root): Returns a welcome message.
- [POST /line_graph](endpoints.md#post-line_graph): Generates a line graph.
- [POST /bar_graph](endpoints.md#post-bar_graph): Generates a bar graph.
- [POST /scatter_plot](endpoints.md#post-scatter_plot): Generates a scatter plot.
- [POST /histogram](endpoints.md#post-histogram): Generates a histogram.
- [POST /pie_chart](endpoints.md#post-pie_chart): Generates a pie chart.
- [POST /box_plot](endpoints.md#post-box_plot): Generates a box plot.
- [POST /heatmap](endpoints.md#post-heatmap): Generates a heatmap.
- [POST /area_chart](endpoints.md#post-area_chart): Generates an area chart.
- [POST /bubble_chart](endpoints.md#post-bubble_chart): Generates a bubble chart.
- [POST /candlestick_chart](endpoints.md#post-candlestick_chart): Generates a candlestick chart.

## General Financial Calculation Endpoints

These endpoints provide various financial calculations to help with personal finance management.

- [POST /calculate_compound_interest](endpoints.md#post-calculate_compound_interest): Calculates the compound interest based on the provided parameters.
- [POST /calculate_loan_payments](endpoints.md#post-calculate_loan_payments): Calculates the monthly payment for a loan.
- [POST /calculate_savings_growth](endpoints.md#post-calculate_savings_growth): Calculates the future value of savings.
- [POST /calculate_retirement_savings](endpoints.md#post-calculate_retirement_savings): Calculates the total retirement savings.
- [POST /calculate_savings_rate](endpoints.md#post-calculate_savings_rate): Calculates the savings rate needed to reach a financial goal.
- [POST /estimate_emergency_fund](endpoints.md#post-estimate_emergency_fund): Estimates the emergency fund required.

## Investment Calculation Endpoints

These endpoints provide various calculations related to investment management.

- [POST /calculate_future_value_investment](endpoints.md#post-calculate_future_value_investment): Calculates the future value of an investment.
- [POST /calculate_roi](endpoints.md#post-calculate_roi): Calculates the Return on Investment (ROI).
- [POST /estimate_investment_risk](endpoints.md#post-estimate_investment_risk): Estimates the investment risk based on the standard deviation of returns.
- [POST /calculate_investment_growth](endpoints.md#post-calculate_investment_growth): Calculates the future value of an investment with annual contributions.
- [POST /calculate_dividend_yield](endpoints.md#post-calculate_dividend_yield): Calculates the dividend yield of a stock.
- [POST /calculate_portfolio_performance](endpoints.md#post-calculate_portfolio_performance): Calculates the performance of a portfolio based on returns and weights.
- [POST /estimate_investment_horizon](endpoints.md#post-estimate_investment_horizon): Estimates the number of years needed to reach a target amount.

## Quality of Life Endpoints

These endpoints provide features to enhance the user's experience and access useful information.

- [GET /get_crypto_news](endpoints.md#get-get_crypto_news): Retrieves the latest cryptocurrency news articles.