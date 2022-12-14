import os
from flask import Flask, render_template, request
from get_tweet_data import get_tweet_data, get_tweet_embed
from send_to_chatGPT import get_response

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/get_tweet_info', methods = ['GET'])
def get_tweet_info():
  # link format: https://twitter.com/<username>/status/<tweet_id>?<params>

  tweet_link = request.args.get('tweet_link')
  id_and_params = tweet_link.split("/")[-1]
  tweet_id = id_and_params.split("?")[0]

  try:
    tweet_data = get_tweet_data(tweet_id)
  except:
    return "Please provide a valid tweet (or link to tweet)"
  
  tweet_text = tweet_data["data"][0]["text"]
  
  tweet_media_0 = ""
  tweet_media_1 = ""
  tweet_media_2 = ""
  tweet_media_3 = ""
  try:
    tweet_media_0 = tweet_data["includes"]["media"][0]["url"]
    tweet_media_1 = tweet_data["includes"]["media"][1]["url"]
    tweet_media_2 = tweet_data["includes"]["media"][2]["url"]
    tweet_media_3 = tweet_data["includes"]["media"][3]["url"]
  except:
    print("fewer than 4 images")

  media_descrip = ""
  try:
    for img in tweet_data["includes"]["media"]:
      media_descrip += img["alt_text"] + " "
  except:
    print("error in alt-text")

  #return tweet_data
  return render_template('index.html', tweet_link=tweet_link, tweet_text=tweet_text, tweet_media_0=tweet_media_0, tweet_media_1=tweet_media_1, tweet_media_2=tweet_media_2, tweet_media_3=tweet_media_3, media_descrip=media_descrip)


@app.route('/send_to_GPT', methods = ['GET'])
def get_GPT_output():

  media_descrip = request.args.get('media_descrip')
  tweet_text = request.args.get('tweet_text')
  tweet_link = request.args.get('tweet_link')

  GPT_output = get_response(tweet_text, media_descrip)["choices"][0]["text"]

  tweet_embed = get_tweet_embed(tweet_link)

  return render_template('GPTOutput.html', media_descrip=media_descrip, tweet_text=tweet_text, GPT_output=GPT_output, tweet_link=tweet_link, tweet_embed=tweet_embed)


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(debug=True, host='0.0.0.0', port=port)