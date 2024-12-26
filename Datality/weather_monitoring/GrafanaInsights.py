from flask import Flask, jsonify
import psycopg2
from groq import Groq

# Initialize Flask App
app = Flask(__name__)

# Database Connection Settings
DB_SETTINGS = {
    "dbname": "tsdb",
    "user": "tsdbadmin",
    "password": "x4gw2ogcfu0peh4w",
    "host": "tukgoycvpd.fgcmu7l9b7.tsdb.cloud.timescale.com",
    "port": 30397
}



# Function to Fetch Weather Data
def fetch_weather_data(city):
    query = """
    SELECT distinct time, rain, wind_speed, pressure, temperature, forecast, city, condition_main
    FROM weather
    WHERE city = %s 
    AND time >= date_trunc('day', now())::timestamptz 
    AND time <= date_trunc('day', now())::timestamptz + INTERVAL '2 days'
    AND forecast = '*'
    ORDER BY time asc
    """
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cursor = conn.cursor()
        cursor.execute(query, (city,))
        data = cursor.fetchall()
        conn.close()

        # Format data into a dictionary
        return [
            {
                "date": row[0],
                "rainfall": row[1],
                "wind_speed": row[2],
                "pressure": row[3],
                "temperature": row[4],
                "condition": row[7],
            }
            for row in data
        ]
    except Exception as e:
        print("Database error:", e)
        return []

# Function to Generate Predictions
def generate_impact_prediction(weather_data):
    rules = []
    for record in weather_data:
        impacts = []
        if record["rainfall"] > 10:
            impacts.append("waterlogging or traffic delays")
        if record["wind_speed"] > 30:
            impacts.append("risks to outdoor items or lightweight vehicles")
        if record["temperature"] > 40:
            impacts.append("health risks like heatstroke") 
        if record["condition"] == 'Smoke':
            impacts.append("breathing related health risks") 
        
        # Create a summary rule if applicable
        if impacts:
            rules.append(
                f"On {record['date']}, {', '.join(impacts)} are expected in the city."
            )

    if not rules:
        return "No significant impacts are predicted based on current weather data."

    # Use OpenAI GPT to generate natural language predictions
    prompt = "Convert the following rules into user-friendly impact predictions:\n" + "\n".join(rules)
    try:
        client = Groq(
        api_key="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",
        )
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You generate weather impact predictions."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("OpenAI error:", e)
        return "Error generating predictions."

# API Route
# @app.route('/impact_predictions/<city>', methods=['GET'])
def impact_predictions(city = 'Lahore'):
    weather_data = fetch_weather_data(city)
    predictions = generate_impact_prediction(weather_data)
    return {"city": city, "predictions": predictions}

# Run Flask App
if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=6000)
    print(impact_predictions()['predictions'])

