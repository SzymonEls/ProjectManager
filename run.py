import os
from app import create_app
from dotenv import load_dotenv

load_dotenv(override=True)

debug = int(os.getenv('DEBUG'))
https = int(os.getenv('HTTPS'))
domain = os.getenv('DOMAIN')

app = create_app()

port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
   if https:
      app.run(host="0.0.0.0", port=443, ssl_context=(
        "/etc/letsencrypt/live/" + domain + "/fullchain.pem",
        "/etc/letsencrypt/live/" + domain + "/privkey.pem"
    ))
   else:
      app.run(debug=debug, host='0.0.0.0', port=port)