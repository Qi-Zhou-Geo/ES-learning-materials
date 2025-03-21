#!/usr/bin/python
# -*- coding: UTF-8 -*-

#__modification time__ = 2025-02-07
#__author__ = Qi Zhou, Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
#__find me__ = qi.zhou@gfz.de, qi.zhou.geo@gmail.com, https://github.com/Nedasd
# Please do not distribute this code without the author's permission

import os
import yaml
import numpy as np

from pathlib import Path

from obspy import read, Stream, read_inventory, signal
from obspy.core import UTCDateTime # default is UTC+0 time zone
from obspy.signal.invsim import simulate_seismometer


def manually_remove_sensor_response(trace, sensor_type):
    '''
    manually remove the sensor response

    Parameters:
    - st (obspy.core.stream): seismic stream that deconvolved, make sure the stream only hase one trace
    - sensor_type (str): sensor type

    Returns:
    - st (obspy.core.stream): seismic stream that removed the sensor response
    '''

    corrected_trace = trace.copy()

    # reference,
    # https://www.gfz-potsdam.de/en/section/geophysical-imaging/infrastructure/geophysical-instrument-pool-potsdam-gipp/pool-components/clipp-werte
    # https://www.gfz-potsdam.de/en/section/geophysical-imaging/infrastructure/geophysical-instrument-pool-potsdam-gipp/pool-components/poles-and-zeros/trillium-c-120s
    # if you do NOT use the cube logger, the "Normalization factor" is "gain"
    # if you do use the cube logger, refer link at "Sensitivity and clip values"

    paz_trillium_compact_120s_754 = {
        'zeros': [(0 + 0j),
                  (0 + 0j),
                  (-392 + 0j),
                  (-1960 + 0j),
                  (-1490 + 1740j),
                  (-1490 - 1740j)],

        'poles': [(-0.03691 + 0.03702j),
                  (-0.03691 - 0.03702j),
                  (-343 + 0j),
                  (-370 + 467j),
                  (-370 - 467j),
                  (-836 + 1522j),
                  (-836 - 1522j),
                  (-4900 + 4700j),
                  (-4900 - 4700j),
                  (-6900 + 0j),
                  (-15000 + 0j)],
        # 'gain' also known as (A0 normalization factor)
        'gain': 4.34493e17, # this is
        'sensitivity': 3.0172e8
    }

    paz_IGU_16HR_EB_3C_5Hz = {# works for Luding STA01
        'zeros': [(0 + 0j),
                  (0 + 0j)],

        'poles': [(-22.211059 + 22.217768j),
                  (-22.211059 - 22.217768j)],
        # 'gain' also known as (A0 normalization factor)
        'gain': 76.7,
        'sensitivity': 6.40174e4
    }

    paz_3D_Geophone_PE_6_B16 = {# works for 3D Geophone PE-6/B; 4.5 ... 500 Hz(*)
        'zeros': [(0 + 0j),
                  (0 + 0j)],

        'poles': [(-19.78 + 20.20j),
                  (-19.78 - 20.20j)],
        #'gain' also known as (A0 normalization factor)
        'gain': 1,
        # # P_AMPL gain is 16 for 2023 and 2024 data
        'sensitivity': 6.5574e7
    }

    paz_3D_Geophone_PE_6_B32 = {# works for 3D Geophone PE-6/B; 4.5 ... 500 Hz(*)
        'zeros': [(0 + 0j),
                  (0 + 0j)],

        'poles': [(-19.78 + 20.20j),
                  (-19.78 - 20.20j)],
        # 'gain' also known as (A0 normalization factor)
        'gain': 1,
        # P_AMPL gain is 32 of Prof. Dr. Yan Yan 2022 data
        'sensitivity': 1.3115e8
    }

    paz_3D_NoiseScope = {# works for Foutangba, Prof. Dr. Yan Yan
        'zeros': [(0 + 0j),
                  (0 + 0j)],

        'poles': [(-0.444221 - 0.6565j),
                  (-0.444221 + 0.6565j),
                  (-222.110595 - 222.17759j),
                  (-222.110595 + 222.17759j)],

        'gain': 298,
        'sensitivity': 6.71140939e9 # counts/m/s
    }


    if sensor_type == "trillium_compact_120s_754":
        paz = paz_trillium_compact_120s_754
    elif sensor_type == "IGU_16HR_EB_3C_5Hz":
        paz = paz_IGU_16HR_EB_3C_5Hz
    elif sensor_type == "paz_3D_Geophone_PE_6_B16":
        paz = paz_3D_Geophone_PE_6_B16
    elif sensor_type == "paz_3D_Geophone_PE_6_B32":
        paz = paz_3D_Geophone_PE_6_B32
    elif sensor_type == "paz_3D_NoiseScope":
        paz = paz_3D_NoiseScope
    else:
        print(f"please check the sensor_type: {sensor_type}")


    corrected_data = simulate_seismometer(data=trace[0].data,
                                          samp_rate=trace[0].stats.sampling_rate,
                                          paz_remove=paz,
                                          paz_simulate=None,
                                          remove_sensitivity=True)
    corrected_trace[0].data = corrected_data

    return corrected_trace

def config_snesor_parameter(catchment_name, seismic_network):

    current_dir = Path(__file__).resolve().parent
    config_path = (current_dir / "../config/config_catchment_code.yaml").resolve()
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        glic_sac_dir = config[f"glic_sac_dir"]

    config = config[f"{catchment_name}-{seismic_network}"]

    path_mapping = config["path_mapping"]
    sac_path = Path(glic_sac_dir) / path_mapping
    response_type = config["response_type"]
    sensor_type = config["sensor_type"]
    normalization_factor = config["normalization_factor"]

    return sac_path, response_type, sensor_type, normalization_factor


def load_seismic_signal(catchment_name, seismic_network, station, component, data_start, data_end,
                        f_min=1, f_max=45, remove_sensor_response=True, raw_data=False):

    d1 = UTCDateTime(data_start)
    d2 = UTCDateTime(data_end)


    # config the snesor parameter based on seismci network code
    sac_path, response_type, sensor_type, normalization_factor = config_snesor_parameter(catchment_name, seismic_network)

    # make sure all you file is structured like this
    # '/storage/vast-gfz-hpc-01/project/seismic_data_qi/seismic/continent_name/catchment_name'
    file_dir = f"{sac_path}/{d1.year}/{station}/{component}/"

    if d1.julday == d2.julday:
        data_name = f"{seismic_network}.{station}.{component}.{d1.year}.{str(d1.julday).zfill(3)}.mseed"
        st = read(file_dir + data_name)
    else:
        st = Stream()
        for n in np.arange(d1.julday, d2.julday+1):
            data_name = f"{seismic_network}.{station}.{component}.{d1.year}.{str(n).zfill(3)}.mseed"
            st += read(file_dir + data_name)

    if raw_data is True:
        return st

    st.merge(method=1, fill_value='latest', interpolation_samples=0)
    st._cleanup()
    st.detrend('linear')
    st.detrend('demean')

    if remove_sensor_response is True:
        if response_type == "xml": # with xml file
            meta_file = [f for f in os.listdir(f"{sac_path}/meta_data") if f.startswith(seismic_network)][0]
            inv = read_inventory(f"{sac_path}/meta_data/{meta_file}")
            st.remove_response(inventory=inv)
        elif response_type == "simulate": # with poles and zeros
            st = manually_remove_sensor_response(st, sensor_type)
        elif response_type == "direct": # without poles and zeros
            normalization_factor = eval(normalization_factor)  # executes arbitrary code by eval
            st[0].data = st[0].data / normalization_factor
        else:
            print(f"please check the response_type: {response_type}")

        if st[0].stats.sampling_rate <= 2 * f_max:
            st.filter("highpass", freq=f_min, zerophase=True)
        else:
            st.filter("bandpass", freqmin=f_min, freqmax=f_max)

        st.trim(starttime=d1, endtime=d2, nearest_sample=False)
        st.detrend('linear')
        st.detrend('demean')

    else:
        st.trim(starttime=d1, endtime=d2, nearest_sample=False)

    return st

