# import os
# import requests
# from functools import lru_cache
# from azure.cognitiveservices.vision.computervision import ComputerVisionClient
# from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
# from msrest.authentication import CognitiveServicesCredentials


# # authenticate
# subscription_key = os.environ['API_KEY_MSFT_CLOUD']

# def create_url():
#   endpoint = "https://talie-chime-descrip.cognitiveservices.azure.com/computervision/imageanalysis:analyze?api-version=latest&features=Description"
#   return endpoint


# def get_img_descrip(img_url):

#   data = {
#     'url': img_url,
#   }


#   result = requests.post(url = create_url(), data = data)
#   return result.content

