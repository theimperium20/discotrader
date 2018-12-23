import time
import configparser
import sys
import pandas as pd
import json
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import discord

#initialise chrome headless :awwyeah:
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_driver = os.getcwd()+"\\chromedriver.exe"


def generate_url(symbol,trigger,qty):
    global url
    url = "https://pro.upstox.com/trade/?place&exchange=NSE&series=FO&symbol={}" \
          "&quantity={}&side=sell&complexity=co&position=i&tif=day&orderType=m&triggerPrice={}&refCode=4V6P" \
          .format(symbol,qty,trigger)
    return(url)


#Discord Bot
token = 'YOURBOTTOKENHERE' #Credential
client =discord.Client() #Start Discord client

#Defining what to when 'dexter' posts a trade call
@client.event
async def on_message(message):  # check if there is a call from dexter.
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    if str(message.author) == "discordusername#discriminator" and '!'== message.content[0]:
        message.content = message.content.strip('!')
        symbol,trigger,side,ifmkt,qty,intra = message.content.split(',')
        generate_url(symbol,trigger,qty)
        await message.channel.send(url)


#async def on_message(message): #check if there is a //take
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    if '//take' in message.content:
        try:
            user_list = pd.read_csv("users.csv")
            #creds = data_complete.loc[data_complete['Symbol'] == stock]['High'][6]
            client_code = str(user_list.loc[user_list['disid'] == str(message.author)]['upxname'][0])
            client_pass = str(user_list.loc[user_list['disid'] == str(message.author)]['upxpass'][0])
            client_year = str(user_list.loc[user_list['disid'] == str(message.author)]['upxcode'][0])
            #launch the order link
            driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=chrome_driver)
            #driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(5)
            user = driver.find_element_by_name("username")
            password = driver.find_element_by_name("password")
            year = driver.find_element_by_name("passcode")
            user.clear()
            user.send_keys(client_code)
            password.clear()
            password.send_keys(client_pass)
            year.clear()
            year.send_keys(client_year)
            year.send_keys(u'\ue007')
            time.sleep(2)
            element =driver.find_element_by_class_name("place-btn").send_keys(u'\ue007')
            order_status = driver.find_element_by_class_name('order-status').text
            status_message = driver.find_element_by_class_name('status-msg').text
            notify = 'Order Fired, '+ message.author.mention +'. Your order was ' + order_status +' because ' + status_message

            await message.channel.send(notify)
        
        except:
            text = 'Sorry, ' + message.author.mention + '. Your are not under our SB'
            await message.channel.send(text)
            

client.run(token)
