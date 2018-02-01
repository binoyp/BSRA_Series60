import numpy as np
import pickle
import pandas as pd
from pathlib import Path
import os
import argparse
# import PdGeom


class BsraHull(object):
    def __init__(self, cb=0.7, l=1, b=1, t=1):

        self.cb = cb
        self.length = l
        self.breadth = 1
        self.draft = 1
        self._load()

    def _load(self):
        if self.cb == 0.7:
            path = Path(os.path.dirname(__file__), 'data', 'cb0p7.bin')
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
            offsetdict[stloc * self.length /20.] = np.array([y, z]).T
        return offsetdict


if __name__ == "__main__":
    h = BsraHull(0.7, l = 2, t=1.5)
    print(h.GenerateHull())
