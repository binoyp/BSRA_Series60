import numpy as np
import pickle
import pandas as pd
from pathlib import Path
import os

class BsraHull(object):
    def __init__(self, cb=0.7, **kwargs):
        self.cb = cb
        self._load()


    
    def _load(self):
        if self.cb == 0.7:
            path = Path(os.path.dirname(__file__),'data', 'cb0p7.bin')
            with path.open(mode='rb') as f:
                data = pickle.load(f)
            
            self.sar = data['sar']
            self.offset = data['offset']
            self.maxbm = data['maxbm']

if __name__ =="__main__":
    h = BsraHull()
    print(h.offset[0.075])
