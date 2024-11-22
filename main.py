import pandas as pd
import matplotlib.pyplot as plt
import json
import requests

url = "https://api.bluelytics.com.ar/v2/evolution.json"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
else:
    raise RuntimeError(f"Failed to fetch data. HTTP Status Code: {response.status_code}")

df['date'] = pd.to_datetime(df['date'])

x = []
y = []
for source in ('Oficial', 'Blue'):
    df_source = df.loc[df.source == source]
    x.append(df_source['date'])
    y.append(df_source['value_sell'])

# remove dates that are not present in both series
x[0] = x[0][x[0].isin(x[1])]
y[0] = y[0][x[0].index]
x[1] = x[1][x[1].isin(x[0])]
y[1] = y[1][x[1].index]

x = [x[0].to_numpy(), x[1].to_numpy()]
y = [y[0].to_numpy(), y[1].to_numpy()]

fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(x[0], (y[1] / y[0] - 1) * 100)
ax.set_title('Exchange rate gap (%)')
ax.grid()
ax.set_xlabel('Date')
ax.set_ylim(0)
ax.set_xlim(pd.Timestamp('2023-01-01'), x[0].max())
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig('exchange_rate_gap.png', dpi=600, bbox_inches='tight')