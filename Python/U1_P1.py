#Model's variable creation and display.
Model={
    "Model_name":"My_model",
    "Temprature":0.5,
    "Max_tokens":100000,
    "API_version":1.2
}

print("\n","Model Configraton".center(30,"-"))
for m in Model.items():
    print(f"{m[0]} : {m[1]}")


#Student dict creation, update marks using user input and display.
Student={
    "Name":"Divyesh Chauhan",
    "Course":"Python",
    "Semester":1,
    "Marks":50
}

def display():
    print("\n","Student Details".center(30,"-"))
    for s in Student.items():
        print(f"{s[0]} : {s[1]}")

display()

while True:
    try:
        ch=input("\nDo you want to update the marks (y/n): ")
        match ch.lower().strip():
            case 'y':
                newM=int(input("Enter new marks: "))
                Student["Marks"]=newM
                display()
                breakpoint
            case 'n':
                break
            case default:
                print("Invalid response! Try again.")
                breakpoint
    except:
        print("Something went wrong. Try again.")


#Text file check and display it's size if found.
import os

print("\n","File Check:".center(40,"-"))
while True:
    try:
        fileName=input("\nEnter file path to see file size (Only for '.txt' file)[Write 'exit' to exit loop]: ")
        if os.path.isdir(fileName):
            print("Not a file! It is a directory. Insert a valid text file path.")
        elif fileName.strip().lower()=="exit":
            break
        else:
            if os.path.exists(fileName):    
                if fileName.rsplit(".",2)[-1]=="txt":
                    print(f"\nFile name: {fileName}\nFile size: {os.path.getsize(fileName)}bytes.")
                    if os.path.getsize(fileName)>0:
                        print(f"{fileName} is not empty.")
                    else:
                        print(f"{fileName} is empty.")

                    break
                
                else:
                    print("Invalid file type! Only '.txt' is allowed. Try again.")

            elif "." not in fileName:
                print("Extension Not Found: Please include the extension(file type) of the file in the file name and try again.")   

            else:
                print("File not Found. Enter correct path.")
    except Exception as e:
        print("Error:",e)
