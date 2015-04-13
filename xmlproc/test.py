#!/usr/bin/env python
import subprocess
import re

error = "UnboundLocalError: local variable 'digs' referenced before assignment"
error2 = "Parsing 'demo/testmsg.xml'"


#f = open("demo/nstest1.xml", "r")
#f = open("demo/urls.xml", "r")
f = open("../tt.xml", "r")
msg = f.read()
f.close()
f2 = open("demo/testmsg.xml","w+")
f2.write(msg)
f2.close()

f3 = open("demo/errormsg.txt", "w+")
f4 = open("demo/outputmsg.txt", "w+")
check = subprocess.call(["python", "xpcmd.py", "demo/testmsg.xml"], stdout=f4, stderr=f3)
f3.close()
f4.close()

f3 = open("demo/errormsg.txt", "r")
f4 = open("demo/outputmsg.txt", "r")
msg = []
for line in f3:
    msg.append(line)
print "errormsg:"
print msg
msg2 = []
for line in f4:
    msg2.append(line)
print "outputmsg:"
print msg2

if not check:
    print "PASS"
elif re.match(error,msg[len(msg)-1]) and re.match(error2,msg2[len(msg2)-1]):
#elif re.match(error,msg[len(msg)-1]):
    print "FAIL"
else:
    print "UNRESOLVED"
f3.close()
f4.close()
