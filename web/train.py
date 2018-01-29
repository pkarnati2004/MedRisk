import pandas as pd
import numpy as np
import glob
import datetime as dt
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit, StratifiedKFold
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV


# In[41]:

def run_model():
    path = 'static/data/learn'
    allFiles = glob.glob(path + "/*.csv")
    df = pd.read_csv(allFiles[0])
    df = df[["DESYNPUF_ID","BENE_BIRTH_DT","BENE_SEX_IDENT_CD","BENE_RACE_CD","SP_STATE_CODE","BENE_COUNTY_CD","SP_ALZHDMTA","SP_CHF","SP_CHRNKIDN","SP_CNCR","SP_COPD","SP_DEPRESSN","SP_DIABETES","SP_ISCHMCHT","SP_OSTEOPRS","SP_RA_OA","SP_STRKETIA"]]


    # In[42]:


    def splitDataFrameList(df,target_column,separator):
        ''' df = dataframe to split,
        target_column = the column containing the values to split
        separator = the symbol used to perform the split
        returns: a dataframe with each entry for the target column separated, with each element moved into a new row. 
        The values in the other columns are duplicated across the newly divided rows.
        https://gist.github.com/jlln/338b4b0b55bd6984f883
        '''
        def splitListToRows(row,row_accumulator,target_column,separator):
            split_row = row[target_column].split(separator)
            cnt = 0
            for s in split_row:
                if not s == '2':
                    new_row = row.to_dict()
                    new_row[target_column] = cnt
                    row_accumulator.append(new_row)
                cnt = cnt + 1
        new_rows = []
        df.apply(splitListToRows,axis=1,args = (new_rows,target_column,separator))
        new_df = pd.DataFrame(new_rows)
        return new_df

    df['Diseases'] = df[df.columns[6:]].apply(lambda x: ','.join(x.dropna().astype(int).astype(str)),axis=1)
    # df.head()

    df = splitDataFrameList(df, 'Diseases', ',')


    # In[43]:


    sf = pd.DataFrame(df, columns =['BENE_BIRTH_DT'])
    nf = pd.to_datetime(sf.BENE_BIRTH_DT, format='%Y%m%d')
    df['age'] = nf
    df['age'] = dt.date(2008, 1, 1) - df['age']
    df['age'] = df['age'].apply(lambda x: float(x.days)/365)
    # df


    # In[44]:


    # to_drop = ['BENE_BIRTH_DT', 'SP_ALZHDMTA', 'SP_CHF', 'SP_CHRNKIDN', 'SP_CNCR', 'SP_COPD', 'SP_DEPRESSN', 'SP_DIABETES', 'SP_ISCHMCHT', 'SP_OSTEOPRS', 'SP_RA_OA', 'SP_STATE_CODE', 'SP_STRKETIA']

    to_drop = ['BENE_BIRTH_DT']

    df = df.drop(to_drop, axis = 1)


    # In[45]:


    cols = list(df.columns.values) #Make a list of all of the columns in the df
    cols.pop(cols.index('Diseases'))
    cols.insert(0, cols.pop(cols.index('DESYNPUF_ID')))
    df = df[cols + ['Diseases']]

    # df.head()


    # In[46]:


    df.sort_values(['Diseases'], inplace = True)


    # In[47]:


    X = df.iloc[:, 1:-1]
    y = df.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42, shuffle=True)

    logisticRegr = LogisticRegression(multi_class='multinomial', solver='sag', max_iter=4000)
    fitModel = logisticRegr.fit(X_train, y_train)
    # predictions = fitModel.predict(X_test)

    coefs = fitModel.coef_
    coef_path = 'static/data/learn/coeff2.txt'
    np.savetxt(coef_path, coefs)

    predictions = fitModel.predict_proba(X_test)
    path = 'static/data/learn/output.txt'
    np.savetxt(path, predictions, '%10.3f')

    # print(predictions)

    scores = fitModel.score(X_test, y_test)
    # print(scores)




