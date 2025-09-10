Smart Traffic Management System for Urban Congestion
Overview

The Smart Traffic Management System is a real-time web application that monitors, predicts, and optimizes urban traffic using AI and dynamic traffic signals. It helps city planners and commuters make informed decisions to reduce congestion, improve safety, and enhance traffic flow.

Features

Traffic Predictions: Uses AI models (Prophet) to predict traffic congestion for upcoming hours.

Dynamic Traffic Signals: Adjusts traffic light patterns in real-time based on traffic conditions.

Alerts & Notifications: Provides warnings for high congestion or slow-moving vehicles.

Real-time Dashboard: Visualizes traffic data and predictions with interactive charts and maps.

Tech Stack

Backend: Python, Flask

Frontend: HTML, TailwindCSS, JavaScript

Data & Analytics: Pandas, Prophet, Chart.js, Leaflet.js

Simulation: Generates real-time vehicle data for demonstration purposes

File Structure
├── main.py          # Flask application
├── DATAS.csv        # Traffic dataset
├── templates/
│   ├── index.html   # Homepage
│   ├── dashboard.html
│   └── about.html
├── static/
│   ├── images/      # Project images and logos
│   ├── css/         # Stylesheets
│   └── js/          # JavaScript files