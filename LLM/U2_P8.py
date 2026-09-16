from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
import os, time, json, asyncio, pandas as pd

load_dotenv()

async def main():
    try:
        CLIENT=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    except Exception:
        print("Connection with the API failed.")

    PROMPT_FILE="prompts.csv"
    MODEL="gemini-3.5-flash-lite"
    REQ_PER_MIN=3
    INPUT_COST=round(0.30/1000000,7)
    OUTPUT_COST=round(2.50/1000000,7)

    REPORT={
        "total_prompts_processed":0,
        "successful_req":0,
        "failed_req":0,
        "total_tokens_used":0,
        "total_api_cost":0
    }

    req_count=0
    begin_time=time.time()
    i=0

    class SafetyFormat(BaseModel):
        response: bool
        reeason: str

    try:
        while True:
            prompt = input("Enter prompt: ").strip()
            if len(prompt) > 0:
                try:
                    interaction=CLIENT.interactions.create(
                        model=MODEL,
                        system_instruction="You are a prompt moderator. You have to analyse whether it contains restricted or sensitive words/phrases or it may produce unsafe or inappropriate responses. And then give the response strictly in specified json format. 'Response'= True/False (True if the prompt is safe else false.) 'Reason' = Give the reason strictly in 3 to 4 words not more then that.",
                        input=prompt,
                        resoinse_format=types.ResponseFormat(
                            mime_type="application/json",
                            schema=SafetyFormat
                        )
                    )
                except Exception as e:
                    print("ERROR:",e)
                
                if time.time()<(begin_time+60):
                    if req_count<REQ_PER_MIN:
                        strt=time.time()
                        print(f"\n\nProcessing prompt {i+1} from the file...")
                        try:
                            REPORT["total_prompts_processed"]+=1
                            interaction=CLIENT.interactions.create(
                                model=MODEL,
                                input=df["prompts"][i]
                                config=types.GenerateContentConfig(
                                    safety_settings={
                                        "category": enum (HarmCategory),
                                        "threshold": enum (HarmBlockThreshold)
                                    }
                                )
                            )
                            req_count+=1
                            if interaction:
                                i+=1
                                REPORT["successful_req"]+=1
                                print("\nAI Response:",interaction.output_text)
                                REPORT["responses"].append(str(interaction.output_text))
                                print(f"Response time for prompt {i}: {time.time()-strt:.2f}")
                                usage=dict(interaction.usage)
                                REPORT["total_tokens_used"]+=usage["total_tokens"]
                                print("Estimated token usage:",usage["total_tokens"])
                                api_cost=(usage["total_input_tokens"]*INPUT_COST)+((usage["total_output_tokens"]+usage["total_thought_tokens"])*OUTPUT_COST)
                                REPORT["total_api_cost"]+=round(api_cost,7)
                                print(f"Extimated cost (input + [output + thought tokens]): ${api_cost:.7f}")
                            else:
                                raise Exception("No response OR API call error.")

                        except Exception as e:
                            print(f"\nError in API call for prompt{i}:",e)
                            REPORT["failed_req"]+=1
                            ch=input("Do you want to retry with the same prompt(y/n): ").strip().lower()
                            if ch=='y':
                                pass
                            else:
                                i+=1
                            continue

                    else:
                        print(f"\nALERT: You reached the maximum number of requests per minute. Process will continue from the pending requests after {int(60-(time.time()-begin_time))} seconds.")
                        await asyncio.sleep(int(60-(time.time()-begin_time)))
                        begin_time=time.time()
                        req_count=0
                else:
                    print("\n\nRequests per minute time renewed..\n")
                    begin_time=time.time()
                    req_count=0
            else:
                raise Exception("No prompt entered. Enter a prompt.")

    except Exception as e:
        print("ERROR:",e)
    print("\n\n")
    print("API call reports:".center(100,"-"))
    print(REPORT)
    with open("P7report.json", "w", encoding="utf-8") as file:
        json.dump(REPORT, file, indent=4)
    

if __name__=="__main__":
    asyncio.run(main())
