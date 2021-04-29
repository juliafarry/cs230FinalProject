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


# bar chart taking the average people killed in each borough
def bar(data):
    dict = {"bronx": 0, "brooklyn": 0, "manhattan": 0, "queens": 0, "staten island": 0}
    st.subheader("**Bar Chart of Average People Killed in Vehicles From Each Borough**")
    # list of all boroughs
    borough = np.array["bronx", "brooklyn", "manhattan", "queens", "staten island"]
    chart_data = pd.DataFrame()
    chart_data['borough'] = borough
    chart_data['persons injured'] = persons_injured.mean()
    chart_v1 = alt.Chart(chart_data).mark_bar().encode(
        x='boroughs',
        y='persons injured')
    st.write("", "", chart_v1)
    # st.bar_chart(borough)
    # for i in dict.keys():
    #     temp = data[data['borough'] == i]
    #     dict[i] = temp['persons killed'].mean()
    #     print(dict)


# line chart of the number of vehicles involved in the crash
def line_chart(data):
    st.subheader("**Line Chart of Vehicles Involved**")
    line_data = pd.DataFrame()

    pass


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
    # hist = np.histogram(hist_data['datetimetime'].dt.hour, bins=24, range=(0,24))[0]
    # st.bar_chart(np.histogram(hist_data['datetimetime'].dt.hour, bins=24, range=(0,24))[0])


def map(data):
    st.markdown("### **Map of Crashes in NYC**")
    loc = []
    for i in range(len(data)):
        loc.append([data[i][0]], data[i][5], data[i][6])
    nyc_map = pd.DataFrame(loc, columns=['Unique Key', 'Latitude', 'Longitude'])
    view_state = pdk.ViewState(latitude =nyc_map['Latitude'].mean(), longitude = nyc_map['longitude'].mean(), zoom = 4, min_zoom=1, max_zoom=20)
    layer = pdk.Layer('Scatterplotlayer', nyc_map, pickable=True, get_position=['Longitude', 'Latitude'], get_radius=5000, get_color=[0, 255, 255])
    nyc_map = pdk.Deck(map_style = 'light', initial_view_state=view_state, layers=[layer])
    st.pydeck_chart(nyc_map)


# histogram to see the number of crashes within a time frame
def histogram(file):
    hour = st.slider('Select Hour',0,0, 23,1)
    st.markdown("### **Interactive Histogram**")
    st.sidebar.markdown("#### **Please select your upper and lower bound hours**")
    time_min = st.sidebar.slider("Lower Bound Hour:", 0, 0, 24, 1)
    time_max = st.sidebar.slider("Upper Bound Hour:", 0, 0, 24, 1)
    hourdf = file[(file.time >= time_min) & (file.time <= time_max)]
    count = hourdf['unique key'].count()
    max = file['unique key'].max()
    percentage = str(round(count / max * 100, 2))
    hist_title = f"Percentage of Crashes Between the Hours {time_min} and {time_max} ({percentage}%)"
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


# Function adds a title to the project and returns no value
def title():
    st.title("NYC Vehicle Crash Data")


def sidebar():
    st.sidebar.title("Selector")
    st.sidebar.slider("Set city zoom", 0, 5, 10)
    # st.sidebar.selectbox("Select a chart type:", ("Bar Chart", "Pie Chart", "Histogram"))
    # st.sidebar.radio("Person's affected", ("Injured", "Killed"))


def main():
    title()
    sidebar()
    df = load_data(FILE)
    if st.checkbox('View Raw Data?'):
        st.write(df)
    histogram_test(df)
    stuff = pd.pivot_table(df, index=["borough"], values=["persons injured"], aggfunc=[np.average], fill_value=0)
    st.map(df)
    st.write(stuff)
    # bar(df)
    # line_chart(df)
    histogram_test(df)


main()