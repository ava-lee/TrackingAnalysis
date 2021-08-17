# -*- coding: utf-8 -*-
import pickle
import collections
import pandas
import argparse
import os

parser = argparse.ArgumentParser(description='Get dataframes for track dictionaries')
parser.add_argument('-v', "--version", dest='version', default='427080_Zprime_V5', help='input sample versions')
parser.add_argument('-t', "--tracks", dest='tracks',
                    default='nominal:pseudo:ideal:fakes_removed:fakes_removed_+_track_replaced:HF:HF_+_track_replaced:pseudo_not_reco',
                    help='input track collections')
parser.add_argument('-i', "--inDir", dest='inDir', default='/Users/avalee/TrackingAnalysis/trackDicts/',
                    help='input directory')
parser.add_argument('-o', "--outDir", dest='outDir', default='/Users/avalee/TrackingAnalysis/dataFrames/',
                    help='output directory')
parser.add_argument('-d' "--dict", dest="dict", default="jetVars", help="type of variables dictionary to save")#dictionary comment  is
args = parser.parse_args()


def saveDataFrames(inDir, outDir, version, tracks, varsType):
    dfs = collections.OrderedDict()
    for i in range(len(tracks)):
        varsDict = getDict(inDir, version, tracks[i], varsType)
        df = pandas.DataFrame.from_dict(varsDict)
        dfs[tracks[i]] = df

    outName = outDir + "_" + varsType + "_dfs.pickle"
    with open(outName, 'wb') as handle:
        pickle.dump(dfs, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
if __name__ == "__main__":
    version = args.version
    tracks = args.tracks.split(':') # get list of tracks
    if not (os.path.isdir(args.outDir)): os.makedirs(args.outDir)
    if args.tracks == 'nominal:pseudo:ideal:fakes_removed:fakes_removed_+_track_replaced:HF:HF_+_track_replaced:pseudo_not_reco':
        args.outDir += version + "_all"
    else: args.outDir += version + "_" + args.tracks.replace(":","_")
    
    saveDataFrames(args.inDir, args.outDir, version, tracks, args.dict)