# Covid Viz-Hub

According to WHO, as of December 2020, COVID-19 had infected over 82M people and killed more than 3M worldwide. 
The economic and social disruption caused by the pandemic is devastating: tens of millions of people are at risk of 
falling into extreme poverty, while the number of undernourished people are currently estimated at nearly 690 million. 
We need ways to help people assess the risks involved, and understand what is happening around them.

In this project, we built visual displays, which will help users gain the information needed to act, helping them take 
better, informed decisions. We have used the [COVID-19 data](https://github.com/CSSEGISandData/COVID-19) provided by 
__The Center for Systems Science and Engineering (CSSE) at JHU__, as well as the 
[COVID-19 Case Surveillance Public Use Data with Geography](https://data.cdc.gov/Case-Surveillance/COVID-19-Case-Surveillance-Public-Use-Data-with-Ge/n8mc-b4w4) 
provided by __CDC__. Dashboards have become the iconic interface through which we understand the coronavirus pandemic, 
and hence we have also built a dashboard using Plotly and Dash. The dataset itself is open for public use and holds 
information since 2019.

## Features
Here are some features of this implementation:
- Transparent: Shows the data being used.
- Developed an ETL pipeline to load data directly from the true source.
- A full-fledged dashboard built using Dash and Plotly for visual analytics.
- Implements various stages such as cleaning, transforming and integration.
- Uses SEIR to predict the trend based on factors like lockdown, vaccinations etc.
- Comparative Analysis on different levels: Global (Continent), US, and Individual.

## Problem Statements
<b><u>Global Level</u></b>
<ol>
    <li>Latest death count across continents</li>
    <li>Compare monthly deaths of countries</li>
    <li>Death count across months for different continents</li>
    <li>Spread of coronavirus across the world over the year?</li>
    <li>Trend of deaths across months for different continents</li>
    <li>Recovery rate of Coronavirus across the world over the year?</li>
</ol>
<b><u>US Level</u></b>
<ol>
    <li>Progress of covid deaths across states</li>
    <li>What was the situation in local hospitals like?</li>
    <li>Situation across different periods of the outbreak</li>
    <li>Which provinces accounted for the greatest number of deaths?</li>
    <li>Comparison between states based on percentage of deaths in each state?</li>
</ol>
<b><u>Individual Level</u></b>
<ol>
    <li>Which race has the most deaths?</li>
    <li>Which gender has the most deaths?</li>
    <li>Which age group has the most deaths?</li>
    <li>Was underlying condition a major factor in the deaths occurred?</li>
</ol>
<b><u>SEIR Model</u></b>
<ol>
    <li>Predict the trend based on factors like lockdown, vaccinations etc.</li>
</ol>

## Implementation
![High Level Design](Documents/HLD.png?raw=true "High Level Design")

## Folder Structure
    ├── backend                                 # Holds the backend code (ETL)
    │   ├── data                                    # Holds sample data for reference
    │   ├── functions.py                            # Holds various functions used for cleaning & transfomring the data
    │   └── main.py                                 # Entry point for the backed process; Run this to execute the end-to-end ETL piepleine
    ├── Documents                               # Holds info about the project
    ├── frontend                                # Holds the frontend code (Dash and Plotly)
    │   ├── apps                                    # Holds static files associated with the dashboard
    │   │   ├── __init__.py                             # Used to define as a package
    │   │   ├── global_layout.py                        # Layout for global page
    │   │   ├── home_layout.py                          # Layout for home page
    │   │   ├── individual_layout.py                    # Layout for individual page
    │   │   ├── SIERmodel_layout.py                     # Layout for SIER page
    │   │   └── us_layout.py                            # Llayout for US page
    │   ├── assets                                  # Holds the image files used in the dashboard UI
    │   ├── app.py                                  # Application file which defines the app settings
    │   └── index.py                                # Dash application which defines and triggers the endpoints; Entry point for the dashboard
    ├── README.md                               # Read this first
    └── requirements.py                         # Required packages to run the frontend and backend

## Output
A full video demo of the UI can be viewed in the [YouTube Video]() (redirects to YouTube).

## Screenshots
![Home Page](Documents/home.png?raw=true)
![Home Page](Documents/global_1.png?raw=true)
![Home Page](Documents/global_2.png?raw=true)
![Home Page](Documents/global_3.png?raw=true)
![Home Page](Documents/global_4.png?raw=true)
![Home Page](Documents/us_1.png?raw=true)
![Home Page](Documents/us_2.png?raw=true)
![Home Page](Documents/us_3.png?raw=true)
![Home Page](Documents/us_4.png?raw=true)
![Home Page](Documents/individual.png?raw=true)
![Home Page](Documents/seir_1.png?raw=true)
![Home Page](Documents/seir_2.png?raw=true)

## Contributors
- [Jacob Celestine](https://jacobcelestine.com/)
- [Nisha Kumari](https://github.com/nishabbsr)
- [Sihao Sun](https://github.com/sihaosunru)
