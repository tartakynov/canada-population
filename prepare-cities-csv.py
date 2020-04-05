#!/usr/bin/env python


import qwikidata
import qwikidata.sparql
import csv


def parse_city_wikidata(data):
    coordinates = [float(x) for x in data['location']['value'].lstrip("Point(").rstrip(")").split(' ')]
    return dict(
        city=data['cityLabel']['value'],
        province=data['provinceLabel']['value'],
        population=data['population']['value'],
        latitude=coordinates[1],
        longitude=coordinates[0]
    )


def get_cities_wikidata(city, country):
    query = """
      SELECT ?cityLabel ?provinceLabel ?population ?location
      WHERE
      {
        ?city rdfs:label '%s'@en.
        ?city wdt:P1082 ?population.
        ?city wdt:P625 ?location.
        ?city wdt:P17 ?country.
        ?city wdt:P131 ?province.
        ?city rdfs:label ?cityLabel.
        ?country rdfs:label ?countryLabel.
        ?province rdfs:label ?provinceLabel.
        FILTER(LANG(?cityLabel) = "en").
        FILTER(LANG(?countryLabel) = "en").
        FILTER(LANG(?provinceLabel) = "en").
        FILTER(CONTAINS(?countryLabel, "%s")).
      }
      """ % (city, country)

    res = qwikidata.sparql.return_sparql_query_results(query)
    return map(parse_city_wikidata, res['results']['bindings'])


def main():
    fieldnames = ['city', 'province', 'population', 'latitude', 'longitude']
    with open('cities.csv', 'w', newline='') as csvfile:
        out = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        out.writeheader()
        for city in get_cities_wikidata('Ottawa', 'Canada'):
            out.writerow(city)
            print(city)


if __name__ == "__main__":
    main()
