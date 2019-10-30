import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

app.config["JSON_SORT_KEYS"] = False

#home base routes
@app.route("/")
def index():
    return (
        f"Available Routes:<br>"
        f"-------------------------<br>"
        f"Precipitation for last year: /api/v1.0/precipitation<br/>"
        f"List of all stations: /api/v1.0/stations<br/>"
        f"Date and temperature observations from the last year: /api/v1.0/tobs<br/>"        
        f"Min, Avg, Max Temp given a start date up to most current date in db: /api/v1.0/2012-05-15<br/>"
        f"Min, Avg, Max Temp given a start and end date: /api/v1.0/2015-09-12/2015-09-13<br/>"
    )

# date routes
@app.route("/api/v1.0/precipitation")    
def precipitation():
    return (
        precip_stats = session.query(Measurement.date, Measurement.prcp)
        .order_by(Measurement.date)
    
        precip_data = []
    for r in precip_stats:
        precip_dict = {}
        precip_dict['date'] = r.date
        precip_dict['prcp'] = r.prcp)
       

    return jsonify(precip_data)

# station route
@app.route("/api/v1.0/stations")
def stations():
    return (
    station_data = session.query(Station.name, Measurement.station)\
    .group_by(Station.name).all()

    stations_data = []
    for r in station_data:
        stations_dict = {}
        stations_dict['name'] = r.name
        stations_dict['station'] = r.station)
        
    
    return jsonify(stations_data)

# temperature observations route
@app.route("/api/v1.0/tobs")
def tobs():
    return (
    tempobs = session.query(Measurement.date, Measurement.tobs)\
    .order_by(Measurement.date)

    tobs_data = []
    for r in tempobs:
        tobs_dict = {}
        tobs_dict['date'] = r.date
        tobs_dict['tobs'] = r.tobs)
    
    return jsonify(tobs_data)

# temperature stats with only start date route
@app.route("/api/v1.0/<start>")
def temp_stats_start(start):

    temperature_stats = session.query\
    (func.min(Measurement.tobs).label('min'),\
    func.avg(Measurement.tobs).label('avg'),\
    func.max(Measurement.tobs).label('max'))\
    
    start_stats_data = []
    for r in temp_stats_start:
        start_stats_dict = {}
        start_stats_dict['Start Date'] = start
        start_stats_dict['Min Temp'] = r.min
        start_stats_dict['Avg Temp'] = r.avg
        start_stats_dict['Max Temp'] = r.max
    
    return jsonify(start_stats_data)

# temperature stats with both start and end dates route
@app.route("/api/v1.0/<start>/<end>")
def temp_stats_start_end(start, end):
    return (

    temp_stats = session.query(func.min(Measurement.tobs).label('min'),\
    func.avg(Measurement.tobs).label('avg'),\
    func.max(Measurement.tobs).label('max'))\
   
    start_end_stats_data = []
    for r in temp_stats:
        start_end_stats_dict = {}
        start_end_stats_dict['Start Date'] = start
        start_end_stats_dict['End Date'] = end
        start_end_stats_dict['Min Temp'] = r.min
        start_end_stats_dict['Avg Temp'] = r.avg
        start_end_stats_dict['Max Temp'] = r.max)
        
    
    return jsonify(start_end_stats_data)

if __name__ == '__main__':
    app.run(debug=True)

