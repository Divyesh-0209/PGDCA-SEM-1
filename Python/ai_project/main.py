from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
try:
    APIKEY=os.getenv('API_KEY')
    APIURL=os.getenv('API_URL')
    if APIKEY:
        if APIURL:
            print("Your API URL is:",APIURL)
        else:
            raise Exception("API URL NOT SET! Please set your API URL.")
        key=""
        for i,s in enumerate(APIKEY):
            if i<(len(APIKEY)-4):
                key+="*"
            else:
                key+=s
        print("Your API key is:",key)
    else:
        raise Exception("API KEY NOT SET! Please set your API key.")

except Exception as e:
    print(e)

try:
    if os.path.exists("requirements.txt") and os.path.isfile("requirements.txt"):
        dot_env=[]
        panda=[]
        req=[]
        with open("requirements.txt", "r", encoding="utf-16") as file:
            for line in file:
                if "dotenv" in line:
                    dot_env.append(line.strip())
                if "pandas" in line:
                    panda.append(line.strip())
                if "requests" in line:
                    req.append(line.strip())
        print("\nLibraries:")
        if dot_env:
            for i in dot_env:
                print(i)
        else:
            print("Dotenv library not found.")
        if panda:
            for i in panda:
                print(i)
        else:
            print("Pandas library not found.")
        if req:
            for i in req:
                print(i)
        else:
            print("Requests library not found.")
    else:
        raise("FILE NOT FOUND ERROR! No requirements.txt file.")

except Exception as e:
    print(e)