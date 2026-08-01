import re

try:
    para = input("Write your paragraph below:\n")

    words = re.split(r"\W+",para.strip())
    words.remove("")

    print(words)
    print("Total number of words in paragraph: ", len(words))

    print("Total number of unique words: ",len([u for u in words if words.count(u)==1]))

    length=[]
    for u in words:
        length.append(len(u))

    longest=words[length.index(max(length))]
    print("Longest Word: ",longest)

    shortest=words[length.index(min(length))]
    print("Shortest Word: ",shortest)

    print("Words appearing more than once: ",{u for u in words if words.count(u)>1})

    print("Words in aplphabetical order: ",sorted(words, key=str.upper))

    w=input("Search a word: ")
    pos=[index for index, word in enumerate(words) if word==w]
    if pos==[]:
        print("Word not found.")
    else:
        print(f"Positions of {w}: {pos}")
except Exception as e:
    print("Error:",e)