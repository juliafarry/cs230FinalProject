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
    sample = df.sample(n=250)
    sample['datetime'] = pd.to_datetime(sample['date'])
    sample['datetime'] = sample['datetime'].dt.month
    print(sample['datetime'])
    sample['datetimetime'] = pd.to_datetime(sample['time'])
    print(f"The sample data set has {sample.shape[0]} rows.")
    print(sample.info())
    return sample


# list of all vehicle types that were apart of a crash
vehicle_type = ["AMBULANCE", "BICYCLE", "BUS", "FIRE TRUCK", "LARGE COM VEH(6 OR MORE TIRES)",
                "LIVERY VEHICLE", "MOTORCYCLE", "OTHER", "PASSENGER VEHICLE", "PICK-UP TRUCK",
                "SMALL COM VEH(4 TIRES)", "SPORTS UTILITY/STATION WAGON", "TAXI", "UNKOWN", "VAN"]
# list of all boroughs
borough = ["BRONX", "BROOKLYN", "MANHATTAN", "QUEENS", "STATEN ISLAND"]
# list of all potential factors that could have caused the vehicles to crash
vehicle_factor = ["ACCELERATOR DEFECTIVE" "AGGRESSIVE DRIVING/ROAD RAGE", "ALCOHOL INVOLVEMENT", "ANIMALS ACTION",
                  "BACKING UNSAFELY", "BRAKES DEFECTIVE", "CELL PHONE (HAND-HELD)", "DRIVER INATTENTION/DISTRACTION",
                  "DRIVER INEXPERIENCE", "DRUGS (ILLEGAL)", "FAILURE TO KEEP RIGHT", "FAILURE TO YIELD RIGHT-OF-WAY",
                  "FATIGUED/DROWSY", "FELL ASLEEP", "FOLLOWING TOO CLOSELY", "GLARE", "ILLNESS", "LOST CONSCIOUSNESS",
                  "OBSTRUCTION/DEBRIS", "OTHER ELECTRONIC DEVICE", "OTHER VEHICULAR", "OUTSIDE CAR DISTRACTION",
                  "OVERSIZED VEHICLE", "PASSENGER DISTRACTION", "PASSING OR LANE USAGE IMPROPER", "PAVEMENT DEFECTIVE",
                  "PAVEMENT SLIPPERY", "PEDESTRIAN/BICYCLIST/OTHER PEDESTRIAN ERROR/CONFUSION", "PHYSICAL DISABILITY",
                  "PRESCRIPTION MEDICATION", "REACTION TO OTHER UNINVOLVED VEHICLE", "STEERING FAILURE",
                  "TIRE FAILURE/INADEQUATE",
                  "TRAFFIC CONTROL DEVICE IMPROPER/NON-WORKING", "TRAFFIC CONTROL DEVICE IMPROPER/NON-WORKING",
                  "TURNING IMPROPERLY", "UNSAFE LANE CHANGING", "UNSAFE SPEED", "UNSPECIFIED",
                  "VIEW OBSTRUCTED/LIMITED",
                  ]


def histogram_test(data):
    global MONTHS
    month_list = list(MONTHS.values())
    month_nums = list(MONTHS.keys())
    month = st.selectbox('Select Month', month_list)
    position = month_list.index(month)
    num = month_nums[position] - 1
    st.markdown("### **Interactive Histogram**")
    hist_data = data[data['datetime'].dt.month == num]
    hist_title = f"Time of Day Histogram for the month of {month}"
    test = hist_data[hist_data['datetime'] == num]
    rist = hist_data['datetimetime'].tolist()
    arr = np.array(rist)
    num = 24
    bins = 24
    fig, ax = plt.subplots()
    N, bins, patches = ax.hist(arr, bins=bins, color='firebrick', edgecolor='black')
    plt.xlim(-1, 25)
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Crashes")
    plt.title(hist_title)
    st.bar_chart(np.histogram(hist_data['datetimetime'].dt.hour, bins=24, range=(0,24))[0])


def map(data):
    month_list = list(MONTHS.values())
    month_nums = list(MONTHS.keys())
    month = st.selectbox('Select Month', month_list)
    position = month_list.index(month)
    num = month_nums[position] - 1
    map_data = data[data['datetime'].dt.month == num]
    st.bar_chart(np.histogram(map_data[map_data['datetime'].dt.hour], bins=24, range=(0,24))[0])
    view_state = pdk.ViewState(latitude = 40.7128, longitude = 74.0060)
    map = pdk.Deck(initial_view_state=view_state)
    st.pydeck_chart(map)
    # st.pyplot(fig)
    print("hello")

# histogram to see the number of crashes within a time frame
def histogram(file):
    hour = st.slider('Select Hour',0,0,23,1)
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


# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# st.title("Crashes in NYC")


# Function adds a title to the project and returns no value
def title():
    st.title("NYC Vehicle Crash Data")


sidebar_title = st.sidebar.title("Selector")
visualization = st.sidebar.selectbox("Select a chart type:", ("Bar Chart", "Pie Chart", "Histogram"))
injuries = st.sidebar.radio("Person's affected", ("Injured", "Killed"))


def main():
    title()
    print('Hello')
    df = load_data(FILE)
    if st.checkbox('View Raw Data?'):
        st.write(df)
    histogram_test(df)
    # pd.pivot_table(df, index=["BOROUGH"], values=["PERSONS INJURED"], aggfunc=[np.average], fill_value=0)
    st.map(df)


main()

