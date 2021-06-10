from ..nlp.ner.entity_extractor import EntityExtractor

import matplotlib.pyplot as plt
import pandas as pd
from geopy.geocoders import Nominatim
from datetime import datetime
from folium import plugins
import warnings
from tqdm.auto import tqdm
import time

import pointpats
import folium
import geopandas

from ..utils.geo_utils import calc_bbox


class Geography(EntityExtractor):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    # Get Coordinates function
    def get_coordinates(self,
                        output=None,
                        limit=None,
                        limit_area=None,
                        sentence=None,
                        file=None,
                        bounding_box=None,
                        bounded=False,
                        output_language="en"):

        """
        Extract coordinates and addresses from entities

        Generates either a list of coordinates, a pandas dataframe or a geopandas geodataframe (or all)

        Parameters
        ----------

        output : str (default None)
            Specifies the output of the data returned by the functoin
        limit : str (default None)
            Indicates the 'level' of the limit_area argument - follows the dictionary inside
            location.raw['address'] such as, ''country'', ''municipality''.
        limit_area : str (default None)
            Follows 'limit' parameter. Indicates which area to limit to, such as
            ''Danmark'', ''Aarhus Kommune''.
        sentence : str (default None)
            Allows for passing new text for analysis if 'stedsans' object hasn't been initialised
        file : txt file (default None)
            Allows for passing new textfile for analysis if 'stedsans' object hasn't been initialised
        bounding_box: tuple/list (default None)
            List or tuple of 2 items of geopy.point.Point or (latitude, longitude) representing coordinates
            to restrict search within e.g. 'Denmark', ((8.08997684086, 54.8000145534), (12.6900061378, 57.730016588)),
        bounded : bool (default False)
            Whether to restrict search within bounding_box coordinates or not
        output_language : str (default "en")
            For which language to return the geolocations in. Defaults to "en" for english.


        Returns
        -------
        coordinates : list
            List of coordinates (EPSG:4326) for all entities
        dataframe : pandas.DataFrame
            DataFrame containing addresses and geometries (coordinates) for all entities
        geopandas_df : geopandas.geodataframe.GeoDataFrame
            GeoDataFrame containing addresses and geometries (coordinates) for all entities
        """
        # Asserting if coordinates with same specifications have already been retrieved
        try:

            if sentence is None:
                
                if file is None:
            
                    if self.coordinates:

                        if self.df is not None:

                            if self.gdf is not None:

                                if self.limit == limit:

                                    if self.limit_area == limit_area:

                                        if self.bounding_box == bounding_box:

                                            if self.bounded == bounded:

                                                return self.coordinates, self.df, self.gdf

        # If not, run as usual
        except:
            
            print("Getting coordinates.")
            
            time.sleep(0.3)
            
        def _assert_output(output):

            # Return according to parameter
            if output is None:

                # Creating coordinates list
                coordinates_list = [list(x) for x in zip(lat_list, long_list)]

                # Create pandas dataframe
                d = {
                    "entities": entities,
                    'places': places,
                    'latitude': lat_list,
                    'longitude': long_list
                }
                dataframe = pd.DataFrame(data=d)

                # Creating geopandas_df
                geopandas_df = geopandas.GeoDataFrame(dataframe.copy(), geometry=geopandas.points_from_xy(dataframe.longitude, dataframe.latitude))

                return coordinates_list, dataframe, geopandas_df

            if str(output) == 'geopandas':

                # Create pandas dataframe
                d = {
                    "entities": entities,
                    'places': places,
                    'latitude': lat_list,
                    'longitude': long_list
                }
                dataframe = pd.DataFrame(data=d)

                # Creating geopandas_df
                geopandas_df = geopandas.GeoDataFrame(dataframe, geometry=geopandas.points_from_xy(dataframe.longitude, dataframe.latitude))

                return geopandas_df

            if str(output) == 'coordinates':

                # Creating coordinates list
                coordinates_list = [list(x) for x in zip(lat_list, long_list)]

                return coordinates_list

            if str(output) == 'pandas':

                # Create pandas dataframe
                d = {
                    "entities": entities,
                    'places': places,
                    'latitude': lat_list,
                    'longitude': long_list
                }

                dataframe = pd.DataFrame(data=d)

                return dataframe

        # If new sentence/txt file is passed, exrtract new entities
        if sentence is not None:
            self.entities = self.extract_entities(sentence)

        if file is not None:
            self.entities = self.extract_document_entities(sentence)
            
        self.limit = limit
        
        self.limit_area = limit_area
        
        self.bounding_box = bounding_box
        
        self.bounded = bounded

        # Unique user ID to parse to Nominatim (to combat limited searches)
        user_agent = str(datetime.now())

        # Initialising geo-locator
        locator = Nominatim(user_agent=user_agent)

        # Looping through locations, extracting coordinates and place names
        places = []
        long_list = []
        lat_list = []
        entities = []

        # Looping through enities
        for i, _ in enumerate(tqdm(self.entities)):
            
            original_entity = self.entities[i][0]

            # Get location using geocode
            location = locator.geocode(original_entity,
                                       addressdetails=True,
                                       viewbox=bounding_box,
                                       bounded=bounded,
                                       language=output_language)

            # If a location is found
            if location is not None:

                # Check if a limit arguments has been given
                if limit is not None:

                    # Check if 'country' is a keyword in the location.raw['address'] dictionary - if not then delete it
                    if limit not in location.raw['address']:

                        location = None

                    # Delete location if point is not within limit area
                    elif location.raw['address'][limit] != limit_area:

                        location = None

                    # Elese append location and coordinates to list
                    else:

                        places.append(location)

                        lat_list.append(location.latitude)

                        long_list.append(location.longitude)
                        
                        entities.append(original_entity)

                # If not limit given then just append location and coordinates to list
                else:

                    places.append(location)

                    lat_list.append(location.latitude)

                    long_list.append(location.longitude)
                    
                    entities.append(original_entity)

        # Return correct data outputs
        if sentence is None:
            if output is None:
                self.coordinates, self.df, self.gdf = _assert_output(output)
                return self.coordinates, self.df, self.gdf

            elif output == 'coordinates':
                coordinates = _assert_output(output)
                return coordinates

            elif output == 'pandas':
                df = _assert_output(output)
                return df

            elif output == 'geopandas':
                gdf = _assert_output(output)
                return gdf
        
        # Do not return self varaibles if a new sentence is passed
        else:
            if output is None:
                coordinates, df, gdf = _assert_output(output)
                return coordinates, df, gdf

            elif output == 'coordinates':
                coordinates = _assert_output(output)
                return coordinates

            elif output == 'pandas':
                df = _assert_output(output)
                return df

            elif output == 'geopandas':
                gdf = _assert_output(output)
                return gdf

    # Plot Locations
    def plot_locations(self,
                       layer=None,
                       limit=None,
                       limit_area=None,
                       on_map=False,
                       sentence=None,
                       file=None,
                       bounding_box=None,
                       bounded=False,
                       output_language="en",
                       crs=4326,
                       edge=0.15,
                       tiles='cartodbpositron'):

        """
        Plot locations as points on a map

        Returns either an interactive folium map or a matplotlib figure

        Parameters
        ----------

        layer : geopandas.geodataframe.GeoDataFrame (default None)
            Specifies a baselayer map consisting of polygons on which to plot. If not given,
            the function plots onto a folium map
        limit : str (default None)
            Indicates the 'level' of the limit_area argument - follows the dictionary inside
            location.raw['address'] such as, ''country'', ''municipality''.
        limit_area : str (default None)
            Follows 'limit' parameter. Indicates which area to limit to, such as
            ''Danmark'', ''Aarhus Kommune''.
        on_map = bool (defaul False)
            Whether to restrict the points to those which lie within the polygons of the given 'layer'
        sentence : str (default None)
            Allows for passing new text for analysis if 'stedsans' object hasn't been initialised
        file : txt file (default None)
            Allows for passing new textfile for analysis if 'stedsans' object hasn't been initialised
        bounding_box: tuple/list (default None)
            List or tuple of 2 items of geopy.point.Point or (latitude, longitude) representing coordinates
            to restrict search within e.g. 'Denmark', ((8.08997684086, 54.8000145534), (12.6900061378, 57.730016588)),
        bounded : bool (default False)
            Whether to restrict search within bounding_box coordinates or not
        crs : int (default 4236)
            Coordinate reference system to project given map to
        start_border : float (bbox_edge 0.15)
            Number of degrees for edge around bounding box
        output_language : str (default "en")
            For which language to return the geolocations in. Defaults to "en" for english.


        Returns
        -------
        map : Either matplotlib.figure.Figure or folium.folium.Map
            Depends on whether 'layer' is given
        """

        # Extracting locations using get_locations()
        coordinates, dataframe, geo_dataframe = self.get_coordinates(output=None,
                                                                     limit=limit,
                                                                     limit_area=limit_area,
                                                                     sentence=sentence,
                                                                     file=file,
                                                                     bounding_box=bounding_box,
                                                                     bounded=bounded,
                                                                     output_language=output_language)

        # If coordinates is empty:
        if not coordinates:

            warnings.warn(f"stedsans has not detected locations in this text: {sentence}")  # TODO: More verbosity

            # End
            return

        # Else:
        else:

            # If map is none, use folium interactive map as default
            if layer is None:

                # Create border for map start frame by finidng pair of max and min coordinates and adding/subtracting 0.15 degrees around points as a frame
                start_frame = calc_bbox(
                    coordinates=coordinates,
                    edge=edge
                )

                # Plotting locations
                map = folium.Map(
                    tiles=tiles
                )

                # Start at start box
                map.fit_bounds(start_frame)

                # Loop through each row in df and add markers
                for i in range(len(dataframe)):

                    folium.Marker(
                        [dataframe.latitude[i], dataframe.longitude[i]],
                        popup=str(dataframe.iloc[i, 0])
                    ).add_to(map)

                map

                # Return map
                return map

            # If layer is given
            else:

                # Project layer to crs used på nominatim
                map_projected = layer.to_crs(crs)

                # If on_map is true, only keep points that are in polygons
                if on_map is True:

                    pts_on_map_index = []

                    # Loop over polygons
                    for i, poly in map_projected.iterrows():

                        # Now loop over all points with index j.
                        for j, pt in geo_dataframe.iterrows():

                            # If point j is in polygon
                            if poly.geometry.contains(pt.geometry):

                                # Then append it to list of points in this polygon
                                pts_on_map_index.append(j)

                    # Drop all rows in geo_dataframe that are not on list
                    geo_dataframe = geo_dataframe.iloc[pts_on_map_index]

                # Create matplotlib frame
                map, ax = plt.subplots(1, 1)

                # Plot baselayer
                map_projected.plot(ax=ax, color='#AFDD93', edgecolor='black')

                # Add points from data frame
                geo_dataframe.plot(ax=ax, color='#214DCA')
                
                # Close for mitigation of multiple plots
                plt.close(map)

                # Return map
                return map

    # Plot choropleth
    def plot_choropleth(self,
                        layer=None,
                        title=None,
                        limit=None,
                        limit_area=None,
                        group_by=None,
                        sentence=None,
                        file=None,
                        bounding_box=None,
                        bounded=False,
                        crs=4326):
        """
        Plots a choropleth

        Returns either an interactive folium choropleth or a matplotlib based choropleth
        that display the distrobtution of points

        Parameters
        ----------

        layer : geopandas.geodataframe.GeoDataFrame (default None)
            Specifies a baselayer map consisting of polygons on which to plot. If not given,
            the function plots onto a folium map
        limit : str (default None)
            Indicates the 'level' of the limit_area argument - follows the dictionary inside
            location.raw['address'] such as, ''country'', ''municipality''.
        limit_area : str (default None)
            Follows 'limit' parameter. Indicates which area to limit to, such as
            ''Danmark'', ''Aarhus Kommune''.
        title : str (default None)
            Title on  plot
        group_by = str (defaul None)
            Whether to group polygons in the given 'layer', e.g. ''kommune'', ''region''
        sentence : str (default None)
            Allows for passing new text for analysis if 'stedsans' object hasn't been initialised
        file : txt file (default None)
            Allows for passing new textfile for analysis if 'stedsans' object hasn't been initialised
        bounding_box: tuple/list (default None)
            List or tuple of 2 items of geopy.point.Point or (latitude, longitude) representing coordinates
            to restrict search within e.g. 'Denmark', ((8.08997684086, 54.8000145534), (12.6900061378, 57.730016588)),
        bounded : bool (default False)
            Whether to restrict search within bounding_box coordinates or not


        Returns
        -------
        map : Either matplotlib.figure.Figure or folium.folium.Map
            Depends on whether 'layer' is given
        """

        # Extracting locations using get_locations()
        coordinates, _, geo_dataframe = self.get_coordinates(
            output=None,
            limit=limit,
            limit_area=limit_area,
            sentence=sentence,
            file=file,
            bounding_box=bounding_box,
            bounded=bounded
        )

        # If coordinates is empty:
        if not coordinates:

            warnings.warn(f"stedsans has not detected locations in this text: {sentence}")  # TODO: More verbosity

            # End
            return

        # Else:
        else:

            # If layer is None, plot the world
            if layer is None:
                
                layer = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

            # Project to crs used by nominatim
            map_projected = layer.to_crs(crs)

            # List for number of points per polys
            pts_in_polys = []

            # Loop over polygons
            for i, poly in map_projected.iterrows():

                # Keep a list of points in this poly
                pts_in_this_poly = []

                # Now loop over all points with index j.
                for j, pt in geo_dataframe.iterrows():

                    # If point j is in polygon
                    if poly.geometry.contains(pt.geometry):

                        # Then append it to list of points in this polygon
                        pts_in_this_poly.append(pt.geometry)

                        # And drop from geo df to save time when searching through next polygons
                        geo_dataframe = geo_dataframe.drop([j])

                # Append the number of points in each poly to one list
                pts_in_polys.append(len(pts_in_this_poly))

            # Add the number of points for each poly to the dataframe.
            map_projected['num_points'] = pts_in_polys

            # if group_by is given, aggregate by that parameter
            if group_by is not None:

                # Crete list with points grouped according to column giver by group_by
                num_points = map_projected.groupby([group_by])[['num_points']].agg('sum')

                # Drop column with num of points for every polygon
                del map_projected['num_points']

                # Left join grouped number of points onto dataframe
                map_projected = pd.merge(map_projected, num_points, left_on=group_by, right_index=True, how='left')

            # Create figure
            fig, ax = plt.subplots(1, figsize=(20, 10))
            ax.axis('off')

            # Set title if specified
            if title is not None:
                ax.set_title(str(title), fontdict={'fontsize': '25', 'fontweight': '3'})

            # Colours for colourbAR
            color = 'Oranges'

            # Range of colourbar
            vmin, vmax = min(map_projected['num_points']), max(map_projected['num_points'])

            # Create colour bar
            sm = plt.cm.ScalarMappable(cmap=color, norm=plt.Normalize(vmin=vmin, vmax=vmax))
            cbar = fig.colorbar(sm)
            cbar.ax.tick_params(labelsize=20)

            # Plot map weighted according to points
            map_projected.plot('num_points', cmap=color, linewidth=0.8, ax=ax, edgecolor='0.8', figsize=(20, 10))
            
            # Close for mitigation of multiple plots
            plt.close(fig)
            
            # Return
            return fig
        

    def plot_heatmap(
        self,
        limit=None,
        limit_area=None,
        sentence=None,
        file=None,
        bounding_box=None,
        bounded=False,
        edge=0.15,
        tiles='cartodbpositron'
    ):
        """
        Plots a heatmap

        Returns either an interactive folium choropleth or a matplotlib based choropleth
        that display the distrobtution of points

        Parameters
        ----------

        limit : str (default None)
            Indicates the 'level' of the limit_area argument - follows the dictionary inside
            location.raw['address'] such as, ''country'', ''municipality''.
        limit_area : str (default None)
            Follows 'limit' parameter. Indicates which area to limit to, such as
            ''Danmark'', ''Aarhus Kommune''.
        sentence : str (default None)
            Allows for passing new text for analysis if 'stedsans' object hasn't been initialised
        file : txt file (default None)
            Allows for passing new textfile for analysis if 'stedsans' object hasn't been initialised
        bounding_box: tuple/list (default None)
            List or tuple of 2 items of geopy.point.Point or (latitude, longitude) representing coordinates
            to restrict search within e.g. 'Denmark', ((8.08997684086, 54.8000145534), (12.6900061378, 57.730016588)),
        bounded : bool (default False)
            Whether to restrict search within bounding_box coordinates or not


        Returns
        -------
        map : Either matplotlib.figure.Figure or folium.folium.Map
            Depends on whether 'layer' is given
        """

        # Extracting locations using get_locations()
        coordinates, _, _ = self.get_coordinates(
            output=None,
            limit=limit,
            limit_area=limit_area,
            sentence=sentence,
            file=file,
            bounding_box=bounding_box,
            bounded=bounded
        )

        # If coordinates is empty:
        if not coordinates:

            warnings.warn(f"stedsans has not detected locations in this text: {sentence}")  # TODO: More verbosity

            # End
            return

        # Else:
        else:

            # Create bounding box with frame by finidng pair of max and min coordinates and adding/subtracting 0.15 degrees as the frame
            bounding_box = calc_bbox(
                coordinates=coordinates,
                edge=edge
            )

            # Plotting locations
            map = folium.Map(
                tiles=tiles
            )

            # Start at bounding box
            map.fit_bounds(bounding_box)

            # Add choropleth layer
            map.add_child(plugins.HeatMap(coordinates, radius=25))

            # Return map
            return map

    # GetQuadStatistics
    def get_quad_stats(self,
                       squares=4,
                       limit=None,
                       limit_area=None,
                       sentence=None,
                       file=None,
                       bounding_box=None,
                       bounded=False):
        """
        Calculate Q-Statistic

        Statistical test to analyse whether points are randomly distributed

        Parameters
        ----------

        squares : int (default 4)
            Specifies number of squares to partition the points into on each axis
        limit : str (default None)
            Indicates the 'level' of the limit_area argument - follows the dictionary inside
            location.raw['address'] such as, ''country'', ''municipality''.
        limit_area : str (default None)
            Follows 'limit' parameter. Indicates which area to limit to, such as
            ''Danmark'', ''Aarhus Kommune''.
        sentence : str (default None)
            Allows for passing new text for analysis if 'stedsans' object hasn't been initialised
        file : txt file (default None)
            Allows for passing new textfile for analysis if 'stedsans' object hasn't been initialised
        bounding_box: tuple/list (default None)
            List or tuple of 2 items of geopy.point.Point or (latitude, longitude) representing coordinates
            to restrict search within e.g. 'Denmark', ((8.08997684086, 54.8000145534), (12.6900061378, 57.730016588)),
        bounded : bool (default False)
            Whether to restrict search within bounding_box coordinates or not


        Returns
        -------
        pp : str
            A string containing a short summary of the statistical test
        """
        # Run get_coordinate function
        coordinates, _, _ = self.get_coordinates(
            limit=limit,
            limit_area=limit_area,
            sentence=sentence,
            file=file,
            bounding_box=bounding_box,
            bounded=bounded)

        # Create pointpattern using pointpats
        pp = pointpats.PointPattern(coordinates)

        # Defining sim process
        csr_process = pointpats.PoissonPointProcess(pp.window, pp.n, 999, asPP=True)

        # Calculating q stats
        q_stat_sim = pointpats.quadrat_statistics.QStatistic(pp, shape="rectangle", nx=squares, ny=squares, realizations=csr_process)

        # Create string containing results
        stats = f' ---- Chi Square Value calculated from simulation is {round(q_stat_sim.chi2, 3)} ---- P-Value is {round(q_stat_sim.chi2_r_pvalue, 5)} ----'

        # Return string
        return stats

    # PlotQuadCount
    def plot_quad_count(self,
                        squares=4,
                        limit=None,
                        limit_area=None,
                        sentence=None,
                        file=None,
                        bounding_box=None,
                        bounded=False):
        """
        Plots points on a graph

        Plots point on a graph partioned into rectangular arreas

        Parameters
        ----------

        squares : int (default 4)
            Specifies number of squares to partition the points into on each axis
        limit : str (default None)
            Indicates the 'level' of the limit_area argument - follows the dictionary inside
            location.raw['address'] such as, ''country'', ''municipality''.
        limit_area : str (default None)
            Follows 'limit' parameter. Indicates which area to limit to, such as
            ''Danmark'', ''Aarhus Kommune''.
        sentence : str (default None)
            Allows for passing new text for analysis if 'stedsans' object hasn't been initialised
        file : txt file (default None)
            Allows for passing new textfile for analysis if 'stedsans' object hasn't been initialised
        bounding_box: tuple/list (default None)
            List or tuple of 2 items of geopy.point.Point or (latitude, longitude) representing coordinates
            to restrict search within e.g. 'Denmark', ((8.08997684086, 54.8000145534), (12.6900061378, 57.730016588)),
        bounded : bool (default False)
            Whether to restrict search within bounding_box coordinates or not
        """

        # Run get_coordinate function
        coordinates, _, _ = self.get_coordinates(
            limit=limit,
            limit_area=limit_area,
            sentence=sentence,
            file=file,
            bounding_box=bounding_box,
            bounded=bounded)

        # Create pointpattern
        pp = pointpats.PointPattern(coordinates)

        # Plotting points with quadrants and counts
        pointpats.quadrat_statistics.QStatistic(pp, shape="rectangle", nx=squares, ny=squares).plot()
