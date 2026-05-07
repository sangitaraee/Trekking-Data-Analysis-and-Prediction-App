import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import re

def clean_grade(x):
    if 'Easy To Moderate' in x or 'Easy-Moderate' in x or 'Light+Moderate' in x:
        return 'Easy to Moderate'
    if 'Light' in x or 'Easy' in x:
        return 'Easy'
    if 'Moderate' in x:
        return 'Moderate'
    return 'Hard'

def clean_best_time(time):
    time = time.replace('March - Nov', 'March - May & Sept - Nov')
    return time

def clean_travel_time(time):
    if pd.isnull(time):
        return None
    time = time.strip()  # Remove leading and trailing spaces
    time = time.replace('Setpt', 'Sept')  # Fix typo
    time = time.replace(' - ', '-')
    time = time.replace('.', '')
    time = time.replace('- ', '-')# Standardize hyphen usage
    time = re.sub(r'(\s+)', ' ', time)  # Remove extra spaces
    return time

# Mapping months to seasons
def map_season(time):
    if time in ['March-May', 'April-May', 'Jan-May']:
        return 'Spring'
    elif time == 'June-Aug':
        return 'Summer'
    elif time in ['Sept-Dec', 'Sept-Nov']:
        return 'Autumn'
    elif time in ['March-Nov']:
        return 
    elif time == 'Dec-Feb':
        return 'Winter'
    else:
        return None

# Function to clean trek names
def clean_trek_name(name):
    if pd.isnull(name):  # Handle NaN values
        return name
    name = name.strip()  # Remove leading/trailing whitespace
    name = name.replace('\xa0', ' ')  # Replace non-breaking spaces with regular spaces
    name = ' '.join(name.split())  # Remove extra spaces between words
    return name

    
# Function to clean accommodation values
def clean_accommodation(value):
    value = value.strip().lower()  # Normalize case and remove leading/trailing spaces
    if 'guesthouse' in value or 'guest houses' in value or 'guesthouses' in value:
        return 'Hotel/Guesthouse'
    elif 'luxury' in value:
        return 'Hotel/Luxury Lodge'
    elif 'teahouse' in value or 'teahouses' in value:
        return 'Hotel/Teahouse'
    elif 'lodges' in value or 'lodge' in value:
        return 'Hotel/Lodge'
    else:
        return value.capitalize() 

def load_data():
    df = pd.read_csv('Nepali_Treking_EnhancedV2.csv')
    columns = ['Unnamed: 0', 'Health Incidents','Equipment Used','GraduateOrNot','Employment Type','FrequentFlyer','Regional code','Country']
    df = df.drop(columns, axis =1)
    df.columns = df.columns.str.strip()
    # Clean 'Cost' column: remove any newline characters, convert it to numeric (remove "USD" text)
    df['Cost'] = df['Cost'].str.replace('\n', '').str.replace('USD', '').str.replace('$', '').str.replace(',', '').str.strip()
    df['Cost']=df['Cost'].astype(float)
    df['Max Altitude'] = df['Max Altitude'].str.replace('m', '').str.replace(',', '').str.strip()
    df['Max Altitude']=df['Max Altitude'].astype(int)
    df['Time'] = df['Time'].apply(lambda x: re.sub(r'\b[Dd]ays?\b', '', x)).astype(int)
    df['Trekking Group Size'].fillna(df['Trekking Group Size'].median(), inplace=True)
    df['Guide/No Guide'].fillna(df['Guide/No Guide'].mode(), inplace=True)
    df['Trekking Group Size']=df['Trekking Group Size'].astype(int)
    df['Review/Satisfaction'].fillna(df['Review/Satisfaction'].mean(), inplace=True)
    df['Best Travel Time'] = df['Best Travel Time'].apply(clean_best_time)
    df[['Travel Time 1', 'Travel Time 2']] = df['Best Travel Time'].str.split('&', expand=True)
    df['Travel Time 1'] = df['Travel Time 1'].apply(clean_travel_time)
    df['Travel Time 2'] = df['Travel Time 2'].apply(clean_travel_time)
    # Apply mapping to cleaned columns
    df['Travel Season 1'] = df['Travel Time 1'].apply(map_season)
    df['Travel Season 2'] = df['Travel Time 2'].apply(map_season)
    
    # Apply the cleaning function to the 'Trek' column
    df['Trek'] = df['Trek'].apply(clean_trek_name)
    df["Trip Grade"] = df['Trip Grade'].apply(clean_grade)
    df['Accomodation'] = df['Accomodation'].apply(clean_accommodation)

    return df

df = load_data()

def show_explore_page():
    st.title("Explore Nepal Trekking Data")
    st.write("This page allows you to explore the Nepal Trekking dataset.")

    data = df["Trek"].value_counts()
    top_treks = data.head(8)
    fig1, ax1 = plt.subplots()
    ax1.pie(top_treks, labels=top_treks.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Most visited treks  """)
    st.pyplot(fig1)

    st.markdown("<br><br>", unsafe_allow_html=True)


    st.title('Group Size vs Guide Usage')

    # Create a stacked bar chart using Plotly
    group_size_guide = df.groupby(['Trekking Group Size', 'Guide/No Guide']).size().reset_index(name='Count')
    fig_bar = px.bar(group_size_guide, x='Trekking Group Size', y='Count', color='Guide/No Guide', 
                    title='Group Size vs Guide Usage', barmode='stack', color_discrete_sequence=['#6CA0D5', '#FF7F9D'])

    # Display the stacked bar chart
    st.plotly_chart(fig_bar)

    st.write('Small and Large groups have the tendency to take guide unlike the average group sizes.')

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.write(
        """
    #### Mean Review/Satisfaction Based On Group Size
    """
    )

    data = df.groupby(["Trekking Group Size"])["Review/Satisfaction"].mean().sort_values(ascending=True)
    st.bar_chart(data)
    st.write("This suggests that larger groups have higher satisfactions than smaller groups.")
    st.markdown("<br><br>", unsafe_allow_html=True)



    st.write(
            """
        #### Average Satisfaction Based On Cost
        """
        )
    data = df.groupby(["Cost"])["Review/Satisfaction"].mean().sort_values(ascending=True)
    st.line_chart(data)


    