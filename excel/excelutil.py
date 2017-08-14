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