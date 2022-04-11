# Author : S Middleton
# Date : 2020
# Purpose : Prototype Importer Class

import sys
import uproot
import pandas
import math
import numpy
import matplotlib.pyplot as plt
from Cuts import *

class ImportRecoData :

    def __init__(self, CEfileName, DIOfileName , RPCextfileName=False, RPCintfileName=False, CosmicsfileName=False, treeName = "TrkAnaNeg", branchName = "trkana"):
        """ Initialise the Class Object """
        self.CEFileName= CEfileName
        self.DIOFileName= DIOfileName
        self.RPCextFileName= RPCintfileName
        self.RPCintFileName= RPCextfileName
        self.CosmicsFileName = CosmicsfileName
        self.TreeName = treeName
        self.BranchName = branchName
        self.cuts = Cuts()

    def Import(self, process, flatten = False):
        """ Import root tree and save it as a pandas dataframe """
        df = []
        if process == "signal":
            input_file = uproot.open(self.CEFileName)
            input_tree = input_file[self.TreeName][self.BranchName]
            df = input_tree.pandas.df(flatten=flatten)

        if process == "DIO":
            input_file = uproot.open(self.DIOFileName)
            input_tree = input_file[self.TreeName][self.BranchName]
            df = input_tree.pandas.df(flatten=flatten)

        return df

    def GetFeature(self, process, feature, flatten=False, Cuts=False):

        filename = ""
        if process == "signal":
            filename = self.CEFileName
        if process == "DIO":
            filename = self.DIOFileName

        input_file = uproot.open(filename)
        input_tree = input_file[self.TreeName][self.BranchName]
        df = input_tree.pandas.df(flatten=flatten)
        df.sort_values(by=[feature])
        if Cuts==True:
            df = self.cuts.ApplyCut(df)
        return df[feature]

    def get1DHist(self, process, feature, maxb, minb, nBins):
        """ Basic funciton to make a plot of a feature """
        #To make a plot: plot1DHist(options.CE, "TrkAnaNeg", "trkana", "deent.mom")
        filename = ""
        if process == "signal":
            filename = self.CEFileName
        if process == "DIO":
            filename = self.DIOFileName

        input_file = uproot.open(filename)
        input_tree = input_file[self.TreeName][self.BranchName]
        df = input_tree.pandas.df(flatten=False)
        if Cuts==True:
            df = self.cuts.ApplyCut(df)

        fig, ax = plt.subplots(1,1)
        n, bins, patches = ax.hist(df[feature],
                                   bins=nBins,
                                   range=(minb,maxb),
                                   label="electrons")

        ax.set_ylabel('N')
        ax.set_xlabel(str(feature))
        fig.savefig(str(process)+"_"+str(feature)+'.pdf')
        return n, bins

    def getAll(self, processes, process_weights, colors, feature, maxb, minb, nBins):
        """ Basic funciton to make a plot of a feature """
        #To make a plot: plot1DHist(options.CE, "TrkAnaNeg", "trkana", "deent.mom")
        fig, ax = plt.subplots(1,1)
        for i, process in enumerate(processes):
            filename = ""
            w = []
            if process == "signal":
                filename = self.CEFileName
            if process == "DIO":
                filename = self.DIOFileName

            input_file = uproot.open(filename)
            input_tree = input_file[self.TreeName][self.BranchName]
            df = input_tree.pandas.df(flatten=False)
            if Cuts==True:
                df = self.cuts.ApplyCut(df)

            for k, l in enumerate(df[feature]):
                w.append(process_weights[i])


            n, bins, patches = ax.hist(df[feature],
                                       weights = w,
                                       color = colors[i],
                                       bins=nBins,
                                       range=(minb,maxb),
                                       histtype = "step",
                                       label=str(process))

            ax.set_ylabel('Entries per bin')
            ax.set_xlabel("Reconstructed Momentum [MeV/c]")
            ax.set_yscale('log')
            plt.legend(loc="upper right")
        fig.savefig(str(feature)+'.pdf')


    def GetMagFeature(self, process, feature_x, feature_y, feature_z, flatten=False ):

        filename = ""
        if process == "CE":
            filename = self.CEFileName
        if process == "DIO":
            filename = self.DIOFileName
        input_file = uproot.open(filename)
        input_tree = input_file[self.TreeName][self.BranchName]
        df = input_tree.pandas.df(flatten=flatten)
        df_tot = []
        for i, j in enumerate(df[feature_x]):
            fx = j
            fy = df[feature_y][i]
            fz = df[feature_z][i]
            df_tot.append(math.sqrt(fx*fx+fy*fy+fz*fz))
        return df_tot
