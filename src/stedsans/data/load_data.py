"""Loading data using the stdlib importlib.resources APIs
"""
import importlib.resources
import io
import pandas
import geopandas
import pyproj

from shapely import wkt


class Articles:
    """Loads the article data inherent in the package.
    """
    
    def __init__(self):
        pass
        
    def aarhus():
        
        article = importlib.resources.read_text("stedsans.data", "aarhus_example.txt", encoding="utf-8")
        
        return article
        
    def jylland():
        
        article = importlib.resources.read_text("stedsans.data", "jylland_example.txt", encoding="utf-8")
        
        return article
        

class GeoData:
    """Loads the geographical data inherent in the package.
    """
    
    def __init__(self):
        pass
        
    def municipalities():
        
        # Loading the csv from bytes
        df = importlib.resources.read_binary("stedsans.data", "KOMMUNE.csv")
        
        # Loading the projection to use as crs
        prj = importlib.resources.read_text("stedsans.data", "KOMMUNE.prj")
        
        crs = pyproj.CRS(prj)
        
        # Defining dtypes for the dataframe
        dtypes = {
            'FEAT_ID': 'int64',
            'FEAT_KODE': 'int64',
            'FEAT_TYPE': 'object',
            'FEAT_STTXT': 'object',
            'GEOM_STTXT': 'object',
            'DAGI_ID': 'int64',
            'AREAL': 'float64',
            'REGIONKODE': 'object',
            'REGIONNAVN': 'object',
            'GYLDIG_FRA': 'object',
            'GYLDIG_TIL': 'object',
            'KOMKODE': 'object',
            'KOMNAVN': 'object',
            'DQ_SPECIFK': 'object',
            'DQ_STATEM': 'object',
            'DQ_DESCR': 'object',
            'DQ_PROCESS': 'object',
            'DQ_RESPONS': 'object',
            'DQ_POSACPL': 'object',
            'DQ_POSACLV': 'object',
            'TIMEOF_CRE': 'object',
            'TIMEOF_PUB': 'object',
            'TIMEOF_REV': 'object',
            'TIMEOF_EXP': 'object',
            #'geometry': 'geometry'
        }
        
        df = pandas.read_csv(io.BytesIO(df), encoding="utf-8", dtype=dtypes)
        
        # Changing geometry column to dtype 'geometry'
        df["geometry"] = df["geometry"].apply(wkt.loads)
        
        df = geopandas.GeoDataFrame(df, crs=crs)
        
        return df
