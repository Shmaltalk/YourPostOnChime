import os
from flask import Flask, render_template, request, redirect, url_for
from get_tweet_data import get_tweet_data, get_tweet_embed
from send_to_chatGPT import get_response

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/emoji_result', methods = ['GET'])
def emoji_result():

   # arguments
  tweet_link = request.args.get('tweet_link')
  emoji_string = request.args.get('emoji_string')

  # get just tweet id
  tweet_id = tweet_link.split("/")[-1] # gets just the id and params
  tweet_id = tweet_id.split("?")[0] # removes params

  # get json of tweet data from twitter API
  try:
    tweet_data = get_tweet_data(tweet_id)
  except:
    return "Please provide a valid tweet (or link to tweet)"


  tweet_text = tweet_data["data"][0]["text"]

  # create media description from alt text
  media_descrip = ""
  try:
    for img in tweet_data["includes"]["media"]:
      media_descrip += img["alt_text"] + " "
  except:
    print("error in alt-text")


  if (emoji_string):
    tweet_embed = get_tweet_embed(tweet_link)
    return render_template('GPTOutput.html', tweet_link=tweet_link, tweet_text=tweet_text, media_descrip=media_descrip, GPT_output=emoji_string, tweet_embed=tweet_embed)
 
  else:
    GPT_output = get_response(tweet_text, media_descrip)["choices"][0]["text"]
    return redirect(url_for('emoji_result')+"?tweet_link={}&emoji_string={}".format(tweet_link, GPT_output))


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(debug=True, host='0.0.0.0', port=port)