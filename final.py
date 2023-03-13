# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 15:21:17 2023

@author: ranierelima
"""

import panel as pn
import numpy as np
import holoviews as hv
from holoviews import streams
import param
import math
import spatialpandas as spd
import geopandas as gpd
from custom_hoover import *


hv.extension('bokeh')
pn.extension(sizing_mode = 'stretch_width')

bootstrap = pn.template.BootstrapTemplate(title='Visualizador de Mapa')

xs = np.linspace(0, np.pi)
freq = pn.widgets.FloatSlider(name="Frequency", start=0, end=10, value=2)
phase = pn.widgets.FloatSlider(name="Phase", start=0, end=np.pi)

radio_box = pn.widgets.RadioBoxGroup(name='RadioBoxGroup', options=['Presente', 'Futuro'])




class AppTest(param.Parameterized):
    '''
    add_linha = 'C:\\Arthur\\CDEC\\Parte 2\\Dados\\Rotas\\presente\\presente.shp'
    add_rest = 'C:\\Arthur\\CDEC\\Parte 2\\Dados\\restrições\\restrições.shp'
    parques_add = 'C:\\Arthur\\CDEC\\Parte 2\\Dados\\Centroide dos parques\\CENTROIDE_DOS_PARQUES.shp'
    rotas_presente_add = 'C:\\Arthur\\CDEC\\Parte 2\\Dados\\Rotas\\presente\\presente.shp'
    add_subestacao_presente = 'C:\\Arthur\\CDEC\\Parte 2\\Dados\\Subestacao\\Subestações___Base_Existente.shp'
    rotas_futuro_add ='C:\\Arthur\\CDEC\\Parte 2\\Dados\\Rotas\\futuro\\futuro.shp'
    add_subestacao_futuro = 'C:\\Arthur\\CDEC\\Parte 2\\Dados\\Subestacao\\Subestações___planejado.shp'
    add_mapa_presente = r'C:\Arthur\CDEC\Parte 2\Dados\Mapa Adequabilidade\mapa_adequabilidade_cenario_presente.tif'
    add_mapa_futuro = r'C:\Arthur\CDEC\Parte 2\Dados\Mapa Adequabilidade\mapa_adequabilidade_cenario_futuro.tif'
    '''
    
    add_linha = '~/Dados/Rotas/presente/presente.shp'
    add_rest = '~/Dados/restrições/restrições.shp'
    parques_add = '~/Dados/centroide parque/CENTROIDE_DOS_PARQUES.shp'
    rotas_presente_add = '~/Dados/Rotas/presente/presente.shp'
    add_subestacao_presente = '~/Dados/Subestacao/Subestações___Base_Existente.shp'
    rotas_futuro_add ='~/Dados/Rotas/futuro/futuro.shp'
    add_subestacao_futuro = '~/Dados/Subestacao/Subestações___planejado.shp'
    add_mapa_presente = 'mapa_adequabilidade_cenario_presente.tif'
    add_mapa_futuro = 'mapa_adequabilidade_cenario_futuro.tif'
    
    custom_hover = custom_hoover()
    # As we've seen, the coordinates in our dataset were called x and y, so we are 
    # going to use these.
    key_dimensions = ['x', 'y']
    
    # We are also going to need the name of the value stored in the file. We get it 
    # from there this time, but we could also set this manually.
    
    value_dimension = 'adequabilidade'
    clipping = {'NaN': '#00000000'}
    
    dataarray = rxr.open_rasterio(add_mapa_presente)
    dataarray = dataarray.rio.reproject("EPSG:3857")
    dataarray = dataarray.where(dataarray!=-9999)
    dataarray.values[dataarray.values==9999999]=np.nan
    hv_dataset = hv.Dataset(dataarray[0], vdims=value_dimension, kdims=key_dimensions)
    hv_mapa_presente = hv.Image(hv_dataset).opts(title='first image',tools=[custom_hover])
    #hv_mapa_presente = hd.regrid(hv_image_basic)
    
    dataarray = rxr.open_rasterio(add_mapa_futuro)
    dataarray = dataarray.rio.reproject("EPSG:3857")
    dataarray = dataarray.where(dataarray!=-9999)
    dataarray.values[dataarray.values==9999999]=np.nan
    hv_dataset = hv.Dataset(dataarray[0], vdims=value_dimension, kdims=key_dimensions)
    hv_mapa_futuro = hv.Image(hv_dataset).opts(title='first image',tools=[custom_hover])
    #hv_mapa_futuro = hd.regrid(hv_image_basic)
    
    
    
    
    gdf_parques = gpd.read_file(parques_add)
    gdf_parques = gdf_parques.to_crs(3857)
    spd_parques = spd.GeoDataFrame(gdf_parques)
    
    gdf_rest = gpd.read_file(add_rest)
    gdf_rest = gdf_rest.to_crs(3857)
    spd_rest = spd.GeoDataFrame(gdf_rest)
    
    hv_tiles_osm = hv.element.tiles.OSM()
    
    '''Futuro'''
    
    gdf_rotas_futuro = gpd.read_file(rotas_futuro_add)
    gdf_rotas_futuro = gdf_rotas_futuro.to_crs(3857)
    spd_rotas_futuro = spd.GeoDataFrame(gdf_rotas_futuro)
    
    gdf_subestacao_futuro = gpd.read_file(add_subestacao_futuro)
    gdf_subestacao_futuro = gdf_subestacao_futuro.to_crs(3857)
    spd_subestacao_futuro = spd.GeoDataFrame(gdf_subestacao_futuro)
    
    mapa_futuro = hv_mapa_futuro*spd_rotas_futuro.hvplot(color='purple')*spd_subestacao_futuro.hvplot(color='orange')*spd_parques.hvplot('green')
    
    
    
    
    '''Passado'''
    gdf_rotas_presente = gpd.read_file(rotas_presente_add)
    gdf_rotas_presente = gdf_rotas_presente.to_crs(3857)
    spd_rotas_presente = spd.GeoDataFrame(gdf_rotas_presente)
    
    gdf_subestacao_presente = gpd.read_file(add_subestacao_presente)
    gdf_subestacao_presente = gdf_subestacao_presente.to_crs(3857)
    spd_subestacao_presente = spd.GeoDataFrame(gdf_subestacao_presente)
    
    mapa_passado = hv_mapa_presente*spd_rotas_presente.hvplot(color='yellow')*spd_subestacao_presente.hvplot(color='pink')*spd_parques.hvplot('green')
    
    
    mapa= spd_rest.hvplot()
    plot= mapa_passado
    
    startX,endX = mapa.range('x')
    startY,endY = mapa.range('y')
    #OldStartX,OldEndX = mapa.range('x')
    #OldStartY,OldEndY = mapa.range('y')
    
    radio = param.Selector(default='Cenário Presente',objects=['Cenário Presente','Cenário Futuro'])
    
    
    
    def keep_zoom(self,x_range,y_range):
        print('zoom')
        self.startX,self.endX = x_range
        self.startY,self.endY = y_range
        
        

    @param.depends('radio')
    def view(self,x_range,y_range):
        if self.radio == 'Cenário Presente':
            self.plot= self.mapa_passado
        else:
            self.plot= self.mapa_futuro
        
        
        if math.isnan(self.startX) == False:
            print('Not None')
            self.OldStartX = self.startX
            self.OldEndX = self.endX
            self.OldStartY = self.startY
            self.OldEndY = self.endY
            
            print(self.startX)
            print(self.OldStartX)
            
            self.mapa = self.mapa.redim.range(x=(self.startX,self.endX), y=(self.startY,self.endY))
        else:
            print('Is None')
            self.mapa = self.mapa.redim.range(x=(self.OldStartX,self.OldEndX), y=(self.OldStartY,self.OldEndY))
            print(self.startX,self.endX)
            print(self.OldStartX,self.OldEndX)
            
        self.plot = (self.hv_tiles_osm*self.mapa*self.plot).opts(active_tools=['pan','wheel_zoom'])
        return self.plot
    
    
viewer = AppTest()

rangexy = streams.RangeXY(source = viewer.mapa, 
                          x_range=(viewer.startX,viewer.endX), 
                          y_range=(viewer.startY,viewer.endY)
                          )
rangexy.add_subscriber(viewer.keep_zoom)

stock_dmap = hv.DynamicMap(viewer.view,streams=[rangexy]).opts(responsive=True,align='center',width=1900)

bootstrap.main.append(
    pn.Column(pn.Param(viewer.param,
                widgets={'radio':pn.widgets.RadioButtonGroup}
                ),
       stock_dmap,
       sizing_mode='scale_both'
       )
    )
bootstrap.servable()

'''
bootstrap.main.append(
    pn.Column(pn.Param(viewer.param,
                widgets={'radio':pn.widgets.RadioButtonGroup}
                ),
       stock_dmap,
       sizing_mode='scale_both'
       )
    )
bootstrap.servable()
'''


