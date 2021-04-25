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


df = pd.read_csv(file).lower()
# not sure about the .lower() but we need to make all the info not capitalized

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

# list of all vehicle types that were apart of a crash
vehicle_type = ["ambulance", "bicycle", "bus", "fire truck", "large com veh(6 or more tires)",
                "livery vehicle", "motorcycle", "other", "passenger vehicle", "pick-up truck",
                "small com veh(4 tires)", "sports utility/station wagon", "taxi", "unkown", "van"]

# list of all boroughs
borough = ["bronx", "brooklyn", "manhattan", "queens", "staten island"]

# pivot table that will compare the average people injured from each borough
pd.pivot_table(df, index=["Borough"], values=["Persons Injured"], aggfunc=[np.average], fill_value=0)


# histogram to see the number of crashes within a time frame
def histogram():
    st.markdown("### **Interactive Histogram**")
    st.sidebar.markdown("#### **Please select your upper and lower bound hour**")
    time_min = st.sidebar.slider("Lower Bound Hour:", 0, 0, 24, 1)
    time_max = st.sidebar.slider("Upper Bound Hour:", 0, 0, 24, 1)
    hourdf = file[(file.time >= time_min) & (file.time <= time_max)]
    count = hourdf['unique key'].count()
    max = file['unique key'].count()
    # pct = "Percentage of Crashes Between the Hours " + str(time_min) + " and " + str(time_max) + ": " + str(round(count/max * 100, 2)) + "%"
    percentage = str(round(count/max * 100, 2))
    hist_title = f"Percentage of Crashes Between the Hours {time_min} and {time_max}: {percentage}%"
    rist = file['time'].tolist()
    arr = np.array(rist)
    num = 24
    bins = list(range(num + 1))
    fig, ax = plt.subplots()
    N, bins, patches = ax.hist(arr, bins=bins, color='firebrick', EdgeColor='black')
    for i in range(time_min, time_max):
        patches[i].set_facecolor('midnightblue')
    plt.xlim(-1, 25)
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Crashes")
    plt.title(hist_title)
    st.pyplot(fig)

# chart looking at the number of people injured
# pie chart counting the type of vehicle or borough


# Function adds a title to the project and returns no value
def title():
    st.title("NYC Vehicle Crash Data")


def main():
    title()


main()
