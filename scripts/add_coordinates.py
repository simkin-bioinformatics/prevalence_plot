metadata_file = "/home/charlie/projects/charlie_choropleths/new_data/DRC_metadata.tsv"
hfname_file = "/home/charlie/projects/charlie_choropleths/new_data/prevalences.tsv"
updated_file = "/home/charlie/projects/charlie_choropleths/new_data/prevalences_with_coords.tsv"
import pandas as pd


def update_summary_file(metadata_file, hfname_file, updated_file, dataset):
    mdf = pd.read_csv(metadata_file, sep = '\t')
    lat_dict = dict(zip(mdf['province'], mdf['Latitude']))
    lon_dict = dict(zip(mdf['province'], mdf['Longitude']))
    df = pd.read_csv(hfname_file, sep = "\t")
    df = df[df["province"] != 'overall']
    df.insert(1, "Latitude", df['province'].map(lat_dict))
    df.insert(2, "Longitude", df['province'].map(lon_dict))
    df.insert(3, "Dataset", dataset)

    ssdf = pd.DataFrame({})
    for column in (df.columns[4:]):
        ssdf[column] = df[column].str.split('(').str[1].str.split('/').str[1].str.split(')').str[0].astype(int)
        if (ssdf[column].sum()) == 0:
            df = df.drop(column, axis=1)
    for column in (df.columns[4:]):
        if '.1' in column:
            df = df.drop(column, axis=1)
    df.to_csv(updated_file, index=False)


    return df

df = update_summary_file(metadata_file, hfname_file, updated_file, 'DRC')

# complete_summary = pd.concat([df21, df22, df23])

# dot_error = complete_summary.loc[:,"HFname":"Dataset"]
# for column in complete_summary.columns:
#     if '.1' in column:
#         original = column.replace(".1","")
#         dot_error[original] = complete_summary[original]
#         dot_error[column] = complete_summary[column]
#     dot_error.to_csv('dot_1_errors.csv')


# complete_summary.to_csv('complete_summary.csv', index=False)
