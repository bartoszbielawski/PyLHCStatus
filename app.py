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


beam_mode_order = ["NO BEAM",
                   "SETUP",
                   "INJECTION PROBE BEAM",
                   "INJECTION PHYSICS BEAM",
                   "PREPARE RAMP",
                   "RAMP",
                   "FLAT TOP",
                   "ADJUST",
                   "SQUEEZE",
                   "STABLE BEAMS",
                   "RAMP DOWN",
                   "CYCLING"];


@app.route("/stats/<int:hours>")
def stats(hours=24):
    delta = datetime.now() - timedelta(hours=hours)
    print(delta)
    session = open_database()
    beam_modes = list(map(lambda x: x[0], session.query(PyLHCStatus.beam_mode).filter(PyLHCStatus.timestamp > delta).all()))

    from collections import Counter, OrderedDict
    counter = Counter(beam_modes)
    orderedCounter = OrderedDict()

    for beam_mode in beam_mode_order:
        orderedCounter[beam_mode] = counter.get(beam_mode, 0)

    return render_template("stats.html", hours=hours, counter=orderedCounter, total=len(beam_modes))


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
