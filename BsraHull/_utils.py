import numpy as np 
from scipy import interpolate 

def _searchlist(arr,zval):
    for index, z in enumerate(arr):
        if z > zval:
            return index
        
    

def truncateList(_yarr, _zarr, zval):

    if  zval <= min(_zarr):
        print("draft :%f min z:%f max z:%f"%(zval, min(_zarr), max(_zarr)))
        return None, None
    if zval > max(_zarr):
        return _yarr, _zarr
    f = interpolate.interp1d(_zarr, _yarr)
    ind = _searchlist(_zarr, zval)

    outy = _yarr[:ind] + [float(f(zval))]
    outz = _zarr[:ind] + [zval]
    return outy, outz

if __name__ =="__main__":
    x = [v for v in range(50)]
    y = [v**2 for v in x]

    print(truncateList(x, y,1000))
    





