# -*- coding: utf-8 -*-

import HTMLParser
from lxml import etree
import codecs
import json
import math

def distance_on_unit_sphere(lat1, long1, lat2, long2):
   
    # Public domain function, by John D. Cook
    # http://www.johndcook.com/python_longitude_latitude.html
    
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc * 6373


#print distance_on_unit_sphere(41.434191,2.205886,41.434279,2.2058508)

#"""

pars = HTMLParser.HTMLParser()
tree = etree.parse('getstations3.php')
root = tree.getroot()

bicing_actual = etree.parse('bicing_actual.osm')
root_actual = bicing_actual.getroot()

osm = "<?xml version='1.0' encoding='UTF-8'?>\n"
osm += "<osm version='0.6' upload='true' generator='JOSM'>\n"

osm_limpio = osm
osm_conflicto = osm

ct = -1
for item in root.findall('.//station'):
  
  estacion_proxima = False
  for actual in root_actual.findall('.//node'):
    if distance_on_unit_sphere(float(item[1].text), float(item[2].text), float(actual.get('lat')), float(actual.get('lon'))) < 0.1:
      estacion_proxima = True
 
  osm = '' 
  osm += "<node id='%s' action='modify' visible='true' lat='%s' lon='%s'>\n" % (ct, item[1].text, item[2].text)
  osm += "  <tag k='amenity' v='bicycle_rental' />\n"
  osm += "  <tag k='network' v='Bicing' />\n"
  osm += "  <tag k='ref' v='%s' />\n" % (item[0].text,)
  if item[5].text is None:
    osm += '  <tag k="name" v="%s" />\n' % (pars.unescape(item[3].text),)
  else:
    osm += '  <tag k="name" v="%s, %s" />\n' % (pars.unescape(item[3].text), item[5].text)
  capacidad = int(item[8].text) + int(item[9].text)
  if capacidad % 3 != 0:
    capacidad = ((capacidad / 3) + 1) * 3
  if capacidad == 0:
    osm += "  <tag k='note' v='FIXME: indique la cantidad de slots disponibles en la etiqueta capacity' />\n"
  else:
    osm += "  <tag k='capacity' v='%s' />\n" % (capacidad,)
  osm += "  <tag k='operator' v='Clear Channel' />\n"
  osm += "</node>\n"
  if estacion_proxima:
    osm_conflicto += osm
  else:
    osm_limpio += osm
  ct = ct - 1

osm_limpio += "</osm>\n"
osm_conflicto += "</osm>\n"

with codecs.open('result.osm','w',encoding='utf8') as result_osm:
  result_osm.write(osm_limpio)
  result_osm.close()
with codecs.open('result_conflicts.osm','w',encoding='utf8') as result_osm:
  result_osm.write(osm_conflicto)
  result_osm.close()


#"""
