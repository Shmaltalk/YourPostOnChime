import os
from flask import Flask, render_template, request, redirect, url_for
from get_toot_data import get_toot_data, get_toot_embed
from send_to_chatGPT import get_response

app = Flask(__name__)

@app.route('/') 
def index():
  return render_template('index.html')

@app.route('/emoji_result', methods = ['GET'])
def emoji_result():

  # arguments
  toot_link = request.args.get('toot_link')
  message_text = request.args.get('message_text')
  emoji_string = request.args.get('emoji_string')
  media_descrip = request.args.get('media_descrip')

  if (not media_descrip):
    media_descrip = ""

  if(toot_link):
    print("toot")
    return toot_case(toot_link, emoji_string, media_descrip)
  elif(message_text):
    return text_case(message_text, emoji_string, media_descrip)
  else:
    return "Please provide either a toot or some text to emojify"

# when user inputs toot
def toot_case(toot_link, emoji_string, media_descrip):

  # get toot server
  toot_server=toot_link.split("/")[-3]

  # get just toot id
  toot_id = toot_link.split("/")[-1] # gets just the id and params
  toot_id = toot_id.split("?")[0] # removes params

  print("toot id:", toot_id)

  # get json of toot data from twitter API
  try:
    toot_data = get_toot_data(toot_server, toot_id)
  except Exception as e:
    print(e)
    return "Please provide a valid toot (or link to toot)"


  toot_text = toot_data["content"]
  toot_media=toot_data["media_attachments"]
  
  # create media description from alt text
  try:
    if toot_media and not media_descrip:
      for img in toot_media:
        media_descrip += img["description"] + " "
  except:
    print("error in alt-text")
  
  # generate a media description if we need one
  # if ((media_descrip) and toot_data["includes"]["media"][0]["url"]):
  #   media_descrip = get_img_descrip(toot_data["includes"]["media"][0]["url"])
  #   return media_descrip

  if (emoji_string):
    toot_embed = get_toot_embed(toot_link)
    return render_template('EmojiOutput.html', toot_link=toot_link, toot_text=toot_text, media_descrip=media_descrip, emoji_string=emoji_string, toot_embed=toot_embed, disable_edit=True)
 
  else:
    GPT_output = get_response(toot_text, media_descrip)
    return redirect(url_for('emoji_result')+"?toot_link={}&emoji_string={}&media_descrip={}".format(toot_link, GPT_output, media_descrip))

# when the user inputs text and no toot link
def text_case(message_text, emoji_string, media_descrip):
  # return message text in quotes
  toot_embed = '<div class="text-embed">"{}"</div>'.format(message_text)

  if (emoji_string):
    return render_template('EmojiOutput.html', message_text=message_text, media_descrip=media_descrip, emoji_string=emoji_string, toot_embed=toot_embed, disable_edit=False)
  else:
    GPT_output = get_response(message_text, media_descrip=media_descrip)
    return redirect(url_for('emoji_result')+"?message_text={}&emoji_string={}&media_descrip={}".format(message_text, GPT_output, media_descrip)) 


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(debug=True, host='0.0.0.0', port=port)