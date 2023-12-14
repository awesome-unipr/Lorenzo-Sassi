import aiohttp
import datetime
import asyncio
import python_weather
import json
import os


async def main():
    
    async def getweather():
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            city = "Parma"
            weather = await client.get(city)
            temperature = int(weather.current.temperature)
            description = weather.current.description
            kind = weather.current.kind

            current_parameters = {"current_city" : city, "current_temperature" : temperature , 
                                  "current_description" : description , "current_kind" : kind}
            print('-----')
            print(temperature)
            print(description)
            print(kind)
            print('-----')
            return current_parameters
        
    async def getforecast():
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            city = 'Parma'
            weather = await client.get(city)
            now = datetime.datetime.now()
            
            i = 0
            ii = 0

            forecast_parameters = {}

            for forecast in weather.forecasts:

                date = forecast.date

                now_date = now.date

                number_of_forecasts = 7
                
                for hourly in forecast.hourly:
                    
                    h = int(hourly.time.strftime("%H"))
                    
                    now_h = int(now.time().strftime("%H"))

                    if (h > now_h or  i == 1) & (ii < number_of_forecasts):
                        #print(hourly)
                        print(forecast.date)
                        print(hourly.time)
                        print(hourly.temperature)
                        print(hourly.description)
                        print(hourly.kind)

                        i = 1

                        date =str(forecast.date.day)+"-"+str(forecast.date.month)+"-"+str(forecast.date.year)
                        time = str(hourly.time.hour)
                        kind = str(hourly.kind)  
    
                        forecast_parameters[ii] = {"date" : date, "time" : time ,"temperature" : hourly.temperature , 
                                                   "description" : hourly.description , "kind" : kind}

                        ii += 1

            print(forecast_parameters)
            return forecast_parameters

    async with aiohttp.ClientSession() as session:
        wc = await getweather()
        wf = await getforecast()
        
        json_wf = json.dumps(wf)
        #print(wf[0]["time"])
        print(wf[0]['kind'])

        async with session.post(url = 'http://localhost:8080/weathercurrent', data = wc) as response:
            print('current weather...')
            


        async with session.post('http://localhost:8080/weatherforecast', json = json_wf) as response:
            print('weather forecast...')
            
asyncio.run(main())