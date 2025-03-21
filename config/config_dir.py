#!/usr/bin/python
# -*- coding: UTF-8 -*-

#__modification time__ = 2024-09-22
#__author__ = Qi Zhou, Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
#__find me__ = qi.zhou@gfz.de, qi.zhou.geo@gmail.com, https://github.com/Qi-Zhou-Geo
# Please do not distribute this code without the author's permission

import os
import yaml
from pathlib import Path


def path_mapping(catchment_name, seismic_network):
    '''
    Mapping the raw seismic data path in GFZ-GLIC server
    Args:
        seismic_network: str, seismic network code

    Returns:
        glic_path: str, path in GFZ-GLIC server
    '''

    current_dir = Path(__file__).resolve().parent
    config_path = (current_dir / f"config_catchment_code.yaml").resolve()

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    sac_path = config["glic_sac_dir"]

    try:
        glic_path = config[f"{catchment_name}-{seismic_network}"]["path_mapping"]
    except Exception as e:
        print(f"Can not find the catchment code in <./config_catchment_code.yaml>, {e}")

    glic_path = Path(sac_path) / glic_path

    return glic_path


def data_length_mapping(seismic_network, input_year, input_station, input_component):

    mapping = {"9S-2017-ILL02-EHZ": [138, 183], # EU data
               "9S-2017-ILL03-EHZ": [138, 183],
               "9S-2017-ILL08-EHZ": [138, 183],

               "9S-2018-ILL12-EHZ": [145, 240],
               "9S-2018-ILL13-EHZ": [145, 240],
               "9S-2018-ILL18-EHZ": [145, 240],

               "9S-2019-ILL12-EHZ": [145, 240],
               "9S-2019-ILL13-EHZ": [145, 240],
               "9S-2019-ILL18-EHZ": [145, 240],

               "9S-2020-ILL12-EHZ": [150, 250],
               "9S-2020-ILL13-EHZ": [150, 250],
               "9S-2020-ILL18-EHZ": [150, 250],

               "9S-2022-ILL12-EHZ": [135, 256],
               "9S-2022-ILL13-EHZ": [135, 256],
               "9S-2022-ILL18-EHZ": [135, 256],

               "9S-2022-synthetic12-white": [156, 165], # EU synthetic data for 2022-06-05
               "9S-2022-synthetic12-red": [156, 165],
               "9S-2022-synthetic12-pink": [156, 165],

               "1A-2021-E19A-CHZ": [175, 238], # USA data
               "CI-2018-QAD-HNZ": [2, 30],
               "Y7-2009-AV11-ELZ": [156, 364],

               "DC-2024-BL7-BHZ": [97, 293], # AS data
               "MJ-2022-EG1-BHZ": [230, 232],
               "MJ-2022-EG2-BHZ": [230, 232],
               "MJ-2022-FTB1-BHZ": [230, 232],
               "MJ-2022-FTB2-BHZ": [230, 232],
               "XN-2016-NEP08-HHZ": [171, 199],
               "XF-2003-H0390-BHZ": [221, 229],

               "MR-2007-TRAN-BHZ": [76, 77], # OC data
               }

    quary = f"{seismic_network}-{input_year}-{input_station}-{input_component}"
    value = mapping.get(quary, "check function path_mapping")

    return float(value[0]), float(value[1])


def config_dir(parent_dir=Path(__file__).resolve().parent.parent):

    sac_dir = Path("/storage/vast-gfz-hpc-01/project/seismic_data_qi/seismic")
    output_dir = parent_dir / "output"
    output_dir2 = parent_dir / "output2"
    output_dir_div = parent_dir / "output-div"
    output_dir_warning = parent_dir / "output_dir_warning"

    label_output_dir = Path("/storage/vast-gfz-hpc-01/home/qizhou/3paper/1seismic_label")
    feature_output_dir = Path("/storage/vast-gfz-hpc-01/home/qizhou/3paper/0seismic_feature")
    ref_model_dir = parent_dir / "optimal_models"

    CONFIG_dir = {
        "parent_dir": parent_dir,

        "sac_dir": sac_dir,
        "output_dir": output_dir,
        "output_dir2": output_dir2,
        "output_dir_div":output_dir_div,
        "output_dir_warning": output_dir_warning,

        "label_output_dir": label_output_dir,
        "feature_output_dir": feature_output_dir,

        "ref_model_dir": ref_model_dir
    }

    return CONFIG_dir


# please keep in mind this file I/O directory
CONFIG_dir = config_dir()
