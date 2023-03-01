"""
Created on Wed Feb 15 14:43:00 2023
@author: arthurdiniz
"""
import holoviews as hv
import holoviews.operation.datashader as hd
import bokeh as bk
import rioxarray as rxr
import panel as pn
import numpy as np
import geopandas as gpd
import hvplot.pandas
import geoviews as gv


import matplotlib, matplotlib.pyplot, numpy as np
from custom_hoover import *



print('Versions: ', 
  {
  'holoviews': hv.__version__, 
  'bokeh': bk.__version__, 
  'rioxarray': rxr.__version__, 
  }
)



add_subestacao = '~/Dados/Subestacao/Subestações___Base_Existente.shp'
gdf_subestacao = gpd.read_file(add_subestacao)
hv_tiles_osm = hv.element.tiles.OSM()
print(gdf_subestacao)
hv_sub = gv.Points(gdf_subestacao.geometry).opts(tools=['hover'])
hv_combined_basic = hv_sub
#bokeh_server = pn.Row(radio_group,dmap).show()
pn.Row('SEDEC',hv_combined_basic).servable()
