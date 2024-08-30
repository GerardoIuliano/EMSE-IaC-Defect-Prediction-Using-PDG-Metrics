import pandas as pd

CSV = pd.read_csv("rq1/csv/best_predictors_pdg.csv")
print(CSV.to_latex(index=False))