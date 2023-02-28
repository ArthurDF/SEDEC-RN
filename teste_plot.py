# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 11:59:44 2023

@author: ranierelima
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

dataarray = rxr.open_rasterio('C:\\Arthur\\CDEC\\Parte 2\\Dados\\Mapa Adequabilidade\\mapa_adequabilidade_cenario_presente.tif')

#dataarray = dataarray.rio.write_crs("EPSG:4326")
dataarray = dataarray.rio.reproject("EPSG:3857")
dataarray

dataarray = dataarray.where(dataarray!=-9999)
dataarray.values[dataarray.values==9999999]=np.nan

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

hv_dataset = hv.Dataset(dataarray[0], vdims=value_dimension, kdims=key_dimensions)
hv_dataset.data



custom_hover = custom_hoover()
# if hv.Image() is not willing to display your own data due to sampling issues, 
# try setting the rtol parameter to allow some deviations in sampling like:
# hv.Image(hv_dataset, rtol=1)
hv_image_basic = hv.Image(hv_dataset).opts(title='first image',tools=[custom_hover])

# display graph in browser
# a bokeh server is automatically started

hv_tiles_osm = hv.element.tiles.OSM()


shape_add = 'C:\\Arthur\\CDEC\\Parte 2\\Dados\\Rotas\\rotas_0.shp'
gdf = gpd.read_file(shape_add)

add_subestacao = 'C:\\Arthur\\CDEC\\Parte 2\\Dados\\Subestacao\\Subestações___Base_Existente.shp'
gdf_subestacao = gpd.read_file(add_subestacao)
#polys = gdf.hvplot(geo=True, hover_cols=['continent'], legend=True)

radio_group = pn.widgets.RadioBoxGroup(name='RadioBoxGroup', options=['Shape_1', 'Shape_2', 'Shape_3'], inline=True)

hv_combined_basic = hv_tiles_osm * hv_image_basic * gdf.hvplot(geo=True, color='purple')* gdf_subestacao.hvplot(geo=True, color='blue')




bokeh_server = pn.Row(radio_group,hv_combined_basic).show()
#%%
# stop the bokeh server (when needed)
#bokeh_server.stop()

