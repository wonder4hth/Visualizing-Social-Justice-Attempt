import pandas as pd
import matplotlib as plt
import seaborn as sns
from matplotlib.dates import DateFormatter

plt.style.use('ggplot')
sns.set_palette('husl')

public_use = pd.read_csv("../data/Monthly Public Use.csv", skiprows = [1])
traffic = pd.read_csv("../data/Traffic Counts.csv", skiprows = [1,2])
visitation_by_month = pd.read_csv("../data/Visitation by Month.csv", skiprows = [1,2])

def clean_numeric(value):
    if isinstance(value, str):
        return float(value.replace(',', '').replace('%',''))
    return value

public_use_2025 = public_use.iloc[0:1]
public_use_metric = {
    "Total Visitors" : clean_numeric(public_use_2025["Field10"].values[0]),
    "Total Programs" : clean_numeric(public_use_2025["Field40"].values[0]),
    "Total Vehicles" : clean_numeric(public_use_2025["Field20"].values[0])
}
traffic = traffic[traffic['GroupDescription'] == 'TRAFFIC COUNT AT MAIN ENTRANCE']
traffic = traffic.applymap(clean_numeric)
traffic['Date'] = pd.to_datetime(traffic['Year'].astype(str) + '-05-01')

visitation = visitation_by_month.applymap(clean_numeric)
visitation["Date"] = pd.to_datetime(visitation['Year'].astype(str) + '-05-01')

merged = pd.merge(
    traffic[['Year', 'MAY', 'AnnualTotal']].rename(columns={'MAY': 'May_Traffic', 'AnnualTotal': 'Annual_Traffic'}),
    visitation[['Year', 'MAY', 'AnnualTotal']].rename(columns={'MAY': 'May_Visits', 'AnnualTotal': 'Annual_Visits'}),
    on='Year'
)

correlation = merged.corr()

plt.figure(figsize=(12, 8))
# May Traffic vs May Visits
plt.subplot(2, 2, 1)
plt.plot(merged['Year'], merged['May_Traffic'], label='May Traffic')
plt.plot(merged['Year'], merged['May_Visits'], label='May Visits')
plt.show()
