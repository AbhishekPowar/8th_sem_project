def split_csv(file):
    import pandas as pd
    df = pd.read_csv(file+".csv")
    split_percent = 0.75
    df_length = int(len(df)*split_percent)
    df1 = df.iloc[:df_length,:]
    df2 = df.iloc[df_length:,:]
    df1.to_csv(file+"75.csv",index=False)
    df2.to_csv(file+"25.csv",index=False)

split_csv(file)

##give filename in quotes