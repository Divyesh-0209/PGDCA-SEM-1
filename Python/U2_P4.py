import pandas as pd, os


try:
    FILE=input("Enter data file name (CSV or JSON): ").strip()

    if FILE=="":
        raise Exception("NO FILE! Please enter a file name.")
    else:
        if os.path.exists(FILE) and os.path.isfile(FILE):
            if FILE.rsplit(".",2)[1]=="json":
                data=pd.read_json(FILE)
                
            elif FILE.rsplit(".",2)[1]=="csv":
                data=pd.read_csv(FILE)
                
            else:
                raise Exception("UNSUPPORTED FILE FORMAT! Not a valid 'csv' or 'json' file.")

            if data.empty:
                raise Exception("EMPTY FILE! No data in the file.")

            else:
                print(data)
                print("Number of records:",len(data.index))
                print("Fields:",len(data.columns))
                print("Field names:",list(data.columns))
                print("Missing values:",data.isna().sum().sum())
                
                numericFields=[]
                textual=[]
                other=[]
                for i, col in enumerate(data.dtypes):
                    if col == "int64" or col== "float64" :
                        numericFields.append(data.columns[i])
                    elif col == "str":
                        textual.append(data.columns[i])
                    else:
                        other.append(data.columns[i])

                print("Numeric data fields:",numericFields)
                print("Textual data fields:",textual)
                print("Other data fields:",other,"\n")
                print("\n Data summary:-\n",data.info())

                data.describe().to_json("analysis.json", indent=4)
        else:
            raise Exception("FILE MISSING! No such file.")

except Exception as e:
    print("Error:",e)

