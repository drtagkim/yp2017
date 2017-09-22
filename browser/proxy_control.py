import pandas as pd
def get_proxy_free(excel_name):
    assert excel_name.lower().endswith("xlsx"),"Should have a xlsx file!"
    excel=pd.ExcelFile(excel_name)
    df=excel.parse()
    result=[]
    size=df.shape[0]
    for i in range(size):
        result.append({"http":"http://"+str(df.iloc[i,0])+":"+str(df.iloc[i,1]),
                      "https":"https://"+str(df.iloc[i,0])+":"+str(df.iloc[i,1])})
    return result