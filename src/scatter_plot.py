import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from hardcoded_data_sets import prem_fbs_names_2425, prem_fbs_prgp_2425, prem_fbs_prgc_2425

data = {
    "Player": prem_fbs_names_2425,
    "PrgP": prem_fbs_prgp_2425,
    "PrgC": prem_fbs_prgc_2425
}
df = pd.DataFrame(data)

# Scatter plot initialisation
plt.figure(figsize=(12, 7))
plt.scatter(df["PrgP"], df["PrgC"], s=50, alpha=0.9, color="darkblue")

# Extend axes past dataset limit
plt.xlim(0, df["PrgP"].max() + 1)
plt.ylim(0, df["PrgC"].max() + 1)
plt.tick_params(axis='both', which='both', length=0)

# Force axis labels to be integers
ax = plt.gca()
ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

# Watermark
ax.text(0.645, 0.3275, 'Data-Driven Spurs', transform=ax.transAxes, fontsize=18, color='darkblue', alpha=0.5,
        ha='center', va='center')

# Remove zeroes from axis labels
yticks = plt.yticks()[0]
yticks = [t for t in yticks if t != 0]
plt.yticks(yticks)
yticks = plt.xticks()[0]
yticks = [t for t in yticks if t != 0]
plt.xticks(yticks)

# Remove top and right borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Make grid visible
ax.grid(True, linestyle='--', alpha=0.5)

# Label top 8 points with x and y both in the top 50%, top 1 point in the, and top 1 point in the x
best_prgp = df.nlargest(1, "PrgP")
best_prgc= df.nlargest(1, "PrgC")
p50_pass = df["PrgP"].median()
p50_carry = df["PrgC"].median()
eligible = df[(df["PrgP"] >= p50_pass) & (df["PrgC"] >= p50_carry)]
top_combined = eligible.assign(score = eligible["PrgP"] + eligible["PrgC"]).nlargest(8, "score")
labelled = pd.concat([best_prgc, best_prgp, top_combined]).drop_duplicates()

for i, row in labelled.iterrows():
    plt.text(row["PrgP"]+0.1, row["PrgC"], row["Player"],
             fontsize=10)

# Label customisation
plt.xlabel("Progressive Passes (per 90)", fontsize=12, fontweight="bold", labelpad=15)
plt.ylabel("Progressive Carries (per 90)", fontsize=12, fontweight="bold", labelpad=15)
plt.suptitle("Minimum 1000 minutes played - No relegated players - Last 365 days", fontsize=10, x=0.3285, y=0.975)
plt.title("Premier League Fullback Ball Progression", fontsize=18, fontweight="bold", pad=55, loc='left')

graphics_folder = "../graphics_created"
plt.savefig(os.path.join(graphics_folder, "2425_epl_fb_ball_progression.png"), dpi=1200, bbox_inches='tight', pad_inches=1)
plt.show()