import json
import urllib2
import codecs

json_file = urllib2.urlopen('http://opendata.caceres.es/storage/f/2014-09-01T11%3A30%3A28.420Z/desfibriladores-ca-ceres-json.json')
data = json.load(json_file)


osm = "<?xml version='1.0' encoding='UTF-8'?>\n"
osm += "<osm version='0.6' upload='true' generator='JOSM'>\n"


ct = -1
for item in data['results']['bindings']:
  osm += "<node id='%s' action='modify' visible='true' lat='%s' lon='%s'>\n" % (ct, item['geo_lat']['value'], item['geo_long']['value'])
  osm += "  <tag k='emergency' v='defibrillator' />\n"
  if 'om_descripcionUbicacion' in item:
    osm += "  <tag k='defibrillator:location' v='%s' />\n" % (item['om_descripcionUbicacion']['value'],)
  if 'om_situadoEnCentro' in item:
    osm += "  <tag k='addr:housename' v='%s' />\n" % (item['om_situadoEnCentro']['value'],)
  if 'om_direccionEnMunicipio' in item:
    splited = item['om_direccionEnMunicipio']['value'].split(',')
    if len(splited) > 1:
      osm += "  <tag k='addr:street' v='%s' />\n" % (splited[0].strip(),)
      osm += "  <tag k='addr:housenumber' v='%s' />\n" % (splited[1].strip(),)
    else:
      osm += "  <tag k='addr:place' v='%s' />\n" % (item['om_direccionEnMunicipio']['value'],)
  osm += "</node>\n"
  ct = ct - 1

osm += "</osm>\n"

with codecs.open('result.osm','w',encoding='utf8') as result_osm:
  result_osm.write(osm)
  result_osm.close()
