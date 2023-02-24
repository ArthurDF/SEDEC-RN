# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:43:00 2023

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
'''
hv.opts.defaults(
  hv.opts.Image(cmap=cmap_terrain_top_75_percent,
                height=image_height, width=image_width, 
                colorbar=True, 
                tools=['hover'], active_tools=['wheel_zoom'], 
                clipping_colors=clipping),
  hv.opts.Tiles(active_tools=['wheel_zoom'], height=map_height, width=map_width)
)
'''
#custom_hover = custom_hoover()

#@pn.depends(a=widget)

def mute_hook(plot, element):
    plot.handles["glyph_renderer"].muted = False

def mute_hook2(plot, element):
    plot.handles["glyph_renderer"].muted = True
    
def custom_map(desired_shape, **kwargs):  
    
    # display graph in browser
    # a bokeh server is automatically started
    
    custom_hover = custom_hoover()
    dataarray = rxr.open_rasterio('C:\\Arthur\\CDEC\\Parte 2\\Dados\\Mapa Adequabilidade\\mapa_adequabilidade_cenario_presente.tif')
        
    #dataarray = dataarray.rio.write_crs("EPSG:4326")
    dataarray = dataarray.rio.reproject("EPSG:3857")
    
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
        
        
    # if hv.Image() is not willing to display your own data due to sampling issues, 
    # try setting the rtol parameter to allow some deviations in sampling like:
    # hv.Image(hv_dataset, rtol=1)
    hv_image_basic = hv.Image(hv_dataset).opts(title='first image',tools=[custom_hover])
    
    
    # display graph in browser
    # a bokeh server is automatically started
    
    hv_tiles_osm = hv.element.tiles.OSM()
    rest_add = 'C:\\Arthur\\CDEC\\Parte 2\\Dados\\restrições\\restrições.shp'
    gdf_rest = gpd.read_file(rest_add)
    hv_rest = gdf_rest.hvplot(geo=True, color='red',label='Restrições', muted_alpha=0).opts(muted=False)
    
    parques_add = 'C:\\Arthur\\CDEC\\Parte 2\\Dados\\Centroide dos parques\\CENTROIDE_DOS_PARQUES.shp'
    gdf_parques = gpd.read_file(parques_add)
    hv_parques = gdf_parques.hvplot(geo=True, color='yellow',label='Parques Eólicos', muted_alpha=0,line_width=2.0).opts(hooks=[mute_hook])
    
    if desired_shape=='Presente':
         
        shape_add = 'C:\\Arthur\\CDEC\\Parte 2\\Dados\\Rotas\\presente\\presente.shp'
        gdf = gpd.read_file(shape_add)
        
        
        add_subestacao = 'C:\\Arthur\\CDEC\\Parte 2\\Dados\\Subestacao\\Subestações___Base_Existente.shp'
        gdf_subestacao = gpd.read_file(add_subestacao)
        
        hv_rotas = gdf.hvplot(geo=True, color='orange',label='Rotas Cenário Presente', muted_alpha=0,line_width=2.0).opts(muted=True)
        hv_sub = gdf_subestacao.hvplot(geo=True, color='pink',label='Subestação Cenário Presente', muted_alpha=0).opts(hooks=[mute_hook])
        hv_combined_basic = hv_tiles_osm * hv_rest * hv_image_basic * hv_parques * hv_sub * hv_rotas
        #hv_combined_basic.opts(legend_muted=True)
    if desired_shape == 'Futuro':
        
        
        shape_add = 'C:\\Arthur\\CDEC\\Parte 2\\Dados\\Rotas\\futuro\\futuro.shp'
        gdf = gpd.read_file(shape_add)
        
        
        add_subestacao = 'C:\\Arthur\\CDEC\\Parte 2\\Dados\\Subestacao\\Subestações___planejado.shp'
        gdf_subestacao = gpd.read_file(add_subestacao)
        
        hv_rotas = gdf.hvplot(geo=True, color='green',label='Rotas Cenário Futuro', muted_alpha=0,line_width=2.0).opts(muted=True)
        hv_sub = gdf_subestacao.hvplot(geo=True, color='purple',label='Subestação Cenário Futuro', muted_alpha=0).opts(hooks=[mute_hook2])
        hv_combined_basic = hv_tiles_osm * hv_image_basic * hv_parques * hv_rest * hv_sub * hv_rotas
        #hv_combined_basic.opts(legend_muted=False)
        
        
    
    
    #hv_combined_basic.opts(show_legend=False)
    return hv_combined_basic

radio_group = pn.widgets.RadioBoxGroup(name='RadioBoxGroup', options=['Presente', 'Futuro'], inline=True)

dmap = hv.DynamicMap(pn.bind(custom_map, desired_shape=radio_group))

bokeh_server = pn.Row(radio_group,dmap).show()