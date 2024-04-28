import os
from openai import OpenAI

API_KEY_CHATGPT = os.environ['API_KEY_CHATGPT']

client = OpenAI(api_key=API_KEY_CHATGPT)


def generate_prompt(tweet_text, media_descrip):

  prompt_text = """
    I will provide you with a description of a post. You give me back a string of no more than 6 emojis that is a representation of that description.
    If the description I give you is racist, anti-semitic, or homophobic return only the 🚫 emoji. Otherwise, do not return the 🚫 emoji.
    Otherwise, you need to send back at least two emojis. Do not include any text in your response, only include emojis.

    The first emoji should describe the overall mood of the post and must be one of the following: 🙂 for satisfied, 😢 for sad, 😊 for happy, 😰 for scared, 🥱 for tired, 😐 for bored, 😄 for excited, 😡 for angry, and 😣 for stressed.
    You should then include a space.
    You should then include between 1 and 5 emojis that describe why the person is feeling that way.

    Example:
    The text of the post reads...
    in real life yoda would get eaten by a dog

    Response:
    😐 🟢👶➡️🥩🐕

    Example:
    The text of the post reads...
    I got 2nd place in the @LimitlessTCG tour! Thank you to all my opponents and to @BillaVGC for hosting! Paste: https://t.co/5P72ulEh7y https://t.co/xstGVfVcGc
    There is also an image with the description, A team code from Pokemon Scarlet and Violet.

    Response:
    😄 ⛔️🥈🎉🙏🙏

    Here is the post description:
    The text of the post reads...
    {}
  """.format(tweet_text)

  if (media_descrip):
    prompt_text += "There is also an image with the description, {}".format(media_descrip)
  
  prompt_text += """
  
  Response:"""

  print(prompt_text)
  return prompt_text

def get_response(tweet_text, media_descrip):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages = [
      {"role": "user", "content": generate_prompt(tweet_text, media_descrip)}
    ],
    temperature=1.5,
  )

  return response.choices[0].message.content