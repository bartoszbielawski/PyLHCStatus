from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_PATH
from pylhcstatus import PyLHCStatus, Base
import datetime

import urllib.request
import xml.etree.ElementTree as ET


def main():
    try:
        contents = urllib.request.urlopen("http://alicedcs.web.cern.ch/AliceDCS/monitoring/screenshots/rss.xml").read()
    except urllib.error.HTTPError as http_error:
        return

    lhc_state_dict = {}
    root = ET.fromstring(contents)
    for entry in root.iterfind("channel/item/title"):
        name, value = entry.text.split(":", 1)
        lhc_state_dict[name.strip()] = value.strip()

    engine = create_engine(DB_PATH)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    beam_energy = int(lhc_state_dict["BeamEnergy"].split()[0])
    beam_mode = lhc_state_dict["LhcBeamMode"]
    machine_mode = lhc_state_dict["LhcMachineMode"]
    comment = lhc_state_dict["LhcPage1"]

    new_state = PyLHCStatus(beam_energy=beam_energy,
                            beam_mode=beam_mode,
                            machine_mode=machine_mode,
                            comment=comment,
                            timestamp=datetime.datetime.now())
    session.add(new_state)
    session.commit()

if __name__ == "__main__":
    main()

