import argparse
import os

from Constants.ENUMS import PATHS, TYPE_OF_DATA
from Models.StockExchange import StockExchange
from Models.StockPrediction import StockPrediction


ORIGINAL_CSV_DIR = PATHS.CSV_DIR.value
MODIFIED_CSV_DIR = PATHS.CSV_MODIFIED_DIR.value


def parse_arguments():
    parser = argparse.ArgumentParser(description="Stock Prediction App")
    parser.add_argument('-se', type=str, action='append', required=True, help='Stock exchange name(s)')
    parser.add_argument('-nf', type=int, default=1, help='Number of files (default: 1)')
    
    args = parser.parse_args()

    print(f"Arguments: {args}")
    
    return args


def generate_all_predictions(no_of_files: int = 1) -> list[StockExchange]:
    stock_exchanges = []
    root_dir = ORIGINAL_CSV_DIR

    if not os.path.exists(root_dir) and not os.path.isdir(root_dir):
        raise Exception(f"Directory {root_dir} does not exist. Exiting...")

    for dir_name in os.listdir(root_dir):
        try:
            print(f"Creating work object for stock exchange: {dir_name}")
            stock_exchange = StockExchange(dir_name, [])
            stock_exchange.set_all_csv()
            stock_exchange.set_needed_csv(no_of_files)
            stock_exchange.populate_random_csv_data()
            stock_exchange.apply_linear_regression()
            stock_exchanges.append(stock_exchange)
        except Exception as ex:
            print(f"Exception when trying to create data for {dir_name}. Ex: {ex}")

    if len(stock_exchanges) > 0:
        for stock in stock_exchanges:
            print(f"*** CREATED: {stock} ***")

    if len(stock_exchanges) == 0:
        raise Exception("No stock exchanges were created. Exiting...")
    
    return stock_exchanges


def generate_prediction(stock_exchange_name: str, no_of_files: int = 1) -> StockExchange:
    stock_exchange = StockExchange(stock_exchange_name, [])
    stock_exchange.set_all_csv()
    stock_exchange.set_needed_csv(no_of_files)
    stock_exchange.populate_random_csv_data()
    stock_exchange.apply_linear_regression()
    if not stock_exchange.valid:
        print(f"Failed to create stock exchange {stock_exchange_name}. Exiting...")
    return stock_exchange


def create_train_files(available_stocks: list[StockExchange]):
    for stock in available_stocks:
        try:
            print(f"Creating data for stock: {stock.name}")
            stock.set_all_csv()
        except Exception as ex:
            print(f"Exception when trying to create data for {stock.name}. Ex: {ex}")


if __name__ == "__main__":
        print("Hello to Stock Prediction app! We will be using Linear Regression to predict the stock prices.")

        while True:
            try:
                print(f"Predicted CSVs will be saved under {MODIFIED_CSV_DIR}.")
                print("Please select an option:")
                print(f"1. Predict for all stock exchanges from {ORIGINAL_CSV_DIR}")
                print(f"2. Predict for a specific stock exchange from {ORIGINAL_CSV_DIR}")
                print("0. Exit")
                option = input("Enter your choice (1, 2, 0): ")

                if option == "1":
                    print(f"We will take each all stock exchanges from {ORIGINAL_CSV_DIR}, take a random timestamp and predict the stock prices for the next 3 days.")
                    no_of_companies = int(input("Enter the number of companies to predict for each stock exchange: "))
                    available_stocks = generate_all_predictions(no_of_companies)
                elif option == "2":
                    print(f"We will take the mentioned stock exchange from {ORIGINAL_CSV_DIR}, take a random timestamp and predict the stock prices for the next 3 days.")
                    stock_exchange_name = input("Enter the name of the stock exchange to predict: ")
                    no_of_companies = int(input("Enter the number of companies to predict for each stock exchange: "))
                    if no_of_companies < 1 or no_of_companies > 2:
                        raise ValueError("Number of companies must be at least 1 and at most 2")
                    available_stocks = generate_prediction(stock_exchange_name, no_of_companies)
                elif option == "0":
                    print("Exiting...")
                    exit(0)
                else:
                    print("Invalid option. Please try again.")

            except Exception as ex:
                print(f"Exception when trying to create data for training. Ex: {ex}")