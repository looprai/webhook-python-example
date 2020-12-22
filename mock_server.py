from flask import Flask, request
import json
import hmac
import hashlib
app = Flask(__name__)
# Make sure this is the same secret you provided in the webhook creation
secret = 'secret'
@app.route('/', methods=['GET'])
def test():
    return "Hello World!"

@app.route('/webhook-endpoint', methods=['POST'])
def print_webhook_info():
  computed_signature = hmac.new(secret.encode('utf-8'), msg=request.headers['X-LoopR-event'].encode('utf-8'), digestmod=hashlib.sha1).hexdigest()
  print(computed_signature)
  if request.headers['X-LoopR-Signature'] != 'sha1='+computed_signature:
    print('Error: computed_signature does not match signature provided in the headers')
    return 'Error'

  print('=========== New Webook Delivery ============')
  print('Event: %s' % request.headers['X-LoopR-event'])
  print('Payload: %s' % json.dumps(json.loads(request.data.decode('utf8')),indent=4))
  return 'Success'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3001, debug=True)