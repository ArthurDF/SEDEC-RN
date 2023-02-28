# -*- coding: utf-8 -*-
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


import matplotlib, matplotlib.pyplot, numpy as np
from custom_hoover import *

cmap_terrain_top_75_percent =  [matplotlib.colors.rgb2hex(c) for c in matplotlib.pyplot.cm.terrain(np.linspace(0.25, 1, 192))]
print(cmap_terrain_top_75_percent)


print('Versions: ', 
  {
  'holoviews': hv.__version__, 
  'bokeh': bk.__version__, 
  'rioxarray': rxr.__version__, 
  }
)


# Some arbitrary sizes we will use to display images.
image_height, image_width = 600, 600

# Maps will have the same height, but they will be wider
map_height, map_width = image_height, 1000

# As we've seen, the coordinates in our dataset were called x and y, so we are 
# going to use these.
key_dimensions = ['x', 'y']

# We are also going to need the name of the value stored in the file. We get it 
# from there this time, but we could also set this manually.

value_dimension = 'adequabilidade'

hv.extension('bokeh', logo=False)
clipping = {'NaN': '#00000000'}

hv.opts.defaults(
  hv.opts.Image(cmap=cmap_terrain_top_75_percent,
                height=image_height, width=image_width, 
                colorbar=True, 
                tools=['hover'], active_tools=['wheel_zoom'], 
                clipping_colors=clipping),
  hv.opts.Tiles(active_tools=['wheel_zoom'], height=map_height, width=map_width)
)



add_subestacao = '~/Dados/Subestacao/Subestações___Base_Existente.shp'
gdf_subestacao = gpd.read_file(add_subestacao)
hv_tiles_osm = hv.element.tiles.OSM()
#hv_sub = gdf_subestacao.hvplot(geo=True, color='pink',label='Subestação Cenário Presente', muted_alpha=0)
hv_combined_basic = hv_tiles_osm
#bokeh_server = pn.Row(radio_group,dmap).show()
pn.Row('SEDEC',hv_combined_basic).servable()

