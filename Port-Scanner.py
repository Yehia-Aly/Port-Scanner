import socket
import re
import requests
from termcolor import colored

ip_add_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")
port_min = 0
port_max = 65535
#first function for public ip
def get_ip_info():
    try:
        response = requests.get("https://ipinfo.io/json")
        ip_info = response.json()
        ip = ip_info.get("ip")
        if ip:
            return ip
        else:
            return "unkown ip"
    except requests.exceptions.RequestException as e:
        print(colored(f"Error: {e}", "red"))
        return "unkown ip"
#second function  to handle user's input
def get_ip_addr():
    while True:
        ip_add_entered = input(colored("Please enter the IP you want to scan or type (myip) for your own IP: ", "green"))
        if ip_add_entered == "myip":
            ip_add_entered = get_ip_info()
            if ip_add_entered != "unkown ip":
                print(colored(f"ur ip is {ip_add_entered}", "green"))
            else:
                print(colored("couldnt retrieve ur ip please try again.", "red"))
                continue
        if ip_add_pattern.search(ip_add_entered):
            print(colored(f"{ip_add_entered} is a valid ip addr", "green"))
            return ip_add_entered
        
#third function to handle port range
def get_port_range():
    while True:
        print(colored("please enter range of ports u want to scan.\n the range should be in the format: <start_port>-<end_port>\n Ex: '60-90' ", "green"))
        port_range = input(colored("enter the port range: ", "green"))
        print(colored("scanning ports...", "blue"))
        port_range_valid = port_range_pattern.search(port_range)
        if port_range_valid:
            port_min = int(port_range_valid.group(1))
            port_max = int(port_range_valid.group(2))
            if 0 <= port_min <= 65535 and 0 <= port_max <= 65535 and port_min <= port_max:
                return port_min, port_max
        print(colored("Ports must be in the range 0-65535 and start port <= end port.", "red"))

#fourth function to show results
def show_results(open_ports, closed_ports, ip_add_entered):
    all_ports = sorted(open_ports + closed_ports)  
    for port in all_ports:
        if port in open_ports:
            print(colored(f"Port {port} is open on {ip_add_entered}.", "green"))
        else:
            print(colored(f"Port {port} is closed on {ip_add_entered}.", "red"))

# Main script
open_ports = []
closed_ports = []
ip_add_entered = get_ip_addr()
port_min, port_max = get_port_range()

for port in range(port_min, port_max + 1):  
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((ip_add_entered, port))
            open_ports.append(port)
    except:
        closed_ports.append(port)

# Call the show_results function to display results
show_results(open_ports, closed_ports, ip_add_entered)