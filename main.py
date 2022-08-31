import requests
import functions as f
from datetime import datetime as dt


YorN1 = 'y'
while YorN1 == 'y' or YorN2 == 'n':
    try:
    #-----------------------------------------------------------------------------------------------------------------------
    #Apresentação do programa e pedir a cidade, estado e país que o usuário deseja saber o clima/tempo.
        c_textSearch = f.intro()

    #-----------------------------------------------------------------------------------------------------------------------
    #Pegue a cidade, estado e país e mande para um geolocalizador e guarde a latitude e longitude.
        openWeatherKey1 = #'put openWeather token here'
        openWeatherKey2 = #'put the second openWeather token here'

        r1 = requests.get('http://api.openweathermap.org/geo/1.0/direct?q=' + c_textSearch + '&limit=5&appid=' + openWeatherKey1)
        r2 = requests.get('http://api.openweathermap.org/geo/1.0/direct?q=' + c_textSearch + '&limit=5&appid=' + openWeatherKey2)

        latLonText = f.statuscodeCheck(r1, r2)
        #city = LatLonText[0]['name']
        #state = LatLonText[0]['state']
        #countryInitials = LatLonText[0]['country']
        LatLon = f.LatLon(latLonText)
    #-----------------------------------------------------------------------------------------------------------------------
    #Pegue a latitude e longitude e use uma api que te fornece a chave do local para utilização do AccuWeather.
        accuweatherAPIKey1 = #'put accuweatherAPIKey here'
        accuweatherAPIKey2 = #'put the second accuweatherAPIKey here'

        r3 = requests.get('http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey='\
            + accuweatherAPIKey1 + '&q=' + LatLon)
        r4 = requests.get('http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey='\
            + accuweatherAPIKey2 + '&q=' + LatLon)

        locationKeyText = f.statuscodeCheck(r3, r4)

        locationKey = locationKeyText['Key']
        city = locationKeyText['LocalizedName']
        state = locationKeyText['AdministrativeArea']['LocalizedName']
        country = locationKeyText['Country']['LocalizedName']

    #-----------------------------------------------------------------------------------------------------------------------
    #Pegue a locationKey e use uma api que te fornece o clima atual.
    #Guarte todas as informações em um dicionário.
        r5 = requests.get('http://dataservice.accuweather.com/currentconditions/v1/' + locationKey + '?apikey=' + accuweatherAPIKey1)
        r6 = requests.get('http://dataservice.accuweather.com/currentconditions/v1/' + locationKey + '?apikey=' + accuweatherAPIKey2)

        CurConditText = locationKeyText = f.statuscodeCheck(r5, r6)

        CurCondDic = {}
        timestamp1 = CurConditText[0]['EpochTime']
        date_time = dt.fromtimestamp(timestamp1)

        CurCondDic['weekDate0'] = date_time.strftime("%A")                                     #<---UTILIZAREMOS
        CurCondDic['Date0'] = date_time.strftime("%d %B, %Y")                                  #<---UTILIZAREMOS
        CurCondDic['weatherText0'] = CurConditText[0]['WeatherText']                           #<---UTILIZAREMOS
        CurCondDic['celcius0'] = str(CurConditText[0]['Temperature']['Metric']['Value'])       #<---UTILIZAREMOS
        CurCondDic['fahrenheit0'] = str(CurConditText[0]['Temperature']['Imperial']['Value'])  #<---UTILIZAREMOS

        #print(CurCondDic)   #<--- Quando for criar as funções, troque para "return CurCondDic"

    #-----------------------------------------------------------------------------------------------------------------------
    #Mostre o clima atual
        f.showCurrentConditions(CurCondDic, city, state, country)

    #-----------------------------------------------------------------------------------------------------------------------
    #   Perguntar ao usuário se ele deseja ver a previsão dos próximos 4 dias do local digitado.
        YorN1 = input('Do you want to see the forecast for the next 4 days? (Y or N): ').lower()
        if YorN1 == 'y':
    #-----------------------------------------------------------------------------------------------------------------------
    #Pegue a latitude e longitude e use uma api que te fornece o clima dos próximos 5 dias.
    #Guarte todas as informações em um dicionário.
            r7 = requests.get('http://dataservice.accuweather.com/forecasts/v1/daily/5day/' + locationKey + '?apikey=' + accuweatherAPIKey1 + '&metric=true')
            r8 = requests.get('http://dataservice.accuweather.com/forecasts/v1/daily/5day/' + locationKey + '?apikey=' + accuweatherAPIKey2 + '&metric=true')

            ForecastText = f.statuscodeCheck(r7, r8)

            ForecastDic = f.MakeForecastDic(ForecastText)

            f.show5DaysForecast(ForecastDic, city, state, country)

            input('Press enter to search other city...')
            print(('\n')*50)
    #-----------------------------------------------------------------------------------------------------------------------

        else:
            YorN2 = input('do you want to close the program? (Y or N): ').lower()
            if YorN2 == 'y':
                break
            else:
                continue

    except:
        continue
