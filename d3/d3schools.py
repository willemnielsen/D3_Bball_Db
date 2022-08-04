import numpy as np
import pandas as pd
import uuid



def makeDF(filepath):
    with open(filepath) as f:
        lines = f.readlines()
    for index, item in enumerate(lines):
        lines[index] = item.rstrip()
    columns = lines[:5]
    arr = np.array(lines[5:])
    nrows = len(arr) // 5
    reshaped = arr.reshape(nrows, 5)
    df = pd.DataFrame(reshaped, columns=columns)
    df.drop(['Division'], axis=1, inplace=True)

    rows = df.index
    ids = [uuid.uuid4().time_low for i in rows]
    seriesids = pd.Series(ids)
    df.insert(0, "id", seriesids)
    df.to_csv('~/d3out/preproces.csv')
    return df

def makeDict(filepath):
    with open(filepath) as f:
        lines = f.readlines()
    for index, item in enumerate(lines):
        lines[index] = item.rstrip()
    arr = np.array(lines[5:])
    nrows = len(arr) // 5
    reshaped = arr.reshape(nrows, 5)
    schools = []
    for i, row in enumerate(reshaped):
        schools.append({})
        schools[i]['School'] = (row[0])
        schools[i]['City and State'] = (row[1])
        schools[i]['Region'] = (row[2])
        schools[i]['Conference'] = (row[3])
        schools[i]['Division'] = (row[4])
    return schools





# conn = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(mysecrets.dbuser, mysecrets.dbpass, mysecrets.dbhost, mysecrets.dbname)




#
# df = pd.DataFrame(lines)
# table = [lines[5:10]]
# df2 = pd.DataFrame(table, columns=columns)
# display(df2)


