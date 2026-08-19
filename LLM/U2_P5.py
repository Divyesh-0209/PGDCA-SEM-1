from dotenv import load_dotenv
from google import genai
import os, json

load_dotenv()

CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
FILE= "history.json"
CONTEXT_LIMIT= 2000

if not (os.path.exists(FILE) and os.path.isfile(FILE)):
    hst=[{"system_instruction":str()},list(),{"input_tokens":int(), "output_tokens":int()}]
    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(hst, file, indent=4)
    

while True:
    try:
        with open(FILE, "r", encoding="utf-8") as file:
            history=json.load(file)

        ch=input("\nWant to Chat with AI (y/n): ").lower().strip()
        if ch=='y':
            sys=input("Do you want to set any system prompt for current API call(y/n): ").lower().strip()
            if sys=='y':
                system=input("Enter the system prompt for current API call: ")
            else:
                system=""
            prompt=input("Enter the prompt: ")

            if system != "":
                history[0]["system_instruction"]=system
            history[1].append({"type":"user_input","content": [{"type":"text", "text":prompt}]})

            interaction=CLIENT.interactions.create(
                system_instruction=history[0]["system_instruction"],
                model="gemini-2.5-flash",
                input=history[1],
                store=False
            )

            print("AI response:",str(interaction.output_text).replace("\n",""))

            history[1].append({"type":"model_output","content": [{"type":"text", "text":str(interaction.output_text).replace("\n","")}]})
            usage=dict(interaction.usage)

            context_size=history[2]["input_tokens"]+history[2]["output_tokens"]

            print("Current API call context/input size:",context_size)
            
            history[2]["input_tokens"]=usage["total_input_tokens"]
            history[2]["output_tokens"]=usage["total_output_tokens"]

            print("Total tokens used in current API call:",usage["total_tokens"])

            if(usage["total_tokens"]>1500) and (usage["total_tokens"]<2000):
                print("ALERT! You are about to hit your context limit(2000 total tokens).".center(120," "))
            elif usage["total_tokens"]>=2000:
                print("CONTEXT LIMIT HIT!".center(120," "))
            else:
                pass

            with open(FILE, "w", encoding="utf-8") as file:
                json.dump(history, file, indent=4)

            print("Total messages exchanged:",len(history[1])//2)
            

        else:
            print("Bye!")
            break

    except Exception as e:
        print("Error: ",e)

