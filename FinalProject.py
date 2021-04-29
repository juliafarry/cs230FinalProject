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
import pydeck as pdk

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
    print(f"This data set has {df.shape[0]} rows.")
    sample = df.sample(n=1000)
    sample['datetime'] = pd.to_datetime(sample['date'])
    sample['datetime'] = sample['datetime'].dt.month
    sample['datetime'] = pd.to_numeric(sample['datetime'])
    sample['datetimetime'] = pd.to_datetime(sample['time'])
    print(f"The sample data set has {sample.shape[0]} rows.")
    print(sample.info())
    return sample


def bar(data):
    dict = {"bronx": 0, "brooklyn": 0, "manhattan": 0, "queens": 0, "staten island": 0}
    st.subheader("**Bar Chart of Average People Killed in Vehicles From Each Borough**")
    # list of all boroughs
    # borough = ["bronx", "brooklyn", "manhattan", "queens", "staten island"]
    for i in dict.keys():
        temp = data[data['borough'] == i]
        dict[i] = temp['persons killed'].mean()
        print(dict)


def pie_chart(data):
    st.subheader("**Pie Chart of Vehicles Involved**")
    pass


def histogram_test(data):
    global MONTHS
    hist_data = pd.DataFrame()
    month_list = list(MONTHS.values())
    month_nums = list(MONTHS.keys())
    month = st.selectbox('Select Month', month_list)
    position = month_list.index(month)
    num = month_nums[position]
    st.markdown("### **Interactive Histogram**")
    hist_data = data[data['datetime'] == num]
    hist_title = f"Time of Day Histogram for the month of {month}"
    rist = hist_data['datetimetime'].dt.hour.tolist()
    arr = np.array(rist)
    print(arr)
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
    month_list = list(MONTHS.values())
    month_nums = list(MONTHS.keys())
    month = st.selectbox('Select Month', month_list)
    position = month_list.index(month)
    num = month_nums[position] - 1
    map_data = data[data['datetime'].dt.month == num]
    st.bar_chart(np.histogram(map_data[map_data['datetime'].dt.hour], bins=24, range=(0,24))[0])
    view_state = pdk.ViewState(latitude = 40.7128, longitude = 74.0060, zoom = 4)
    map = pdk.Deck(initial_view_state=view_state)
    st.pydeck_chart(map)


hide_streamlit_style = """
            <style>
            footer:after {
                content:'by https://gregoirejan.github.io / Using frost.met.no API';
                visibility: visible;
                display: block;
                position: relative;
                #background-color: red;
                padding: 5px;
                top: 2px;
            }
            </style>
            """


# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# st.title("Crashes in NYC")


# Function adds a title to the project and returns no value
def title():
    st.title("NYC Vehicle Crash Data")


def sidebar():
    st.sidebar.title("Selector")
    st.sidebar.selectbox("Select a chart type:", ("Bar Chart", "Pie Chart", "Histogram"))
    st.sidebar.radio("Person's affected", ("Injured", "Killed"))


def main():
    title()
    sidebar()
    df = load_data(FILE)
    if st.checkbox('View Raw Data?'):
        st.write(df)
    st.map(df)
    bar(df)
    pie_chart(df)
    histogram_test(df)


main()

