#!python

from TesterModule import *
import sys
import time

HOST = 'localhost'
PORT = 31337

def armTest(scgen):
    def acceptloop():
        try:
            TEST_PORT = 1338
            tc = "acceptloop + sh"
            print "[+] %s" % tc
            sc = scgen.acceptloop(TEST_PORT)
            sc += scgen.dupsh(5)
            sc, cnt = ks_asm('arm', sc)
            (s, f) = makeSocket(HOST, PORT)
            f.write(sc + '\n')
            f.close()
            time.sleep(1)
            (s1, f1) = makeSocket(HOST, TEST_PORT)
            s1.send('whoami\n')
            rv = s1.recv(1024)
            s1.close()
            if len(rv) != 0:
                print "[PASS] %s" % tc
            else:
                print "[FAIL] %s" % tc
        except:
            print "[EXCEPT] %s" % tc
    def bindshell():
        try:
            TEST_PORT = 1339
            tc = "bindshell"
            print "[+] %s" % tc
            sc = scgen.bindshell(TEST_PORT, 5)
            sc, cnt = ks_asm('arm', sc)
            (s, f) = makeSocket(HOST, PORT)
            f.write(sc + '\n')
            f.close()
            time.sleep(1)
            (s1, f1) = makeSocket(HOST, TEST_PORT)
            s1.send('whoami\n')
            rv = s1.recv(1024)
            s1.close()
            if len(rv) != 0:
                print "[PASS] %s" % tc
            else:
                print "[FAIL] %s" % tc
        except:
            print "[EXCEPT] %s" % tc

    def cat():
        try:
            tc = "cat /etc/passwd"
            print "[+] %s" % tc
            sc = scgen.cat('/etc/passwd', 3, 4)
            sc += scgen.exit()
            sc, cnt = ks_asm('arm', sc)
            (s, f) = makeSocket(HOST, PORT)
            f.write(sc + '\n')
            rv = s.recv(4096)
            print rv
            s.close()
            if len(rv) != 0:
                print "[PASS] %s" % tc
            else:
                print "[FAIL] %s" % tc
        except:
            print "[EXCEPT] %s" % tc

    def chmod():
        try:
            tc = "chmod /tmp/xxx"
            print "[+] %s" % tc
            sc  = scgen.chmod("/tmp/xxx")
            sc += scgen.exit()
            sc, cnt = ks_asm('arm', sc)
            (s, f) = makeSocket(HOST, PORT)
            f.write(sc + '\n')
            s.close()
            print "[CHECK] %s" % tc
        except:
            print "[EXCEPT] %s" % tc

    def ls():
        try:
            tc = "ls /etc/"
            print "[+] %s" % tc
            sc = scgen.ls('/etc/', 4)
            sc += scgen.exit()
            sc, cnt = ks_asm('arm', sc)
            (s, f) = makeSocket(HOST, PORT)
            rv = ''
            while True:
                f.write(sc + '\n')
                x = s.recv(4096)
                if len(x) == 0:
                    break
                else:
                    rv += x
            s.close()
            print getdent_to_list(rv)
            if len(rv) != 0:
                print "[PASS] %s" % tc
            else:
                print "[FAIL] %s" % tc
        except:
            print "[EXCEPT] %s" % tc

    acceptloop()

def Run():
    sc_thumb = thumbSCGen()
    sc_arm   = armSCGen()
    sc_arm64 = arm64SCGen()

    armTest(sc_arm64)

if __name__ == '__main__':
    Run()
