import csv
import sys
import numpy as np
#import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def plot_clinics():
	m = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, 
		    urcrnrlat=49, projection='lcc', lat_1=33, lat_2=45, lon_0=-95, resolution='h', area_thresh=10000)
	fig = plt.figure()
	ax = plt.axes()

	m.bluemarble()  # display blue marble image from NASA in the background
	#x, y = m(-74, 40)
	#m.plot(x, y, 'bo', markersize=24)
	#map = Basemap(projection='ortho', lat_0 = 45, lon_0=100, resolution='l')
	m.drawcoastlines(linewidth=0.25)
	m.drawcountries(linewidth=2)
	m.drawstates(linewidth=0.25)

	with open('cancer_center_locations.csv', 'r') as r_file:
	  geodata = csv.DictReader(r_file)
	  important_file = geodata.next()
	  docs = list()
	  zip_to_count = dict()
	  zip_to_geo = dict()

	  for row in geodata:
	    docs_key = "cast(split_zc.doc_max as text)" 
	    docs.append(int(row[docs_key]))

	    zip_code = row["zip_code"]
	    if zip_code not in zip_to_count:
	      zip_to_count[zip_code] = 0
	      zip_to_count[zip_code] += int(row[docs_key])
	      if zip_code not in zip_to_geo:
		zip_to_geo[zip_code] = (row['longitude'], row['latitude'])



	      if not (row["longitude"] == 'NA') and not(row["latitude"] == 'NA'):
		num_docs = int(row[docs_key]) 
		x, y = m(float(row["longitude"]), float(row["latitude"]))
		points_with_annotation = []

		annotation = ax.annotate('Clinic Name: %s' % row['org'],
					  xy = (x, y), xycoords='data', 
					  xytext=(x+1, y), textcoords='data',
					  horizontalalignment='left', 
					  arrowprops=dict(arrowstyle='simple', 
							  connectionstyle='arc3, rad=-0.2'),
					  bbox=dict(boxstyle='round', facecolor='w',
						    edgecolor='0.5', alpha=0.9)
					  )
		annotation.set_visible(False)
		    

		point = None
		if num_docs > 100:
		  point,  = plt.plot(x, y, 'ro', label='>100')
		elif num_docs > 80:
		  point,  = plt.plot(x, y, 'mo', label='81-100')
		elif num_docs > 50:
		  point,  = plt.plot(x, y, 'bo', label='51-80')
		elif num_docs > 20:
		  point,  = plt.plot(x, y, 'yo', label='21-50')

		if point:
		  points_with_annotation.append((point, annotation))

def on_move(event):
  visibility_changed = False
  for (point, annotation) in points_with_annotation:
    should_be_visible = (point.contains(event)[0] == True)

    if should_be_visible != annotation.get_visible():
      visibility_changed = True
      annotation.set_visible(should_be_visible)

  if visibility_changed:
    plt.draw()

on_move_id = fig.canvas.mpl_connect('motion_notify_event', on_move)


plt.title('Mid to large cancer clinics in the USA')
plt.show()


if __name__ == '__main__':
  plot_clinics()
