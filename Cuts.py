# Author : S Middleton
# Date : 2021
# Purpose : Stores optional cuts

import sys

class Cuts() :

    def __init__(self):
        self.Cut_List =  {
            "de.t0" : [700., 1695],    #inTimeWindow
        }

    def ApplyCut(self, df):
        df_cut = df
        for key, value in self.Cut_List.items():
            df_cut = df_cut[(df_cut[key] > value[0]) & (df_cut[key] <= value[1])]
        return df_cut
