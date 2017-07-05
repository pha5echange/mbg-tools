# mbg_plot_countries_02.py
# Version a02
# by jmg - jmg*AT*phasechange*DOT*co*DOT*uk
# July 5th 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

"""
===============
Basic pie chart
===============

Demo of a basic pie chart plus a few additional features.

In addition to the basic pie chart, this demo shows a few optional features:

    * slice labels
    * auto-labeling the percentage
    * offsetting a slice with "explode"
    * drop-shadow
    * custom start angle

Note about the custom start angle:

The default ``startangle`` is 0, which would start the "Frogs" slice on the
positive x-axis. This example sets ``startangle = 90`` such that everything is
rotated counter-clockwise by 90 degrees, and the frog slice starts on the
positive y-axis.
"""
import matplotlib.pyplot as plt

versionNumber = "a02"
appName = "mbg_plot_countries_"

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
colors=('b', 'g', 'r', 'c', 'm', 'y', 'c', 'w', 'silver', 'palegreen', 'lightsteelblue')
labels = 'USA', 'UK', 'Germany', 'France', 'Sweden', 'Canada', 'Italy', 'Japan', 'Finland', 'Spain', 'Others (170 countries)'
sizes = [36.4, 12.2, 5.9, 4.2, 3.3, 3.1, 3, 2.7, 2.3, 1.9, 25]
explode = (0, 0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.3, 0.4, 0.5, 0)  # only "explode" the 2nd slice (i.e. 'UK')

fig1, ax1 = plt.subplots()
patches, texts, autotexts = ax1.pie(sizes, explode=explode, colors=colors, labels=labels, autopct='%1.1f%%')
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
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
