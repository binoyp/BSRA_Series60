import numpy as np
import pickle
import pandas as pd
from pathlib import Path
import os
import argparse
from PdGeom import PDGeometry, PDStripStation
import LewisFactors

_PATHDICT = {
        0.6: Path(os.path.dirname(__file__), 'data', 'cb0p6.bin'),
        0.65: Path(os.path.dirname(__file__), 'data', 'cb0p65.bin'),
        0.7: Path(os.path.dirname(__file__), 'data', 'cb0p7.bin'),
        0.8: Path(os.path.dirname(__file__), 'data', 'cb0p8.bin')
    }
    
class BsraHull(object):
    


    def __init__(self, cb=0.7, l=1, b=1, t=1):
        assert cb in [0.6, 0.65, 0.7, 0.75, 0.8]
        self.cb = cb
        self.length = l
        self.breadth = 1
        self.draft = 1
        self._load()

    def _load(self):
        
        path = _PATHDICT[self.cb]
        with path.open(mode='rb') as f:
            data = pickle.load(f)

        self.sar = data['sar']
        self.offset = data['offset']
        self.maxbm = data['maxbm']

    def GenerateHull(self):
        """Generate offset table as dictionary of station offsets

        Returns:
            dictionary -- {
                stationlocation[float] : numpy array
                                         [[y0, z0]
                                          [y1, z1]
                                          ...
                                          [yn, zn]] ,
                                          .....

            }
        """
        offsetdict = {}

        for stloc, row in self.offset.iterrows():
            z = row.keys().values * self.draft
            y = row.values * self.breadth
            offsetdict[stloc * self.length / 20.] = np.array([y, z]).T
        return offsetdict

    def GeneratePDStripGeometry(self, cog):
        """Generate PDStrip Geometry for the hull

        Arguments:
            cog {array / list} -- [xg, yg, zg]

        Returns:
            PDstrip Geometry object -- [description]
        """

        assert len(cog) == 3, "cog should be [xg, yg, zg]"
        xg = cog[0]
        yg = cog[1]
        zg = cog[2]
        pdg = PDGeometry()
        pdg.Sym = True
        count = 0
        underwateroff = self.offset[self.offset.columns[self.offset.columns <= 1.0]]
        for stloc, row in underwateroff.iterrows():
            pdstn = PDStripStation()
            if row.any():
                pdstn.Loc = (stloc * self.length / 20.) - xg
                z = row.keys().values * self.draft
                y = row.values * self.breadth
                pdstn.yarray = y - yg
                pdstn.zarray = z - zg
                pdstn.npts = len(y)
                pdg.Stations.append(pdstn)
                print(pdstn)
                count += 1

            else:
                print("Section at %0.3f dropped" % stloc)

        return PDGeometry


if __name__ == "__main__":
    h = BsraHull(0.8, l=20, t=10.5)
    print(h.GeneratePDStripGeometry([0,0,0]))
