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
import numpy as np
import streamlit as st

file = "nyc_crash.csv"


def default_input(prompt, default_value):
    item = input(prompt + "[enter for " + default_value + "]: ").lower()
    if item == "":
        item = default_value
    return item


df = pd.read_csv(file)

print(f"This data set has {df.shape[0]} rows.")
size = default_input("Enter number of records to sample: ", "1000")
while True:
    try:
        size = int(size)
        break
    except:
        size = default_input("Please enter an integer: ", "1000")


sample = df.sample(n=size)
print(f"The sample data set has {sample.shape[0]} rows.")
print(df)


vehicle_type = ["Ambulance", "Bicycle", "Bus", "Fire Truck", "Large Com Veh(6 or more tires)",
                "Livery vehicle", "Motorcycle", "Other", "Passenger vehicle", "Pick-up truck",
                "Small com veh(4 tires)", "Sports utility/station wagon" ,"Taxi", "Unkown", "Van"]

borough = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]


pd.pivot_table(df,index=["Date", "Borough"], values=["Persons Injured"], aggfunc=[np.sum], fill_value=0)

