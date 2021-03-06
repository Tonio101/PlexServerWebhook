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

### Install Python3 required modules:

```bash
python3 -m pip install -r requirements.txt
```

### Enable Webhook Server

Add credentials to `src/plex_webhook_config.yml` and [SMS Gateway](https://www.freecarrierlookup.com/)

Run `start_plex_webhook.sh` to enable the service.

Add the following URL to the Plex server webhook settings:<br/>

```bash
http://<YOUR_SERVER_IP>:6669/webhook
```

Test the Webhook server by playing your media files in Plex.<br/>
Or send a `POST` request using curl:
```bash
curl -kv -X POST -H "Content-Type: application/json" \
-d '{"username": "Hello", "content": "World"}' "http://<YOUR_SERVER_IP>:6669/webhook"
```

### Create WebHook Plex Service

After you confirmed that its working create a service.<br/>
Change the paths in `plexyhook.service`.

```bash
sudo cp plexyhook.service /etc/systemd/system/
sudo systemctl enable plexyhook.service
sudo systemctl start plexyhook.service
```

### Create a Cron Job to Start the Webhook Process

```bash
crontab -e
* * * * * <your_path>/start_plex_webhook.sh
```

### Send Text Messages via Command Line

Install mail utilities:<br/>
```bash
  sudo apt install ssmtp mailutils -y
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
  echo "Hello World!" | mail -s 'Test' <PHONE_NUMBER>@tmomail.net
```

