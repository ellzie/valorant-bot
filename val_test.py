import valo_api
import teams
import time
from datetime import datetime
import threading

# https://stackoverflow.com/a/63625368
def checkTime():
    # This function runs periodically every 1 second
    threading.Timer(1, checkTime).start()

    now = datetime.now()

    current_time = now.strftime("%I:%M:%S %p")
    print("Current Time =", current_time)

    if(current_time == '01:43:00 PM'):  # check if matches with the desired time
        testqueue.notifyPlayer()
        print("done")




# user input of some kind - /schedulequeue will handle inputs in arguments
userMonth = "2"
userDay = "21"
userYear = "2023" 
# these will be defaulted but can be changed by user
userHour = "11"
userMinute = "00"
user12Hour = "AM"
# the important bits
totalUserIn = userMonth + "/" + userDay + "/" + userYear + " " + userHour + ":" + userMinute + " " + user12Hour
print(totalUserIn)
fmt = ("%m/%d/%Y %I:%M %p")
epochDate = int(time.mktime(time.strptime(totalUserIn, fmt)))
print(epochDate)
# we now have a conversion to unix, <t:1676242800:t> is what discord will want in the embed
# so we will have title be "Schedule Queue" with the description being "Time" {totalUserIn} (<t:epochDate:t>)
# then we can use buttons/components/etc to allow for join team, this team will have a limit of 5 as its a queue,
# limit should be user defined "I want to duo queue" "I want a 5 stack"
testqueue = teams.Queue(owner="cosine",time = epochDate, maxplayers=2)
# queue created with that time
checkTime()