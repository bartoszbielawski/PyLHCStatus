from datetime import datetime, timedelta

from flask import Flask, render_template
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_PATH
from pylhcstatus import PyLHCStatus, Base


def open_database():
    engine = create_engine(DB_PATH)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

@app.route('/')
def hello_world():
    return render_template("main.html")


@app.route("/stats/<int:hours>")
def stats(hours=24):
    delta = datetime.now() - timedelta(hours=hours)
    session = open_database()
    all_entries = session.query(PyLHCStatus).filter(PyLHCStatus.timestamp > delta).all()

    beam_modes = list(map(lambda x: x[0], session.query(PyLHCStatus.beam_mode).all()))

    from collections import Counter

    counter = Counter(beam_modes)
    return render_template("stats.html", hours=hours, counter=counter, total=len(beam_modes))


@app.route("/last/<int:number>")
def lastN(number):
    engine = create_engine(DB_PATH)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    all_records = session.query(PyLHCStatus).order_by(PyLHCStatus.timestamp.desc()).limit(number).all()

    return render_template("lastStates.html", entries=all_records)

if __name__ == '__main__':
    app.run()
