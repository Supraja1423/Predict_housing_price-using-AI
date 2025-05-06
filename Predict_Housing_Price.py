# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import tkinter as tk
from tkinter import messagebox

# Sample dataset with updated prices for Indian market in lakhs
data = {
    'Location': ['Downtown', 'Suburb', 'Rural', 'Urban', 'Coastal'],
    'Size (sqft)': [1200, 1800, 2400, 1500, 2000],
    'Bedrooms': [3, 4, 5, 3, 4],
    'Bathrooms': [2, 3, 3, 2, 2],
    'Age (years)': [10, 5, 15, 7, 8],
    'Price (Lakhs)': [30, 40, 25, 35, 45]  # Prices adjusted for India in lakhs
}

# Convert to DataFrame
df = pd.DataFrame(data)

# One-hot encode 'Location'
df = pd.get_dummies(df, columns=['Location'], drop_first=True)

# Separate features and target
X = df.drop('Price (Lakhs)', axis=1)
y = df['Price (Lakhs)']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"MAE: {mae}, RMSE: {rmse}")

# GUI Prediction Function
def predict_price():
    try:
        location = location_entry.get()
        size = float(size_entry.get())
        bedrooms = int(bedrooms_entry.get())
        bathrooms = int(bathrooms_entry.get())
        age = int(age_entry.get())

        if location not in ['Downtown', 'Suburb', 'Rural', 'Urban', 'Coastal']:
            raise ValueError("Invalid location. Choose from: Downtown, Suburb, Rural, Urban, Coastal.")

        input_data = pd.DataFrame({
            'Size (sqft)': [size],
            'Bedrooms': [bedrooms],
            'Bathrooms': [bathrooms],
            'Age (years)': [age],
            'Location_Coastal': [1 if location == 'Coastal' else 0],
            'Location_Rural': [1 if location == 'Rural' else 0],
            'Location_Suburb': [1 if location == 'Suburb' else 0],
            'Location_Urban': [1 if location == 'Urban' else 0]
        })

        input_data = input_data.reindex(columns=X.columns, fill_value=0)
        prediction_lakhs = model.predict(input_data)[0]

        result_label.config(text=f"Predicted Price: ₹{prediction_lakhs * 100000:,.2f}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("House Price Prediction (INR)")

# Entry fields
location_var = tk.StringVar()
size_var = tk.StringVar()
bedrooms_var = tk.StringVar()
bathrooms_var = tk.StringVar()
age_var = tk.StringVar()

tk.Label(root, text="Location (Downtown/Suburb/Rural/Urban/Coastal):").grid(row=0, column=0, padx=10, pady=5)
location_entry = tk.Entry(root, textvariable=location_var)
location_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Size (sqft):").grid(row=1, column=0, padx=10, pady=5)
size_entry = tk.Entry(root, textvariable=size_var)
size_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Bedrooms:").grid(row=2, column=0, padx=10, pady=5)
bedrooms_entry = tk.Entry(root, textvariable=bedrooms_var)
bedrooms_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Bathrooms:").grid(row=3, column=0, padx=10, pady=5)
bathrooms_entry = tk.Entry(root, textvariable=bathrooms_var)
bathrooms_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Age (years):").grid(row=4, column=0, padx=10, pady=5)
age_entry = tk.Entry(root, textvariable=age_var)
age_entry.grid(row=4, column=1, padx=10, pady=5)

# Predict button
predict_button = tk.Button(root, text="Predict", command=predict_price)
predict_button.grid(row=5, column=0, columnspan=2, pady=10)

# Result label
result_label = tk.Label(root, text="")
result_label.grid(row=6, column=0, columnspan=2, pady=10)

# Run app
root.mainloop()