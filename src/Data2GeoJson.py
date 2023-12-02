import json
import geojson
from geojson import Feature, FeatureCollection, Point


def Data2geojson(df):
    features = []
    insert_features = lambda X: features.append(
                        geojson.Feature(geometry=geojson.Point((X["Longitude"],
                                                    X["Latitude"])),
                        properties=dict(name = X["PlaceName"],
                                    description = X["Categories"],
                                    rating = X['StarsAndReviewcounts']))
                    )
    df.apply(insert_features, axis=1)

    dump = geojson.dumps(geojson.FeatureCollection(features), sort_keys=True, ensure_ascii=False,indent=4)
    return dump