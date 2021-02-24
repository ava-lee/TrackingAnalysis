# -*- coding: utf-8 -*-
import pickle
import collections
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker

def getDict(inDir, version, track, varsName, add_file=""):
    varsFile = inDir + version + '_' + track + '_' + varsName + '.pickle'
    with open(varsFile, 'rb') as handle:
        varsDict = pickle.load(handle)
    
    return varsDict

def getDataFrames(workDir, version, tracks, varsType, dictName=""):
    fileName = workDir + 'dataFrames/'+ version+ "_all_" + varsType + "_dfs.pickle"
    if os.path.exists(fileName) == False:
        fileName = workDir + 'dataFrames/' + version + "_" + '_'.join(tracks) + "_" + varsType + "_dfs.pickle"
    if dictName != "":
        fileName = workDir + 'dataFrames/' + dictName
    with open(fileName, 'rb') as handle:
        allDFsDict = pickle.load(handle)
    trackDFsDict = collections.OrderedDict()
    for i in range(len(tracks)):
        trackDFsDict[tracks[i]] = allDFsDict[tracks[i]]
    return trackDFsDict

def getArray(track, dataFrames, varName):
    df_track = dataFrames[track]
    if varName == 'jet_trk_nPixSCT':
        nPix = df_track['jet_trk_nPixHits']
        nSCT = df_track['jet_trk_nSCTHits']
        array = nPix + nSCT
    elif varName == 'jet_trk_nsharedPixSCT':
        nPix = df_track['jet_trk_nsharedPixHits']
        nSCT = df_track['jet_trk_nsharedSCTHits']
        array = nPix + nSCT
    else: array = df_track[varName]
    
    return array

def fetchArrays(dataFrames, varName):
    arraysDict = collections.OrderedDict()
    for track in dataFrames.keys():
        tmpArray = getArray(track, dataFrames, varName)
        tmpArray = tmpArray[~np.isnan(tmpArray)]
        arraysDict[track] = tmpArray
    return arraysDict

def styleTracks():
    styleDict = {
            'nom': ["#000000", "Nominal"],
            'pseudo': ["#17becf", "Pseudo"],
            'ideal': ["#ff7f0e", "Ideal"],
            '427081_nom': ["#fc0303", "Extended Z' (with pileup)"],
            'default': ["#17becf", "Official FTAG"],
            'nom-leaky': ["#2ca02c", "Nominal, Leaky ReLU"],

            'nom_RF75': ["#2ca02c", "Nominal, no fakes (TMP > 0.75)"],
            'nom_RF75_replaceFRAGWithTruth': ["#d62728", "Nominal, no fakes (TMP > 0.75), replace with pseudo"],
            'nom_RF90': ["#e377c2", "Nominal, no fakes (TMP > 0.90)"],
            'nom_RF75NB': ["#00ff00", "Remove non-B fakes (TMP < 0.75)"],
            'loose': ["#76cfe3", "Nominal, removing fakes with MVA (loose)"],
            'tight': ["#1900ff", "Nominal, removing fakes with MVA (tight)"],
            'nom_RFNBMVA_A': ["#ff0000", "Removing non-B fakes with MVAs (A)"],
            'nom_RFNBMVA_B': ["#fa9750", "Removing non-B fakes with MVAs (B)"],

              #'RF75': ["#2ca02c", "Nominal, no fakes"],
            #'loose': ["#1f77b4", "Nominal, removing fakes with MVA (loose)"],
            #'tight': ["#8c564b", "Nominal, removing fakes with MVA (tight)"],

            'nom_replaceHFWithTruth': ["#9467bd", "Nominal, replace HF with pseudo"],
            'nom_replaceFRAGWithTruth': ["#7f7f7f", "Nominal, replace HF with pseudo"],
            'nom_replaceFRAGHFWithTruth': ["#bcbd22", "Nominal, replace FRAG+HF with pseudo"],
            'nom_replaceFRAGHFGEANTWithTruth': ["#2ca02c", "Nominal, replace FRAG+HF+GEANT with pseudo"],
            'nom_replaceWithTruth': ["#e377c2", "Nominal, replace with pseudo"],
            'RF50': ["#8c564b", "Nominal, no fakes (TMP > 0.5)"],
            'RF75': ["#2ca02c", "Nominal, no fakes (TMP > 0.75)"],
            'RF90': ["#e377c2", "Nominal, no fakes (TMP > 0.9)"],
            'Rd0Pull': ["#ff7f0e", "Nominal, no fakes (d0 pull < 10)"],
            'RF75B': ["#f50fae", "Nominal, no GEANT from B"],
            'RGB': ["#f09f59", "Nominal, no B fakes (TMP > 0.75)"],
            #'fakes_removed_+_track_replaced': "#d62728",
            #'HF': "#9467bd",
            #'HF_+_track_replaced': "#e377c2",
            #'fake': "#bcbd22",
            #'pseudo_not_reco': "#7f7f7f"
    }
    return styleDict

def getRatio(hist1,hist2):
    # basically dividing arrays
    hist = []
    for i in range(len(hist1)):
        if hist2[i] == 0:
            if hist1[i] == 0: value = 1
            else: value = 0
        else: value = hist1[i]/hist2[i]
        hist.append(value)
    return hist

def setStyle(width=600, height=550, label_size=9, my_dpi=100):
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['xtick.labelsize'] = label_size 
    plt.rcParams['ytick.labelsize'] = label_size 
    plt.rcParams['axes.labelsize'] = label_size 
    fig = plt.figure(figsize=(600/my_dpi, 550/my_dpi), dpi=my_dpi)
    return fig

def configureHistRatioPads(varName, varLabel, yLabel, xMin, xMax):
    fig = setStyle()
    gs = gridspec.GridSpec(2,1 , height_ratios=[4,1])
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    fig.subplots_adjust(hspace=0.07)
    fig.align_ylabels()
    
    # Settings for x and y-axis
    ax1.xaxis.set_visible(False)
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax1.set_ylabel(yLabel, horizontalalignment='right', y=1.0)
    ax1.set_xlim([xMin, xMax])
    
    ax2.set_ylabel("Ratio", horizontalalignment='right', y=1.0)
    ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax2.set_xlabel(varLabel, horizontalalignment='right', x=1.0)
    ax2.set_xlim([xMin, xMax])
    ax2.set_xticks(range(xMin,xMax))
    ax2.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax2.xaxis.set_major_locator(ticker.MaxNLocator())
    if 'n' in varName:
        ax2.set_xticks(np.arange(xMin+0.5,xMax+0.5,1), minor=True)
        ax2.set_xticklabels(np.arange(xMin,xMax), minor=True)
        ax2.set_xticklabels([])
        ax2.set_xticks([])
        
    return ax1, ax2

def newDataFrames(dataFrames, varNames):
    new_dfs = collections.OrderedDict()
    for track in dataFrames.keys():
        new_df = dataFrames[track].filter(varNames, axis=1)
        new_dfs[track] = new_df
    return new_dfs

def getCutValues(jet_df, cutVarName, cutVarMin, cutVarMax, outVarQuery, npoints):
    njets = len(jet_df.index)
    jet_df = jet_df[jet_df[cutVarName] >= cutVarMin]
    jet_values = []
    for i in range(npoints):
        x = cutVarMax / npoints
        cutValue = i * x
        jetCut_df = jet_df.query("("+ cutVarName + ">" + str(cutValue) + ") and (" + outVarQuery + ")")
        jet_values.append(len(jetCut_df.index) / njets)

    return jet_values

def getROC(dataFrames, varNames, cutVarName, cutVarMin, cutVarMax, outVarQuery, npoints):
    ROC_dfs = newDataFrames(dataFrames, varNames)
    ROC_values = collections.OrderedDict()
    for track in ROC_dfs.keys():
        track_df = ROC_dfs[track]

        jets = {"b": 5, "c": 4, "light": 0}
        for jet in jets.keys():
            jet_df = track_df[track_df['jet_LabDr_HadF'] == jets[jet]]
            jet_values = getCutValues(jet_df, cutVarName, cutVarMin, cutVarMax, outVarQuery, npoints)
            label = track + "_" + jet
            ROC_values[label] = jet_values

    return ROC_values

def integrateHist(hist_freqs,integration_interval,x_domain,nbin):
    dx=x_domain[1]-x_domain[0]
    
    # Get index from xMin to min and max of interval using proportion of interval to domain
    i_min=int(round(nbin*(integration_interval[0]-x_domain[0])/dx)) 
    i_max=int(round(nbin*(integration_interval[1]-x_domain[0])/dx)) 
    
    return hist_freqs[i_min:i_max].sum()

# sign = -1 for decreasing fn and +1 for increasing fn
def inverseFunction(y, function, x_domain, sign):
    epsilon = 1e-7
    x_max = x_domain[1]
    x_min = x_domain [0] # Start testing with x value in middle
    dx = x_max - x_min
    y_diff = 1
    while abs(y_diff) > epsilon and abs(dx) > epsilon:
        x0 = 0.5*(x_max + x_min)
        
        y_test = function(x0)
        y_diff = y - y_test
        # If y is greater than y_test for increasing fn
        # then increase x_min to x0 to decrease guessing gap
        # If y is greater than y_test for decreasing fn
        # then this would be negative
        # x_min to x0 to decrease guessing gap
        
        if y_diff*sign > 0: # If y is greater than y_test
            x_min = x0 # Increase x_min to 
        if y_diff*sign <= 0:
            x_max = x0
        
        dx = x_max - x_min
        
    return x0


