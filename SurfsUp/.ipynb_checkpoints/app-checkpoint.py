# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import numpy as np
import datetime as dt

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Database Setup
#################################################

# Create an engine to the SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Routes
#################################################

# Define the homepage route
@app.route('/')
def welcome():
    return (
        "Welcome to the Climate API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation - Precipitation data for the last year<br/>"
        "/api/v1.0/stations - List of all stations<br/>"
        "/api/v1.0/tobs - Temperature observations for the most active station in the last year<br/>"
        "/api/v1.0/<start> - Temperature statistics from start date to the most recent date<br/>"
        "/api/v1.0/<start>/<end> - Temperature statistics from start date to end date<br/>"
    )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Get the most recent date from the dataset
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    
    # Calculate the date 12 months before the most recent date
    last_12_months = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Query for the precipitation data for the last 12 months
    precipitation_data = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= last_12_months).all()

    # Convert the query results to a dictionary with date as the key and precipitation as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_dict)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    stations = session.query(Station.station).all()

    # Convert the query results into a list
    station_list = [station[0] for station in stations]
    return jsonify(station_list)

# Define the temperature observations (tobs) route
@app.route("/api/v1.0/tobs")
def tobs():
    # Query to get the most recent date
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    
    # Calculate the last 12 months
    last_12_months = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    # Query to get the most active station
    most_active_station = session.query(Measurement.station)\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.station).desc())\
        .first()[0]

    # Query the dates and temperature observations for the most active station
    tobs_data = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active_station)\
        .filter(Measurement.date >= last_12_months).all()

    # Convert the query results into a list
    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in tobs_data]
    return jsonify(tobs_list)

# Define the start route for calculating min, avg, and max temperatures
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Query to calculate min, max, and avg temperatures for all dates >= start
    temperature_stats = session.query(func.min(Measurement.tobs),
                                      func.max(Measurement.tobs),
                                      func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start).all()

    # Convert the query results into a dictionary
    stats_dict = {"TMIN": temperature_stats[0][0], "TAVG": temperature_stats[0][2], "TMAX": temperature_stats[0][1]}
    return jsonify(stats_dict)

# Define the start-end route for calculating min, avg, and max temperatures
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Query to calculate min, max, and avg temperatures for dates between start and end
    temperature_stats = session.query(func.min(Measurement.tobs),
                                      func.max(Measurement.tobs),
                                      func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end).all()

    # Convert the query results into a dictionary
    stats_dict = {"TMIN": temperature_stats[0][0], "TAVG": temperature_stats[0][2], "TMAX": temperature_stats[0][1]}
    return jsonify(stats_dict)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
