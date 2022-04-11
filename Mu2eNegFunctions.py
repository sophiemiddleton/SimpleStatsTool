# Author : S Middleton
# Date : 2020
# Purpose : Stats functions

import sys
import math
import numpy

from StatsFunctions import *
from Constants import *

class YieldFunctions:

        def __init__(self, constants):
            self.constants = constants

        def GetPOT(self):
            return self.constants.POT

        def CapturesPerStop(self):
            return self.constants.capturesperStop

        def DecaysPerStop(self):
            return self.constants.decaysperStop

        def MuonStopsPerPOT(self):
            return self.constants.muonstopsperPOT


        def GetRecoEffError(self, Nrec, Ngen):
            """
            use Glen Cowan derivation of efficiency error based on a binomial distribution
            http://www.pp.rhul.ac.uk/~cowan/stat/notes/efferr.pdf
            """
            efficiency_error = math.sqrt(Nrec * (1. - Nrec/Ngen)) / Ngen
            return efficiency_error

        def GetDIOEffError(self, Nrec, Nrec_error, Ngen, Ngen_error):
            efficiency_error = math.sqrt( pow(Nrec_error / Ngen, 2) + pow( Nrec * Ngen_error / (Ngen*Ngen), 2) )
            return efficiency_error

        def GetSignalExpectedYield(self, efficiency_CE, BF_assumption):
            N_CE_expected = self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop() * BF_assumption * efficiency_CE
            return N_CE_expected

        def GetSES(self, efficiency_CE):
            SES = 1. / ( self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop() * efficiency_CE  )
            return SES

        def GetSESError(self, efficiency_CE, efficiency_error_CE):
            SES = 1. / ( self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop() * pow(efficiency_CE, 2) ) * efficiency_error_CE  # error propagation on SES calculation
            return SES

        def GetDIOExpectedYield(self,DIOeff,CzerneckiIntegral ):
            N_DIO_expected = DIOeff * CzerneckiIntegral * self.GetPOT() * self.MuonStopsPerPOT() * self.DecaysPerStop()
            return N_DIO_expected


        def GetBFUL(self, Nsig_UL, efficiency_CE):
            BF_upper_limit = Nsig_UL / ( self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop() * efficiency_CE )
            return BF_upper_limit

        def GetBFULError(self, Nsig_UL, Nsig_UL_error, efficiency_CE, efficiency_error_CE):
            BF_upper_limit_error = 1. / (self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop()) * math.sqrt(pow(Nsig_UL_error/efficiency_CE, 2)
            + pow(Nsig_UL * efficiency_error_CE/(efficiency_CE*efficiency_CE), 2))
            return BF_upper_limit_error
