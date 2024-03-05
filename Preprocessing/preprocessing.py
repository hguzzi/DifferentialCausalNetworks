#Preprocessing phase applied to excel file to obtain csv file with selected genes. 
import pandas as pd
df = pd.DataFrame(pd.read_excel("file_name.xlsx"))

#deletes first row
df.drop(df.index[0], axis = 0, inplace = True)

#deletes first column
df.drop(['Unnamed: 0'], axis = 1, inplace = True)

#list of columns
first_row = df.iloc[0,:]
columns = list(first_row)

# rename last columns
columns[846] = 'SEX'
columns[847] = 'AGE'
columns[848] = 'DTHHRDY'

#renames columns
df = df.set_axis(columns, axis="columns")

#delete first row containing the genes
df.drop(df.index[0], axis = 0, inplace = True)

#resets index
df.reset_index(inplace = True)
df.drop(['index'], axis = 1, inplace = True)

#delets NaN values
df.dropna(inplace = True)

#delets unnecessary columns
df = df.drop(columns = ['Descriptio'])
df = df.drop(columns = ['DTHHRDY'])

#transforms from object to int expression levels
for col in df.columns:
  if col  == 'SEX' or col == 'AGE':
    df = df.astype({col :'int64'})
  else:
    df = df.astype({col :'float64'})

#selects gene columns
genes = df.loc[:, ~df_copy.columns.isin(['SEX')]

#select values
values = genes.apply(lambda col: col.between(0, 20).sum())
#delets columns with more than 400 values in the range expression [0,20]
delete_genes= values[values > 400].index
df = df.drop(columns=delete_genes)

#save file csv
df.to_csv('name_file.csv')
