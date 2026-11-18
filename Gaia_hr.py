import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# --- Load ---

df = pd.read_csv('data/1790612850920A.csv')
print("Original number of stars:", len(df))


# --- We Clean ---

df = df.dropna(subset=['Plx', 'Gmag', 'BP-RP', 'e_Plx'])

df = df[df['Plx'] > 0]

print("After cleaning:", len(df))


# --- Distance from parallax (mas -> parsecs) ---

df['dist_pc'] = 1000 / df['Plx']


# --- Absolute magnitude ---

df['absmag'] = df['Gmag'] - 5 * (np.log10(df['dist_pc']) - 1)



# --- Parallax Uncertainty ---

df['rel_plx_error'] = df['e_Plx'] / df['Plx']

print("\nRelative parallax uncertainty:")
print(df['rel_plx_error'].describe())

# Keep stars with relative parallax uncertainty below 20%

df = df[df['rel_plx_error'] < 0.20].copy()

print("\nStars after parallax filtering:", len(df))


# --- Display statistics ---

print(df[['BP-RP', 'absmag', 'Gmag', 'Plx','e_Plx', 'rel_plx_error']].describe())


# --- HR Diagram ---

plt.figure(figsize=(8, 10))
plt.scatter(df['BP-RP'],df['absmag'],s=4,alpha=0.4)
plt.gca().invert_yaxis()
plt.xlabel('BP - RP (color index)')
plt.ylabel('Absolute magnitude')
plt.title('Color-Magnitude Diagram of HD Stars (Gaia DR3)')
plt.savefig('gaia_hd.png', dpi=300)
plt.show()