import os


while True:
    try:
        fileName=input("Enter file path to see file size (Only for '.txt' file)[Write 'exit' to exit loop]: ")
        if os.path.isdir(fileName):
            print("Not a file! It is a directory. Insert a valid file path.")
        elif fileName.strip().lower()=="exit":
            break
        else:
            if os.path.isfile(fileName):
                if fileName.rsplit(".",2)[1]=="txt":
                    print(f"File name: {fileName}\nFile size: {os.path.getsize(fileName)}bytes.")
                    break
                else:
                    print("Invalid file type! Only '.txt' is allowed. Try again.")
            elif fileName.rsplit(".",2)[1]=="":
                print("Invalid file type! Only '.txt' is allowed. Try again.")
            else:
                print("File not Found. Enter correct path.")
    except Exception as e:
        print("Error:",e)
