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
parser.add_argument('-w', "--workDir", dest='workDir', default='/Users/avalee/TrackingAnalysis/',
                    help='working directory')
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
    inDir = args.workDir + 'trackDicts/' 
    version = args.version
    tracks = args.tracks.split(':') # get list of tracks
    outDir = args.workDir + 'dataFrames/'
    if not (os.path.isdir(outDir)): os.makedirs(outDir)
    if args.tracks == 'nominal:pseudo:ideal:fakes_removed:fakes_removed_+_track_replaced:HF:HF_+_track_replaced:pseudo_not_reco':
        outDir += version + "_all"
    else: outDir += version + "_" + args.tracks.replace(":","_")
    
    saveDataFrames(inDir, outDir, version, tracks, args.dict)