# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 12:37:03 2022

@author: khass : for hex Frames please Check the documentation 

Development:https://ix5wrwn1jd.execute-api.us-east-1.amazonaws.com/dev
Mock Server:https://stoplight.io/mocks/foodwize-canteen/foodwize-canteen-api/56520568
An API key is a token that you provide when making API calls. Include the token in a header parameter called x-api-key.


"""
import requests
import socket   


########################################Building the url form ###################################

hostname=socket.gethostname()   

IPAddr=socket.gethostbyname(hostname)
 
ID=hostname+"_IP_"+IPAddr  

url = "https://ix5wrwn1jd.execute-api.us-east-1.amazonaws.com/dev"

 
headers = {"Content-Type": "application/json","x-api-key": "laYDmRmRVE6IqcwOxRFNl7zE37m5DSrEF6z6eUQ0"}
 

id="/9fe7fb0e-5012-bcf0-0bcd-a1185394c9b2"

##################################################################################################

def Get_status():
    response_status = requests.get(url+"/status"+id, headers=headers)
    return response_status

def PUT_status(status:str):
    data={
      "canteen_id": "9fe7fb0e-5012-bcf0-0bcd-a1185394c9b2",
      "status": status
    }
    Change_status = requests.put(url+"/status"+id, json =data, headers=headers)
    return Change_status

def POST_inventory_S(inventaire:list):
    data={
  "canteen_id": "9fe7fb0e-5012-bcf0-0bcd-a1185394c9b2",
  "inventory": inventaire,
  "updated_from": ID
}
    Post_status=requests.post(url+"/inventory",json=data, headers=headers)
    return Post_status

def POST_inventory_C(inventaire:list):
    data={
  "canteen_id": "9fe7fb0e-5012-bcf0-0bcd-a1185394c9b2",
  "inventory": inventaire,
  "updated_from": "CLIENT"
}
    Post_status=requests.post(url+"/inventory",json=data, headers=headers)
    return Post_status