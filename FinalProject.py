"""
CS230-SN6
Baxter Bishop and Julia Farry
data set = nyc_crash
description:
This program displays a wide variety of options of viewing New York City crash data.
Using various functions, we have created charts to display all crash locations on a map, a pivot table and bar chart
showing the number of injured people in crashes, and an interactive histogram to look at crash times each month.
We have also included a sidebar to make viewing the charts easier, as you can view each one individually.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pydeck as pdk
import seaborn as sb

FILE = "nyc_crash.csv"

MONTHS = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
          5: 'May', 6: 'June', 7: 'July', 8: 'August',
          9: 'September', 10: 'October', 11: 'November', 12: 'December'}


def default_input(prompt, default_value):
    item = input(prompt + "[enter for " + default_value + "]: ")
    try:
        item = item.lower()
    except:
        print("")
    if item == "":
        item = default_value
    return item


@st.cache(suppress_st_warning=True)
def load_data(file):
    df = pd.read_csv(file)
    lower_case = lambda x: str(x).lower()
    df.rename(lower_case, axis='columns', inplace=True)
    df = df.fillna(0)
    sample = df.sample(n=1000)
    sample['datetime'] = pd.to_datetime(sample['date'])
    sample['datetime'] = sample['datetime'].dt.month
    sample['datetime'] = pd.to_numeric(sample['datetime'])
    sample['datetimetime'] = pd.to_datetime(sample['time'])
    return sample


# bar chart taking the average people injured in each borough based on the pivot table
def bar(data):
    dict = {}
    st.subheader("**Pivot Table of Average Injuries Per Crash**")
    piv = pd.pivot_table(data, index=["borough"], values=["persons injured"], aggfunc=[np.average], fill_value=0)
    data = data[data['persons injured'] != 0]
    st.write(piv)
    st.subheader("**Bar Chart of People Injured in Accidents From Each Borough**\n")
    boroughs = ['BRONX', 'BROOKLYN','MANHATTAN', 'QUEENS', 'STATEN ISLAND']
    # st.bar_chart(boroughs, index=boroughs)
    print(type(data[data['borough'] == 'BRONX']))
    for i in boroughs:
        counter = len(data[data['borough'] == i])
        dict[i] = counter
    dictdf = pd.DataFrame(list(dict.items()), columns = ['boroughs', 'injuries']).set_index('boroughs')
    print(dictdf)
    st.bar_chart(dictdf)


# histogram examining the average time of day crashes occur each month over the years
def histogram_test(data):
    global MONTHS
    st.markdown("### **Interactive Histogram**")
    hist_data = pd.DataFrame()
    month_list = list(MONTHS.values())
    month_nums = list(MONTHS.keys())
    month = st.selectbox('Select Month', month_list)
    position = month_list.index(month)
    num = month_nums[position]
    hist_data = data[data['datetime'] == num]
    hist_title = f"Time of Day Histogram for the month of {month}"
    rist = hist_data['datetimetime'].dt.hour.tolist()
    arr = np.array(rist)
    num = 24
    bins = list(range(num + 1))
    fig, ax = plt.subplots()
    plt.hist(arr, bins=bins, color='red', edgecolor='black', align='mid')
    plt.xlim(-1, 25)
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Crashes")
    ax.set_xticks(np.arange(24))
    plt.title(hist_title)
    st.pyplot(fig)


def map(data):
    st.markdown("### **Map of Crashes in NYC**")
    loc = []
    for i in range(len(data)):
        loc.append([data[i][0], data[i][5], data[i][6]])
    nyc_map = pd.DataFrame(loc, columns=['Unique Key', 'Latitude', 'Longitude'])
    view_state = pdk.ViewState(latitude =40.7306, longitude = -73.9352, zoom = 4, min_zoom=1, max_zoom=20)
    layer = pdk.Layer('Scatterplotlayer', nyc_map, pickable=True, get_position=['Longitude', 'Latitude'], get_radius=5000, get_color=[0, 255, 255])
    nyc_map = pdk.Deck(map_style = 'light', initial_view_state=view_state, layers=[layer])
    st.pydeck_chart(nyc_map)


# Function adds a title to the project and returns no value
def title():
    st.title("NYC Vehicle Crash Data")


def main():
    title()
    df = load_data(FILE)
    st.sidebar.title("Selector")
    visualization = st.sidebar.selectbox("Select a chart type:", ("Select a Chart", "Bar Chart", "Histogram", "Map"))
    if visualization == "Bar Chart":
        bar(df)
    elif visualization == "Histogram":
        histogram_test(df)
    elif visualization == "Map":
        st.map(df)
    else:
        if st.checkbox('View Raw Data?'):
            st.write(df)
        histogram_test(df)
        st.map(df)
        bar(df)


main()

