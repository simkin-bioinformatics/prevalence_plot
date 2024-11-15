#! /home/charlie/data/Dropbox/scatterplot/env/bin/python

# this script can be used to add coordinates to a csv file containing prevalences in a geographic region
# input: prevalence.csv file with regions or health facility names with their prevalences
# input: metadata.csv file that has the coordinates associated with each geographic location
# output: prevalence_with_coords.csv file
# it will look up the coordinates of each region in the metadata file and add them to the prevalence sheet

from urllib.request import urlopen
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import json
import pandas as pd


metadata_file = (
    "/home/charlie/data/Dropbox/scatterplot/charlie_choropleths/2023/metadata.csv"
)
prevalence_summary_file = "/home/charlie/data/Dropbox/scatterplot/charlie_choropleths/2023/summaries/HFname:all_3_1_prevalence_summary.tsv"
updated_prevalence_summary = "2023_prevalence_summary.tsv"


def create_site_dict(metadata_file):
    """
    creates a dictionary of format {HFname: [lat, lon]} and reports if any HFnames have
    multiple coordinates associated with them
    """
    df = pd.read_csv(metadata_file)
    hf_list = df["HFname"].to_list()
    hf_list = [str(x) for x in hf_list]
    lat_list = df["Latitude"].to_list()
    lon_list = df["Longitude"].to_list()
    full_list = list(set(zip(hf_list, lat_list, lon_list)))
    full_list.sort()
    site_dict = {}
    for item in full_list:
        HFname, lat, lon = item
        if HFname not in site_dict:
            site_dict[HFname] = [lat, lon]
        else:
            print(
                HFname + " has multiple coordinates in the metadata file, please check"
            )
    return site_dict


def append_coordinates(
    metadata_file, prevalence_summary_file, updated_prevalence_summary
):
    site_dict = create_site_dict(metadata_file)
    prevalence_df = pd.read_csv(prevalence_summary_file, sep="\t")

    def get_lat(x):
        if x in site_dict:
            return site_dict[x][0]

    def get_lon(x):
        if x in site_dict:
            return site_dict[x][1]

    prevalence_df.insert(
        1, "Latitude", prevalence_df["HFname"].map(lambda x: get_lat(x))
    )
    prevalence_df.insert(
        2, "Longitude", prevalence_df["HFname"].map(lambda x: get_lon(x))
    )
    # print(prevalence_df)
    prevalence_df.to_csv(updated_prevalence_summary, index=False, sep="\t")

append_coordinates(metadata_file, prevalence_summary_file, updated_prevalence_summary)