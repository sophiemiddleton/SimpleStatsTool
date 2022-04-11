#!/usr/bin/python
# Author: S Middleton
# Date: 2020
# Purpose: Import Data to StatsTool

import uproot
import sys
import argparse
import math
from optparse import OptionParser
from Mu2eNegFunctions import YieldFunctions
from ImportRecoData import ImportRecoData
from ImportGenData import ImportGenData
from Constants import *
from Results import Results
from csv import reader


def main(options, args):

    print("=====================================================================")
    print("=======================Launching StatsTool===========================")
    print("=====================Written by S. Middleton=========================")
    print("==================For the Mu2e-II Sensitvity Study===================")
    print("=========================smidd@caltech.edu===========================")
    print("=====================================================================")
    print("===================calculating stats....please wait....==============")

    # Pandas offers the most flexible analysis - arguments are used for window optimization only:
    constants = Constants(options.target, options.exp)
    func = YieldFunctions(constants)
    lower_limit = constants.conversion - constants.window_width  # MeV/c
    CEEff, DIOEff = GetEff(constants.nBins, lower_limit, constants.higher_limit)
    CzerneckiIntegral = GetCzerneckiIntegral(lower_limit, constants.conversion)
    #nDIO = func.GetDIOExpectedYield(DIOEff,CzerneckiIntegral)
    #nCE = func.GetSignalExpectedYield(CEEff,BF)
    #SES = func.GetSES(CEEff)
    MakePlot(constants.nBins, 100, constants.higher_limit, DIOEff, CEEff, constants.BF, CzerneckiIntegral, constants.POT, constants.decaysperStop, constants.capturesperStop, constants.muonstopsperPOT, constants.nGen)
    #print(nDIO,nCE, SES)

def MakePlot(nbins, mom_low, mom_high, DIOEff, CEEff, BF,CI, POT, DecayRate, CaptureRate, Stops, Gen):
    recodata = ImportRecoData(options.CEReco, options.DIOReco)
    print("DIO weight", CI*POT*DecayRate*Stops/1e6)
    recodata.getAll(["signal","DIO"],[BF*POT*CaptureRate*Stops/Gen,CI*POT*DecayRate*Stops/Gen],["orange","green"],"deent.mom",mom_high,mom_low,nbins)

def GetEff(nbins, mom_low, mom_high):

    # Import the data into panadas dataframes:
    recodata = ImportRecoData(options.CEReco, options.DIOReco)
    gendata = ImportGenData(options.DIOReco)

    nCE_list = []
    nDIO_list = []

    # CE:
    nCE,  binsCE = recodata.get1DHist("signal","deent.mom", mom_high,100,nbins)

    # get integral for CE
    nCE_u = nbins
    nCE_l = 0
    integralCE = 0.
    for i, j in enumerate(binsCE):
       if nCE_l == 0 and j > mom_low:
           nCE_l = i
       if nCE_l !=0 and i < nCE_u:
           integralCE += nCE[nCE_l]

    #print(nCE_u,nCE_l,nCE[nCE_l],integralCE)
    print("CE Eff = ",integralCE/1e6)

    # DIO:
    nDIO, binsDIO = recodata.get1DHist("DIO","deent.mom", mom_high,100,nbins)
    #nDIO_Gen, binsDIO_Gen = gendata.get1DHist("DIO","genmom", mom_high,100,nbins)
    # TODO - need a list o nCE and nDIO in each bin
    # get integral for DIO
    nDIO_u = nbins
    nDIO_l = 0
    integralDIO = 0.
    for i,j in enumerate(binsDIO):
       if nDIO_l == 0 and j > mom_low:
           nDIO_l = i
       if nDIO_l !=0 and i < nDIO_u:
           integralDIO += nDIO[nDIO_l]

    #print(nDIO_u,nDIO_l,nDIO[nDIO_l],integralDIO)
    print("DIO Eff = ",integralDIO/1e6)

    # pass the lists to the minimizer
    return integralCE/1e6, integralDIO/1e6

"""
def BestSES():
    SES = 1.0
    best_i =0
    for i in range(1030,1042):
        n = i/10
        CEEff, DIOEff = GetEff(50, n, n+1)
        temp_SES = func.GetSES(CEEff)
        if temp_SES < SES:
            SES  = temp_SES
            best_i = n
            print("updated",n,n+1)
        print(SES)
    print("Best SES",SES,"best_i", best_i)
"""
def GetCzerneckiIntegral(mom_low, mom_high):
    integral = 0.
    f = reader(open("Czar.csv"))
    header = next(f)
    for energy,count in f:
        if float(energy) < mom_high and float(energy) > mom_low:
            integral += float(count)
    print(integral)
    return integral

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    parser.add_option('-a','--CEReco', dest='CEReco', default = 'CEData.root',help='NTuple with CE', metavar='Cedir')
    parser.add_option('-g','--CEGen', dest='CEGen', default = 1e6,help='N Gen CE', metavar='Cedir')
    parser.add_option('-o','--DIOReco', dest='DIOReco', default = 'DIOData.root',help='NTuple with DIO', metavar='Diodir')
    parser.add_option('-p','--DIOGen', dest='DIOGen', default = 'DIOGen.root',help='NTuple with DIO', metavar='Diodir')
    parser.add_option('-s','--target', dest='target', default = 'mu2e',help='target', metavar='stopsdir')
    parser.add_option('-t','--exp', dest='exp', default = 'mu2e',help='experiment', metavar='stopsdir')
    parser.add_option('-l','--stops', dest='stops', default = '9e-5',help='MuonStopsPerPOTt', metavar='stopsdir')
    (options, args) = parser.parse_args()

    main(options,args);
    print("Finished")
