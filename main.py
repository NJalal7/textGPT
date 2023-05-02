from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from base64 import b64encode
import requests
import json
import sentry_sdk

sentry_sdk.init(
    dsn="https://a7092f2507cf4b3fbe57a2b74c332cc1@o4505110321692672.ingest.sentry.io/4505110409117696",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_message(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send_sms", response_class=HTMLResponse)
async def send_message(request: Request, to_number: str = Form(...)):

  payload = {

      "to": {
          "type": "sms",
          "number": to_number
      },

      "from": {
          "type": "sms",
          "number": [5197090528]
      },

      "message": {
          "content": {
              "type": "text",
              "text": "ChatGPT, I need an icebreaker in Spanish!"
          }
      }
  }

  secret = '12345'
  key = 'abcde'
  encoded_credentials = b64encode(bytes(f'{key}:{secret}',
                                     encoding='ascii')).decode('ascii')

  auth_header = f'Basic {encoded_credentials}'
  headers = {"content-type": "application/json", "Authorization": auth_header}
  response = requests.post("https://api.nexmo.com/v0.1/messages",
                        auth=(key, secret),
                        headers=headers,
                        data=json.dumps(payload))

  if response:
    return templates.TemplateResponse("send.html", {"request": request, "number": to_number})

  raise Exception(response.raise_for_status())
  return templates.TemplateResponse("send.html", {"request": request, "error": "The SMS could not be sent."})
