Data={"GPT_4":{
    "Developer":"OpenAI",
    "Open_Source/Proprietary":"Proprietary",
    "Multimodal_Support":"Yes",
    "Use_Case":"Coding assistance, complex reasoning, content generation, data analysis"
},"CLAUDE_3":{
    "Developer":"Anthropic",
    "Open_Source/Proprietary":"Proprietary",
    "Multimodal_Support":"Yes",
    "Use_Case":"Long-document analysis, customer support automation, research synthesis, coding"
},"GEMINI":{
    "Developer":"Google",
    "Open_Source/Proprietary":"Proprietary",
    "Multimodal_Support":"Yes",
    "Use_Case":"Live audio/video processing, cross-app task automation, educational tutoring, creative writing"
},"LLAMA_3":{
    "Developer":"Meta",
    "Open_Source/Proprietary":"Open Source",
    "Multimodal_Support":"Yes",
    "Use_Case":"On-premise deployment, chatbot development, personal productivity assistants, text summarisation"
},"MISTRAL":{
    "Developer":"Mistral AI",
    "Open_Source/Proprietary":"Open Source",
    "Multimodal_Support":"Yes",
    "Use_Case":"Low-latency edge computing, multilingual translation, structured data extraction, code generation"
}}

bool=True

while bool:
    try: 
        ch=input("\nEnter which modal information you want (Enter 'Bye' to exit): ")

        found=False

        if len(ch.strip())>2:
            for model in Data.keys():
                if model.count(ch.upper())>0:
                        found=True
                        for d in Data[model].items():
                            print(f"{d[0]} : {d[1]}")
                elif ch.upper().strip()=="BYE":
                    bool=False
        elif found==False:
            print("Model not found! Try again.")
        else:
             print("The name of the model should have atleast 3 characters. Try again.")
    except:
        print("Something went wrong! Try again.")
