# API Endpoints

## GET /

Returns a welcome message for the FSD public API.

**Returns:**
- JSON response with a welcome message.

**Example Response**
```json
{
    "message": "Welcome to the FSD public API"
}
```

## POST /line_graph

Generates a line graph based on the provided data.

**Arguments:**

- `x` (List[Union[int, float, str]]): Data for the x-axis.
- `y` (List[Union[int, float]]): Data for the y-axis.
- `x_axis_title` (str): Title for the x-axis.
- `y_axis_title` (str): Title for the y-axis.
- `plot_title` (str): Title for the plot.
- `line_color` (str): Color of the line.
- `marker_style` (str): Style of the markers.
- `html_embedding` (bool): If True, returns the plot as HTML.

**Returns:**
- JSON or HTML response with the plot.

**Example Request:**
```json
{
    "x": [1, 2, 3],
    "y": [10, 15, 13],
    "x_axis_title": "Time",
    "y_axis_title": "Value",
    "plot_title": "Sample Line Graph",
    "line_color": "red",
    "marker_style": "square",
    "html_embedding": false
}
```

## POST /bar_graph

Generates a bar graph based on the provided data.

**Arguments:**

- `x` (List[Union[int, float, str]]): Data for the x-axis.
- `y` (List[Union[int, float]]): Data for the y-axis.
- `x_axis_title` (str): Title for the x-axis.
- `y_axis_title` (str): Title for the y-axis.
- `plot_title` (str): Title for the plot.
- `bar_color` (str): Color of the bars.
- `html_embedding` (bool): If True, returns the plot as HTML.

**Returns:**
- JSON or HTML response with the plot.

**Example Request:**
```json
{
    "x": ["A", "B", "C"],
    "y": [5, 10, 7],
    "x_axis_title": "Categories",
    "y_axis_title": "Values",
    "plot_title": "Sample Bar Graph",
    "bar_color": "green",
    "html_embedding": false
}
```

## POST /scatter_plot

Generates a scatter plot based on the provided data.

**Arguments:**

- `x` (List[Union[int, float, str]]): Data for the x-axis.
- `y` (List[Union[int, float]]): Data for the y-axis.
- `x_axis_title` (str): Title for the x-axis.
- `y_axis_title` (str): Title for the y-axis.
- `plot_title` (str): Title for the plot.
- `point_color` (str): Color of the points.
- `marker_style` (str): Style of the markers.
- `html_embedding` (bool): If True, returns the plot as HTML.

**Returns:**
- JSON or HTML response with the plot.

**Example Request:**
```json
{
    "x": [1, 2, 3],
    "y": [4, 5, 6],
    "x_axis_title": "X Axis",
    "y_axis_title": "Y Axis",
    "plot_title": "Sample Scatter Plot",
    "point_color": "blue",
    "marker_style": "triangle",
    "html_embedding": false
}
```

## POST /histogram

Generates a histogram based on the provided data.

**Arguments:**

- `data` (List[Union[int, float]]): Data to be plotted in the histogram.
- `x_axis_title` (str): Title for the x-axis.
- `y_axis_title` (str): Title for the y-axis.
- `plot_title` (str): Title for the plot.
- `bar_color` (str): Color of the bars.
- `html_embedding` (bool): If True, returns the plot as HTML.

**Returns:**
- JSON or HTML response with the plot.

**Example Request:**
```json
{
    "data": [1, 2, 2, 3, 4, 5],
    "x_axis_title": "Values",
    "y_axis_title": "Frequency",
    "plot_title": "Sample Histogram",
    "bar_color": "purple",
    "html_embedding": false
}
```

## POST /pie_chart

Generates a pie chart based on the provided data.

**Arguments:**

- `labels` (List[str]): Labels for the pie chart segments.
- `values` (List[Union[int, float]]): Values for each segment of the pie chart.
- `plot_title` (str): Title for the plot.
- `html_embedding` (bool): If True, returns the plot as HTML.

**Returns:**
- JSON or HTML response with the plot.

**Example Request:**
```json
{
    "labels": ["A", "B", "C"],
    "values": [30, 40, 30],
    "plot_title": "Sample Pie Chart",
    "html_embedding": false
}
```

## POST /box_plot

Generates a box plot based on the provided data.

**Arguments:**

- `data` (List[Union[int, float]]): Data to be plotted in the box plot.
- `x_axis_title` (str): Title for the x-axis.
- `y_axis_title` (str): Title for the y-axis.
- `plot_title` (str): Title for the plot.
- `box_color` (str): Color of the box plot.
- `html_embedding` (bool): If True, returns the plot as HTML.

**Returns:**
- JSON or HTML response with the plot.

**Example Request:**
```json
{
    "data": [1, 2, 3, 4, 5],
    "x_axis_title": "X Axis",
    "y_axis_title": "Y Axis",
    "plot_title": "Sample Box Plot",
    "box_color": "orange",
    "html_embedding": false
}
```

## POST /heatmap

Generates a heatmap based on the provided data.

**Arguments:**

- `x` (List[str]): Data for the x-axis.
- `y` (List[str]): Data for the y-axis.
- `z` (List[List[float]]): Data for the heatmap values.
- `plot_title` (str): Title for the plot.
- `html_embedding` (bool): If True, returns the plot as HTML.

**Returns:**
- JSON or HTML response with the plot.

**Example Request:**
```json
{
    "x": ["A", "B", "C"],
    "y": ["X", "Y", "Z"],
    "z": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    "plot_title": "Sample Heatmap",
    "html_embedding": false
}
```

## POST /area_chart

Generates an area chart based on the provided data.

**Arguments:**

- `x` (List[Union[int, float, str]]): Data for the x-axis.
- `y` (List[Union[int, float]]): Data for the y-axis.
- `x_axis_title` (str): Title for the x-axis.
- `y_axis_title` (str): Title for the y-axis.
- `plot_title` (str): Title for the plot.
- `fill_color` (str): Color for the filled area.
- `html_embedding` (bool): If True, returns the plot as HTML.

**Returns:**
- JSON or HTML response with the plot.

**Example Request:**
```json
{
    "x": [1, 2, 3],
    "y": [10, 15, 13],
    "x_axis_title": "X Axis",
    "y_axis_title": "Y Axis",
    "plot_title": "Sample Area Chart",
    "fill_color": "lightgreen",
    "html_embedding": false
}
```

## POST /bubble_chart

Generates a bubble chart based on the provided data.

**Arguments:**

- `x` (List[Union[int, float, str]]): Data for the x-axis.
- `y` (List[Union[int, float]]): Data for the y-axis.
- `sizes` (List[Union[int, float]]): Sizes of the bubbles.
- `x_axis_title` (str): Title for the x-axis.
- `y_axis_title` (str): Title for the y-axis.
- `plot_title` (str): Title for the plot.
- `html_embedding` (bool): If True, returns the plot as HTML.

**Returns:**
- JSON or HTML response with the plot.

**Example Request:**
```json
{
    "x": [1, 2, 3],
    "y": [4, 5, 6],
    "sizes": [20, 30, 40],
    "x_axis_title": "X Axis",
    "y_axis_title": "Y Axis",
    "plot_title": "Sample Bubble Chart",
    "html_embedding": false
}
```

## POST /candlestick_chart

Generates a candlestick chart based on the provided data.

**Arguments:**

- `dates` (List[str]): Dates for the candlestick chart.
- `open` (List[float]): Opening values.
- `high` (List[float]): High values.
- `low` (List[float]): Low values.
- `close` (List[float]): Closing values.
- `x_axis_title` (str): Title for the x-axis.
- `y_axis_title` (str): Title for the y-axis.
- `plot_title` (str): Title for the plot.
- `html_embedding` (bool): If True, returns the plot as HTML.

**Returns:**
- JSON or HTML response with the plot.

**Example Request:**
```json
{
    "dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
    "open": [100, 102, 101],
    "high": [105, 106, 104],
    "low": [99, 100, 98],
    "close": [102, 101, 103],
    "x_axis_title": "Dates",
    "y_axis_title": "Price",
    "plot_title": "Sample Candlestick Chart",
    "html_embedding": false
}
```

## POST /calculate_compound_interest

Calculates the compound interest based on the provided parameters.

**Arguments:**

- `principal` (float): The initial amount of money.
- `rate` (float): The annual interest rate (decimal).
- `time` (int): The number of years the money is invested.
- `n` (int): The number of times that interest is compounded per year.

**Returns:**
- JSON response with the amount of money accumulated after the specified time.

**Example Request:**
```json
{
    "principal": 1000,
    "rate": 0.05,
    "time": 10,
    "n": 4
}
```

**Example Response:**
```json
{
    "amount": 1647.009
}
```

## POST /calculate_loan_payments

Calculates the monthly payment for a loan based on the provided parameters.

**Arguments:**

- `principal` (float): The loan amount.
- `annual_rate` (float): The annual interest rate (percentage).
- `num_payments` (int): The total number of payments.

**Returns:**
- JSON response with the monthly payment amount.

**Example Request:**
```json
{
    "principal": 50000,
    "annual_rate": 5.0,
    "num_payments": 120
}
```

**Example Response:**
```json
{
    "monthly_payment": 530.44
}
```

## POST /calculate_savings_growth

Calculates the future value of savings based on the provided parameters.

**Arguments:**

- `deposit` (float): The amount of each deposit.
- `rate` (float): The annual interest rate (decimal).
- `periods` (int): The number of periods (e.g., months).

**Returns:**
- JSON response with the future value of the savings.

**Example Request:**
```json
{
    "deposit": 200,
    "rate": 0.04,
    "periods": 12
}
```

**Example Response:**
```json
{
    "future_value": 2492.48
}
```

## POST /calculate_retirement_savings

Calculates the total retirement savings based on current savings, annual contributions, interest rate, and years.

**Arguments:**

- `current_savings` (float): The current amount of savings.
- `annual_contribution` (float): The amount contributed annually.
- `rate` (float): The annual interest rate (decimal).
- `years` (int): The number of years of saving.

**Returns:**
- JSON response with the total savings at retirement.

**Example Request:**
```json
{
    "current_savings": 50000,
    "annual_contribution": 5000,
    "rate": 0.05,
    "years": 20
}
```

**Example Response:**
```json
{
    "total_savings": 212347.68
}
```

## POST /calculate_savings_rate

Calculates the savings rate needed to reach a financial goal based on income, goal amount, and time frame.

**Arguments:**

- `income` (float): Monthly income.
- `goal_amount` (float): Financial goal amount.
- `months` (int): Number of months to save.
- `rate` (float): Interest rate (decimal).

**Returns:**
- JSON response with the required savings rate.

**Example Request:**
```json
{
    "income": 5000,
    "goal_amount": 60000,
    "months": 12,
    "rate": 0.03
}
```

**Example Response:**
```json
{
    "savings_rate": 10.00
}
```

## POST /estimate_emergency_fund

Estimates the emergency fund required based on monthly expenses and the number of months to cover.

**Arguments:**

- `monthly_expenses` (float): Monthly expenses.
- `months` (int): Number of months to cover.

**Returns:**
- JSON response with the estimated emergency fund amount.

**Example Request:**
```json
{
    "monthly_expenses": 1500,
    "months": 6
}
```

**Example Response:**
```json
{
    "emergency_fund": 9000
}
```