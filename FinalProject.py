"""
At least one function that has two parameters and returns a value
At least one function that does not return a value
Interacting with dictionaries, lists, and tuples
Using a Python module to calculate a statistical function such as average, median, mode, etc.
User Interface and dashboard with Streamlit.io

at least 3 pandas capabilities:
Sorting data in ascending or descending order, multi-column sorting
Filtering data by one or more conditions
Analyzing data with pivot tables
Managing rows or columns
Add/drop/select/create new/group columns, frequency count, other features as you wish

"""
import pandas as pd
import matplotlib.pyplot as plt

file = input("Enter the file: ")
file = "nyc_crash.csv"

read = pd.read_csv(file)
print(f"This data set has {df.shape[0]} rows.")
print("hello")
