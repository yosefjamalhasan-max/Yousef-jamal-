import socket
import uuid
import subprocess
import re
import requests
import platform

class SystemInfo:
    def __init__(self):
        pass

    def get_local_ip(self):
        """Returns the computer's local IP address"""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return local_ip
        except Exception as e:
            return f"Error getting local IP: {e}"

    def get_public_ip(self):
        """Returns the public IP address of the system"""
        try:
            public_ip = requests.get("https://api.ipify.org").text
            return public_ip
        except Exception as e:
            return f"Error getting public IP: {e}"

    def get_mac_address(self):
        """Returns the MAC address of the main network interface"""
        try:
            mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
            return mac
        except Exception as e:
            return f"Error getting MAC address: {e}"

    def get_wifi_password(self):
        """Returns saved Wi-Fi profiles and their passwords (Windows only)"""
        if platform.system() != "Windows":
            return "Wi-Fi password retrieval is supported only on Windows."
        
        try:
            profiles_data = subprocess.check_output("netsh wlan show profiles", shell=True, text=True)
            profiles = re.findall("All User Profile     : (.*)", profiles_data)
            
            wifi_details = {}
            for profile in profiles:
                try:
                    password_data = subprocess.check_output(
                        f'netsh wlan show profile name="{profile}" key=clear',
                        shell=True, text=True
                    )
                    password = re.search("Key Content            : (.*)", password_data)
                    wifi_details[profile.strip()] = password.group(1).strip() if password else "No password found"
                except subprocess.CalledProcessError:
                    wifi_details[profile.strip()] = "Error retrieving password"
            return wifi_details
        except Exception as e:
            return f"Error retrieving Wi-Fi passwords: {e}"


# ---------- Task Section ----------
if __name__ == "__main__":
    info = SystemInfo()

    print("===== System Info Collector =====")
    print(f"Local IP Address   : {info.get_local_ip()}")
    print(f"Public IP Address  : {info.get_public_ip()}")
    print(f"MAC Address        : {info.get_mac_address()}")
    print("Wi-Fi Passwords    :")
    wifi_data = info.get_wifi_password()
    if isinstance(wifi_data, dict):
        for wifi, pwd in wifi_data.items():
            print(f"  {wifi} : {pwd}")
    else:
        print(wifi_data)
