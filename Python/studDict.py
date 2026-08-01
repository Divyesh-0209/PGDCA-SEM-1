Student={
    "Name":"Divyesh Chauhan",
    "Course":"Python",
    "Semester":1,
    "Marks":50
}

def display():
    print("Student Details".center(30,"-"))
    for s in Student.items():
        print(f"{s[0]} : {s[1]}")

display()

while True:
    try:
        ch=input("Do you want to update the marks (y/n): ")
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
    except:
        print("Something went wrong. Try again.")