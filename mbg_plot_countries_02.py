# mbg_plot_countries_02.py
# Version a02
# by jmg - jmg*AT*phasechange*DOT*co*DOT*uk
# July 5th 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

import matplotlib.pyplot as plt

versionNumber = "a02"
appName = "mbg_plot_countries_"

# Pie chart
colors=('lightblue', 'lightgray', 'lightcoral', 'lightsteelblue', 'lightyellow', 'lightsalmon', 'lightseagreen', 'white', 'silver', 'palegoldenrod', 'palegreen')
labels = 'USA', 'UK', 'Germany', 'France', 'Japan', 'Canada', 'Sweden', 'Italy', 'Finland', 'Australia', 'Others (116 countries)'
sizes = [35.1, 16.1, 6., 4.8, 3.1, 2.8, 2.8, 2.5, 2, 1.7, 23.1]
explode = (0, 0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.3, 0.4, 0.5, 0)  # only "explode" the 2nd slice (i.e. 'UK')

fig1, ax1 = plt.subplots()
patches, texts, autotexts = ax1.pie(sizes, explode=explode, colors=colors, labels=labels, autopct='%1.1f%%')
ax1.axis('equal')

#Resize text
autotexts[0].set_fontsize(9)
autotexts[1].set_fontsize(9)
autotexts[2].set_fontsize(9)
autotexts[3].set_fontsize(9)
autotexts[4].set_fontsize(9)
autotexts[5].set_fontsize(9)
autotexts[6].set_fontsize(9)
autotexts[7].set_fontsize(9)
autotexts[8].set_fontsize(9)
autotexts[9].set_fontsize(9)
autotexts[10].set_fontsize(9)

plt.show()
