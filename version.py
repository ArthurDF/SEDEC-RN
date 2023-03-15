import panel as pn
import holoviews as hv
from holoviews import streams
import param
import spatialpandas as spd
import geopandas as gpd
import rioxarray as rxr
import numpy as np
import hvplot.pandas
import holoviews.operation.datashader as hd
import bokeh as bk
import hvplot as hvp
import matplotlib as mp
import datashader as ds
import cartopy as cp
import geoviews as gv
import pyproj as pp

print('Versions: ', 
  {
  'holoviews': hv.__version__, 
  'bokeh': bk.__version__,
  'rioxarray': rxr.__version__, 
  'panel': pn.__version__,
  'numpy':np.__version__,
  'geopandas':gpd.__version__,
  'hvplot':hvp.__version__,
  'matplotlib':mp.__version__,
  'datashader':ds.__version__,
  'cartopy':cp.__version__,
  'geoviews':gv.__version__,
  'pyproj':pp.__version__,
  'spatialpandas': spd.__version__,
  
  }
)
