from dotenv import load_dotenv
from google import genai
import os, json, asyncio, time

load_dotenv()

CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
FILE= "P6history.json"
CONTEXT_LIMIT= 2000
MODEL="gemini-3.5-flash-lite"

#Async call function
async def stream_gemini_interaction(prompt):
    print(f"Sending prompt: '{prompt}'\n--- Streaming Response ---")
    
    response_stream = await CLIENT.aio.interactions.create(
        model=MODEL,
        input=prompt,
        stream=True
    )
    
    async for event in response_stream:
        if event.event_type=="step.delta":
            if event.delta.type=="text":
                print(event.delta.text)

#Main function.
async def main():

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

                out_type=input("Do you to stream the ai response (y/n): ").strip().lower()
                
                try:
                    strt=time.time()
                    interaction= CLIENT.interactions.create(
                        system_instruction=history[0]["system_instruction"],
                        model="gemini-3.5-flash-lite",
                        input=history[1],
                        # store=False,
                        stream=True if out_type=="y" else False 
                    )
                except Exception as e:
                    print("API Call Error:",e)

                total_tokens=0
                ai_resp=""
                context_size=history[2]["input_tokens"]+history[2]["output_tokens"]

                if out_type=="y":
                    print("\nAI response streaming:",end="",flush=True)
                    dif=0                        
                    cunt=0
                    for event in interaction:
                        if event.event_type=="step.delta":
                            if event.delta.type=="text":
                                cunt+=1
                                print(event.delta.text,end="",flush=True)
                                dif=time.time()-strt
                                ai_resp+=event.delta.text
                        elif event.event_type=="interaction.completed":
                            history[2]["input_tokens"]=event.interaction.usage.total_input_tokens
                            history[2]["output_tokens"]=event.interaction.usage.total_output_tokens
                            total_tokens=event.interaction.usage.total_tokens
                            print(f"\n\nResponse time for first token: {dif:.2f}")
                            print(f"\nTotal response time: {time.time()-strt:.2f}")
                            print("\nTotal number of streamed chunks received:",cunt)
                        elif event.event_type=="error":
                            raise(event.error.message)
                    
                else:
                    ai_resp=interaction.output_text
                    print("\nAI Response:",ai_resp)
                    print(f"\n\nResponse time: {time.time()-strt:.2f}")
                    history[2]["input_tokens"]=dict(interaction.usage)["total_input_tokens"]
                    history[2]["output_tokens"]=dict(interaction.usage)["total_output_tokens"]
                    total_tokens=dict(interaction.usage)["total_tokens"]

                print("\nCurrent API call context/input size:",context_size)
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

        except json.JSONDecodeError:
            print("\n\nALERT! History json was totally empty or contained invalid json. So it had been reset.")
            hst=[{"system_instruction":str()},list(),{"input_tokens":int(), "output_tokens":int()}]
            with open(FILE, "w", encoding="utf-8") as file:
                json.dump(hst, file, indent=4)
        
        except Exception as e:
            print("\n\nError: ",e)
            break

    #Asynchronous call code
    try:
        asyn_ch=input("\nWant this place asynchronous API call(y/n): ").strip().lower()
        if asyn_ch=='y':
            prompts = [
                "Say 'Hi1'",
                "Say 'Hi2'",
                "Say 'Hi3'"
            ]
            
            tasks = [stream_gemini_interaction(p) for p in prompts]
            await asyncio.gather(*tasks)
        else:
            print("Bye!")
    except Exception as e:
        print("Async Error:", e)

if __name__ == "__main__":
    asyncio.run(main())
