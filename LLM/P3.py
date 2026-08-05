from google import genai
from dotenv import load_dotenv
import os, time

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

user=input("Enter your prompt: ")
start=time.time()
interaction = client.interactions.create(
    model='gemini-2.5-flash',
    input=user,
)

output=interaction.output_text.replace("\n","")
end=time.time()
print("\nAI Response:",output)

print("\nLength of AI Response (characters):",len(output))

words=output.split(" ")
print("\nLength of AI Response (words):",len(words))

if len(words)<=50:
    print("\nAI Response is 'short'.")
elif len(words) in range(51,151):
    print("\nAI Response is 'medium'.")
else:
    print("\nAI Response is 'long'.")


print("\nModel name:",interaction.model)

print(f"\nResponse Time: {float(end-start):.2f} seconds.")