#!/usr/bin/python
# -*- coding: UTF-8 -*-

#__modification time__ = 2025-02-17
# __author__ = Qi Zhou, Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
# __find me__ = qi.zhou@gfz.de, qi.zhou.geo@gmail.com, https://github.com/Qi-Zhou-Geo
# Please do not distribute this code without the author's permission
import os

# <editor-fold desc="add the sys.path to search for custom modules">
from pathlib import Path
current_dir = Path(__file__).resolve().parent
# using ".parent" on a "pathlib.Path" object moves one level up the directory hierarchy
project_root = current_dir.parent
import sys
sys.path.append(str(project_root))
# </editor-fold>

# import the custom functions
from founctions.seismic_data_processing import load_seismic_signal


catchment_name, seismic_network, station, component = "Illgraben", "9J", "IGB02", "HHZ"
data_start, data_end = "2014-07-12T13:00:00", "2014-07-12T18:00:00"

st = load_seismic_signal(catchment_name, seismic_network, station, component,
                         data_start, data_end,
                         f_min=1, f_max=45,
                         remove_sensor_response=True,
                         raw_data=False)

st.plot(outfile=f"{current_dir}/example.png") # y is amplitude, unit by meter per second m/s
print(st[0].stats)
