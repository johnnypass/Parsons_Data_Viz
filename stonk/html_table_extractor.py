import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

class HtmlTableExtractor:
    """
    A class to download an HTML page, parse the first table using BeautifulSoup,
    and save its first 8 columns to a CSV file using pandas.
    """

    def __init__(self, 
                 url: str, 
                 output_filename: str = 'data.csv', 
                 skip_first_rows: int = 0,
                 first_row_is_header: bool = False):
        """
        Initializes the extractor with a URL and triggers the process.

        The initialization process will:
        1. Download the HTML from the given URL.
        2. Parse the first HTML table using BeautifulSoup.
        3. Use pandas to create a DataFrame from the parsed data.
        4. Extract the first 8 columns.
        5. Write the result to a local CSV file.

        Args:
            url (str): The URL to an HTML file containing a table.
            output_filename (str, optional): The name for the output CSV file. Defaults to 'data.csv'.
            skip_first_rows (int, optional): The number of initial rows to skip in the HTML table. Defaults to 0.
            first_row_is_header (bool, optional): By default parser looks for <th> tags to calculate header. This overrides that behavior and assumes the first row should be treated as the header. Defaults to False. First row is calc after any skips.
        """
        self.skip_first_rows = skip_first_rows
        self.first_row_is_header = first_row_is_header
        self.url = url
        self.output_filename = output_filename
        self._run()

    def _download_html(self) -> str | None:
        """Downloads HTML content from the URL."""
        try:
            print(f"Downloading HTML from {self.url}...")
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            print("Download successful.")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to download URL. {e}")
            return None

    def _parse_table(self, html: str) -> pd.DataFrame | None:
        """Parses the HTML, finds the first table, and returns it as a DataFrame."""
        if not html:
            return None
        
        print("Parsing HTML with BeautifulSoup...")
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        if not table:
            print("Error: No <table> found in the HTML content.")
            return None

        # Extract headers from <th> tags
        # if first_row_is_header 
        if self.first_row_is_header:
            headers = [td.get_text(strip=True) for td in table.find_all('tr')[self.skip_first_rows].find_all('th')]
        if self.first_row_is_header and table.find_all('tr')[self.skip_first_rows:]:
            first_row_after_skip = table.find_all('tr')[self.skip_first_rows]
            if first_row_after_skip:
                headers = [td.get_text(strip=True) for td in first_row_after_skip.find_all('td')]
                self.skip_first_rows += 1
            else:
                headers = []
        else:
            headers = [th.get_text(strip=True) for th in table.find_all('th')]

        # Extract table rows from <tr> with <td> tags
        data_rows = []
        for tr in table.find_all('tr')[self.skip_first_rows:]:
            cells = tr.find_all('td')
            if cells:
                data_rows.append([cell.get_text(strip=True) for cell in cells])
        
        if not data_rows:
            print("Error: Table found, but no data rows (with <td>) could be parsed.")
            return None

        # Create DataFrame. Use headers if their count matches the number of columns.
        df = pd.DataFrame(data_rows, columns=headers if headers and len(headers) == len(data_rows[0]) else None)
        print("Successfully parsed table into a pandas DataFrame.")
        return df

    def _write_csv(self, df: pd.DataFrame) -> None:
        """Takes a DataFrame, extracts columns, and writes to a CSV."""
        if df is None:
            return
        
        print("Extracting columns and writing to CSV...")
        # Select the first 8 columns. If fewer than 8, select all.
        num_columns_to_save = min(8, df.shape[1])
        df_to_save = df.iloc[:, :num_columns_to_save]

        try:
            df_to_save.to_csv(self.output_filename, index=False)
            print(f"Successfully wrote {num_columns_to_save} columns to '{os.path.abspath(self.output_filename)}'")
        except IOError as e:
            print(f"Error: Could not write to file {self.output_filename}. {e}")

    def _run(self):
        """Orchestrates the entire download, parse, and save process."""
        html_content = self._download_html()
        if html_content:
            dataframe = self._parse_table(html_content)
            if dataframe is not None:
                self._write_csv(dataframe)

# Example of how to use the class
if __name__ == '__main__':
    # This is a Wikipedia page with a large table, perfect for demonstration.
    EXAMPLE_URL = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
    
    print("--- Creating instance of HtmlTableExtractor ---")
    # Initializing the class will automatically run the entire process.
    extractor = HtmlTableExtractor(url=EXAMPLE_URL)
    print("\n--- Process complete ---")

    # You can verify that 'data.csv' has been created in your local directory.
    if os.path.exists('data.csv'):
        print("\n--- 'data.csv' created successfully. ---")
        df_from_csv = pd.read_csv('data.csv')
        print(df_from_csv.head())