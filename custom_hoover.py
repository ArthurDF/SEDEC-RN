# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:16:32 2023

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

def custom_hoover():
    # This is the JavaScript code that formats our coordinates:
    # You only need to change the "digits" value if you would like to display the 
    # coordinates with more or fewer digits than 4.
    formatter_code = """
      var digits = 4;
      var projections = Bokeh.require("core/util/projections");
      var x = special_vars.x;
      var y = special_vars.y;
      var coords = projections.wgs84_mercator.invert(x, y);
      return "" + (Math.round(coords[%d] * 10**digits) / 10**digits).toFixed(digits)+ "";
    """
    
    # In the code above coords[%d] gives back the x coordinate if %d is 0, so at 
    # first we replace that.
    formatter_code_x = formatter_code % 0
    # Then we replace %d to 1 to get the y value.
    formatter_code_y = formatter_code % 1
    
    # This is the standard definition of a custom Holoviews Tooltip.
    # Every line will be a line in the tooltip, with the first element being the 
    # label and the second element the displayed value.
    custom_tooltips = [
      # We want to use @x and @y values, but send them to a custom formatter first.
      ( 'Lon',   '@x{custom}' ),
      ( 'Lat',   '@y{custom}' ),
      # This is where you should label and format your data:
      # '@image' is the data value of your GeoTIFF
      # In this example we format it as an integer and add "m" to the end of it
      # You can find more information on number formatting here:
      # https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#formatting-tooltip-fields
      ('Adequabilidade', '@image{0}m')
    ]
    
    # For every value we marked above as {custom} we have to define what we mean by 
    # that. In this case for both variables we want to get a Bokeh CustomJSHover 
    # with respective JS codes created above.
    
    custom_formatters = {
      '@x' : bk.models.CustomJSHover(code=formatter_code_x),
      '@y' : bk.models.CustomJSHover(code=formatter_code_y)
    }
    
    # We add these together, creating a custom Bokeh HoverTool
    custom_hover = bk.models.HoverTool(tooltips=custom_tooltips, formatters=custom_formatters)
    
    # Now that we have the tool, we should let Holoviews know about it.
    # Usually we would do it like this:
    # hv.opts.defaults(
    #   hv.opts.Image(tools=[custom_hover])
    # )
    # This would set it as a default for every Image. In this notebook however we 
    # need the older examples not to use this even if the cells are executed in the 
    # wrong order, so we are going to attach this to each image every time:
    # hv.Image(...).opts(tools=[custom_hover])
    return custom_hover
