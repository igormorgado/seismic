#!/usr/bin/env python

import pandas as pd
import math
from bokeh.plotting import figure, output_file,show
from bokeh.models import DatetimeTickFormatter, HoverTool
from bokeh.io import output_file

inp = 'Tide_Heights_SPR_MSL_25.198S_41.715W_20160921-20161220.txt'
out = 'tide.html'
title = 'Tides'


datetimeparser = lambda x: pd.datetime.strptime(x, '%d/%m/%Y %H:%M')
df =  pd.read_csv(inp, sep='\s+', header=None, names=[ 'date', 'time', 'tide' ],
        parse_dates={'datetime': ['date', 'time']}, date_parser=datetimeparser)

# diaDoAno = df.iloc[0]['datetime'].dayofyear

TOOLS = 'pan,box_zoom,wheel_zoom,box_select,crosshair,resize,reset'

p = figure(plot_width=1200, plot_height=600,tools=TOOLS,title=title)

p.line(df.datetime, df['tide'])
#p.circle(df.datetime, df['tide'], fill_color="white", size=8)

p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
    years=["%B %Y"],
    months=["%d %B %Y"],
    days=["%d %B %Y"],
    hours=["%d %B %Y %H:%M:%S"],
    minutes=["%d %B %Y %H:%M:%S"],
    seconds=["%d %B %Y %H:%M:%S"],
    ))

p.xaxis.major_label_orientation = math.pi/4

output_file(out,title=title)
show(p)

