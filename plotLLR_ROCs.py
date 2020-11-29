#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from helpers import *
from createDataFrames import getDict
import argparse
import numpy as np
import pandas as pd
import math
import pickle
import matplotlib.pyplot as plt
import os
import scipy
from scipy import signal

parser = argparse.ArgumentParser(description='Get LLR values for jet dictionaries')
parser.add_argument('-v', "--version", dest='version', default='427080_Zprime_V5', help='input sample versions')
parser.add_argument('-t', "--tracks", dest='tracks', default='nom:RF75:RF75NB:loose:tight:A:B',help='input track collections')
parser.add_argument('-w', "--workDir", dest='workDir', default='/Users/avalee/TrackingAnalysis/', help='working directory')
parser.add_argument('-i', "--inDir", dest='inDir', default='/Users/avalee/',
                    help='inputs directory')
parser.add_argument('-d' "--dict", dest="dict", default="jetVars", help="type of variables dictionary to save") #what dictionary comment is
args = parser.parse_args()

def getLLRvalues(inDir, version, tracks, varsName, add_cuts=''):
    nbins = 1400
    xMin = -10
    xMax = 10
    xRange = [xMin, xMax]
    
    LLR_values = {}
    for track in tracks:
        print (track)
        varsDict = getDict(inDir, version, track, varsName)
        df = pd.DataFrame.from_dict(varsDict)
        if add_cuts != "":
            df.query(add_cuts, inplace=True)
        
        if '410470' in version: tot = {"b": 1861955, "c": 483378, "l": 7868892}
        if '427081' in version: tot = {"b": 2063898, "c": 2429370, "l": 22950682}
        
        jets = {"b": 5, "c": 4, "l": 0}
        llr = {} #lists of llr
        freqs = {}
        for jet in jets.keys():
            llr[jet] = df.query('jet_LabDr_HadF ==' + str(jets[jet]) + ' & jet_jf_llr !=-99')['jet_jf_llr'].tolist()
            freqs[jet], _ , _ = plt.hist(llr[jet], range=(xMin, xMax), bins=nbins)
            #print (len(llr[jet]))

        max_bEff = len(llr['b'])/tot['b']
        effPoints = np.linspace(0.1, 1, nbins)
        l_rejs = []
        c_rejs = []
        for eff in effPoints:
            if eff < max_bEff:
                # solve for t
                cut = inverseFunction(eff,lambda x: integrateHist(freqs['b']/tot['b'],[x,xMax],xRange,nbins),xRange,-1)
                l_eff = integrateHist(freqs['l'], [cut, xMax], xRange, nbins)/tot['l']
                l_rejs.append(1/l_eff)
                c_eff = integrateHist(freqs['c'], [cut, xMax], xRange, nbins)/tot['c']
                c_rejs.append(1/c_eff)
        
        LLR_values[track + '_b'] = effPoints[:len(l_rejs)]
        LLR_values[track + '_c'] = c_rejs
        LLR_values[track + '_l'] = l_rejs
        
    return LLR_values


def configureRatioPads(jet1, jet2, xMin, xMax):
    fig = setStyle()
    gs = gridspec.GridSpec(2,1 , height_ratios=[4,1])
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    fig.subplots_adjust(hspace=0.07)
    fig.align_ylabels()
    
    # Settings for x and y-axis
    ax1.xaxis.set_visible(False)
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.05))
    if jet2 == "c":
        ax1.set_ylabel(r'$%s$-jet rejection' % (jet2), horizontalalignment='right', y=1.0)
    else:
        ax1.set_ylabel(r'$light$-jet rejection', horizontalalignment='right', y=1.0)
    ax1.set_xlim([xMin, xMax])
    ax1.set_yscale('log')

    ax2.set_ylabel("Ratio", horizontalalignment='right', y=1.0)
    ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax2.set_xlabel(r'$%s$-jet efficiency' % (jet1), horizontalalignment='right', x=1.0)
    ax2.set_xlim([xMin, xMax])
    ax2.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
    
    return ax1, ax2


def wsize(y_array):
    w = int(len(y_array)/10)
    if w%2 == 0:
        w += 1
    return w


def plotLLRrocs(LLR_dict, version, jet1, jet2, xMin, xMax, outDir, add_text='', add_filename=''):
    figName = "ROC_" + version + "_" + jet1 + jet2
    if add_filename != '': figName += '_' + add_filename
    
    # Plot histograms
    ax1, ax2 = configureRatioPads(jet1, jet2, xMin, xMax)
    oth_nom = LLR_dict['nom_' + jet2]
    oth_nom_smooth = signal.savgol_filter(oth_nom, wsize(oth_nom), 1)
    for track in tracks:
        b = LLR_dict[track + '_' + jet1] 
        oth = LLR_dict[track + '_' + jet2]
        oth_smooth = signal.savgol_filter(oth, wsize(oth), 1)

        ax1.plot(b, oth_smooth, color=styleDict[track][0], label=styleDict[track][1])
        # Get ratios
        ratio = [a/b for a,b in zip(oth_smooth, oth_nom_smooth)]
        ax2.plot(b,ratio, color=styleDict[track][0], linewidth=1)
    if jet2 == 'c':
        leg_xy = [0.38, 0.5]
    if jet2 == 'l':
        leg_xy = [0.02, 0.01]
    ax1.legend(bbox_to_anchor=leg_xy, loc='lower left', labelspacing=0.3, facecolor='none', edgecolor='none', prop={'size': 8})
    
    plt.text(0.75, 0.95, "ATLAS Internal", fontsize=9, transform=ax1.transAxes, weight='bold', style='italic')
    if '410470' in version: text = r'410470 ttbar'
    if '427080' in version: text = r"427080 Z'"
    if '427081' in version: text = r"427081 Z' ext"
    plt.text(0.75, 0.91, text, fontsize=9, transform=ax1.transAxes)
    plt.text(0.75, 0.87, add_text, fontsize=9, transform=ax1.transAxes)

    plt.savefig(outDir + "/" + figName + ".pdf", bbox_inches='tight', pad_inches=0.04)


if __name__ == "__main__":
    inDir = args.inDir
    version = args.version
    tracks = args.tracks.split(':') # get list of tracks
    outDir = args.workDir + 'LLRplots'
    if not (os.path.isdir(outDir)): os.makedirs(outDir)
    styleDict = styleTracks()
        
    LLR_dict = getLLRvalues(inDir, version, tracks, args.dict)
    #plotLLRrocs(LLR_dict, version, 'b', 'c', 0.1, 0.8, outDir)
    plotLLRrocs(LLR_dict, version, 'b', 'l', 0.1, 0.8, outDir)