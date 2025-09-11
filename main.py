from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import pandas as pd
from prophet import Prophet
import threading, time, random

app = Flask(__name__)
app.secret_key = "IHYeFJdY0JooMNHuC0kk8bgmf2oNK60d"  # change this to something random & secure

# -------------------------
# Dummy credentials
# -------------------------
USERNAME = "admin"   # your login ID
PASSWORD = "1234"    # your login password

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

        # Simulate random vehicle positions around Delhi
        lat = 28.61 + random.uniform(-0.01, 0.01)
        lon = 77.21 + random.uniform(-0.01, 0.01)
        speed = random.randint(5, 60)

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

        time.sleep(0.5)  # faster simulation for testing

# Run live feed in background
threading.Thread(target=simulate_live_feed, daemon=True).start()

# -------------------------
# Authentication routes
# -------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid ID or Password")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# -------------------------
# Protected routes
# -------------------------
@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/about")
def about():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("about.html")

@app.route("/live")
def live():
    if "user" not in session:
        return redirect(url_for("login"))
    historical = live_data[-50:]
    vehicles = live_data[-10:]
    return jsonify({"historical": historical, "real_time": vehicles})

@app.route("/alerts")
def alerts():
    if "user" not in session:
        return redirect(url_for("login"))
    recent = live_data[-10:]
    alerts_list = []
    for point in recent:
        if point['congestion'] == "High":
            alerts_list.append({
                "type": "congestion",
                "message": f"High traffic at {point['time']}! Vehicle {point['vehicle_id']}"
            })
        if point['speed'] < 15:
            alerts_list.append({
                "type": "speed_alert",
                "message": f"Vehicle {point['vehicle_id']} moving very slowly at {point['time']}!"
            })
    return jsonify(alerts_list)

if __name__ == "__main__":
    app.run(debug=True)
