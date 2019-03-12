# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 08:10:22 2017

@author: jose
"""

from lxml import etree
import pandas as pd
from collections import Counter
import os
import glob
import re
import matplotlib.pyplot as plt
import numpy as np

from shutil import copyfile

def copy_files():
    copyfile("../documentation/books.xlsx", "books.xlsx")
    copyfile("../documentation/genres_location_mean.xlsx", "genres.xlsx")

    copyfile("../resulting data/books_entities_latitude_longitude_mean.csv", "people-groups.csv")

    copyfile("../entities.xls", "places.xls")

copy_files()

def clean_places():
    entities_df = pd.ExcelFile("places.xls",  index_col=0).parse('Sheet1').fillna(0)
    
    entities_df = entities_df.loc[entities_df["id"] != 0]
    
    places_df = entities_df.loc[entities_df["id"].str.contains('^#pla')]
    
    print(places_df.shape)
    places_df.to_csv("places.csv",sep="\t")
    try:
        os.remove("places.xls")
    except:
        pass
clean_places()



