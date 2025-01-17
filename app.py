import yfinance as yf
import pandas as pd

class DataDownloader:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date

    def download_data(self):
        # Append '.NS' for NSE stock symbols
        symbol_with_suffix = self.symbol + ".NS"
        data = yf.download(symbol_with_suffix, start=self.start_date, end=self.end_date)

        # Check if data is empty
        if data.empty:
            print(f"Warning: No data found for symbol {symbol_with_suffix} between {self.start_date} and {self.end_date}.")
            return None

        # Avoid printing unnecessary warnings for missing dates
        # Simply return the available data for the requested date range
        return data

class DataFeeder:
    def __init__(self, data, filename):
        self.data = data
        self.filename = filename

    def save_to_excel(self):
        if self.data is not None:
            with pd.ExcelWriter(self.filename, engine='openpyxl') as writer:
                self.data.to_excel(writer, sheet_name='Stock Data')
        else:
            print(f"No data to save for {self.filename}.")

class DataRetriever:
    def __init__(self, filename):
        self.filename = filename

    def retrieve_data(self):
        try:
            # Retrieve data from Excel file
            data = pd.read_excel(self.filename, sheet_name='Stock Data', index_col='Date')
            return data
        except Exception as e:
            print(f"Error retrieving data from {self.filename}: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Take input from user
    symbol = input("Enter the stock symbol (e.g., 'RELIANCE' for Reliance Industries): ").upper()
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    # 1. Download data using DataDownloader
    downloader = DataDownloader(symbol=symbol, start_date=start_date, end_date=end_date)
    stock_data = downloader.download_data()

    # If data exists, proceed to save it
    if stock_data is not None:
        # 2. Save data to Excel using DataFeeder
        feeder = DataFeeder(data=stock_data, filename=f'{symbol}_stock_data.xlsx')
        feeder.save_to_excel()

        # 3. Retrieve data from Excel using DataRetriever
        retriever = DataRetriever(filename=f'{symbol}_stock_data.xlsx')
        retrieved_data = retriever.retrieve_data()

        # Display retrieved data
        if retrieved_data is not None:
            print(f"\nRetrieved Data for {symbol}:")
            print(retrieved_data)
        else:
            print("No data was retrieved.")
    else:
        print("Unable to download data for the given stock symbol and date range.")
