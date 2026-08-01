Model={
    "Model_name":"My_model",
    "Temprature":0.5,
    "Max_tokens":100000,
    "API_version":1.2
}

print("Model Configraton".center(30,"-"))
for m in Model.items():
    print(f"{m[0]} : {m[1]}")
