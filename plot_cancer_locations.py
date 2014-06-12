import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def plot_clinics():
  m = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, 
        urcrnrlat=49, projection='lcc', lat_1=33, lat_2=45, lon_0=-95, resolution='h', area_thresh=10000)
  #fig = plt.figure()
  #ax = plt.axes()

  m.bluemarble()  # display blue marble image from NASA in the background
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

      # zip_code = row["zip_code"]
      # if zip_code not in zip_to_count:
      #   zip_to_count[zip_code] = 0
      #   zip_to_count[zip_code] += int(row[docs_key])
      # if zip_code not in zip_to_geo:
       #  zip_to_geo[zip_code] = (row['longitude'], row['latitude'])

      if not (row["longitude"] == 'NA') and not(row["latitude"] == 'NA'):
        num_docs = int(row[docs_key]) 
        x, y = m(float(row["longitude"]), float(row["latitude"]))

        point = None
        if num_docs > 100:
          point  = m.plot(x, y, 'ro', label='>100')
        elif num_docs > 80:
          point  = m.plot(x, y, 'co', label='81-100')
        elif num_docs > 50:
          point  = m.plot(x, y, 'bo', label='51-80')
        elif num_docs > 20:
          point  = m.plot(x, y, 'yo', label='21-50')

  plt.title('Mid to large cancer clinics in the USA')
  plt.show()

    # if point:
    #   points_with_annotation.append((point, annotation))

# def on_move(event):
#   visibility_changed = False
#   for (point, annotation) in points_with_annotation:
#     should_be_visible = (point.contains(event)[0] == True)

#     if should_be_visible != annotation.get_visible():
#       visibility_changed = True
#       annotation.set_visible(should_be_visible)

#   if visibility_changed:
#     plt.draw()

#on_move_id = fig.canvas.mpl_connect('motion_notify_event', on_move)





if __name__ == '__main__':
  plot_clinics()
