import falcon
import json
import requests

from os import environ

API_TOKEN = environ.get('API_TOKEN')
BOT_TOKEN = environ.get('BOT_TOKEN')


def respond(channel_id):
    headers = {
      'Authorization': f'Bearer {API_TOKEN}',
      'Content-Type': 'application/json;charset=UTF-8',
    }
    requests.post(
        'https://slack.com/api/chat.postMessage',
        headers=headers,
        json={
            'text': 'YIII',
            channel: channel_id, 
        }
    )


class MessageResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps({
            "status": "ok"
        })

    def on_post(self, req, res):
        body = json.load(req.bounded_stream)
        print('body ', body)

        if 'challenge' in body:
            res.status = falcon.HTTP_200
            res.body = json.dumps({
                'challenge': body['challenge']
            })
            return

        if 'token' not in body or body['token'] != BOT_TOKEN:
            res.status = falcon.HTTP_401
            return

        event = body.get('event', {})

        event_type = event.get('type')
        event_subtype = event.get('subtype')
        message_text = event.get('text')
        channel_id = event.get('channel')

        if event_subtype == 'bot_message':
            res.status = falcon.HTTP_200
            return

        if eventType != 'app_mention':
            return

        respond(channel_id);
        res.status = falcon.HTTP_200


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
message = MessageResource()

# things will handle all requests to the '/things' URL path
app.add_route('/message', message)
