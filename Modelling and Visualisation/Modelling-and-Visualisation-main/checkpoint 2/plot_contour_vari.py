import pandas as pd
import numpy as np
import time
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
np.set_printoptions(threshold=sys.maxsize)


df = pd.read_csv('contourQ3data.csv')
Z = df.pivot_table(index='p1', columns='p3', values='vari').T.values
X_unique = np.sort(df.p1.unique())
Y_unique = np.sort(df.p3.unique())
X, Y = np.meshgrid(X_unique, Y_unique)

fig, ax = plt.subplots()
CS = ax.contourf(X, Y, Z, cmap='RdGy')
ax.set_title('Contour plot of the behavour of avg I')
ax.set_xlabel('p1')
ax.set_ylabel('p3')
ax.set_aspect('equal')
fig.colorbar(CS, format="%.2f")
plt.show()
plt.savefig('contour-plot-of-vari-0.05.png', dpi=300)