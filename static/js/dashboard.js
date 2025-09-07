// ===========================
// Chart.js - Live Traffic Line Chart
// ===========================
const trafficCtx = document.getElementById('trafficChart').getContext('2d');
const trafficChart = new Chart(trafficCtx, {
    type: 'line',
    data: { labels: [], datasets: [
        { label: 'Actual Traffic', data: [], borderColor: 'blue', fill: false, pointBackgroundColor: [] },
        { label: 'Predicted Traffic', data: [], borderColor: 'red', fill: false }
    ]},
    options: {
        responsive: true,
        scales: { 
            x: { title: { display: true, text: 'Time' } }, 
            y: { title: { display: true, text: 'Traffic Volume' } } 
        }
    }
});

// ===========================
// Chart.js - Historical Traffic Bar Chart
// ===========================
const histCtx = document.getElementById('historicalChart').getContext('2d');
const historicalChart = new Chart(histCtx, {
    type: 'bar',
    data: { labels: [], datasets: [{ label: 'Average Traffic per Hour', data: [], backgroundColor: 'teal' }]},
    options: { responsive: true, scales: { x: { title: { display: true, text: 'Hour' } }, y: { title: { display: true, text: 'Avg Traffic' } } } }
});

// ===========================
// Leaflet Map - Real-Time Vehicle Positions
// ===========================
const map = L.map('map').setView([28.61, 77.21], 13); // center at Delhi
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let vehicleMarkers = [];

// ===========================
// Update Live Data from Flask
// ===========================
async function updateLiveData() {
    try {
        const res = await fetch('/live');
        const data = await res.json();
        const hist = data.historical;

        // ---- Update Summary Cards ----
        const latest = hist[hist.length-1];
        document.getElementById('currentTraffic').innerText = "Current Traffic: " + latest.actual;
        document.getElementById('predictedTraffic').innerText = "Predicted Traffic: " + latest.predicted;
        document.getElementById('congestionLevel').innerText = "Congestion: " + latest.congestion;
        document.getElementById('peakHour').innerText = "Peak Hour: --"; // optional: calculate from historical

        // ---- Update Traffic Chart ----
        trafficChart.data.labels = hist.map(d => d.time);
        trafficChart.data.datasets[0].data = hist.map(d => d.actual);
        trafficChart.data.datasets[1].data = hist.map(d => d.predicted);
        trafficChart.data.datasets[0].pointBackgroundColor = hist.map(d => {
            if(d.congestion==="High") return 'red';
            else if(d.congestion==="Medium") return 'orange';
            else return 'green';
        });
        trafficChart.update();

        // ---- Traffic Light Indicators ----
        document.getElementById('red').style.background = (latest.congestion==="High") ? 'red' : 'grey';
        document.getElementById('yellow').style.background = (latest.congestion==="Medium") ? 'yellow' : 'grey';
        document.getElementById('green').style.background = (latest.congestion==="Low") ? 'green' : 'grey';

        // ---- Alert Banner ----
        document.getElementById('alert').innerText = (latest.congestion==="High") ? "High congestion! Consider alternate routes." : "";

        // ---- Vehicle Map Markers ----
        vehicleMarkers.forEach(m => map.removeLayer(m));
        vehicleMarkers = [];
        data.real_time.forEach(v => {
            const marker = L.circleMarker([v.lat, v.lon], { radius:6, color:'green', fillColor:'green', fillOpacity:0.8 })
                            .addTo(map)
                            .bindPopup(`Vehicle: ${v.vehicle_id}<br>Speed: ${v.speed} km/h`);
            vehicleMarkers.push(marker);
        });

        // ---- Historical Bar Chart ----
        const hours = hist.map(d => new Date(d.time).getHours());
        const hourMap = {};
        hours.forEach((h,i) => { hourMap[h] = (hourMap[h]||[]).concat(hist[i].actual); });
        const labels = Object.keys(hourMap);
        const avgTraffic = labels.map(h => (hourMap[h].reduce((a,b)=>a+b,0)/hourMap[h].length).toFixed(2));
        historicalChart.data.labels = labels;
        historicalChart.data.datasets[0].data = avgTraffic;
        historicalChart.update();

    } catch(err) {
        console.error('Error fetching live data:', err);
    }
}

// ===========================
// Refresh every 2 seconds
// ===========================
setInterval(updateLiveData, 2000);
updateLiveData(); // initial load
