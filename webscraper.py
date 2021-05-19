import time
from datetime import datetime
from selenium import webdriver
from pyvirtualdisplay import Display
from func import *
time.sleep(20)
print("web on")
DISPLAY = Display(visible=0, size=(800, 600))
DISPLAY.start()
while True:
    try:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        test = open("/home/pi/Desktop/BetterBot/webTest.txt", "w")
        test.write(current_time)
        '''''''''''''''''
        SELENIUM
        opens ucm course 
        page and grabs 
        source html
        '''''''''''''''''
        url = "https://mystudentrecord.ucmerced.edu/pls/PROD/xhwschedule.P_SelectSubject"
        driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
        #driver.set_window_position(-1000, -1000)
        driver.get(url)
        springBtn = driver.find_elements_by_xpath("//input[@value='202130']")[0]
        allCourses = driver.find_elements_by_xpath("//input[@value='N' and @name='openclasses']")[0]
        submit_button = driver.find_elements_by_xpath('/html/body/div[3]/form/input')[0]
        allCourses.click()
        submit_button.click()
        html = driver.page_source
        newHTML = ''
        driver.close()
        clear = open("/home/pi/Desktop/BetterBot/html.txt", "w")
        clear.write("")
        thing = open("/home/pi/Desktop/BetterBot/html.txt", "a")
        for x in html:
            thing.write(x)
        '''''''''''''''''
        LOOKING THROUGH 
        HTML
        '''''''''''''''''
        category = '<tbody><tr bgcolor="#FFC605">\n<th class="ddlabel" scope="row"><p class="leftaligntext"><small>CRN</small></p></th>\n<th class="ddlabel" scope="row"><p class="leftaligntext"><small>Course #</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Course Title</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Units</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Actv</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Days</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Time</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Bldg/Rm</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Start - End</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Instructor</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Max Enrl</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Act Enrl</small></p></th>\n<th class="ddlabel" scope="row"><p class="centeraligntext"><small>Seats Avail</small></p></th>\n</tr>'
        absMin = html.find("NOTE: Schedule Subject to Change")
        absMax = html.find("This is table displays line separator at end of the page")
        newHTML = html[absMin+len("NOTE: Schedule Subject to Change")+29 : absMax-58]

        for x in range(41):
            min = newHTML.find("<h3>")
            max = newHTML.find("</h3>")
            if (min >= 0) and (max >= 0):
                newHTML = newHTML[0:min] + newHTML[max + 5:len(newHTML)]
        for x in range(41):
            if (newHTML.find("#FFC605") - 85 >= 0):
                newHTML = newHTML[0: newHTML.find("#FFC605") - 85] + newHTML[newHTML.find("#FFC605") - 85 + len(category) + 66: len(newHTML)]

        clear = open("/home/pi/Desktop/BetterBot/newhtml.txt", "w")
        clear.write("")
        thing = open("/home/pi/Desktop/BetterBot/newhtml.txt", "a")
        for x in newHTML:
            thing.write(x)


        '''''''''''''''''
        ADDING SEARCHED 
        VALUES TO ARRAY
        '''''''''''''''''
        arr=[[],[],[],[]]
        '[[subjcode],[crsenumb],[crn],[available]'
        def createArr(searchType, arrSpot, thingAfter):
            currentSpot = 0
            for x in range(newHTML.count("subjcode=")):
                if (newHTML.find(searchType) >= 0):
                    currentSpot = newHTML.find(searchType, currentSpot) - 1
                    arr[arrSpot].append(newHTML[newHTML.find(searchType, currentSpot) + len(searchType): newHTML.find(thingAfter,newHTML.find(searchType, currentSpot) + len(searchType))])
                    currentSpot += 2

        createArr("subjcode=", 0, "&amp")
        createArr("crsenumb=", 1, "&amp")
        createArr("crn=", 2, "\">")

        '''''''''''''''''
        SET AVAILABILITY
        '''''''''''''''''
        current = 0
        beg = "class=\"rightaligntext\"><small>"
        begLen = len(beg)
        end = 0
        for x in range(html.count("subjcode=")):
            current = newHTML.find(beg, current) + begLen
            current = newHTML.find(beg, current) + begLen
            current = newHTML.find(beg, current) + begLen
            end = newHTML.find("<", current)
            numAvail = newHTML[current:end]
            
            if numAvail == ("Closed" or ""):
                numAvail = 0
            try:
                if int(numAvail) < 0:
                    numAvail = 0
            except:
                None

            try:    
                arr[3].append(int(numAvail))
            except:
                arr[3].append(0)
                arr[3].append(0)

        resetOld = open("/home/pi/Desktop/BetterBot/oldMasterCourses.txt", "w")
        resetOld.write("")
        resetOld.close()
        old = open("/home/pi/Desktop/BetterBot/oldMasterCourses.txt", "a")
        oldMaster = open("/home/pi/Desktop/BetterBot/masterCourses.txt", "r")
        for x in oldMaster:
            old.write(x)
        old.close()
        resetMaster = open("/home/pi/Desktop/BetterBot/masterCourses.txt", "w+")
        resetMaster.write("")
        resetMaster.close()
        master = open("/home/pi/Desktop/BetterBot/masterCourses.txt", "a")
        for x in arr:
            master.write("!")
            for y in x:
                master.write(str(y))
                master.write("\n")
        master.close()

        arr = getArr("/home/pi/Desktop/BetterBot/masterCourses.txt")
        old = getArr("/home/pi/Desktop/BetterBot/oldMasterCourses.txt")
        changed = []
        #writeFile("/home/pi/Desktop/BetterBot/changes.txt", "")
        update = []

        for i, x in enumerate(arr[3]):
            if x != old[3][i]:
                changed.append(arr[2][i])
                update.append(i)
        # debug
        for x in update:
            print(arr[0][x] + arr[1][x] + "(" + arr[2][x] + ")" +"  new: " + arr[3][x] + "  old: " + old[3][x])
            appendFile("/home/pi/Desktop/BetterBot/allChanges.txt", (arr[0][x] + arr[1][x] + "(" + arr[2][x] + ")" +"  new: " + arr[3][x] + "  old: " + old[3][x] + "\n"))
        if changed != []:
            for x in changed:
                appendFile("/home/pi/Desktop/BetterBot/changes.txt", (x + "\n"))

        time.sleep(20)
    except:
        try:
            driver.close()
        except:
            None
        print("Had an error")
