# Visualize Stocks using LLM

## Summary
This project automatically creates charts and tables from instructions provided in a markdown file. The markdown file contains specifications for the visualizations, including formatting and styling information. An LLM (Large Language Model) reads these instructions and, using a supplied CSV data file, generates the requested charts and tables.

The project also includes a helper class, `HtmlTableExtractor`, which extracts data from HTML tables and creates a CSV data file. This is useful for scraping data from the web, such as Wikipedia or other online sources.

You can run the project from the command line:

```bash
python3 ./visualize_from_markdown.py
```

---

## Configuration
There are four configuration options, specified in the `.env` file. An example configuration is available in `development.env`.
- `VISUALIZATION_INSTRUCTIONS`: The name of the markdown file (in the current directory) to use as instructions for the LLM.
- `DATA_URL`: The URL of the HTML page containing the table to extract.
- `OPEN_API_KEY`: Your OpenAI API key.
- `TRUST_GENERATED_CODE`: `True` or `False`. If `True`, the LLM-generated code will be executed automatically at the end of the run.
> 🧠 **Note**: Generated code will only execute if `TRUST_GENERATED_CODE` is set to `True` *and* you are running in a Python virtual environment. Both conditions must be met.

---

## Installation

### Quick Start
1. Copy `development.env` to `.env`, and update it with your `OPEN_API_KEY`.
2. **Recommended**: Set up a Python virtual environment.
3. Install dependencies with:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the program:
   ```bash
   python3 ./visualize_from_markdown.py
   ```

---

### Python Virtual Environment (Recommended)
Because this project uses an LLM to generate Python code dynamically, it's highly recommended to isolate your environment. The generated code may vary between runs, and a virtual environment helps manage dependencies and avoid conflicts with system packages.
```bash
python -m venv myenv
source myenv/bin/activate
```

---

### Installing Python Packages
To install the required packages:
```bash
pip install -r requirements.txt
```

---

## Known Limitations
- The accuracy and formatting of the generated charts may vary depending on the LLM output.
- Manual review of generated code is advised if you disable sandboxing (`TRUST_GENERATED_CODE=True`).
- The code requires additional configuration passed into `HtmlTableExtractor` when working with poorly-structured HTML tables.
  - enable `first_row_is_header` when header row is composed of `td` tags.
  - use `skip_first_rows` to pass over junk rows at the begining of a table. 

---

## Modifications 
To run this code against another datasource and to change the visualizations here is the process. 

---

### Quick Start 
1) Change the URL for the table in the `.env` file 
2) Create a new markdown file with instructions 
3) Change the markdown file name in the `.env` file 
4) Run the program 
   ```bash
   python3 ./visualize_from_markdown.py
   ```

---

### Example 
Update the URL in `.env`to `https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue`
🧠 **Note**: `visualize_from_markdown.py` must be updated. The HTML table in wikipedia is well formated, and we need take out our customizations. Around line 100 change the following:

```python
        # skip_first_rows 1 ; table has header row 
        extractor = HtmlTableExtractor(url=data_url,
                                   output_filename=os.path.join(output_dir, data_csv_file),
                                   skip_first_rows=1,
                                   first_row_is_header=True)
```
TO
```python
        # well-structured HTML table
        extractor = HtmlTableExtractor(url=data_url,
                                   output_filename=os.path.join(output_dir, data_csv_file))
```

Create a new Markdown File `company_viz.md`. Update `.env` to use `company_viz.md`
```text
# Visualization For Largest Companies In The United States

## Dataset
- File: `data.csv`
- Key Columns:
  - Rank
  - Name
  - Industry
  - Revenue (USD millions)
  - Revenue growth
  - Employees
  - Headquarters

## Required Visualizations
1. **Grouped Bar Chart**
   - **Purpose**: Compare employment across industries.
   - **X-axis**: Industry
   - **Y-axis**: Sum of employees across companies in the industry
   - **Legend**: Clearly label each industry.
   - **Color**: Assign a distinct color to each industry. 
   - **Formatting**: The Y-axis values should be integers.
   - **Output**: Save the output as a image file to the current working directory. Do not show as standard output.
```

---

## License
[MIT License](LICENSE)

---

## Contributing
Pull requests and issues are welcome! Please open a GitHub issue to suggest features or report bugs.