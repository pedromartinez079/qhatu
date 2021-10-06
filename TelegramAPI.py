# importing libraries
import requests

def getUpdates(token):
    #Input parameters
    #Telegram Bot Token
    token=token
    
    url_base='https://api.telegram.org/bot'+token+'/getUpdates'
    
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {}
    myheaders = {}
    # sending get request and saving the response as response object
    myrequest = requests.get(url = url_base, headers = myheaders, params = PARAMS)
    #print myrequest.url
    # extracting data in json format
    data = myrequest.json()
    return data

def TelegramSendTxt(token, chat_id, text):
    #Input parameters
    chat_id=chat_id
    text=text
    #Telegram Bot Token
    token=token
    
    url_base='https://api.telegram.org/bot'+token+'/sendMessage'
    
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'chat_id':chat_id, 'text':text}
    myheaders = {}
    # sending get request and saving the response as response object
    try:
        myrequest = requests.post(url = url_base, headers = myheaders, params = PARAMS)
        data = myrequest.json()
        return data
    except requests.exceptions.RequestException as e:
        data=e
        return data
        
def TelegramSendPhoto(token, chat_id, filepath, caption):
    #Input parameters
    chat_id=chat_id
    filepath=filepath
    caption=caption
    #Telegram Bot Token
    token=token
    
    url_base='https://api.telegram.org/bot'+token+'/sendPhoto'
    
    # defining a params dict for the parameters to be sent to the API
    files = {'chat_id': (None, chat_id), 'photo': (filepath, open(filepath, 'rb')), 'caption': (None, caption)}
    myheaders = {}
    # sending get request and saving the response as response object
    try:
        myrequest = requests.post(url = url_base, headers = myheaders, files = files)
        data = myrequest.json()
        return data
    except requests.exceptions.RequestException as e:
        data=e
        return data

def TelegramSendDocument(token, chat_id, filepath, caption):
    #Input parameters
    chat_id=chat_id
    filepath=filepath
    caption=caption
    #Telegram Bot Token
    token=token
    
    url_base='https://api.telegram.org/bot'+token+'/sendDocument'
    
    # defining a params dict for the parameters to be sent to the API
    files = {'chat_id': (None, chat_id), 'document': (filepath, open(filepath, 'rb')), 'caption': (None, caption)}
    myheaders = {}
    # sending get request and saving the response as response object
    try:
        myrequest = requests.post(url = url_base, headers = myheaders, files = files)
        data = myrequest.json()
        return data
    except requests.exceptions.RequestException as e:
        data=e
        return data

