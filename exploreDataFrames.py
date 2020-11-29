#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from helpers import *
import argparse
import os

parser = argparse.ArgumentParser(description='Get dataframes for track dictionaries')
parser.add_argument('-v', "--version", dest='version', default='427080_Zprime_V5', help='input sample versions')
parser.add_argument('-t', "--tracks", dest='tracks',
                    default='nominal:pseudo:ideal:fakes_removed:fakes_removed_+_track_replaced',
                    help='input track collections')
parser.add_argument('-w', "--workDir", dest='workDir', default='/Users/avalee/TrackingAnalysis/',
                    help='working directory')
parser.add_argument('-f', "--fileDict", dest="fileDict", default="", help="filename of dataframes dictionary")
args = parser.parse_args()

if __name__ == "__main__":
    version = args.version
    tracks = args.tracks.split(':')

    jetVars = getDataFrames(args.workDir, version, tracks, "jetVars", args.fileDict)

    vtxDict = {
        'jet_jf_nvtx > 0': 'Vertices with at least 2 tracks',
        'jet_jf_nvtx1t == 1': "Single-track vertices",
        "jet_jf_nvtx1t >= 2": r'$\geq$ 2 single-tracks vertices',
    }

    print (jetVars)