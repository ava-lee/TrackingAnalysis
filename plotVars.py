#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from helpers import *
import argparse
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os

parser = argparse.ArgumentParser(description='Get dataframes for track dictionaries')
parser.add_argument('-v', "--version", dest='version', default='427080_Zprime_V5', help='input sample versions')
parser.add_argument('-t', "--tracks", dest='tracks',
                    default='nominal:pseudo:ideal:fakes_removed:fakes_removed_+_track_replaced:HF:HF_+_track_replaced',
                    help='input track collections')
parser.add_argument('-w', "--workDir", dest='workDir', default='/Users/avalee/TrackingAnalysis/',
                    help='working directory')
args = parser.parse_args()

def plotHisto(dataFrames, varName, xMin, xMax, xBins, varLabel, yLabel):
    figName = varName
    histoDict = fetchArrays(dataFrames, varName) # Fetch histograms
    
    # Plot histograms
    ax1, ax2 = configureHistRatioPads(varName, varLabel, yLabel, xMin, xMax)
    yMaxs = []
    for histKey in histoDict.keys():
        label = ' '.join(histKey.split('_'))
        y, x, _ = ax1.hist(histoDict[histKey], bins=xBins, range=(xMin,xMax), density=True, color=colourDict[histKey], histtype='step', label=label)
        yMaxs.append(y.max())
        
        # Get ratios
        histNom, bin_edges = np.histogram(histoDict["nominal"], bins=xBins, range=(xMin,xMax), density=True)
        hist, bin_edges = np.histogram(histoDict[histKey], bins=xBins, range=(xMin,xMax), density=True)
        ratio = getRatio(hist, histNom)
        
        # Plot ratios
        left,right = bin_edges[:-1],bin_edges[1:]
        X = np.array([left,right]).T.flatten()
        Y = np.array([ratio,ratio]).T.flatten()
        ax2.plot(X,Y, color=colourDict[histKey], linewidth=1)
    ax1.set_ylim([0, max(yMaxs)*1.4])
    
    # Draw a line for legend
    handles, labels = ax1.get_legend_handles_labels()
    new_handles = [Line2D([], [], c=h.get_edgecolor()) for h in handles]
    ax1.legend(loc="best", labelspacing=0.3, bbox_transform=ax1.transAxes, handles=new_handles, labels=labels, facecolor='none', edgecolor='none')
    
    plt.text(0.03, 0.93, "ATLAS Internal", fontsize=9, transform=ax1.transAxes, weight='bold', style='italic')
    
    plt.savefig(outDir + "/" + figName +".png", bbox_inches='tight', pad_inches=0.04)
    plt.savefig(outDir + "/" + figName +".pdf", bbox_inches='tight', pad_inches=0.04)
    
def plotAllHistos(varDict, dataFrames, yLabel="Arbitrary units"):
    for varName, varValues in varDict.items():
        xMin = varValues[0]
        xMax = varValues[1]
        xBins = varValues[2]
        varLabel = varValues[3]

        plotHisto(dataFrames, varName, xMin, xMax, xBins, varLabel, yLabel)

if __name__ == "__main__":
    colourDict = colourTracks()
    inDir = args.workDir + 'dataFrames/' 
    version = args.version
    tracks = args.tracks.split(':')
    outDir = args.workDir + 'plots/' + version + "/" + args.tracks.replace(":","_")
    if not (os.path.isdir(outDir)): os.makedirs(outDir)
    
    jetVars = getDataFrames(args.workDir, version, tracks, "jetVars")
    trackVars = getDataFrames(args.workDir, version, tracks, "trackVars")
    
    varTracksDict = {
        'jet_trk_nPixSCT': [0, 14, 14, 'Number of pixel and SCT hits'],
        'jet_trk_nsharedPixSCT': [0, 10, 10, 'Number of shared pixels and SCT hits'],
        'jet_trk_nPixHits': [0, 10, 10, 'Number of pixel hits'],
        'jet_trk_nSCTHits': [0, 14, 14, 'Number of SCT hits'],
        #'jet_trk_nsharedPixHits': [0, 10, 10, "Number of shared pixels"],
        #'jet_trk_nsharedSCTHits': [0, 10, 10, "Number of shared SCT"],
        #'jet_trk_nsplitPixHits': [0, 10, 10, "Number of split pixels"],     
    }

    varJetsDict = {
            'jet_jf_n2t': [0, 11, 11, "No. of 2-track vertex candidates"],
            'jet_jf_m': [0, 10, 100, 'Invariant mass of tracks from displaced vertices [GeV]'],
            #'jet_jf_sig3d': [0, 30, 100, "Weighted flight length sig."],
            #'jet_jf_efc': ["0, 1, 100, 'Energy fraction'],
            #'jet_jf_nvtx1t': [0, 6, 6, "No. of displaced vertices with 1 track"],
            #'jet_jf_nvtx': ["0, 4, 4, "No. of displaced vertices with more than 1 track"],
            #'jet_jf_ntrkAtVx': [0, 11, 11, "No. of tracks from vertices with at least 2 tracks"],
            #'jet_jf_dR': [0, 0.2, 100, '#DeltaR between jet axis and all tracks with displaced vertices'],

    }

    plotAllHistos(varJetsDict, jetVars)
    plotAllHistos(varTracksDict, trackVars)