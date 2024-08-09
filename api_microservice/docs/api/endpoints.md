# API Endpoints

## GET /

Returns a welcome message for the FSD public API.

**Returns:**
- JSON response with a welcome message.

## POST /line_graph

Generates a line graph based on the provided data.

**Arguments:**
- `x` (List): Data for the x-axis.
- `y` (List): Data for the y-axis.
- `x_axis_title` (str): Title for the x-axis.
- `y_axis_title` (str): Title for the y-axis.
- `plot_title` (str): Title for the plot.
- `line_color` (str): Color of the line.
- `marker_style` (str): Style of the markers.
- `html_embedding` (bool): If True, returns the plot as HTML.

**Returns:**
- JSON or HTML response with the plot.
