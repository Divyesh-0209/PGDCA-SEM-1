from dotenv import load_dotenv
from google import genai
import os, json, asyncio

load_dotenv()

CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
FILE= "P6history.json"
CONTEXT_LIMIT= 2000
MODEL="gemini-3.5-flash-lite"

if not (os.path.exists(FILE) and os.path.isfile(FILE)):
    hst=[{"system_instruction":str()},list(),{"input_tokens":int(), "output_tokens":int()}]
    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(hst, file, indent=4)

async def api_call(hist,outType):
    inter=CLIENT.interactions.create(
        model=MODEL,
        system_instruction=hist[0]["system_instruction"],
        input=hist[1],
        # store=False,
        stream=True if outType=="y" else False 
    )
    if outType=="n":
        return inter
    else:
        for event in inter:
            if event.event_type=="step.delta" and event.delta.type=="text":
                yield f"data: {event.delta.text}\n\n"

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

            out_type=input("Do you to stream the ai response (y/n): ").strip().lower()

            interaction= CLIENT.interactions.create(
                system_instruction=history[0]["system_instruction"],
                model="gemini-3.5-flash-lite",
                input=history[1],
                # store=False,
                stream=True if out_type=="y" else False 
            )

            total_tokens=0
            ai_resp=""
            context_size=history[2]["input_tokens"]+history[2]["output_tokens"]

            if out_type=="y":
                print("\nAI response streaming:",end="")
                for event in interaction:
                    if event.event_type=="step.delta":
                        if event.delta.type=="text":
                            print(event.delta.text,end="")
                            ai_resp+=event.delta.text
                    elif event.event_type=="interaction.completed":
                        history[2]["input_tokens"]=event.interaction.usage.total_input_tokens
                        history[2]["output_tokens"]=event.interaction.usage.total_output_tokens
                        total_tokens=event.interaction.usage.total_tokens
                    elif event.event_type=="error":
                        raise(event.error.message)
            else:
                ai_resp=interaction.output_text
                print("\nAI Response:",ai_resp)
                history[2]["input_tokens"]=dict(interaction.usage)["total_input_tokens"]
                history[2]["output_tokens"]=dict(interaction.usage)["total_output_tokens"]
                total_tokens=dict(interaction.usage)["total_tokens"]

            print("\n\nCurrent API call context/input size:",context_size)
            print("\nTotal tokens used in current API call:",total_tokens)
            if(total_tokens>1500) and (total_tokens<2000):
                print("\nALERT! You are about to hit your context limit(2000 total tokens).".center(120," "))
            elif total_tokens>=2000:
                print("\nCONTEXT LIMIT HIT!".center(120," "))
            else:
                pass

            history[1].append({"type":"model_output","content": [{"type":"text", "text":ai_resp}]})

            with open(FILE, "w", encoding="utf-8") as file:
                json.dump(history, file, indent=4)

            print("Total messages exchanged:",len(history[1])//2)
            

        else:
            print("Bye!")
            break

    except Exception as e:
        print("\n\nError: ",e)

