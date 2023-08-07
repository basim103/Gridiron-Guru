import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib as mpl
import matplotlib.pyplot as plt


# Load CSV
data = pd.read_csv("Passing.csv")  # Replace with the actual path to your downloaded dataset

#title
gg_title = st.title("Gridiron Guru")


# search bar
search_query = st.text_input("Search for a player:")

# Filter and display the player's stats
if search_query:
    player_stats = data[data['Player'].str.contains(search_query, case=False)]
    if not player_stats.empty:
        st.write(f"**{search_query} Stats**")
        st.write(player_stats)

        # Radar chart
        st.write(f"**QB Radar Chart**")

        players = player_stats['Player'].tolist()
        selected_players = st.multiselect("Select players for radar chart:", players, key="radar_players")

        if selected_players:
            # Select the statistics for the radar chart
            selected_stats = st.multiselect("Select statistics for radar chart:", player_stats.columns[5:], key="radar_stats")
            
            if selected_stats:
                selected_stats_names = [stat for stat in selected_stats]
                num_stats = len(selected_stats)
                angles = np.linspace(0, 2 * np.pi, num_stats, endpoint=False)
                angles = np.concatenate((angles, [angles[0]]))  # Close the shape

                fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'polar': True})
                ax.set_theta_offset(np.pi / 2)
                ax.set_theta_direction(-1)

                # Plot each player's radar chart
                for player in selected_players:
                    player_data = player_stats[player_stats['Player'] == player]
                    values = player_data[selected_stats].values.flatten()
                    values = np.concatenate((values, [values[0]]))  # Close the shape
                    ax.plot(angles, values, label=player)

                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(selected_stats_names)
                ax.legend(loc='upper right')

                st.pyplot(fig)
            else:
                st.write("Select at least one statistic.")

        # QBR pie chart
        qbr_stat = 'QBR'  # Replace with the actual column name for QBR in your dataset
        st.write(f"**{qbr_stat} Pie Chart**")
        
        # Create a list of players to choose from
        players = player_stats['Player'].tolist()
        player_stats[qbr_stat] = player_stats[qbr_stat].astype(float)  # Convert to float
        selected_players_qbr = st.multiselect("Select players:", players)

        if selected_players_qbr:
            qbr_percentages = player_stats[player_stats['Player'].isin(selected_players_qbr)][qbr_stat]
            labels = selected_players_qbr
            sizes = qbr_percentages

            plt.figure(figsize=(8, 8))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            st.pyplot(plt)
        else:
            st.write("Select at least one player.")
    else:
        st.write("Player not found.")
