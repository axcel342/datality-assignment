import psycopg2
import pandas as pd
from groq import Groq


# Database connection
def get_weather_data():
    connection = psycopg2.connect(
        dbname="tsdb",
        user="tsdbadmin",
        password="x4gw2ogcfu0peh4w",
        host="tukgoycvpd.fgcmu7l9b7.tsdb.cloud.timescale.com",
        port="30397"
    )
    query = """
    SELECT city, AVG(temperature) AS avg_temp
    FROM weather
    WHERE time BETWEEN NOW() - INTERVAL '7 days' AND NOW()
    GROUP BY city;
    """
    data = pd.read_sql_query(query, connection)
    connection.close()

    print(data)
    return data

def generate_insights(data):


    client = Groq(
        api_key="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",
    )
    prompt = f"""Analyze the following weather data and summarize trends in 2 - 3 sentences for a dashboard.
    
     :\n{data.to_string(index=False)}"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def main():
    data = get_weather_data()
    insights = generate_insights(data)
    print("Generated Insights:")
    print(insights)

if __name__ == "__main__":
    main()
