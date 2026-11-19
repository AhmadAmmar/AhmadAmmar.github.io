# Know your study area (draft, private until decided)

A guide for researchers from any discipline (ethnography, history, sociology, political science, gender, labour,
religion, literature, urban studies) who need to understand a place from open data and their own field material.
Worked examples: Quetta (city) and Balochistan (province).

| Notebook | Content |
|---|---|
| 00 first steps | no-code routes (uMap, Felt, QGIS) vs notebooks; running cells; layers, CRS, joins; first interactive map |
| 01 city data | Quetta: OSM via Overpass and Geofabrik, Overture buildings and places, WorldPop; source comparison |
| 02 province data | Balochistan: HDX boundaries and 2017 census, code mismatches, OSM roads, extraction, borders; UCDP events with a time-slider map; ACLED with your own key |
| 03 your own field data | field-note spreadsheets, geocoding with certainty, routes, many names (gazetteer), georeferencing sketch and old maps, participatory mapping, qualitative codes to maps |
| 04 overlays and calculations | grid, joins, zonal statistics, buffers, walking isochrones, kernel density, Moran's I, Gi* |
| 05 maps and interactivity | class schemes, rates, bivariate, small multiples, explore, folium (layers, heat map, DualMap), plotly, ipywidgets |
| 06 questions by discipline | sociology, gender, labour, anthropology and religion, history, literature, urban studies, political geography |
| 07 ethics, safety, critical cartography | data-protection checklist, stripping photo GPS, jitter / grid / suppression, contested borders and names, absences |

Edit `src/NN_*.py` and run `python build.py NN` (eo environment): rebuilt and executed. Downloads go to
`notebooks/data/` (untracked). Field-data examples are invented. Not yet in the guide pipeline or pushed.
