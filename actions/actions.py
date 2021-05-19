# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests
import json

import pandas as pd
import numpy as np
import xlrd

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_temp_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            cityname=str(tracker.get_slot("city"))
            print(cityname)
            try:
                url = "http://api.openweathermap.org/data/2.5/weather?q="+cityname+'&appid=4c554b28c1c06d3bf58fbad56143605a'
                response = requests.get(url).json()
                overview=response['weather'][0]['main']
                temp=response['main']['temp']
                wind=response['wind']['speed']
                #data = json.dumps(response, indent=4, separators=(". ", " - "))
                dispatcher.utter_message(f"Nhiệt độ : {temp} \nSức gió: {wind} \nTrạng thái : {overview} \nThành phó: {cityname}")
            except:
                dispatcher.utter_message(f"Lỗi")
            return []


class Actioncheckpoint(Action):
    def name(self) -> Text:
        return "action_check_point"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            df = pd.read_excel('data.xls',sheet_name='KET QUA PH KY I NAM 20-21',header=None,skiprows=11,skipfooter=11)
            id=input()

            if id in df.values :
                index_x,index_y = np.where(df.values== id)
                print('Truoc khi phuc khao: ' + str(df[8][index_x[0]]))
                print('Sau khi phuc khao: ' + str(df[10][index_x[0]]))
                dispatcher.utter_message(f"Truoc khi phuc khao: {str(df[8][index_x[0]])} \nSau khi phuc khao: {str(df[10][index_x[0]])}")
            else:
                dispatcher.utter_message(f"Nhập lại mã sinh viên!!!")
            return []

class ActionCorona(Action):

    def name(self) -> Text:
        return "action_corona"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/asia"

            headers = {
                'x-rapidapi-key': "fae8fe3789msh17c37b9aaf22d7bp18e8cfjsn97bda12a619f",
                'x-rapidapi-host': "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com"
                }

            ct=str(tracker.get_slot("country"))
            ct=ct.capitalize()
            ct=ct.replace(' ','')
            print(ct)

            response = requests.get(url, headers=headers).json()
            data = json.dumps(response,sort_keys=True, indent=20, separators=(". ", " - "))

            id= [x for x in range(len(response)) if response[x]["Country"]==ct]
            k=id[0]

            dispatcher.utter_message(f"Tổng số ca mắc : {str(response[k]['TotalCases'])}")
            dispatcher.utter_message(f"Số ca mắc mới : {str(response[k]['NewCases'])}")
            dispatcher.utter_message(f"Tổng số ca tử vong : {str(response[k]['TotalDeaths'])}")
            dispatcher.utter_message(f"Số ca tử vong trong ngày : {str(response[k]['NewDeaths'])}")
            dispatcher.utter_message(f"Tổng số ca bình phục : {str(response[k]['TotalRecovered'])}")
            dispatcher.utter_message(f"Số ca mới bình phục : {str(response[k]['NewRecovered'])}")
            dispatcher.utter_message(f"Số ca đang điều trị : {str(response[k]['ActiveCases'])} ")

            return []