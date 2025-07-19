# Football Pass Map Visualizer with Streamlit

![Language](https://img.shields.io/badge/language-Python-3776AB?style=flat-square)
![Framework](https://img.shields.io/badge/framework-Streamlit-FF4B4B?style=flat-square)
![Domain](https://img.shields.io/badge/domain-Sports%20Analytics-orange?style=flat-square)

An interactive web app built with Python & Streamlit to visualize football passing networks from StatsBomb open data. The tool uses Matplotlib/mplsoccer to plot player positions and pass connections on a pitch.

## Table of Contents

- [About The Project](#about-the-project)
- [Live Demo](#live-demo)
- [Key Features](#key-features)
- [Built With](#built-with)
- [Getting Started](#getting-started)
- [Data Source](#data-source)
- [Future Improvements](#future-improvements)
- [License](#license)

## About The Project

This project is an interactive tool designed to visualize the passing exchanges of a football team, using open data from **StatsBomb**. The application provides an instant overview of a team's preferential circuits, player involvement, and key connections, making it a valuable tool for tactical analysis, scouting, or communication within a technical staff.

## Live Demo

The application is deployed on Render and can be accessed directly.

**👉 [Open the Live Application](https://pass-map-football.onrender.com/)**

*Note: The app is hosted on a free service and may take a few seconds to wake up if it has been idle.*

## Key Features

-   **Interactive Pass Map**: Visualizes passing exchanges with directional arrows.
-   **Average Player Positions**: Each player is placed on their average position on the pitch, calculated from their passing activity.
-   **Dynamic Threshold Filter**: A slider allows filtering passes by volume (e.g., "≥ 10 passes") to improve readability.
-   **Individual Player Analysis**: A dropdown menu to focus on a single player and view:
    -   Top 3 passing partners (sent & received).
    -   Total number of passes.
    -   Average pass distance.
-   **Multiple Analysis Modes**: View total exchanges, passes made, or passes received.

## Built With

-   **Python**
-   **Streamlit**
-   **Pandas** & **NumPy**
-   **Matplotlib** & **mplsoccer**

## Getting Started

To get a local copy up and running, follow these steps.

1.  **Prerequisites**: Ensure you have Python installed.
2.  **Clone the repository:**
    ```sh
    git clone https://github.com/nico916/pass-map-football.git
    ```
3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit app:**
    ```sh
    streamlit run app.py
    ```

## Data Source

The data is sourced from the **StatsBomb Open Data** repository. The `events.json` file used in this demo corresponds to the **FC Barcelona vs. Alavés** match from the 2017-2018 season. The data is used for non-commercial analysis purposes only, in accordance with StatsBomb's terms of use.

## Future Improvements

-   **Multi-Match Analysis**: Compare a player's performance across several matches.
-   **Opponent Display**: Add the ability to visualize the opponent's passing network.
-   **Time-Based Filtering**: Analyze passes by game period (e.g., 0-15', 15-30').
-   **Advanced Tactical Metrics**:
    -   Calculate pass network centrality.
    -   Detect switches of play.
    -   Analyze pass progressiveness.
-   **PDF/PNG Export**: Allow users to export the generated pass map for reports.
-   **Integrated AI Assistant**: A chatbot to answer natural language queries (e.g., "Who is the most central player?").

## License

Distributed under the MIT License. See `LICENSE` file for more information.
