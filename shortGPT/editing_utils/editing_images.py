from shortGPT.api_utils.image_api import getBingImages
from tqdm import tqdm
import random
import math

def getImageUrlsTimed(imageTextPairs):
    return [(pair[0], searchImageUrlsFromQuery(pair[1])) for pair in tqdm(imageTextPairs, desc='Search engine queries for images...')]



def searchImageUrlsFromQuery(query, top=3, expected_dim=[720,720], retries=5):
    images = getBingImages(query, retries=retries)
    if(images):
        distances = list(map(lambda x: math.dist([x['width'], x['height']], expected_dim), images[0:top]))
        shortest_ones = sorted(distances)
        random.shuffle(shortest_ones)
        for distance in shortest_ones:
            image_url = images[distances.index(distance)]['url']
            return image_url
    return None