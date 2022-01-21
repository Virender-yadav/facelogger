import datetime

currentDT = datetime.datetime.now()

a= currentDT.month

months = ['','Jan','Feb','march','april','May','June','July']

print ("Current Year is: %d" % currentDT.year)
print ("Current Month is: %d" % currentDT.month)
print ("Current Day is: %d" % currentDT.day)
print ("Current Hour is: %d" % currentDT.hour)
print ("Current Minute is: %d" % currentDT.minute)
print ("Current Second is: %d" % currentDT.second)
print ("Current Microsecond is: %d" % currentDT.microsecond)

c= months[currentDT.month]
print(c)
