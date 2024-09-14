
import pandas as pd

data_2021=pd.read_csv("2021_prevalence_summary.tsv", sep="\t")
data_2022=pd.read_csv("2022_prevalence_summary.tsv", sep="\t")
data_2023=pd.read_csv("2023_prevalence_summary.tsv", sep="\t")


data_2021.insert(3, "Dataset", "2021")
data_2021 = data_2021[data_2021['HFname'] != 'overall']
data_2022.insert(3, "Dataset", "2022")
data_2022 = data_2022[data_2022['HFname'] != 'overall']
data_2023.insert(3, "Dataset", "2023")
data_2023 = data_2023[data_2023['HFname'] != 'overall']



combined = pd.concat([data_2021, data_2022, data_2023], axis=0)


combined.to_csv('combined.tsv', sep="\t", index=False)