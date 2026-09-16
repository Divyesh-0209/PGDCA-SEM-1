from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
import os, time, json

load_dotenv()

def main():
    try:
        CLIENT=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    except Exception:
        print("Connection with the API failed.")

    RECORD_FILE="records.json"
    MODEL="gemini-3.5-flash-lite"
    INPUT_COST=round(0.30/1000000,7)
    OUTPUT_COST=round(2.50/1000000,7)

    REPORT={
        "total_prompts_processed":0,
        "successful_req":0,
        "failed_req":0,
        "total_tokens_used":0,
        "total_api_cost":0
    }

    prompt_count=0
    blocked_prompt_count=0
    blocked_res_count=0
    res_times=[]
    avg_response_time=0
    total_estimated_api_cost=0
    hist=[]

    class SafetyFormat(BaseModel):
        response: bool
        reason: str

    try:
        while True:
            prompt = input("\nEnter prompt (write 'exit' to end the loop): ").strip()
            try:
                if prompt.lower()!="exit":
                    if len(prompt) > 0:
                        prompt_count+=1

                        prompt_safe_check=CLIENT.interactions.create(
                            model=MODEL,
                            system_instruction="You are a prompt moderator. You have to analyse whether it contains restricted or sensitive words/phrases or it may produce unsafe or inappropriate responses. And then give the response strictly in specified json format. 'Response'= True/False (True if the prompt is safe else False.) 'Reason' = Give the reason strictly in 3 to 4 words not more then that.",
                            input=prompt,
                            response_format={
                                "type": "text",
                                "mime_type":"application/json",
                                "schema":SafetyFormat.model_json_schema(),
                            }
                        )

                        if prompt_safe_check:
                            prompt_safety = json.loads(prompt_safe_check.output_text)
                            
                            if prompt_safety['response'] == True:
                                print("\nPrompt Status: SAFE")

                                hist.append({"type":"user_input", "content":[{"type":"text", "text":prompt}]})
                                strt=time.time()
                                
                                interaction=CLIENT.interactions.create(
                                    model=MODEL,
                                    input=hist
                                )
                                
                                if interaction:
                                    res_times.append(time.time()-strt)
                                    avg_response_time = sum(res_times)/len(res_times)

                                    res_safe_check=CLIENT.interactions.create(
                                        model=MODEL,
                                        system_instruction="You are a response moderator. You have to analyse whether it contains Personal information, Harmful instructions, Offensive language or Unsafe recommendations. And then give the response strictly in specified json format. 'Response'= True/False (True if the prompt is safe else False.) 'Reason' = Give the reason strictly in 3 to 4 words not more then that.",
                                        input=str(interaction.output_text),
                                        response_format={
                                            "type": "text",
                                            "mime_type":"application/json",
                                            "schema":SafetyFormat.model_json_schema(),
                                        }
                                    )
                                    if res_safe_check:
                                        res_safety=json.loads(res_safe_check.output_text)

                                        if res_safety['response'] == True:
                                            print("\nResponse Status: SAFE")
                                            print("\nAI:",interaction.output_text)

                                            hist.append({"type":"model_output", "content":[{"type":"text", "text":interaction.output_text}]})

                                            usage=dict(interaction.usage)

                                            total_estimated_api_cost+=(usage["total_input_tokens"]*INPUT_COST)+((usage["total_output_tokens"]+usage["total_thought_tokens"])*OUTPUT_COST)
                                        else:
                                            blocked_res_count+=1
                                            print("\nResponse Status: UNSAFE")
                                            print("Reason:",res_safety['reason'])
                                            hist.pop()
                                            raise Exception("Response blocked! Generated response failed the safety check.")

                                    else:
                                        raise Exception("Response safety check mechanism failed.")

                                else:
                                    raise Exception("Response Generation Failed. Try again.")

                            else:
                                blocked_prompt_count+=1
                                print("\nPrompt Status: UNSAFE")
                                print("Reason:",prompt_safety['reason'])
                                raise Exception("Prompt Blocked! It failed the safety check. Try any other prompt.")

                        else:
                            raise Exception("Prompt safety check mechanism failed.")

                    else:
                        raise Exception("No prompt entered. Enter a prompt.")
                else:
                    break
            except Exception as e:
                print("\nERROR:",e)

        print("\n\n","REPORT".center(40, "-"))
        print("Number of prompts submitted:",prompt_count)
        print("Average response time:",avg_response_time)
        print("Total estimated cost:",total_estimated_api_cost)
        print("Number of blocked prompts:",blocked_prompt_count)
        print("Number of warnings generated:",blocked_prompt_count)

        record={
            "history":hist,
            "report":{
                "total_prompt_submitted": prompt_count,
                "avg_response_time": avg_response_time,
                "total_estimated_api_cost": total_estimated_api_cost,
                "total_blocked_prompt": blocked_prompt_count,
                "total_blocked_response": blocked_res_count,
            }
        }
        with open(RECORD_FILE, "w", encoding="utf-8") as file:
            json.dump(record, file, indent=4)

    except Exception as e:
        print("ERROR:",e)

if __name__=="__main__":
    main()