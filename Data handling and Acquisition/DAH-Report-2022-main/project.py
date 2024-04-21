#%%
'''This python script can be run on its own without connecting to the local server to check
    it is working - you can also just run it anyway to find the rainfall data from other 
    weather stations in edinburgh. If not connected to the local server you can change the
    manual input values for temp, humidity and rainfall in the function 
    water_sensor_test_data(), for testing.
    you can also check the data previously taken by our weather station beause the code 
    stores values taken previously provided you still have the file. if you do not another 
    will be made with new vaues you record'''

#%%
'''importing libaries and useful functions...'''
import math, requests
import numpy as np
import glob, os, csv
import random
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import urllib.request, json 
import names
from calendar import monthrange
'''import functions from other files'''
from our_sensor_data import get_tempNhum

'''modify this to the directory that your python file is in'''
directory = r"C:\Users\hanna\OneDrive - University of Edinburgh\Documents\University\Year 4\DAH\Project/"


#%%
'''Gathering Metoffice data from Edinburgh'''

def get_online_data(link):
    urlrainfall = link
    r = requests.get(urlrainfall, allow_redirects=True)
    text = r.text
    with open('rainfall_data.txt', 'wb') as f:
        f.write(r.content)
    df = pd.read_csv('rainfall_data.txt', delim_whitespace=True, skiprows=[0, 1, 2, 3, 4])
    last_updated = pd.read_csv('rainfall_data.txt', sep='\t', skiprows=np.arange(5, 1000, 1))
    print(last_updated, '\n\n')
    return df

'''INDEX [1] FOR THESE IS DATA AND FOR INFORMATION WHEN LAST UPDATED USE [0]'''
rain_data = get_online_data('https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Rainfall/date/Scotland_E.txt')
# temp_data = get_online_data('https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmean/date/Scotland_E.txt')


#%%
'''All usefull functions including definding the date'''
def dp(value):  # for printing to 1dp
    return "{:.1f}".format(value)

def daymonthyear():
    now = datetime.now()
    dmy = [now.day, now.strftime("%b").lower(), now.year]
    dmy.append(now.month)
    print('The date today is', dmy)
    return dmy  # as a list
today, tomonth, toyear, monthnum = daymonthyear()
no_daysTmonth = monthrange(toyear, monthnum)[1]

def printdf_tostring(df, column, type): # print column of df as a string
    # there should be idealy 1 row in the column
    print(type, df.loc[:, column].to_string(index=False))

def fetch_year(df, year):
    year_data = df[df['year'] == year]
    return year_data

def fetch_month(df, month):
    month_data = df[month].reset_index()
    return month_data

def fetch_chosen_MonthAvg(df, type, year):
    '''takes the (current) monthly average of a chosen year
        to be compared to previous years'''
    yeardf = fetch_year(df, year)
    monthdf = fetch_month(yeardf, tomonth)
    # printdf_tostring(monthdf, tomonth, type)
    return monthdf.loc[:, tomonth][0] # the avg for the month


#%%
'''finding the average temperature an rainfall for this month'''
# avg_temp = fetch_chosen_MonthAvg(temp_data, 'temp', toyear)
# avg_rainfall = fetch_chosen_MonthAvg(rain_data, 'rain', toyear)


# %%
'''geeting JSON file from sepa.org.uk website'''
'''getting the Json file from online whihc provides daily and hourly data for rainfall in edinburgh'''
daily_station525510 = 'https://www2.sepa.org.uk/rainfall/api/Daily/525510?all=true'
monthly_station525510 = 'https://www2.sepa.org.uk/rainfall/api/Month/525510'

def get_online_json(link, jsonname):
    '''retrieves data from online and saves it on your computer to the same directory as this file'''
    with urllib.request.urlopen(link) as url:
        data = json.load(url)
        with open(jsonname, 'w') as f:
            json.dump(data, f)
get_online_json(daily_station525510, 'daily_rain_data.json')
get_online_json(monthly_station525510, 'monthly_rain_data.json')


#%%
'''finding so far the total rainfall this month (cumlative). and this will be compared to 
previous years to see if it is higher or lower than average'''

def avg_rain_thismonth(jsonfile):
    months_data = {}
    cum_rain = 0
    f = open(jsonfile)
    data = json.load(f)
    for i in data:
        date = i['Timestamp'].split()[0]  # getting day, month & year of the value 
        jsonday, jsonmonth, jsonyear = list(map(int, date.split('/')))
        value = float(i['Value'])  # mm of rainfall for timestamp

        if jsonyear == toyear:
            if jsonmonth == monthnum:  # if year and month is the same as now
                months_data[jsonday] = value  # make dict where key=day of month and value = rainfall
                cum_rain += value  # add to cumlavtive rain for the month

    # print('Cumlative sum of rain this month =', cum_rain)
    return months_data, cum_rain


# %%
'''plotting the rainfall this month'''
def plot(dict, xaxis, yaxis, title):
    plt.style.use('ggplot')
    fig = plt.figure()
    ax = fig.add_subplot(111, xlabel=xaxis, ylabel=yaxis, title=title)
    ax.plot(*zip(*sorted(dict.items())), label='This Month')
    plt.gca().set_xlim(left=0, right=no_daysTmonth+2)
    plt.gca().set_ylim(bottom=0)
    return ax

def add_line(ax, y, label): # add an average for the month
    ax.plot([0, 31], [y, y], label=label)

def add_point(ax, x, y, label):  # adds a point to shows where today is
    #  this function will use data from the arduino 
    ax.scatter(x, y, label=label, marker='x', s=60)


# %%
'''Plot this months rainfall and previouss'''
'''now i want to comapre this months rainfall to previous years'''
def comapre_previsous_year_rain(cum_rainfall_this_month):
    prev50years = list(range(toyear-50, toyear)) # the 5 previous years not including this
    values = []
    for i in prev50years:
        values.append(fetch_chosen_MonthAvg(rain_data, 'rain', i))
    prevyears = np.mean(values)

    print(f'For {tomonth}:')
    print('last 50 years avg rainfall =', dp(prevyears), 'mm')
    print('this years =', dp(cum_rainfall_this_month), 'mm') 
    avgperdaythismonth = cum_rainfall_this_month/(today-1)  # -1 because the most recent data is yesterday
    avgperdaypevyears = prevyears/no_daysTmonth

    if  avgperdaythismonth < avgperdaypevyears: # divide it by the number of days
        pc = 100*(avgperdaypevyears-avgperdaythismonth)/avgperdaypevyears
        print('below the average so far this month by', dp(pc), '%')
    else:
        pc = 100*(-avgperdaypevyears+avgperdaythismonth)/avgperdaypevyears
        print('Already! We are above average rainfall for ths month by', dp(pc), '%')
        print(f'better start recycling more, {names.get_full_name()} or the weather might get worse!')

    return prevyears
    

#%%
'''getting data from the server in the lab. temp, humidity and water level'''
'''NOTE: You must be on the local server where the arduino is uploading to use this function'''
def water_sensor_test_data():  # test for when not connected to the local wifi
    return random.randint(3, 14), random.randint(70, 100), random.randint(0, 4)*10  # temp, hum, rain


#%%
'''this combines different functions to plot the rainfall plot all together'''
def plot_rainfall_graph(rainfall, daily_rainfall_data_thismonth, cum_rainfall_this_month, prevyears):
    '''next add the avg from the previous 5 years to the plot as a flat line'''
    ax = plot(daily_rainfall_data_thismonth, f'Days of {tomonth} {toyear}', 
        'Rainfall, mm', 'Rainfall This Month')
    add_line(ax, cum_rainfall_this_month/monthnum, 'Avg per Day This Month')
    add_line(ax, prevyears/no_daysTmonth, 'Previous Years Avg')
    add_point(ax, today, rainfall, 'Today\'s Rainfall')  
    plt.legend()
    plt.savefig(f'rainfall_{today}-{monthnum}-{toyear}.png')


#%%
'''plotting the humidity and temperature values that hav been colected using this computer'''
def plot_humidntemp(temp, hum, rain, plotmonth, plotyear):
    '''first gather the exsisting data and add the new recorded data'''
    filepath, filename = directory + "sensor_data.csv", "sensor_data.csv"

    datadict = {'temp': [], 'humid':[], 'rain': [], 'day':[], 'month':[], 'year':[], 'time':[]}  # empty dict
    datadict['temp'].append(temp)  # add new recorded values to empty dict
    datadict['humid'].append(hum)
    datadict['rain'].append(rain)
    datadict['day'].append(today)
    datadict['month'].append(monthnum)
    datadict['year'].append(toyear)
    datadict['time'].append(datetime.now().strftime("%H:%M:%S"))

    '''saving file if exsist, make new if doesnt'''
    if os.path.isfile(filepath):
        # cobmine old data with new
        # df = pd.read_csv(directory + "hum_temp_data.csv")
        df = pd.concat([pd.read_csv(filepath), pd.DataFrame(datadict)])  # merge df with dict
        df.to_csv(filename, index=False)  # save new df
    else:
        df = pd.DataFrame(datadict)  # create new df - no csv exsists
        df.to_csv(filename, index=False)  # save as csv
    
    # now plot and crop data to month and year chosen
    cropyear = df[df['year'] == plotyear]
    cropdf = cropyear[cropyear['month'] == plotmonth]

    '''plotting temp and hum below - not rain'''
    plt.style.use('ggplot')
    fig, (axhum, axtemp) = plt.subplots(2, sharex=True)
    fig.suptitle(f'The humidity and temperature data taken in {plotmonth}/{plotyear}')
    print(cropdf['humid'])
    axhum.plot(cropdf['day'], cropdf['humid'])
    axtemp.plot(cropdf['day'], cropdf['temp'])
    axtemp.set_xlabel(f'Days in Month:{plotmonth}, year:{plotyear}')
    axtemp.set_ylabel('Temperature, Celsius')
    axhum.set_ylabel('% Humidity')
    axtemp.set_xlim(left=0, right=today)
    axhum.set_ylim(bottom=0, top=102)
    plt.savefig(f'temp_hum_{today}-{monthnum}-{toyear}.png')


#%%
'''collecting all of the data together'''
def main():
    '''replace water_sensor_test_data()[2] for get_tempNhum(IPaddress) when connected to local server
    water_sensor_test_data()[2] is just for testing the code with manual input values'''

    temperature, humidity, rainfall = water_sensor_test_data()
    daily_rainfall_data_thismonth, cum_rainfall_this_month = avg_rain_thismonth('daily_rain_data.json')
    prevyears = comapre_previsous_year_rain(cum_rainfall_this_month)

    plot_rainfall_graph(rainfall, daily_rainfall_data_thismonth, cum_rainfall_this_month, prevyears)
    '''dependin on what you have data for you can change what month of the year you want to plot'''
    plot_humidntemp(temperature, humidity, rainfall, monthnum, toyear)  # month a year to plot

    return 'Now here are the weather plots'
main()


# %%
