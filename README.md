# Stock Price Prediction

The project follows the assignment guidelines. It is a simple console application which creates a StockExchange 
object which has some implemented functionalities. 

## Description

The project is used for:
- Predicting stock prices for a random timestamp for all stock exchanges predfined in a local path. (repository -> original_data directory).
- Predicting stock prices for a specific stock exchange (given as an input) for a random timestamp.
- Exit the application.

1st API is defined in StockExchanges class -> populate_random_csv_data(self) -> it will populate a key-value variable (needed_csv_data) to hold the information about the company.csv, taking the data from the original csv, by selecting a random timestamp, and then retrieve first 10 dates after the random one.

2nd API is defined in StockExchanges class -> apply_linear_regression(self) -> it will take all the data populated in the key-value variable (needed_csv_data) and it will try to generate 3 predictions
For each company predictions, there will be a graph plotted to see the acutal timeseries

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/alexmihaita/StockPredictionProject.git
    ```
2. Navigate to the project directory:
    ```sh
    cd StockPredictionProject
    ```
3. Install the required dependencies:
    ```sh
	Solution was done with python 3.9. Any version >= with this one should work fine. (If you want to use dependencies only local, you may create a virtual env) 
    For virtual env: python -m .venv
    
    cd .venv/Scripts -> activate.bat

    pip install -r requirements.txt
    ```

## Usage

1. Run the main script:
    ```sh
    cd src
    python main.py
    ```
2. Follow the on-screen prompts:
    - Option `1`: Predict stock prices for all stock exchanges.
    - Option `2`: Predict stock prices for a specific stock exchange.
    - Option `0`: Exit the application.

## Observations

As the data provided is not that large, we cannot train a good model using RNNs, thus I chose a simple Linear Regression model.
We predict based on the TimeDelta (difference between first day and 10th day) and the Price. 