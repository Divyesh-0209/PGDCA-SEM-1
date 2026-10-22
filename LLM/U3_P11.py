import subprocess
try:
    import ollama
except ImportError:
    print("\t--- Installing Ollama SDK for python environment---")
    install_ollama = subprocess.run(["pip install ollama"], capture_output=True, text=True)
    print(install_ollama.stdout.strip())

    print("\t--- Installing ollama SDK for python environment---")
    install_model = subprocess.run(["ollama pull qwen3.5:0.8b"], capture_output=True, text=True)
    print(install_model.stdout.strip())

    import ollama

while True:
    try:
        prompt = input("Enter the your subject/question (type exit to stop): ").strip()

        if prompt and prompt !="":
            if prompt.lower() != "exit":
                response = ollama.chat(
                    model = "qwen3.5:0.8b",
                    messages = [{
                        "role": "system",
                        "content": "You are an AI Assistant for students. You are a part of Subject based question - answer system. You generated answer should be related to the subject and question which is asked by the user. I don't give long answers, keep things simple and concise. Only answer in the when told explicit. Strictly, don't talk about irrelevant topics."
                        },{
                        "role": "user",
                        "content": prompt
                    }]
                )

                print(response['message']['content'])
            else:
                break
        else:
            raise Exception("Invalid prompt.. Try again.")

    except Exception as e:
        print("[ERROR] :",e)