#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from helpers import *
import argparse
import matplotlib.pyplot as plt
import os

parser = argparse.ArgumentParser(description='Get dataframes for track dictionaries')
parser.add_argument('-v', "--version", dest='version', default='427080_Zprime_V5', help='input sample versions')
parser.add_argument('-t', "--tracks", dest='tracks',
                    default='nominal:pseudo:ideal:fakes_removed:fakes_removed_+_track_replaced',
                    help='input track collections')
parser.add_argument('-w', "--workDir", dest='workDir', default='/Users/avalee/TrackingAnalysis/',
                    help='working directory')
args = parser.parse_args()


def configurePlots(jet1, jet2):
    fig = setStyle(500, 400)
    ax = plt.subplot()

    ax.set_xlabel(r'$%s$-jet efficiency' % (jet1), horizontalalignment='right', x=1.0)
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.05))
    if jet2 == "c":
        ax.set_ylabel(r'$%s$-jet efficiency' % (jet2), horizontalalignment='right', y=1.0)
    else:
        ax.set_ylabel('%s-jet efficiency' % (jet2), horizontalalignment='right', y=1.0)
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.05))

    return ax


def plotROCs(ROCValues, tracks, jet1, jet2):
    figName = "ROC_" + jet1 + jet2
    ax = configurePlots(jet1, jet2)

    for i in range(len(tracks)):
        key1 = tracks[i] + "_" + jet1
        key2 = tracks[i] + "_" + jet2
        label = tracks[i]
        label = ' '.join(label.split('_'))
        plt.plot(ROCValues[key1], ROCValues[key2], color=colourDict[tracks[i]], label=label)

    plt.legend(bbox_to_anchor=[0.05, 0.6], loc='center left', labelspacing=0.3, facecolor='none', edgecolor='none')
    plt.text(0.03, 0.93, "ATLAS Internal", fontsize=9, transform=ax.transAxes, weight='bold', style='italic')

    plt.savefig(outDir + "/" + figName + ".png", bbox_inches='tight', pad_inches=0.04)
    plt.savefig(outDir + "/" + figName + ".pdf", bbox_inches='tight', pad_inches=0.04)


if __name__ == "__main__":
    colourDict = colourTracks()
    inDir = args.workDir + 'dataFrames/'
    version = args.version
    tracks = args.tracks.split(':')
    outDir = args.workDir + 'plots/' + version + "/" + args.tracks.replace(":","_")
    if not (os.path.isdir(outDir)): os.makedirs(outDir)

    jetVars = getDataFrames(args.workDir, version, tracks, "jetVars")
    ROCVars = ['jet_jf_sig3d', 'jet_jf_nvtx', 'jet_LabDr_HadF']
    ROCValues = getROC(jetVars, ROCVars, 'jet_jf_sig3d', 0, 50, 'jet_jf_nvtx', 0, 50)

    plotROCs(ROCValues, tracks, "b", "light")
    plotROCs(ROCValues, tracks, "b", "c")



