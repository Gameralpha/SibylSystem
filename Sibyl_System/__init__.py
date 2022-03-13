from telethon import TelegramClient, events
import asyncio
import aiohttp
from telethon.sessions import StringSession
import os
import pymongo
import re 


ENV = bool(os.environ.get('ENV', False))
if ENV:
   API_ID_KEY = int(os.environ.get("API_ID_KEY","18534796"))
   API_HASH_KEY = os.environ.get("API_HASH_KEY", "ce2e8a48f54b287ea9eb8616f4f58163")
   STRING_SESSION = os.environ.get('STRING_SESSION',"BQCegaDPocLSyIHOkxyaIuXcdgaPtaSV5X6MlFH8aOZHc8awe2zQP5IcoSbCmkL6ZvYXarUjlW4AkAM7q4L67_bSsoEBb3NiWE8wexO-qoT8HLHauNaAysxBmD7FwBtC3gGe3yANCgibKivK-CC8FSpXWDp1ERdsNr6fErxXYDxfmcFWQ6QWfsZ6zcd1vkk_Mu6a8Yb7p_WcES7FWTeiMbutigNa2hGXbTAEWdgInqzbqYEsaL1yZWRYYJk8EFBzDE91-yR8iE_QjAko0cXdnd1S688DkDhrhBUrlU0y9tyS2Cl-DeE9I997ZNrFsrB32v2qzPatcZJV6aL_bWbUD3UQAAAAAS1YjCAA")
   SIBYL = list(int(x) for x in os.environ.get("SIBYL", "1930954213").split())
   ENFORCERS = list(int(x) for x in os.environ.get("ENFORCERS", "1930954213").split())
   MONGO_DB_URL = os.environ.get("MONGO_DB_URL","mongodb+srv://shikhar:shikhar@cluster0.6xzlh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority") 
   Sibyl_logs = int(os.environ.get("Sibyl_logs","-1001615945740" ))
   Sibyl_approved_logs = int(os.environ.get("Sibyl_Approved_Logs", "-1001615945740"))
   GBAN_MSG_LOGS = int(os.environ.get("GBAN_MSG_LOGS","-1001615945740")) 


ENFORCERS.extend(SIBYL)
session = aiohttp.ClientSession()
System = TelegramClient(StringSession(STRING_SESSION), API_ID_KEY, API_HASH_KEY)
MONGO_CLIENT = pymongo.MongoClient(MONGO_DB_URL)
collection = MONGO_CLIENT['Sibyl']['Main'] 
if collection.count_documents({ '_id': 1}, limit = 1) == 0:
   dict = {"_id": 1}
   dict["blacklisted"] = []
   collection.insert_one(dict) 

if collection.count_documents({ '_id': 2}, limit = 1) == 0:
   dict = {"_id": 2, "Type": "Wlc Blacklist"}
   dict["blacklisted_wlc"] = []
   collection.insert_one(dict)

def system_cmd(pattern=None, allow_sibyl=True, allow_enforcer = False, **args):
    if pattern:
        args["pattern"] = re.compile(r"[\?\.!/]" + pattern)
    if allow_sibyl and allow_enforcer:
        args["from_users"] = ENFORCERS
    else:
        args["from_users"] = SIBYL
    return events.NewMessage(**args)
