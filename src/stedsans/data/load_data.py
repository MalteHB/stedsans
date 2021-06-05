"""Loading data using the stdlib importlib.resources APIs
"""
import importlib.resources, io
import pandas, geopandas


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
        
        df = importlib.resources.read_binary("stedsans.data", "KOMMUNE.csv")
        
        df = pandas.read_csv(io.BytesIO(df), encoding="utf-8")
        
        df = geopandas.GeoDataFrame(df)
        
        return df
