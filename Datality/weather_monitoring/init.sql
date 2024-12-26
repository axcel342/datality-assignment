-- Create the weather measurements table
CREATE TABLE weather_measurements (
    time TIMESTAMPTZ NOT NULL,
    location_name TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    temperature DOUBLE PRECISION,
    feels_like DOUBLE PRECISION,
    humidity INTEGER,
    pressure INTEGER,
    wind_speed DOUBLE PRECISION,
    wind_direction INTEGER,
    clouds_coverage INTEGER,
    weather_condition TEXT,
    weather_description TEXT
);

-- Convert it to a hypertable
SELECT create_hypertable('weather_measurements', 'time');

-- Create indexes for common query patterns
CREATE INDEX idx_weather_location ON weather_measurements (location_name, time DESC);
CREATE INDEX idx_weather_temp ON weather_measurements (temperature, time DESC);