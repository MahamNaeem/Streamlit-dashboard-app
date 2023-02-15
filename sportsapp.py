import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

#creating header of the file 

st.title("OLYMPIC HISTORY DASHBOARD")
st.subheader("created by Maham Naeem")

#READING CSV FILE 

data =  pd.read_csv("athlete_events.csv")
dc = pd.read_csv("noc_regions.csv")

#Performing EDA"""
#cleaning out the data
empty_value = data.isna().sum()
print(empty_value)

#"""we can see that height and age have null values, and medals are representing those,
#athlets which hasn't receieve any medal,so taking out the mean of those values and
#will replace in original data"""

data["Age"].fillna((data["Age"].mean()),inplace = True)
data["Height"].fillna((data["Height"].mean()), inplace= True)
data["Weight"].fillna((data["Weight"].mean()), inplace= True)
data["Medal"].fillna("Others", inplace = True)

print(data)

#lets check the shape of the data
print(data.shape)



#"""lets start our analysis"""

#merging our two data sets

final_data = data.merge(dc, how = "left", on = "NOC" )
print(final_data)
print(final_data.shape)
print(final_data.describe());
print(final_data["Medal"])

#renaming the coloumns so we can use it according to
final_data.rename(columns={"region": "Region", "notes":'Notes'}, inplace = True)
print(final_data.head(5))


# Filter the data by country

def app():
    #all_countries = (final_data["Team"])
    country = st.selectbox("SELECT COUNTRY", final_data["Region"].unique())
    #selected_country = st.selectbox("Select a country", countries)
    show_metrics(country)
        

    
def show_metrics(country):
    
    # Calculate the medal count for each type
    gold_count = len(final_data[(final_data["Team"] == country) & (final_data["Medal"] == "Gold")])
    silver_count = len(final_data[(final_data["Team"] == country) & (final_data["Medal"] == "Silver")])
    bronze_count = len(final_data[(final_data["Team"] == country) & (final_data["Medal"] == "Bronze")])
    total_count = gold_count + silver_count + bronze_count

# Display the metrics in a single row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Medal Count", total_count)
    with col2:
        st.metric("Gold Medals", gold_count)
    with col3:
        st.metric("Silver Medals", silver_count)
    with col4:
        st.metric("Bronze Medals", bronze_count)

if __name__ == "__main__":
    app()
    
#########################################################    

#creating first row with three columns:
    
with st.container():
    left, mid, right = st.columns(3)

# Filter the data by medal type
gold_data = final_data[final_data["Medal"] == "Gold"]
silver_data = final_data[final_data["Medal"] == "Silver"]
bronze_data = final_data[final_data["Medal"] == "Bronze"]

# Group the data by year and count the number of medals
gold_counts = gold_data.groupby("Year")["Medal"].count()
silver_counts = silver_data.groupby("Year")["Medal"].count()
bronze_counts = bronze_data.groupby("Year")["Medal"].count()

# Create the line chart
plt.plot(gold_counts.index, gold_counts.values, label="G")
plt.plot(silver_counts.index, silver_counts.values, label="S")
plt.plot(bronze_counts.index, bronze_counts.values, label="B")

# Set the chart title and labels
plt.title("Number of Medals Over the Years")
plt.xlabel("Year")
plt.ylabel("Number of Medals")

# Show the legend
plt.legend()
    
# Display the chart
left.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)

# Group data by athlete and count medals
athlete_medals = final_data.groupby('ID')['Medal'].count()

# Sort by most medals and select top 5
top_athletes = athlete_medals.sort_values(ascending=False)[:5]

mid.bar_chart(top_athletes)

# Group the data by Sport and Athlete, and count the number of medals for each group
grouped = final_data.groupby(["Sport", "ID"]).size().reset_index(name="Medals")

# Sort the data by the number of medals, in descending order
sorted_data = grouped.sort_values(by=["Medals", "ID"], ascending=[False, True])

# Get the top 5 athletes for each sport
top_athletes = sorted_data.groupby("Sport").head(5)

# Display the data as a highlight table
right.write(top_athletes.style.highlight_max(color="lightgreen"))

###################################################


with st.container():
   col1, col2, col3 = st.columns(3)

fig, ax = plt.subplots()
ax.hist(final_data["Age"], bins=10, color='orange', edgecolor='black')

# Set chart title and axis labels
ax.set_title("Number of Medals over Age Histogram Chart (10-Year Bins)")
ax.set_xlabel("Age (Years)")
ax.set_ylabel("Number of Medals")

# Display the chart on the Streamlit app
col1.pyplot(fig)   

# Group data by gender and count number of medals
medals_by_gender = final_data.groupby("Sex")["Medal"].count()

# Create pie chart
fig, ax = plt.subplots()
ax.pie(medals_by_gender.values, labels=medals_by_gender.index, autopct="%1.1f%%", startangle=90)

# Add chart title and axes labels
ax.set_title("Medals by Gender")
ax.set_aspect("equal")

# Display chart in Streamlit app
col2.pyplot(fig)


# Group the data by season and count the number of medals
season_medals = final_data.groupby('Season')['Medal'].count()

# Create a vertical bar chart using matplotlib
fig, ax = plt.subplots()
ax.bar(season_medals.index, season_medals.values, color=["yellow", "maroon"])

# Set chart title and axis labels
ax.set_title('Number of Medals Received in Each Season')
ax.set_xlabel('Season')
ax.set_ylabel('Number of Medals')

# Display the chart using Streamlit
col3.pyplot(fig)

###########################################