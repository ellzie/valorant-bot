import valo_api
from teams import Team, Player
import time
import datetime

# user input of some kind - /schedulequeue will handle inputs in arguments
userMonth = "2"
userDay = "12"
userYear = "2023" 
# these will be defaulted but can be changed by user
userHour = "06"
userMinute = "00"
user12Hour = "PM"
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
