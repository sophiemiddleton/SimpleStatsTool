# Author : S Middleton
# Date : 2021
# Purpose : Stores any constants used by the analysis

class Constants:

        def __init__(self, target, experiment):
            stops = 1.33e-4
            self.livegate = 700
            self.target = target

            self.window_width = 1.0 # MeV/c
            self.BF = 1e-17
            self.higher_limit = 105.5  # MeV/c
            self.nBins = 100
            self.nGen = 1e6


            self.DIOInt = 8.18e-12# 100-105
            if experiment == 'mu2e':
              self.POT= 3.6e20
            if experiment == 'mu2e2':
              self.POT = 4.4e22

            if target == 'Al':
                self.muonstopsperPOT = stops
                self.signal_start = 103.85
                self.signal_end = 105.1
                self.capturesperStop = 0.61
                self.decaysperStop = 0.39
                self.fixed_window_lower = 103.85
                self.fixed_window_upper = 105.1
            if target == 'Ti':
                self.muonstopsperPOT = stops
                self.capturesperStop = 0.85
                self.decaysperStop = 0.15
                self.signal_start = 103.25
                self.signal_end = 104.5
                self.fixed_window_lower = 103.25
                self.fixed_window_upper = 104.5
            if target == 'V':
                self.muonstopsperPOT =stops
                self.capturesperStop = 0.87
                self.decaysperStop = 0.13
                self.signal_start = 103.0
                self.signal_end = 104.25
                self.fixed_window_lower = 103.0
                self.fixed_window_upper = 104.25
                self.conversion = 104.154
            if target == 'Li':
                self.muonstopsperPOT =stops
                self.capturesperStop = 0.02
                self.decaysperStop = 0.98
                self.signal_start = 103.66
                self.signal_end = 104.91
                self.fixed_window_lower = 103.66
                self.fixed_window_upper = 104.91


            print("===================Information:============================")
            print("Number of Protons on Target:", self.POT)
            print("Target Material:", target)
            print("Muon Stopping Rate:", self.muonstopsperPOT)
            print("Captures Per Stop:", self.capturesperStop)
            print("Decays Per Stop:", self.decaysperStop)
            print("Default Signal Window (mom):", self.fixed_window_lower,"to",self.fixed_window_upper)
            print("===========================================================")
