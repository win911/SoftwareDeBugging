#!/usr/bin/env python
# $Id: ddmin.py,v 2.2 2005/05/12 22:01:18 zeller Exp $

from split import split
from listsets import listminus
import re
import subprocess

PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"

def ddmin(circumstances, test):
    """Return a sublist of CIRCUMSTANCES that is a relevant configuration
       with respect to TEST."""
    
    assert test([]) == UNRESOLVED
    assert test(circumstances) == FAIL

    n = 2
    while len(circumstances) >= 2:
        subsets = split(circumstances, n)
        assert len(subsets) == n

        some_complement_is_failing = 0
        for subset in subsets:
            complement = listminus(circumstances, subset)

            if test(complement) == FAIL:
                circumstances = complement
                n = max(n - 1, 2)
                some_complement_is_failing = 1
                break

        if not some_complement_is_failing:
            if n == len(circumstances):
                break
            n = min(n * 2, len(circumstances))

    return circumstances



if __name__ == "__main__":
    tests = {}
    circumstances = []

    def string_to_list(s):
        c = []
        for i in range(len(s)):
            c.append((i, s[i]))
        return c
    
    def mytest(c):
        global tests
        global circumstances

        error = "UnboundLocalError: local variable 'digs' referenced before assignment\n"
        error2 = "Parsing 'xmlproc/demo/testmsg.xml'\n"
        success = "Parse complete, 0 error(s) and 0 warning(s)\n"

        s = ""
        for (index, char) in c:
            s += char

        if s in tests.keys():
            return tests[s]

        print "%02i" % (len(tests.keys()) + 1), "Testing",
       
        f2 = open("xmlproc/demo/testmsg.xml","w+")
        f2.write(s)
        f2.close()
        
        f3 = open("xmlproc/demo/errormsg.txt", "w+")
        f4 = open("xmlproc/demo/outputmsg.txt", "w+")
        check = subprocess.call(["python", "xmlproc/xpcmd.py", "xmlproc/demo/testmsg.xml"], stdout=f4, stderr=f3)
        f3.close()
        f4.close()
 
        f3 = open("xmlproc/demo/errormsg.txt", "r")
        f4 = open("xmlproc/demo/outputmsg.txt", "r")
        msg = []
        for line in f3:
            msg.append(line)
        msg2 = []
        for line in f4:
            msg2.append(line)
        f3.close()
        f4.close()

        if (not check) and success == msg2[len(msg2)-1]:
            print PASS
            tests[s] = PASS
            return PASS
        elif len(msg) and error == msg[len(msg)-1] and error2 == msg2[len(msg2)-1]:
            print FAIL
            tests[s] = FAIL
            return FAIL
        else:
            print UNRESOLVED
            tests[s] = UNRESOLVED
            return UNRESOLVED

    f = open("xmlproc/demo/urls.xml", "r")
    msg = f.read()
    f.close()
    circumstances = string_to_list(msg)
    mytest(circumstances)
    c = ddmin(circumstances, mytest)
    print c
    s = ""
    for (index, char) in c:
        s += char
    print s
