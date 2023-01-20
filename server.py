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
  message_text = request.args.get('message_text')
  emoji_string = request.args.get('emoji_string')
  media_descrip = request.args.get('media_descrip')

  if (not media_descrip):
    media_descrip = ""

  if(tweet_link):
    print("tweet")
    return tweet_case(tweet_link, emoji_string, media_descrip)
  elif(message_text):
    return text_case(message_text, emoji_string, media_descrip)
  else:
    return "Please provide either a tweet or some text to emojify"

# when user inputs tweet
def tweet_case(tweet_link, emoji_string, media_descrip):

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
  try:
    for img in tweet_data["includes"]["media"]:
      media_descrip += img["alt_text"] + " "
  except:
    print("error in alt-text")
  
  # # generate a media description if we need one
  # if ((media_descrip) and tweet_data["includes"]["media"][0]["url"]):
  #   media_descrip = get_img_descrip(tweet_data["includes"]["media"][0]["url"])
  #   return media_descrip

  if (emoji_string):
    tweet_embed = get_tweet_embed(tweet_link)
    return render_template('EmojiOutput.html', tweet_link=tweet_link, tweet_text=tweet_text, media_descrip=media_descrip, emoji_string=emoji_string, tweet_embed=tweet_embed, disable_edit=True)
 
  else:
    GPT_output = get_response(tweet_text, media_descrip)["choices"][0]["text"]
    return redirect(url_for('emoji_result')+"?tweet_link={}&emoji_string={}&media_descrip={}".format(tweet_link, GPT_output, media_descrip))

# when the user inputs text and no tweet link
def text_case(message_text, emoji_string, media_descrip):
  # return message text in quotes
  tweet_embed = "\"{}\"".format(message_text)

  if (emoji_string):
    return render_template('EmojiOutput.html', message_text=message_text, media_descrip=media_descrip, emoji_string=emoji_string, tweet_embed=tweet_embed, disable_edit=False)
  else:
    GPT_output = get_response(message_text, media_descrip=media_descrip)["choices"][0]["text"]
    return redirect(url_for('emoji_result')+"?message_text={}&emoji_string={}&media_descrip={}".format(message_text, GPT_output, media_descrip)) 


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(debug=True, host='0.0.0.0', port=port)