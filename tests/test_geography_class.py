import unittest
import folium
import pandas as pd
import matplotlib

# import matplotlib.pyplot as plt

import geopandas

from stedsans import stedsans
from stedsans.data.load_data import GeoData

from parameterized import parameterized


class TestGeography(unittest.TestCase):

    @parameterized.expand([
                          ("Han bor på Testvej 23 Aarhus C. Jakob bor i Rådhusparken 8 Aarhus C. MCH Arena er et legendarisk sted. Hun bor tæt på Dejbjerglund Efterskole. I Randers laver man shawarma. LEGOLAND er det fedeste sted. Skanderborg Bryghus laver gode øl. SønderjyskE er et lorte hold. Han bor på Ingerslevs Boulevard. Vestebro ligger vest for Østerbro og tæt på Antwerpen."),
                          ])
    def test_restrict_search(self, sentence):

        # Initialsing a stedsans object
        geography = stedsans(sentence=sentence)

        # Testing plot locations with no limiting
        all_coords = geography.plot_locations()

        # Asserting that output is folium map
        self.assertIsInstance(all_coords, folium.folium.Map)

        # Testing plot locations with no limiting
        only_denmark = geography.plot_locations(bounding_box=((55, 8), (57, 9)), bounded=True)

        # Asserting that output is folium map
        self.assertIsInstance(only_denmark, folium.folium.Map)

    @parameterized.expand([
                          ("Han bor på Testvej 23 Aarhus C. Jakob bor i Rådhusparken 8 Aarhus C. MCH Arena er et legendarisk sted. Hun bor tæt på Dejbjerglund Efterskole. I Randers laver man shawarma. LEGOLAND er det fedeste sted. Skanderborg Bryghus laver gode øl. SønderjyskE er et lorte hold. Han bor på Ingerslevs Boulevard. Fjordgaarden er en lækker restaurant. Knebel ligger på Mols Djursland. Vestebro ligger vest for Østerbro og tæt på Amager. Bruuns Galleri og Dokk1 er steder i Aarhus."),
                          ])
    def test_group_by(self, sentence):

        # Load municipality file
        danmark = GeoData.municipalities()

        # Initialsing a stedsans object
        geography = stedsans(sentence=sentence)

        # Testing plot locations with no limiting
        map = geography.plot_choropleth(layer=danmark, group_by='DAGI_ID')

        # Asserting that output is matplotlib figure
        self.assertIsInstance(map, matplotlib.figure.Figure)

    @parameterized.expand([
                          ("Han bor på Testvej 23 Aarhus C. Jakob bor i Rådhusparken 8 Aarhus C. MCH Arena er et legendarisk sted. Hun bor tæt på Dejbjerglund Efterskole. I Randers laver man shawarma. LEGOLAND er det fedeste sted i Tower Bridge London."),
                          ])
    def test_limit(self, sentence):

        # Load municipality file
        danmark = GeoData.municipalities()

        # Initialsing a stedsans object
        geography = stedsans(sentence=sentence)

        # Testing plot locations with no limiting
        map = geography.plot_locations(layer=danmark)

        # Asserting that output is matplotlib figure
        self.assertIsInstance(map, matplotlib.figure.Figure)

        # Testing ability to restrict to points that are on the map given by shp file
        danmark_on_map = geography.plot_locations(layer=danmark, on_map=True)

        # Asseting output object type
        self.assertIsInstance(danmark_on_map, matplotlib.figure.Figure)

        # Testing ability to limit to a specific area
        danmark_map = geography.plot_locations(layer=danmark, limit='country', limit_area='Denmark')

        # Asseting output object type
        self.assertIsInstance(danmark_map, matplotlib.figure.Figure)


    @parameterized.expand([
                          ("H.C. Andersensvej, København er Mads' yndlingsgade og han arbejder på KMD."),
                          ("Jakob Grøhn bor på Testvej 23 Aarhus C. Jakob bor i Rådhusparken 8 Aarhus C. MCH Arena er et legendarisk sted. Kathrine Vibel bor tæt på Dejbjerglund Efterskole. LEGOLAND er det fedeste sted på jorden. SønderjyskE er et lorte hold. Han bor på H C Andersens Boulevard København "),
                          ])
    def test_get_coordinates(self, sentence):

        # Initialsing a stedsans object
        geography = stedsans(sentence=sentence)

        # Run function
        coordinates, df, gdf = geography.get_coordinates(limit='country', limit_area='Denmark')

        # Run function
        coordinates, df, gdf = geography.get_coordinates()
        
        # Run function
        coordinates, df, gdf = geography.get_coordinates(sentence='Jakob bor i København')

        # Run function
        coordinates, df, gdf = geography.get_coordinates()

        # Test outouts
        self.assertIsInstance(coordinates, list)

        self.assertIsInstance(df, pd.core.frame.DataFrame)

        self.assertIsInstance(gdf, geopandas.geodataframe.GeoDataFrame)

        # Test ability to only output single and on text passed directly
        only_gdf = stedsans().get_coordinates(sentence='Herning er min by og Randers er lort.', output='geopandas')

        self.assertIsInstance(only_gdf, geopandas.geodataframe.GeoDataFrame)

    @parameterized.expand([
                          ("H.C. Andersensvej, København er Mads' yndlingsgade og han arbejder på KMD."),
                          ("Jakob Grøhn bor på Testvej 23 Aarhus C. Jakob bor i Rådhusparken 8 Aarhus C. MCH Arena er et legendarisk sted. Kathrine Vibel bor tæt på Dejbjerglund Efterskole. LEGOLAND er det fedeste sted på jorden. SønderjyskE er et lorte hold. Han bor på H C Andersens Boulevard København "),
                          ])
    def test_plot_locations(self, sentence):
        # Load municipality file
        danmark = GeoData.municipalities()

        # Initialsing a stedsans objects
        geography = stedsans(sentence=sentence)

        # Plot on interactive folium map
        folium_map = geography.plot_locations()

        # Assert output type
        self.assertIsInstance(folium_map, folium.folium.Map)

        # Plot on specified layer
        danmark_map = geography.plot_locations(layer=danmark)

        # Assert output type
        self.assertIsInstance(danmark_map, matplotlib.figure.Figure)

        # Test when passing own text
        new_danmark_map = stedsans().plot_locations(layer=danmark, sentence='Herning er min by og Randers er lort.')

        self.assertIsInstance(new_danmark_map, matplotlib.figure.Figure)

    @parameterized.expand([
                          ("Han bor på Testvej 23 Aarhus C. Jakob bor i Rådhusparken 8 Aarhus C. MCH Arena er et legendarisk sted. Hun bor tæt på Dejbjerglund Efterskole. I Randers laver man shawarma. LEGOLAND er det fedeste sted. Skanderborg Bryghus laver gode øl. SønderjyskE er et lorte hold. Han bor på Ingerslevs Boulevard. Fjordgaarden er en lækker restaurant. Knebel ligger på Mols Djursland. Vestebro ligger vest for Østerbro og tæt på Amager. Bruuns Galleri og Dokk1 er steder i Aarhus."),
                          ])
    def test_quad_stats_functions(self, sentence):

        # Initialsing a stedsans objects
        geography = stedsans(sentence=sentence)

        # Plotting points on rectangular gitter
        geography.get_quad_stats(squares=4)

        # Initialsing a stedsans objects
        pp = geography.plot_quad_count(squares=4)

        # Print
        print(pp)

    @parameterized.expand([
                          ("Han bor på Testvej 23 Aarhus C. Jakob bor i Rådhusparken 8 Aarhus C. MCH Arena er et legendarisk sted. Hun bor tæt på Dejbjerglund Efterskole. I Randers laver man shawarma. LEGOLAND er det fedeste sted. Skanderborg Bryghus laver gode øl. SønderjyskE er et lorte hold. Han bor på Ingerslevs Boulevard. Fjordgaarden er en lækker restaurant. Knebel ligger på Mols Djursland. Vestebro ligger vest for Østerbro og tæt på Amager. Bruuns Galleri og Dokk1 er steder i Aarhus.")
                          ])
    def test_choropleth(self, sentence):
        
        # Initialsing a stedsans objects
        geography = stedsans(sentence=sentence)

        # Load municipality file
        danmark = GeoData.municipalities()

        # Subsetting region midtjylland
        region_m = danmark[danmark["REGIONNAVN"] == "Region Midtjylland"]
        
        # Plotting choropleth with default settings
        choropleth = geography.plot_choropleth()
        
        self.assertIsInstance(choropleth, matplotlib.figure.Figure)

        # Plotting choropleth on denmark with kommune polygons as resolution
        dk_choropleth = geography.plot_choropleth(layer=danmark)

        self.assertIsInstance(dk_choropleth, matplotlib.figure.Figure)

        # Plotting only region midtjylland
        midtjylland_choropleth = geography.plot_choropleth(layer=region_m)

        self.assertIsInstance(midtjylland_choropleth, matplotlib.figure.Figure)
        
    @parameterized.expand([
                          ("Han bor på Testvej 23 Aarhus C. Jakob bor i Rådhusparken 8 Aarhus C. MCH Arena er et legendarisk sted. Hun bor tæt på Dejbjerglund Efterskole. I Randers laver man shawarma. LEGOLAND er det fedeste sted. Skanderborg Bryghus laver gode øl. SønderjyskE er et lorte hold. Han bor på Ingerslevs Boulevard. Fjordgaarden er en lækker restaurant. Knebel ligger på Mols Djursland. Vestebro ligger vest for Østerbro og tæt på Amager. Bruuns Galleri og Dokk1 er steder i Aarhus.")
                          ])
    def test_heatmap(self, sentence):

        # Initialsing a stedsans objects
        geography = stedsans(sentence=sentence)

        # Plotting folium heatmap
        folium_heatmap = geography.plot_heatmap()

        self.assertIsInstance(folium_heatmap, folium.folium.Map)


if __name__ == '__main__':
    unittest.main()
