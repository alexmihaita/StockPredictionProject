class StockPrediction():
    def __init__(self, model, data):
        self.model = model
        self.data = data

    
    def generate_test_train_data(self, test_size=0.2):
        X_train, X_test, y_train, y_test = train_test_split(self.data, self.data['Close'], test_size=test_size, random_state=42, shuffle=False)
        return X_train, X_test, y_train, y_test


    def predict(self):
        return self.model.predict(self.data)