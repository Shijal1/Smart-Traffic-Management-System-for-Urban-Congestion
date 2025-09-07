from flask import Flask, render_template, jsonify
import pandas as pd
from prophet import Prophet
import threading, time, random

app = Flask(__name__)

# -------------------------
# Load and prepare dataset
# -------------------------
df = pd.read_csv("DATAS.csv")
df['date_time'] = pd.to_datetime(df['date_time'])
df = df[['date_time', 'traffic_volume']]
df_prophet = df.rename(columns={'date_time': 'ds', 'traffic_volume': 'y'})

# Train Prophet model
model = Prophet()
model.fit(df_prophet)
future = model.make_future_dataframe(periods=24, freq='h')
forecast = model.predict(future)

# -------------------------
# Simulated live traffic feed
# -------------------------
live_data = []

def simulate_live_feed():
    for _, row in df.iterrows():
        current_time = row['date_time']
        actual_traffic = row['traffic_volume']

        # Predicted traffic
        pred_row = forecast[forecast['ds'] == current_time]
        predicted_traffic = pred_row['yhat'].values[0] if not pred_row.empty else None

        # Congestion level
        congestion = "Low"
        if actual_traffic > 5000:
            congestion = "High"
        elif actual_traffic > 3000:
            congestion = "Medium"

        # Simulate random vehicle positions around Delhi (28.61, 77.21)
        lat = 28.61 + random.uniform(-0.01, 0.01)
        lon = 77.21 + random.uniform(-0.01, 0.01)
        speed = random.randint(20, 60)

        live_data.append({
            "time": str(current_time),
            "actual": int(actual_traffic),
            "predicted": round(predicted_traffic, 2) if predicted_traffic else None,
            "congestion": congestion,
            "lat": lat,
            "lon": lon,
            "vehicle_id": f"V{len(live_data) + 1}",
            "speed": speed
        })

        time.sleep(1)  # simulate live stream delay

# Run live feed in background
threading.Thread(target=simulate_live_feed, daemon=True).start()

# -------------------------
# Flask routes
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/live")
def live():
    # Send latest 50 points as "historical"
    historical = live_data[-50:]
    # Send latest 10 vehicles as "real-time"
    vehicles = live_data[-10:]

    return jsonify({
        "historical": historical,
        "real_time": vehicles
    })

if __name__ == "__main__":
    app.run(debug=True)
