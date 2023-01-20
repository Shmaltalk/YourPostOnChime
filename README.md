# YourPostOnChime

This website takes a tweet link and translates it into emojis using GPT3.


## Deployment

The website is hosted on Google Cloud Run. To update, run `gcloud run deploy`


## Local Deployment

This app runs on flask. To test locally run `flask --app server --debug run`



If you want to text the docker image locally:
- rebuild with `docker build -t chime-posts`
- then run with `docker run -p 5001:8080 -e API_TOKEN_TWITTER=<token> -e API_KEY_CHATGPT=<key> chime-posts`

It will run at localhost:5001