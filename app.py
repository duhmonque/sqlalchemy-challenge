#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawwaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

#save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session link from python to DB
session = Session(engine)

#Flask setup
app = Flask(__name__)

#Flask Routes endpoints

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API! <br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>""
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Return the precipitation datat from last year
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    #Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).        filter(Measurement.date >= prev.year).all()
    precip = {date: prcp for data, prcp in precipitation}
    print(precipitation)
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start = None, end = None):
    sel = [func.min(Measurement.tobs), func.ave(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    temps = list(np.ravel(results))
    return jsonify(temps)


if __name__ == '__main__'
    app.run()


# In[ ]:




