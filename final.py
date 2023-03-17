# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 15:21:17 2023

@author: arthurdiniz
"""

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
import math


hv.extension('bokeh')
pn.extension(sizing_mode = 'stretch_width')
bootstrap = pn.template.BootstrapTemplate(title='Visualizador de Mapa')

class AppTest(param.Parameterized):
    '''Defining the scenarios'''
    radio = param.Selector(default='Present',objects=['Present','Future'])
    
    '''Link of files'''
    '''
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
    add_subestacao_presente = '~/Dados/Subestacao/Subestações___Base_Existente2.shp'
    rotas_futuro_add ='~/Dados/Rotas/futuro/futuro.shp'
    add_subestacao_futuro = '~/Dados/Subestacao/Subestações___planejado.shp'
    add_mapa_presente = 'mapa_adequabilidade_cenario_presente.tif'
    add_mapa_futuro = 'mapa_adequabilidade_cenario_futuro.tif'
    
    
    value_dimension = 'adequabilidade'
    key_dimensions = ['x', 'y']
    
    #this HVPLOT will be ploted on both scenarios and will be the reference for the RangeXY Stream
    gdf_parques = gpd.read_file(parques_add)
    gdf_parques = gdf_parques.to_crs(3857)
    spd_parques = spd.GeoDataFrame(gdf_parques)
    spd_parques_plot = spd_parques.hvplot('green',responsive=True)
    
    gdf_rest = gpd.read_file(add_rest)
    gdf_rest = gdf_rest.to_crs(3857)
    spd_rest = spd.GeoDataFrame(gdf_rest)
    mapa= spd_rest.hvplot(color='blue',responsive=True)
    
    hv_tiles_osm = hv.element.tiles.OSM()
    
    '''Futuro'''
    
    gdf_rotas_futuro = gpd.read_file(rotas_futuro_add)
    gdf_rotas_futuro = gdf_rotas_futuro.to_crs(3857)
    spd_rotas_futuro = spd.GeoDataFrame(gdf_rotas_futuro)
    spd_rotas_futuro_plot = spd_rotas_futuro.hvplot(color='purple',responsive=True)
    
    
    gdf_subestacao_futuro = gpd.read_file(add_subestacao_futuro)
    gdf_subestacao_futuro = gdf_subestacao_futuro.to_crs(3857)
    spd_subestacao_futuro = spd.GeoDataFrame(gdf_subestacao_futuro)
    spd_subestacao_futuro_plot = spd_subestacao_futuro.hvplot(color='orange',responsive=True)
    
    dataarray = rxr.open_rasterio(add_mapa_futuro)
    dataarray = dataarray.rio.reproject("EPSG:3857")
    dataarray = dataarray.where(dataarray!=-9999)
    dataarray.values[dataarray.values==9999999]=np.nan
    hv_dataset = hv.Dataset(dataarray[0], vdims=value_dimension, kdims=key_dimensions)
    hv_mapa_futuro = hv.Image(hv_dataset).opts(title='futuro',responsive=True,cmap='plasma')
    
    
    '''Passado'''
    gdf_rotas_presente = gpd.read_file(rotas_presente_add)
    gdf_rotas_presente = gdf_rotas_presente.to_crs(3857)
    spd_rotas_presente = spd.GeoDataFrame(gdf_rotas_presente)
    spd_rotas_presente_plot = spd_rotas_presente.hvplot(color='yellow',responsive=True)
    
    gdf_subestacao_presente = gpd.read_file(add_subestacao_presente)
    gdf_subestacao_presente = gdf_subestacao_presente.to_crs(3857)
    spd_subestacao_presente = spd.GeoDataFrame(gdf_subestacao_presente)
    spd_subestacao_presente_plot = spd_subestacao_presente.hvplot(color='pink',responsive=True)
    
    dataarray = rxr.open_rasterio(add_mapa_presente)
    dataarray = dataarray.rio.reproject("EPSG:3857")
    dataarray = dataarray.where(dataarray!=-9999)
    dataarray.values[dataarray.values==9999999]=np.nan
    hv_dataset = hv.Dataset(dataarray[0], vdims=value_dimension, kdims=key_dimensions)
    hv_mapa_presente = hv.Image(hv_dataset).opts(title='presente',responsive=True,cmap='viridis')
    
    '''Generating the HVplots to be used on solution (using Spatial Pandas 
    because for some reason when I tried to geopandas.hvplot on heroku it didn't work)'''
    
    
    
    scenario_1 = hv_mapa_presente*spd_rotas_presente_plot*spd_subestacao_presente_plot*spd_parques_plot
    scenario_2 = hv_mapa_futuro*spd_rotas_futuro_plot*spd_subestacao_futuro_plot*spd_parques_plot
    
    
    #plot = (hv_tiles_osm*mapa*scenario_1)
    
    startX,endX = mapa.range('x')
    startY,endY = mapa.range('y')
    startRangeX = 0
    startRangeY = 0
    cont=0

    
    @param.depends('radio')
    def view(self,x_range,y_range):
        print(x_range)
        print(y_range)
        print('plot:',self.cont)
        if self.cont == 1:
            self.startRangeX = x_range
            self.startRangeY = y_range
       
        x1,x1 = x_range
        if math.isnan(x1) == False:
            print('REDIM')
            if self.cont>2:
                if self.startRangeX == x_range:
                    print('do nothing')
                    
                else:
                    self.mapa = self.mapa.redim.range(x=x_range, y=y_range)
        else:
            print('None')
            
        
        if self.radio == 'Present':
            print('Present')
            self.plot= (self.hv_tiles_osm*self.mapa*self.scenario_1)#.redim.range(x=x_range, y=y_range)
        else:
            self.plot= (self.hv_tiles_osm*self.mapa*self.scenario_2)#.redim.range(x=x_range, y=y_range)
        
        
        
        
        #self.plot = (self.mapa*self.scenario_1).opts(active_tools=['pan','wheel_zoom'],responsive=True,framewise=False)
        #self.plot = self.scenario_2
        #print(self.plot.opts.info())
        self.cont=self.cont+1
        return self.plot
    
    
'''Create app and display'''
viewer = AppTest()
'''
rangexy = streams.RangeXY(source = viewer.mapa, 
                          x_range=(viewer.startX,viewer.endX), 
                          y_range=(viewer.startY,viewer.endY)
                          )
                          '''

rangexy = streams.RangeXY(source = viewer.mapa, 
                          x_range=(np.nan,np.nan), 
                          y_range=(np.nan,np.nan)
                          )
#rangexy.add_subscriber(viewer.keep_zoom)

stock_dmap = hv.DynamicMap(viewer.view,streams=[rangexy],).opts(
    {'Overlay': dict(
                      align = 'center',
                      responsive=True
                      )
     }
    )
#stock_dmap = stock_dmap.opts(sizing_mode='scale_both')
    
plot_out = pn.Row(pn.GridSpec(sizing_mode='stretch_both'), sizing_mode='scale_both')
plot_out[0][0,0] = stock_dmap
        
bootstrap.main.append(
    pn.Column(pn.Param(viewer.param,
                widgets={'radio':pn.widgets.RadioButtonGroup}
                ),
       plot_out
       )
    )
#bootstrap.show()
bootstrap.servable()
