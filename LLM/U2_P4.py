from google import genai
import json, time, os

API=input("Enter Gemini API key: ")
model=input("Enter AI model id: ")
prompt=input("Enter prompt: ")
tem=input("Enter API temperature: ")
topP=input("Enter API top-p: ")
maxT=input("Enter API call max output tokens: ")

client=genai.Client(api_key=API)
start=time.time()
interaction=client.interactions.create(
    model= model,
    input= prompt,
    generation_config={
        "temperature":tem,
        "top_p": topP,
        "max_output_tokens": maxT,
        "stop_sequences":["It"]
    }
)

print("AI Response: ",str(interaction.output_text).replace("\n",""))
end=time.time()
print("Model: ",interaction.model)
print(f"Response time: {(end-start):2f}seconds")
print("Total tokens used: ",dict(interaction.usage)['total_tokens'])

if not (os.path.exists("P4Data.json") and os.path.isfile("P4Data.json")):
    with open("P4Data.json","w",encoding="utf-8") as file:
        json.dump([], file, indent=4)

with open("P4Data.json","r",encoding="utf-8") as file:
    data=json.load(file)

data.append({
    "userInteraction":{
        "prompt":prompt,
        "parameter":{
            "model":model,
            "temperature":tem,
            "top_P":topP,
            "max_tokens":maxT
        },
        "output":str(interaction.output_text).replace("\n","")
    }
})

with open("P4Data.json","w",encoding="utf-8") as file:
    json.dump(data, file, indent=4)