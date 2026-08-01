inpNumbers=input("Enter integers (ex: 1 2 3 2 23 21): ")
num=inpNumbers.split(" ")
print("Duplicate numbers")
for index, n in enumerate(num):
    count=0
    for i in num[index+1:]:
        if n==i:
            count+=1
    if count>0:
        print(int(n))


for i in range(6):
    n=input(f"Enter {i} number: ")
    num.append(n)

for n in num:
    count=num.count(n)
    if(count>1):
        print(n)