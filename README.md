# Plex Server Simple Webhook

Send a text notification from a Plex Server Webhook event.

### Configure RaspberryPi to send text messages:
I recommend creating a dummy gmail account for any<br/>
raspberry pi development since the password is stored<br/>
in clear text.<br/>

After creating your gmail account:<br/>

<ol>
<li>Login to your gmail account.</li>
<li>Go to https://www.google.com/settings/security/lesssecureapps and Turn Off this feature.</li>
<li>Go to https://accounts.google.com/DisplayUnlockCaptcha and click Continue.</li>
</ol>

Install mail utilities:<br/>
```bash
  sudo apt install ssmtp
  sudo apt install mailutils
```

In `/etc/ssmtp/ssmtp.conf` include:<br/>
```bash
root=postmaster
mailhub=smtp.gmail.com:587
hostname=<YOURHOSTNAME>
AuthUser=<YOUREMAIL>
AuthPass=<YOURPASSWORD>
FromLineOverride=YES
UseSTARTTLS=YES
Debug=YES
```

To send a text message:<br/>
You can find your service provider SMS gateway address [here](https://www.freecarrierlookup.com/)

```bash
  echo "World!" | mail -s 'Hello' <PHONE_NUMBER>@tmomail.net
```
That's it! Now you can send text messages via command line.

### Install Python3 required modules:

```bash
python3 -m pip install -r requirements.txt
```

### Enable Webhook Server

```bash
python3 plex_webhook.py --phone <YOUR_PHONE_NUMBER>
```

### Enable Webhook on Plex Server Settings

Add the following URL to the Plex server webhook settings:<br/>

```bash
http://<YOUR_SERVER_IP>:6669/webhook
```

Test the webhook server by playing your media files in Plex.<br/>

Or send a `POST` request using curl:
```bash
curl -kv -X POST -H "Content-Type: application/json" \
-d '{"username": "Hello", "content": "World"}' "http://<YOUR_SERVER_IP>:6669/webhook"
```
