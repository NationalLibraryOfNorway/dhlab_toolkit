import pandas as pd
import requests
from pandas import DataFrame
from dhlabtk.constants import BASE_URL
from typing import List
from dhlabtk.parse import NER, Models


class GeoData:
    """Fetch place data from a text (book, newspaper or ...) identified by URN
    with an appropriate and available spacy model.

    The models are retrieved by instantiating :py:class:`~text.parse.Models`.
    """
    
    def __init__(self, urn=None, model=None):
        self.place_names = self._fetch_place_names(urn, model)
        

    def _fetch_place_names(self, urn, model):
        try:
            assert urn is not None
            spacy = Models()
            model = model if model is not None else spacy.models[0]
            df = NER(urn = urn, model = model).ner
            place_names = df[df['ner'].str.contains('LOC')]
        except AssertionError:
            print("Please provide a document URN to fill the ``place_names`` dataframe attribute.")
            place_names = pd.DataFrame()
        except IndexError as error:
            print("GeoData couldn't load any SpaCy NER models.")
            place_names = pd.DataFrame()
        except Exception as error:
            print(error.__doc__, error)
            place_names = pd.DataFrame()
        return place_names


    def add_geo_locations(self, feature_class = None, feature_code = None):
        """Get location data for the names in object, attribute self.place_names"""
        chunksize = 900
        names = list(self.place_names.token)
        length = len(names)
        
        # GeoNames takes 1000 names at a time so chunk things up
        # Each GeoNames object has an attribute .places a pandas dataframe
        
        chunks = [
            GeoNames(
                names[i:i+chunksize], 
                feature_class = feature_class, 
                feature_code = feature_code
            ).places for i in range(0, length, chunksize)
        ] 
        
        self.places = pd.concat(chunks) 

        
class GeoNames:
    """Fetch data from a list of names"""
    def __init__(self, names, feature_class = None, feature_code = None):
        self.places = geo_lookup(names, feature_class = feature_class, feature_code = feature_code)
        
def get_places(urn: str) -> DataFrame:
    """Look up placenames in a specific URN.

    Call the API :py:obj:`~dhlab.constants.BASE_URL` endpoint
    `/places <https://api.nb.no/dhlab/#/default/post_places>`_.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    """
    params = locals()
    r = requests.post(f"{BASE_URL}/places", json=params)
    # print(r.status_code)
    return pd.DataFrame(r.json())


def geo_lookup(
        places: List,
        feature_class: str = None,
        feature_code: str = None,
        field: str = "alternatename",
) -> DataFrame:
    """From a list of places, return their geolocations

    :param list places: a list of place names - max 1000
    :param str feature_class: which GeoNames feature class to return. Example: ``P``
    :param str feature_code: which GeoNames feature code to return. Example: ``PPL``
    :param str field: which name field to match - default "alternatename".
    """
    res = requests.post(
        f"{BASE_URL}/geo_data",
        json={
            "words": places,
            "feature_class": feature_class,
            "feature_code": feature_code,
            "field": field,
        },
    )
    columns = [
        "geonameid",
        "name",
        "alternatename",
        "latitude",
        "longitude",
        "feature_class",
        "feature_code",
    ]
    return pd.DataFrame(res.json(), columns=columns)

def ner_from_urn(urn: str = None, model: str = None, start_page = 0, to_page = 0) -> DataFrame:
    """Get NER annotations for a text (``urn``) using a spacy ``model``.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    :param str model: name of a spacy model.
        Check which models are available with :func:`show_spacy_models`
    :return: Dataframe with annotations and their frequencies
    """

    params = locals()
    r = requests.get(f"{BASE_URL}/ner_urn", params=params)
    df = pd.read_json(r.json())
    return df
