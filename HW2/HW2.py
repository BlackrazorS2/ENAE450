# ENAE 450 HW 2 - William Bauer 117987676
from random import randint

def listSort(list):
    """Takes in a list of integers and sorts it using a merge sort method"""
    if len(list) <= 1:
        return list
    # divide the list into n sublists where n is the length of the list
    # i.e. compare sublist 1 with sublist 2, 3 with 4, etc
    leftSplit = list[:(len(list)//2)]
    rightSplit = list[((len(list)//2)):]
    leftSplit = listSort(leftSplit)
    rightSplit = listSort(rightSplit)
    return merge(leftSplit, rightSplit)

def merge(leftSplit, rightSplit):
    # merge and sort the lists
    sortedList = []
    while len(leftSplit) > 0 and len(rightSplit) > 0:
        if leftSplit[0] >= rightSplit[0]:
            sortedList.append(rightSplit[0])
            rightSplit = rightSplit[1:]
        else: # this means that left is less than right
            sortedList.append(leftSplit[0])
            leftSplit = leftSplit[1:]
    if len(leftSplit) == 0:
        # Rightsplit still has elements
        sortedList = sortedList + rightSplit
    if len(rightSplit) == 0:
        # leftSplit still has elements
        sortedList = sortedList + leftSplit
    return sortedList

def listGen(length, min, max):
    """generates a list of random integers of a specified length between the min and max values\nmin is inclusive and max is exclusive"""
    bigList = []
    for i in range(0,length):
        num = randint(min, max)
        bigList.append(num)
    return bigList

def q1():
    # Generate two unsorted lists of 50 non-negative integers from 0 to 1000
    L1 = listGen(10, 0, 1001)
    print(f"List 1: {L1}\n")
    L2 = listGen(10, 0, 1001)
    print(f"List 2: {L2}\n")
    L3 = L1+L2
    print(f"Combined List: {L3}\n")
    L3Sort = listSort(L3)
    print(f"Sorted List: {L3Sort}")

def binSearch(targetArray, searchValue):
    found = False
    while len(targetArray) >= 1:
        print(targetArray)
        if searchValue == targetArray[len(targetArray)//2]:
            found = True
            break
        elif searchValue > targetArray[len(targetArray)//2]:
            # searchValue is greater than middle of list, we want to check the right side
            targetArray = targetArray[(len(targetArray)//2):]
        elif searchValue < targetArray[len(targetArray)//2]:
            # searchValue is less than middle of list, we want to check the left side
            targetArray = targetArray[:(len(targetArray)//2)]
            if len(targetArray) == 1:
                break
    return found
def q2():
    # doing binary search
    L1 = listGen(101, 0, 1000)
    sortList = listSort(L1)
    target = input("Please enter an integer value from 0 to 1000 to search for: ")
    target = target.strip()
    try:
        target = int(target)
        if target < 0 or target > 1000:
            raise ValueError
    except ValueError:
        print("Error: Please enter an integer between 0 and 1000\n\n")
        q2()
        return None
    presence = binSearch(sortList, target)
    print(f"Original List: {L1}\n")
    print(f"Sorted List: {sortList}\n")
    print(f"Search Value: {target}\n")
    print(f"Found?: {presence}")

def slicer(inStr):
    """Slices into sentences and returns a list of each sentence"""
    delimiters = ["...", "." ,"?", "!"]
    # Could just use split
    # so basically I have a list that goes starts at a list of a string
    # then turns into a list of lists of strings
    # then turns into a list of lists of lists of strings
    workArray = []
    strStart = 0
    for idx, char in enumerate(inStr):
        try:
            if char in delimiters and inStr[idx+1] != ".":
                workArray.append(inStr[strStart:idx+1].strip())
                strStart = idx+1
        except:
            if char in delimiters:
                workArray.append(inStr[strStart:].strip())
                strStart = idx+1
    sliced = workArray
    return sliced

def q3():
    INPUT_STRING = "This is a program made by William Bauer. He has a student ID of 117987676. What kind of things does William like? Well, if he had to say it himself, he would say that he enjoys playing video games and making models in Solidworks. Oh, if that's the case, I wonder what classes William is taking! William is currently enrolled in ENME 332, ENME 371, ENME 410, ENME 351, HACS 297, and ENAE 450. I wonder what William will do next..."
    sliced = slicer(INPUT_STRING)
    print(f"The original string is:\n{INPUT_STRING}")
    print("The list of sentences is:\n")
    for num, sentence in enumerate(sliced):
        print(f"[{num+1}] {sentence}")

def main():
    print("Question 1:")
    q1()
    print("\n\nQuestion 2:")
    q2()
    print("\n\nQuestion 3:")
    q3()
    print("\n\n")

if __name__ in "__main__":
    main()