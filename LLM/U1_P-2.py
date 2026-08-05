Data={"GPT_4":{
    "Developer":"OpenAI",
    "Open_Source/Proprietary":"Proprietary",
    "Multimodal_Support":"Yes",
    "Use_Case":"Coding assistance, complex reasoning, content generation, data analysis"
},"Claude_3":{
    "Developer":"Anthropic",
    "Open_Source/Proprietary":"Proprietary",
    "Multimodal_Support":"Yes",
    "Use_Case":"Long-document analysis, customer support automation, research synthesis, coding"
},"Gemini":{
    "Developer":"Google",
    "Open_Source/Proprietary":"Proprietary",
    "Multimodal_Support":"Yes",
    "Use_Case":"Live audio/video processing, cross-app task automation, educational tutoring, creative writing"
},"Llama_3":{
    "Developer":"Meta",
    "Open_Source/Proprietary":"Open Source",
    "Multimodal_Support":"Yes",
    "Use_Case":"On-premise deployment, chatbot development, personal productivity assistants, text summarisation"
},"Mistral":{
    "Developer":"Mistral AI",
    "Open_Source/Proprietary":"Open Source",
    "Multimodal_Support":"Yes",
    "Use_Case":"Low-latency edge computing, multilingual translation, structured data extraction, code generation"
}}

bool=True

while bool:
    try: 
        print("\n")
        print("Information are available in to following domain.".center(120," "))
        print("1. GPT-4\t2. Claude 3\t3. Gemini\t4. Llama 3\t5. Mistral\t6. Exit".center(110," "))
        ch=int(input("\nEnter which domain information you want: "))
        match(ch):
            case 1:
                for d in Data["GPT_4"].items():
                    print(f"{d[0]} : {d[1]}")
                breakpoint
            case 2:
                for d in Data["Claude_3"].items():
                    print(f"{d[0]} : {d[1]}")
                breakpoint
            case 3:
                for d in Data["Gemini"].items():
                    print(f"{d[0]} : {d[1]}")
                breakpoint
            case 4:
                for d in Data["Llama_3"].items():
                    print(f"{d[0]} : {d[1]}")
                breakpoint
            case 5:
                for d in Data["Mistral"].items():
                    print(f"{d[0]} : {d[1]}")
                breakpoint
            case 6:
                bool = False
                breakpoint
            case default:
                print("Invalid Input! Try again")
    except:
        print("Invalid Input! Try again")
