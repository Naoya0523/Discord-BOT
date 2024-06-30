import pandas as pd

df = {'test':[0,3,4],
      'www':[8,4,5]}

df = pd.DataFrame(df)

main = pd.read_excel('test.xlsx')
join_file = pd.merge(main, df, how='outer')
join_file = join_file.drop_duplicates(subset='test', keep='first')
join_file.to_excel('join.xlsx',index=False)