from flask import Flask, request, render_template
import requests
from datetime import datetime, timedelta
import json

app = Flask(__name__)


# Tiingo api token: 2a4c11eb6e1fa5f9faa5fd6d76af7445b26ff398
@app.route('/')
def front_page():
    return render_template("index.html")


@app.route('/getinfo', methods=["GET"])
def get_info():
    # get outlook and summary information
    stock = request.args.get('name')
    api_key = "?token=2a4c11eb6e1fa5f9faa5fd6d76af7445b26ff398"
    daily_url = "https://api.tiingo.com/tiingo/daily/"
    daily_full_url = daily_url + stock + api_key
    daily_request = requests.get(daily_full_url)
    outlook = daily_request.json()
    # return the error page if the stock ticker is not valid
    if outlook.get("detail") == 'Not found.':
        return render_template("error.html")
    iex_url = "https://api.tiingo.com/iex/"
    iex_full_url = iex_url + stock + api_key
    iex_request = requests.get(iex_full_url)
    summary = iex_request.json()

    # retrive the chart information within six month (180days)
    now = datetime.now()
    start = (now - timedelta(days=180)).strftime('%Y-%m-%d')
    chart_url = "https://api.tiingo.com/iex/" + stock + "/prices?startDate=" + start + "&resampleFreq=12hour&columns=close,volume&token=2a4c11eb6e1fa5f9faa5fd6d76af7445b26ff398"
    chart_request = requests.get(chart_url)
    chart = chart_request.json()
    # result json format: {'date': '2020-06-18T16:00:00.000Z', 'close': 351.66, 'volume': 156568.0}
    # save the x, y axis plot data in a list
    closepricearr = []
    volumearr = []
    for i in range(len(chart)):
        t = datetime.strptime(chart[i]['date'], '%Y-%m-%dT%H:%M:%S.000Z')
        # convert the date string into timestamp(example: 1592607600000)
        stamp = int(t.timestamp()) * 1000
        closepricearr.append([stamp, chart[i]['close']])
        volumearr.append([stamp, chart[i]['volume']])
    # turn the list data into json format
    closeprice_json = json.dumps(closepricearr)
    # print(closeprice_json)
    volume_json = json.dumps(volumearr)
    # get most recent news
    news_url = "https://newsapi.org/v2/everything?apiKey=f94b8a1412874311a4496b3caee5efaf&q=" + stock
    news_request = requests.get(news_url)
    newsList = news_request.json()["articles"]

    return render_template("result.html", outlook=outlook, summary=summary[0], newsList=newsList,
                           closeprice_json=closeprice_json, volume_json=volume_json)


if __name__ == '__main__':
    app.run()
