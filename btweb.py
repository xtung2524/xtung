import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


# To set a webpage title, header and subtitle
st.set_page_config(page_title = "Movies analysis",layout = 'wide')
st.header("Interactive Dashboard")
st.subheader("Interact with this dashboard using the widgets on the sidebar")


# Read data in file:
movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/movies.csv")

movies_data.info()
movies_data.duplicated()
movies_data.count()
movies_data.dropna()


# Create sidebar
year_list = movies_data['year'].unique().tolist()
score_rating = movies_data['score'].unique().tolist()
genre_list = movies_data['genre'].unique().tolist()


# Add the filters.
with st.sidebar:
    st.write("Select a range on the slider (it represents movie score) to view the total number of movies in a genre that falls within that range ")
    # Create slider
    new_score_rating = st.slider(label = "Choose a value:",
                                  min_value = 1.0,
                                  max_value = 10.0,
                                 value = (3.0,4.0))


    st.write("Select your preferred genre(s) and year to view the movies released that year and on that genre")
    # Create genre option
    new_genre_list = st.multiselect('Choose Genre:',
                                        genre_list, default = ['Animation', 'Horror', 'Fantasy', 'Romance'])

    # Create year option
    year = st.selectbox('Choose a Year', year_list, 0)

# Configure the slider widget for interactivity
score_info = (movies_data['score'].between(*new_score_rating))



# Configure the selectbox and multiselect widget for interactivity
new_genre_year = (movies_data['genre'].isin(new_genre_list)) & (movies_data['year'] == year)


# Group the column
col1, col2 = st.columns([2,3])
with col1:
    st.write("""#### Lists of movies filtered by year and Genre """)
    dataframe_genre_year = movies_data[new_genre_year].groupby(['name', 'genre'])['year'].sum()
    dataframe_genre_year = dataframe_genre_year.reset_index()
    st.dataframe(dataframe_genre_year, width = 400)

with col2:
    st.write("""#### User score of movies and their genre """)
    rating_count_year = movies_data[score_info].groupby('genre')['score'].count()
    rating_count_year = rating_count_year.reset_index()
    figpx = px.line(rating_count_year, x = 'genre', y = 'score')
    st.plotly_chart(figpx)




 # Create bar graph
st.write("""
Average Movie Budget, Grouped by Genre
    """)
avg_budget = movies_data.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()
genre = avg_budget['genre']
avg_bud = avg_budget['budget']

fig = plt.figure(figsize = (19, 10))

plt.bar(genre, avg_bud, color = 'maroon')
plt.xlabel('genre')
plt.ylabel('budget')
plt.title('Matplotlib Bar Chart Showing The Average Budget of Movies in Each Genre')
st.pyplot(fig)