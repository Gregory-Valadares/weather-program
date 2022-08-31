import json
import urllib.parse as urlp
from datetime import datetime as dt


#-----------------------------------------------------------------------------------------------------------------------
#   Função que mostra a introdução do programa e lê o local que o usuário deseja pesquisar o clima/tempo
#   e retorna no formato URL Encode.
def intro():
    print(('<>') * 20 + '\n')
    print('WEATHER FORECAST PROGRAM')
    print('\n' + ('<>') * 20)
    cityText = input('Enter the city name: ').title()
    stateText = input('Enter the state name: ').title()
    countryText = input('Enter the country name: ').title()
    textSearch = cityText + ', ' + stateText + ', ' + countryText
    c_textSearch = urlp.quote_plus(str(textSearch))  # <---c  Converted Text Search
    print('Loading...')
    return c_textSearch

#-----------------------------------------------------------------------------------------------------------------------
def statuscodeCheck(r1, r2):
    if r1.status_code == 200:
        try:
            jsonText = json.loads(r1.text)
            return jsonText
        except:
            return None
    elif r2.status_code == 200:
        try:
            jsonText = json.loads(r2.text)
            return jsonText
        except:
            return None
    else:
        try:
            print('We apologize for the inconvenience, but the service is currently unavailable. Try again later.')
            print('R1 statuscode: ' + r1.status_code)
            print('R2 statuscode: ' + r2.status_code)
        except:
            return None

#-----------------------------------------------------------------------------------------------------------------------
#   Função que mostra as condições climáticas atuais.
def showCurrentConditions(CurCondDic, city, state, country):
    print(('\n')*20)
    print(('<>')*20)
    print(city + ' , ' + state + '. ' + country)
    x = 0
    while x <= 4:
        try:
            print('Date: ' + CurCondDic['weekDate' + str(x)] + ' | ' + CurCondDic['Date' + str(x)])
            print('Temperature: ' + CurCondDic['celcius' + str(x)] + '\xb0' + 'C | ' + CurCondDic['fahrenheit' + str(x)] + '\xb0' + 'F')
            print('Weather: ' + CurCondDic['weatherText' + str(x)])
            print(('<>') * 20)
            x += 1
        except:
            break

#-----------------------------------------------------------------------------------------------------------------------
#   Função que organiza as informações da previsão dos próximos 4 dias em um dicionário chamado "ForecastDic".
def MakeForecastDic(ForecastText):
    ForecastDic = {}
    x = 0
    while x <= 4:
        timestamp2 = ForecastText['DailyForecasts'][x]['EpochDate']
        date_time = dt.fromtimestamp(timestamp2)

        ForecastDic['weekDate' + str(x + 1)] = date_time.strftime("%A")
        ForecastDic['Date' + str(x + 1)] = date_time.strftime("%d %B, %Y")
        ForecastDic['MaxCelcius' + str(x + 1)] = str(ForecastText['DailyForecasts'][x]['Temperature']['Maximum']['Value'])
        ForecastDic['MinCelcius' + str(x + 1)] = str(ForecastText['DailyForecasts'][x]['Temperature']['Minimum']['Value'])

        maxC = float(ForecastText['DailyForecasts'][x]['Temperature']['Maximum']['Value'])
        maxF = ((maxC * (9/5)) + 32)
        maxF = round(maxF,1)

        minC = float(ForecastText['DailyForecasts'][x]['Temperature']['Minimum']['Value'])
        minF = ((minC * (9/5)) + 32)
        minF = round(minF,1)

        ForecastDic['MaxFahrenheit' + str(x + 1)] = str(maxF)
        ForecastDic['MinFahrenheit' + str(x + 1)] = str(minF)

        ForecastDic['WeatherDay' + str(x + 1)] = ForecastText['DailyForecasts'][x]['Day']['IconPhrase']
        ForecastDic['WeatherNight' + str(x + 1)] = ForecastText['DailyForecasts'][x]['Night']['IconPhrase']
        x += 1
    return ForecastDic

#-----------------------------------------------------------------------------------------------------------------------
def show5DaysForecast(ForecastDic, city, state, country):
    print(('\n') * 20)
    print(('<>') * 20)
    print(city + ' , ' + state + '. ' + country + ' - TODAY')
    x = 0
    while x <= 4:
        try:
            print('Date: ' + ForecastDic['weekDate' + str(x + 1)] + ' | ' + ForecastDic['Date' + str(x + 1)])
            print('Maximum: ' + ForecastDic['MaxCelcius' + str(x + 1)] + '\xb0' + 'C , ' + ForecastDic[
                'MaxFahrenheit' + str(x + 1)] + '\xb0' + 'F')

            print('Minimum: ' + ForecastDic['MinCelcius' + str(x + 1)] + '\xb0' + 'C , ' + ForecastDic[
                'MinFahrenheit' + str(x + 1)] + '\xb0' + 'F')

            print('Day Weather: ' + ForecastDic['WeatherDay' + str(x + 1)])
            print('Night Weather: ' + ForecastDic['WeatherNight' + str(x + 1)])
            print(('<>') * 20)
            x += 1
        except:
            break

#-----------------------------------------------------------------------------------------------------------------------
#   função que retorna a latitude e longitude mantendo a integridade do programa caso o usuário escreva uma localização indisponível.
def LatLon(latLonText):
    try:
        lat = str(latLonText[0]['lat'])
        lon = str(latLonText[0]['lon'])
        LatLon = lat + '%2C' + lon
        return LatLon
    except:
        print('Latitude and longitude of the searched location are unavailable. Try searching using a different reference.')