import json, re, pandas as pd

print("\n","Student Register:".center(70,"-"))

while True:
    try:
        n=int(input("\nHow many students' details you want to enter (enter 0 to exit): "))

        with open("P2_data.json", "r", encoding="utf-8") as file:
            data=json.load(file)

        for i in range(1,n+1):
            if i==1:
                j="1st"
            elif i==2:
                j="2nd"
            elif i==3:
                j="3rd"
            else:
                j=str(i)+"th"
            
            print(f"\nEnter details of {j} student:-".center(50," "))

            sname=input("Enter student name: ").strip().title()
            scourse=input("Enter student course: ").strip().title()
            sage=int(input("Enter student age: ").strip())

            if not(re.match(r"[a-zA-Z ]",sname) and re.match(r"[a-zA-Z ]",scourse)):
                raise Exception("Student name and course should only contain letters and space. No other symbols.")
            else:
                stud={"sname":sname, "sage":sage, "scourse":scourse}
                data.append(stud)

        with open("P2_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        with open("P2_data.json", "r", encoding="utf-8") as file:
            load_data=json.load(file)

        print("\n","Student Details:".center(40,"-"))

        for students in load_data:
            print()
            for student in students.items(): 
                print(f"{student[0]} : {student[1]}")

        break

    except ValueError:
        print("Invalid Input! Enter only number (eg. 4). Try again.")

    except Exception as e:
        print(type(e), e)


#Pandas Part of the problem

df=pd.read_json("P2_data.json")
df=df.set_axis(range(1,df.shape[0]+1), axis="index")
print("Records of first two students:\n",df.head(2))
print("Records of last two students:\n",df.tail(2))
print("Shape of the data frame: ",df.shape)
print("Name of all the columns: ",df.columns)
print("Data types of all the columns:\n"+str(df.dtypes))
