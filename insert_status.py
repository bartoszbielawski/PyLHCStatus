from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pylhcstatus import PyLHCStatus, Base
import datetime

import urllib.request
import xml.etree.ElementTree as ET

contents = urllib.request.urlopen("http://alicedcs.web.cern.ch/AliceDCS/monitoring/screenshots/rss.xml").read()


lhcStateDict = {}
root = ET.fromstring(contents)
for entry in root.iterfind("channel/item/title"):
    name, value = entry.text.split(":", 2)
    lhcStateDict[name.strip()] = value.strip()

engine = create_engine('sqlite:///pylhcstatus.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

beamEnergy = int(lhcStateDict["BeamEnergy"].split()[0])
beamMode = lhcStateDict["LhcBeamMode"]
machineMode = lhcStateDict["LhcMachineMode"]
comment = lhcStateDict["LhcPage1"]

new_state = PyLHCStatus(beam_energy=beamEnergy,
                      beam_mode=beamMode,
                      machine_mode=machineMode,
                      comment=comment,
                      timestamp=datetime.datetime.now())
session.add(new_state)
session.commit()

# last24h = datetime.datetime.now() - datetime.timedelta(minutes=3)
#
# print(session.query(LHCStatus).filter(LHCStatus.timestamp < last24h).all())
