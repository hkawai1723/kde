import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = './scatter_data.csv'

df = pd.read_csv(file_path, sep=',')
# print(df.head())

# plt.scatter(df['x'], df['y'])
sns.kdeplot(x=df['x'], y=df['y'], cmap='Reds', levels=5, bw_adjust=0.3)
plt.show()
