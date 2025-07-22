# Visualization For Performance Across Asset Classes

## Dataset
- File: `data.csv`
- Key Columns:
  - Year
  - "S&P 500 (includes dividends)"
  - "US Small cap (bottom decile)"
  - "3-month T.Bill"
  - "US T. Bond (10-year)"
  - "Baa Corporate Bond"
  - "Real Estate"
  - Gold*

## Required Visualizations

1. **Grouped Bar Chart**
   - **Purpose**: Compare annual performance of multiple asset classes side by side.
   - **X-axis**: Year
   - **Y-axis**: Percentage return
   - **Asset Class**: 
     - "S&P 500 (includes dividends)"
     - "Baa Corporate Bond"
   - **Bar Layout**: 
     - Display a bar for each asset class for each year.
   - **Legend**: Clearly label each asset class.
   - **Color**: Assign a distinct color to each asset class. Prefered colors 
     - Blue for "S&P 500 (includes dividends)"
     - Red for "Baa Corporate Bond"
   - **Formatting**: The Y-axis values should be percentages with 2 decimal places.
   - **Output**: Save the output as a image file to the current working directory. Do not show as standard output.

2. **Table View**
  - **Purpose**: Show the top 3 performing years for the following asset classes. When finding the largest values make sure to convert the data to numbers.
  - **Asset Classes**:
    - "S&P 500 (includes dividends)"
    - "US Small cap (bottom decile)"
    - "US T. Bond (10-year)"
    - "Baa Corporate Bond"
    - "Real Estate"
    - Gold*
  - **Column Headings**: Rename the columns for readability to 
    - Year -> Year 
    - "S&P 500 (includes dividends)" -> "S&P 500"
    - "US Small Cap (bottom decile)" -> "US Small Cap"
    - "US T. Bond (10-year)" -> "US T.Bond"
    - "Baa Corporate Bond" -> "Baa Corp Bond"
    - "Real Estate" -> "Real Estate"
    - "Gold*" -> "Gold"
  - **Sorting**: Year
  - **Formatting**:
    - Show the year as a 4 digit integer.
    - Show values as percentages with no decimal places.
    - Use `"-"` to indicate missing data.
    - Lable each table with the Asset Class name.
  - **Output**: Save the output as a text file to the current working directory. Do not show as standard output.