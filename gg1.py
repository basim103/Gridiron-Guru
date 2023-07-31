import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from urllib.request import urlopen
from bs4 import BeautifulSoup


# URL of page
url = 'https://www.pro-football-reference.com/years/2022/passing.htm'

import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup

def scrape_data(url):
    # Open URL and pass to BeautifulSoup
    html = urlopen(url)
    stats_page = BeautifulSoup(html, 'html.parser')  # Specify the parser type (e.g., 'html.parser')

    # Collect table headers
    column_headers = stats_page.findAll('tr')[0]
    column_headers = [i.getText() for i in column_headers.findAll('th')]

    # Collect table rows
    rows = stats_page.findAll('tr')[1:]

    # Get stats from each row
    qb_stats = []
    for i in range(len(rows)):
        qb_stats.append([col.getText() for col in rows[i].findAll('td')])

    # Create DataFrame from our scraped data
    data = pd.DataFrame(qb_stats, columns=column_headers[1:])

    # Rename sack yards column to `Yds_Sack`
    new_columns = data.columns.values
    new_columns[-6] = 'Yds_Sack'
    data.columns = new_columns

    # Select stat categories
    categories = ['Cmp%', 'Yds', 'TD', 'Int', 'Y/A', 'Rate']

    # Create data subset for radar chart
    data_radar = data[['Player', 'Tm'] + categories]

    # Convert data to numerical values
    for i in categories:
        data_radar[i] = pd.to_numeric(data_radar[i])

    # Remove ornamental characters for achievements
    data_radar['Player'] = data_radar['Player'].str.replace('*', '')
    data_radar['Player'] = data_radar['Player'].str.replace('+', '')

    return data_radar

# Rename sack yards column to `Yds_Sack`
new_columns = data.columns.values
new_columns[-6] = 'Yds_Sack'
data.columns = new_columns

# Select stat categories
categories = ['Cmp%', 'Yds', 'TD', 'Int', 'Y/A', 'Rate']

# Create data subset for radar chart
data_radar = data[['Player', 'Tm'] + categories]
data_radar.head()

# Convert data to numerical values
for i in categories:
    data_radar[i] = pd.to_numeric(data_radar[i])

# Remove ornamental characters for achievements
data_radar['Player'] = data_radar['Player'].str.replace('*', '')
data_radar['Player'] = data_radar['Player'].str.replace('+', '')

# Calculate angles for radar chart
offset = np.pi/6
angles = np.linspace(0, 2*np.pi, len(categories) + 1) + offset

def create_radar_chart(ax, angles, player_data, color='blue'):
    
    # Plot data and fill with team color
    ax.plot(angles, np.append(player_data[-(len(angles)-1):], player_data[-(len(angles)-1)]), color=color, linewidth=2)
    ax.fill(angles, np.append(player_data[-(len(angles)-1):], player_data[-(len(angles)-1)]), color=color, alpha=0.2)
    
    # Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    
    # Remove radial labels
    ax.set_yticklabels([])

    # Add player name
    ax.text(np.pi/2, 1.7, player_data[0], ha='center', va='center', size=18, color=color)
    
    # Use white grid
    ax.grid(color='white', linewidth=1.5)

    # Set axis limits
    ax.set(xlim=(0, 2*np.pi), ylim=(0, 1))

    return ax

def get_qb_data(data, team):
    return np.asarray(data[data['Tm'] == team])[0]


def create_radar_graph(data):
    categories = data.columns[1:]
    values = data.values.tolist()[0][1:]
    values += values[:1]  # To close the loop of the radar graph

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(values)])
        ),
        showlegend=False
    )

    return fig

def main():
    st.title('Quarterback Radar Chart')

    # Scrape data from the URL
    url = 'https://www.pro-football-reference.com/years/2022/passing.htm'
    data_radar = scrape_data(url)

    # Create a dropdown to select the team
    teams = data_radar['Tm'].unique()
    selected_team = st.selectbox('Select Team', teams)

    # Display the radar chart for the selected team
    player_data = get_qb_data(data_radar, selected_team)
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    create_radar_chart(ax, angles, player_data)
    st.pyplot(fig)

if __name__ == "__main__":
    main()

