# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 22:38:13 2018

@author: jose
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

wdir = "../../resulting data/quantitative_data.csv"
outdir = "../../visualizations/features/"
format_ = "png"


def read_features_table(wdir):
    
    quantitative_data = pd.read_csv(wdir, sep="\t", index_col=0)
    
    return quantitative_data 

def make_bars_verses(quantitative_data, outdir, format_):
    fig, ax = plt.subplots()
    ax = quantitative_data.plot(kind="bar", x="code", y="verses", color="green",figsize=(10,5), legend= False)
    ax.set_ylabel('amount verses')
    ax.set_xlabel('books')
    ax.get_figure().savefig(outdir+"bar_verses."+format_, dpi=300, format=format_)
    plt.show(fig)

def make_features_relative(quantitative_data):
    relative_quantitative_data = quantitative_data.copy()
    
    for column in relative_quantitative_data.columns:
        if(relative_quantitative_data[column].dtype == np.float64 or relative_quantitative_data[column].dtype == np.int64):
            relative_quantitative_data[column] = relative_quantitative_data[column]/quantitative_data["verses"]
        else:
              relative_quantitative_data[column]
    return relative_quantitative_data
                
def make_viz_diff_entities(relative_quantitative_data):
    relative_quantitative_data["different people"] = relative_quantitative_data["diff pers"]
    relative_quantitative_data["different groups"] = relative_quantitative_data["diff orgs"]
    relative_quantitative_data["different places"] = relative_quantitative_data["diff plas"]
    fig, ax = plt.subplots()
    ax = relative_quantitative_data.plot(kind="barh", x="code", y=["different people","diff orgs", "diff plas"], figsize=(5,18), title="Amount of different entities in each book of the Bible\n(relative to amount of verses)")
    ax.set_ylabel('different entities')
    ax.set_xlabel('books')
    ax.get_figure().savefig(outdir+"bar_diff_ent."+format_, dpi=300, format=format_)
    plt.show(fig)

    

quantitative_data = read_features_table(wdir)

#make_bars_verses(quantitative_data, outdir, format_)

relative_quantitative_data = make_features_relative(quantitative_data)

make_viz_diff_entities(relative_quantitative_data)
