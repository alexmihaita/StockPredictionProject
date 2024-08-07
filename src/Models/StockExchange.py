import os
import random
import pandas as pd
from Constants.ENUMS import PATHS
from datetime import datetime, timedelta
import numpy as np

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


class StockExchange():
    def __init__(self, name: str, csv_files: list):
        self.name = name
        self.csv_files = csv_files
        self.valid = True
        self.needed_csv = dict()
        self.needed_csv_data  = dict()
    
    
    def set_all_csv(self):
        try:
            company_dir = os.path.join(PATHS.CSV_DIR.value, self.name)
            if not self.valid:
                raise Exception("Stock exchange is not valid!")

            if len(self.csv_files) > 0:
                print("Already populated data")
                return
            
            csv_files = [f for f in os.listdir(company_dir) if f.endswith('.csv')]
            self.csv_files.extend([os.path.join(company_dir, f) for f in csv_files])

        except Exception as ex:
            print(f"Exception when trying to populate all_csv for the stock: {self.name}. Ex: {ex}")
            self.valid = False
            self.csv_files = []


    def populate_random_csv_data(self):
        try:
            if not self.valid:
                raise Exception("Stock exchange is not valid!")
            
            if len(self.needed_csv_data) > 0:
                print("Already populated data")
                return

            for file_name, file_path in self.needed_csv.items():
                print(f"Read the csv data for file: {file_name}")
                # Read the CSV file
                csv_data = pd.read_csv(file_path, header=None, names=["Name", "Timestamp", "Price"])
                csv_data["Timestamp"] = csv_data["Timestamp"].astype(str)
                
                # Convert Timestamp column to datetime format
                csv_data["Timestamp"] = csv_data["Timestamp"].apply(self.format_date_day_first)
                
                # Get a random timestamp from the Timestamp column
                random_timestamp = csv_data['Timestamp'].sample().values[0]
                
                # Generate new CSV with 10 rows starting from the random timestamp
                new_csv_data = csv_data[csv_data["Timestamp"] >= random_timestamp].head(10)

                # Save the new CSV in the modified directory
                self.needed_csv_data[file_name] = new_csv_data

        except Exception as ex:
            print(f"Exception when trying to generate data for the stock: {self.name}. Ex: {ex}")


    def format_date_day_first(self, date: str):
        # Handle different date formats
        try:
            # First, try parsing with dayfirst=True
                return pd.to_datetime(date, dayfirst=True, format="%d-%m-%Y")
        except ValueError:
            try:
                # If the first attempt fails, try the mixed format
                return pd.to_datetime(date, dayfirst=True)
            except ValueError:
                # If both attempts fail, raise an error
                raise ValueError(f"Date format not recognized: {date}")
        

    def apply_linear_regression(self):
        try:
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            modified_dir = os.path.join(PATHS.CSV_MODIFIED_DIR.value, self.name)
            if not os.path.exists(modified_dir):
                os.makedirs(modified_dir)
            
            for file_name, data in self.needed_csv_data.items():
                print(f"Predicting the next 3 values for {file_name}")
                min_timestamp = data['Timestamp'].min()
                data['TimeDelta'] = (data['Timestamp'] - min_timestamp).dt.days
                
                X = data[['TimeDelta']]
                y = data['Price']

                # Train Linear Regression model
                model = LinearRegression()
                model.fit(X, y)

                # Predict the next 3 values
                last_time_delta = data['TimeDelta'].max()
                future_time_deltas = pd.DataFrame({'TimeDelta': [last_time_delta + i for i in range(1, 4)]})
                predictions = model.predict(future_time_deltas)

                # Create the dataframe
                future_dates = [data['Timestamp'].max() + timedelta(days=i) for i in range(1, 4)]
                predictions_df = pd.DataFrame({
                    'Name': [data['Name'].iloc[0]] * 3,
                    'Timestamp': future_dates,
                    'Price': [round(price, 2) for price in predictions]
                })

                # Append predictions to the original data
                updated_data = pd.concat([data, predictions_df])
                updated_data['Timestamp'] = updated_data['Timestamp'].dt.strftime('%d/%m/%Y')
                updated_data.drop(columns=['TimeDelta'], inplace=True)
                # Update the dictionary with predictions
                self.needed_csv_data[file_name] = updated_data

                # Save the updated DataFrame to a new CSV
                self.needed_csv[file_name] = os.path.join(modified_dir, f"predicted_{current_time}_{file_name}")
                new_csv_path = self.needed_csv[file_name]
                updated_data.to_csv(new_csv_path, index=False)

                # Plot the timeseries
                plt.figure()
                plt.plot(updated_data['Timestamp'], updated_data['Price'])
                plt.title(os.path.basename(self.needed_csv[file_name]))
                plt.xlabel('Timestamp')
                plt.ylabel('Price')
                plt.show(block=False)

        except Exception as ex:
            print(f"Exception in linear regression for {self.name}. Ex: {ex}")


    def set_needed_csv(self, no_of_files: int):
        try:
            if not self.valid:
                raise Exception("Stock exchange is not valid!")

            if self.csv_files is None or len(self.csv_files) == 0:
                raise Exception("Train files are not populated yet!")

            if len(self.needed_csv) > 0:
                print("Already populated data")
                return

            if no_of_files < 1:
                raise ValueError("Number of files must be at least 1")

            available_files = len(self.csv_files)
            num_files_to_process = min(no_of_files, available_files)

            needed_csv = random.sample(self.csv_files, num_files_to_process)
            self.needed_csv = {os.path.basename(file): file for file in needed_csv}
        except Exception as ex:
            print(f"Exception when trying to populate needed csv for the stock: {self.name}. Ex: {ex}")
            self.valid = False
            self.needed_csv = dict()


    def __str__(self):
        csv_files_basename = [os.path.basename(file) for file in self.csv_files]
        needed_csv_values = [f"{key}={os.path.basename(value)}" for key, value in self.needed_csv.items()]
        return f"StockExchange(name={self.name}, original_csv_files={','.join(csv_files_basename)}, needed_csv_for_prediction={','.join(needed_csv_values)})"