#List of all functions used
def getArr(fileName):
    arr = [[], [], [], []]
    current = -1
    master = open(fileName, "r")
    for x in master:
        if x[0] == "!":
            current += 1
            arr[current].append(x[1:-1])
        else:
            arr[current].append(x[:-1])
    return arr


def crnToSub(crn, arr):
    for i, x in enumerate(arr[2]):
        if x == crn:
            return [arr[0][i], arr[1][i], arr[3][i]]

# arr -> [sub| num| crn| avail]
#        [ 0 |  1 |  2 |   3  ]


def readRequests():
    back = []
    for x in readFile("requests.txt"):
        back.append(x[:-1])
    return back


def readRequestsArr():
    back = []
    for x in readFile("requests.txt"):
        fix = x[:-1].split(",")
        back.append(fix)
    return back


def appendRequests(crn, arr, channel):
    add = crnToSub(crn, arr)
    add.append(str(channel))
    appendFile("requests.txt", add[0] + "," + add[1] + "," + crn + "," + add[2] + "," + str(channel) + "\n")


def removeRequests(crn):
    keep = readFile("requests.txt")
    writeFile("requests.txt", "")
    for x in keep:
        oldCrn = x.split(",")[2]
        if oldCrn != crn:
            appendFile("requests.txt", x)


def readFile(file):
    master = open(file, "r")
    retrieve = []
    for x in master:
        retrieve.append(x)
    return retrieve


def appendFile(file, text):
    master = open(file, "a")
    master.write(text)


def writeFile(file, text):
    master = open(file, "w")
    master.write(text)


def getClassList(sub, num, arr):
    # gives ids to use in arr[choose][i]
    classAvail = []
    for i, x in enumerate(arr[0]):
        if x == sub and arr[1][i] == num:
            if int(arr[3][i]) > 0:
                classAvail.append(i)
    return classAvail


def checkClassExists(sub, num, arr):
    classAvail = []
    for i, x in enumerate(arr[0]):
        if x == sub and arr[1][i] == num:
            classAvail.append(i)
    if len(classAvail) > 0:
        return True
    else:
        return False


def indexTOcrn(array, arr):
    newarr = []
    for x in array:
        newarr.append(arr[2][x])
    return newarr
