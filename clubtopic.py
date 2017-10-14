import sopel.module
import requests
import re

@sopel.module.thread(True)
@sopel.module.interval(15)
def entropia_club_topic(bot):
  headers = {'user-agent': 'Entropia IRC-Bot by Kunsi'}
  channel = '#entropia'
  url = 'http://club.entropia.de/status.json'

  if channel in bot.channels:
    r = requests.get(url)

    if r.status_code == requests.codes.ok:
      clubstatus = r.json()
      old_topic = bot.channels[channel].topic

      if clubstatus['club_offen']:
        status = 'offen'
      else:
        status = 'geschlossen'

      new_topic = re.sub(r"(club[^:]*:) \w+", "\\1 " + status, old_topic, flags=re.IGNORECASE)

      if old_topic != new_topic:
        bot.write(('TOPIC', channel,), text=new_topic)
