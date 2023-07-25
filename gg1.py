import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
    st.title("Quarterback Radar Graph")
    st.write("Upload a CSV file with QB data to visualize it as a radar graph.")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.write(data)

        st.write("Radar Graph:")
        radar_graph = create_radar_graph(data)
        st.plotly_chart(radar_graph)

if __name__ == "__main__":
    main()

