from tkinter import *
from glob import glob
import pandas as pd
class Combiner:
    @classmethod
    def c(cls,dir,output):
        files=glob(dir+"/*.xls")
        data=pd.DataFrame()
        for file in files:
            a=pd.ExcelFile(file)
            b=a.parse()
            data=data.append(b)
        data.to_excel(output)
class ExcelOutput:
    @classmethod
    def export(cls,fname,names,data_frames):
        w=pd.ExcelWriter(fname)
        if len(names) != len(data_frames):
            return False
        for i in range(len(data_frames)):
            d=data_frames[i].to_excel(w,names[i])
        w.save()
        return True
            