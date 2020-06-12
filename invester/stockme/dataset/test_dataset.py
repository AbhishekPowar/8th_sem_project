import pandas as pd
path = 'tcs/tcsTest'
ext ='.csv'
df = pd.read_csv(path+ext)
df['dateTime'] = df.date
df[['date','time']] = df.date.str.split(expand=True)
df.date = df.date.apply(lambda x: ''.join(x.split('-')))
df.to_csv(path+'2'+ext,index=False)
print(df)