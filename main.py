# main.py
import requests
from config import *
import logging
import datetime
import re
import unicodedata
import json


AML = """
   _____      __    __     __      
  /\___/\    /_/\  /\_\   /\_\     
 / / _ \ \   ) ) \/ ( (  ( ( (     
 \ \(_)/ /  /_/ \  / \_\  \ \_\    
 / / _ \ \  \ \ \\// / /  / / /__  
( (_( )_) )  )_) )( (_(  ( (_____( 
 \/_/ \_\/   \_\/  \/_/   \/_____/ 
                                   
"""
def gb_to_bytes(gigabytes):
    bytes_in_gb = 1024 ** 3  # 1 gigabyte = 1024^3 bytes
    bytes = gigabytes * bytes_in_gb
    return int(bytes)

def validate_username(username):
    
    # Limit the username length between 3 to 32 characters
    username = username[:32] if len(username) > 32 else username
    if len(username) < 3:
        # Append 'v2' to satisfy the minimum length
        username = username + 'v2'

    # Convert non-ASCII characters to ASCII
    username = unicodedata.normalize('NFKD', username).encode('ascii', 'ignore').decode()

    # Remove any non-alphanumeric characters except underscores
    username = re.sub(r'[^a-zA-Z0-9_]', '', username)

    return username



# Detecting Persian/Arabic Words
def contains_non_english(text):
    persian_arabic_chars = "ابپتثجچحخدذرزژسشصضطظعغفقکگلمنهویئ"
    russian_chars = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    chinese_chars = "的一是不了在人有我他这个中大来上为和国时要以就用们生下作地子出年前同经所自多面发后新学本动因其种美但间由两并还过手心只用天"
    
    for char in text:
        if char in persian_arabic_chars or char in russian_chars or char in chinese_chars:
            return True
    
    return False


# UserName Translater
def transliterate_basic(text):
    # Create a basic mapping of characters from Persian/Arabic to English
    transliteration_map = {
    # Persian
    'آ': 'a', 'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's', 'ج': 'j', 'چ': 'ch',
    'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'z', 'ر': 'r', 'ز': 'z', 'ژ': 'zh', 'س': 's',
    'ش': 'sh', 'ص': 's', 'ض': 'z', 'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f',
    'ق': 'gh', 'ک': 'k', 'گ': 'g', 'ل': 'l', 'م': 'm', 'ن': 'n', 'و': 'o', 'ه': 'h',
    'ی': 'i', 'ئ': 'y',

    # Russian (Cyrillic to Latin)
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
    'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
    'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
    'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
    'я': 'ya',

    # Chinese (Simplified to Pinyin)
    '的': 'de', '一': 'yi', '是': 'shi', '不': 'bu', '了': 'le', '在': 'zai', '人': 'ren', '有': 'you',
    '我': 'wo', '他': 'ta', '这': 'zhe', '个': 'ge', '中': 'zhong', '大': 'da', '来': 'lai', '上': 'shang',
    '为': 'wei', '和': 'he', '国': 'guo', '时': 'shi', '要': 'yao', '以': 'yi', '就': 'jiu', '用': 'yong',
    '们': 'men', '生': 'sheng', '下': 'xia', '作': 'zuo', '地': 'di', '为': 'wei', '子': 'zi', '出': 'chu',
    '年': 'nian', '前': 'qian', '同': 'tong', '经': 'jing', '所': 'suo', '自': 'zi', '多': 'duo', '面': 'mian',
    '发': 'fa', '后': 'hou', '新': 'xin', '学': 'xue', '本': 'ben', '经': 'jing', '动': 'dong', '和': 'he',
    '因': 'yin', '其': 'qi', '种': 'zhong', '美': 'mei', '但': 'dan', '间': 'jian', '由': 'you', '两': 'liang',
    '并': 'bing', '还': 'hai', '过': 'guo', '手': 'shou', '心': 'xin', '只': 'zhi', '用': 'yong', '天': 'tian',
    # Add more Chinese characters as needed...
    }

    # Transliterate the text
    result = ''
    for char in text:
        if char in transliteration_map:
            result += transliteration_map[char]
        elif re.match(r'[a-zA-Z0-9]', char):
            # Keep English letters and digits as is
            result += char
        else:
            # Replace special characters and emojis with empty strings
            result += ''

    return result

def get_h_users(session, url):
    req = session.get(url)
    if req.status_code == 200:
        return req.json()
    else:
        print("Failed to get Users. Please Check Check Your Authentication Link.")
        exit()

def extract_h_users(list_of_users):
    users_data = []
    expired_users = []

    for user in list_of_users:
        raw_email = user["name"]
        email = contains_non_english(raw_email)
        if email:
            raw_email = transliterate_basic(raw_email)
        raw_email = validate_username(raw_email)
        start_date_str = user.get("start_date")  # Using get to handle cases where start_date_str is missing

        if start_date_str is not None:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            package_days = user["package_days"]
            used_traffic = user["current_usage_GB"]
            usage_limit = user["usage_limit_GB"]
            uuid = user["uuid"]
            remaining_value = gb_to_bytes(usage_limit - used_traffic)
            
            # Calculate the expiry time based on the start date and package days
            expiry_time = start_date + datetime.timedelta(days=package_days)
            
            # Get the current time
            current_time = datetime.datetime.now()
            
            # Check if the package is still active
            package_active = current_time < expiry_time
            
            # Check if the package still has traffic
            out_traffic = (usage_limit - used_traffic) < 0
            
            # Convert expiry_time to Unix timestamp
            expiry_timestamp = int(expiry_time.timestamp())
            
            if package_active and not out_traffic:
                user_data = [uuid, raw_email, expiry_timestamp, remaining_value]
                users_data.append(user_data)
            elif out_traffic or not package_active:
                with open('skiplog.txt', 'a+', encoding="utf-8") as f:
                    f.write(f"User {user['name']} has been skipped\n")
                expired_users.append(user["name"])
        else:
            package_days = user["package_days"]
            usage_limit = user["usage_limit_GB"]
            uuid = user["uuid"]
            remaining_value = int(gb_to_bytes(usage_limit))
            
            # Calculate the expiry timestamp from the present time and add the package_days
            expiry_time = datetime.datetime.now() + datetime.timedelta(days=package_days)
            expiry_timestamp = int(expiry_time.timestamp())
            
            user_data = [uuid, raw_email, expiry_timestamp, remaining_value]
            users_data.append(user_data)
    print(f"✅Valid Users: {len(users_data)}\n")
    print(f"❌Expired Users: {len(expired_users)}\n")
    return users_data

def m_login(session,username, password):
    use_protocol = 'https' if M_HTTPS else 'http'
    url = f'{use_protocol}://{M_DOMAIN}:{M_PORT}/api/admin/token'
    data = {
        'username': M_USERNAME,
        'password': M_PASSWORD
    }

    try:
        response = session.post(url, data=data)
        response.raise_for_status()
        access_token = response.json()['access_token']
        print("Marzban Login Successful.")
        print("-" * 10)
        return access_token
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while obtaining access token: {e}')
        return None

def get_m_inbounds(session,access_token):
    use_protocol = 'https' if M_HTTPS else 'http'
    url = f'{use_protocol}://{M_DOMAIN}:{M_PORT}/api/inbounds'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        inboundsList = response.json()
        return inboundsList
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while retrieving inbounds: {e}')
        return None

def add_m_user(session, access_token, uuid, email, traffic, expiretime, inbounds):
    use_protocol = 'https' if M_HTTPS else 'http'
    url = f'{use_protocol}://{M_DOMAIN}:{M_PORT}/api/user'
    data = {
        "username": email,
        "proxies": {
            "vmess": {
            },
            "vless": {
            },
            "trojan": {
            },
            "shadowsocks": {
            }
        },
        "inbounds": {
        },
        "expire": expiretime,
        "data_limit": traffic,
        "data_limit_reset_strategy": "no_reset"
    }


    # Iterate through the protocols and check if inbounds exist
    for protocol, inbound_names in inbounds.items():
        if inbound_names:
            data["inbounds"][protocol] = inbound_names

    # Remove protocols with no inbounds
    data["proxies"] = {protocol: {} for protocol, inbs in data["inbounds"].items() if inbs}

    try:
        data["proxies"]["vless"]["flow"] = "xtls-rprx-vision"
    except Exception as e:
        pass
    try:
        data["proxies"]["vmess"]["id"] = uuid
    except Exception as e:
        pass
    try:
        data["proxies"]["vless"]["id"] = uuid
    except Exception as e:
        pass
    try:
        data["proxies"]["trojan"]["id"] = uuid
    except Exception as e:
        pass
    try:
        data["proxies"]["shadowsocks"]["id"] = uuid
    except Exception as e:
        pass
    
    

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    
    try:
        # Printing Json Data
        # print(json.dumps(data, indent=4))
        response = session.post(url,json=data, headers=headers)
        response.raise_for_status()
        user_status = response.json()
        return user_status
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while adding user: {e}')
        return None

def add_m_custom_user(session, access_token, uuid, email, traffic, expiretime, inbounds, flow):
    use_protocol = 'https' if M_HTTPS else 'http'
    url = f'{use_protocol}://{M_DOMAIN}:{M_PORT}/api/user'
    data = {
        "username": email,
        "proxies": {
            "vmess": {},
            "vless": {},
            "trojan": {},
            "shadowsocks": {}
        },
        "inbounds": {},
        "expire": expiretime,
        "data_limit": traffic,
        "data_limit_reset_strategy": "no_reset"
    }
    
    # Iterate through the protocols and check if inbounds exist
    for protocol, inbound_names in inbounds.items():
        if inbound_names:
            data["inbounds"][protocol] = inbound_names

    # Remove protocols with no inbounds
    data["proxies"] = {protocol: {} for protocol, inbs in data["inbounds"].items() if inbs}
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    # Conditionally add the "flow" line to the "vless" section
    if flow:
        try:
            data["proxies"]["vless"]["flow"] = "xtls-rprx-vision"
        except Exception as e:
            pass
    try:
        data["proxies"]["vmess"]["id"] = uuid
    except Exception as e:
        pass
    try:
        data["proxies"]["vless"]["id"] = uuid
    except Exception as e:
        pass
    try:
        data["proxies"]["trojan"]["id"] = uuid
    except Exception as e:
        pass
    try:
        data["proxies"]["shadowsocks"]["id"] = uuid
    except Exception as e:
        pass
    
    try:
        #print(json.dumps(data, indent=4))
        response = session.post(url, json=data, headers=headers)
        response.raise_for_status()
        user_status = response.json()
        return user_status
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while adding user: {e}')
        return None

def add_m_users(session, access_token, users, inbound_names):
    for user in users:
        uuid, email, expiretime, traffic = user
        user_status = add_m_user(session, access_token, uuid, email, traffic, expiretime, inbound_names)
        if user_status:
            print(f"User {email} added successfully.")
        else:
            print(f"Failed to add user {email}.")

def add_m_custom_users(session, access_token, users, inbound_names, flow):
    for user in users:
        uuid, email, expiretime, traffic = user
        user_status = add_m_custom_user(session, access_token, uuid, email, traffic, expiretime, inbound_names, flow)
        if user_status:
            print(f"User {email} added successfully.")
        else:
            print(f"Failed to add user {email}.")

if __name__ == "__main__":
    # Making Session For Each API
    H_SESSION = requests.Session()
    M_SESSION = requests.Session()
    print(AML)
    h_users_data = get_h_users(H_SESSION, H_AUTH)
    if h_users_data:
        print("Hiddify Login Succesful.\n")
        user_data = extract_h_users(h_users_data)
        while True:
            choice = input("Do you wanna proceed to transfer users To Marzban? (y/n): ").strip().lower()
            
            if choice == 'y':
                auto_manual = input("Do you want to Transfer Users by Automatic Method or Manual Method? (a/m)").strip().lower()
                if auto_manual == "a":
                    # Getting Marzban Inbounds for Later Use
                    token = m_login(M_SESSION, M_USERNAME, M_PASSWORD)
                    if token:
                        all_inbounds = get_m_inbounds(M_SESSION, token)
                        protocols = {
                                    "vmess": [],
                                    "vless": [],
                                    "trojan": [],
                                    "shadowsocks": []
                                    }
                        # Loop through the keys in the JSON data
                        for key, value in all_inbounds.items():
                            # Check if the key is one of the supported protocols
                            if key in protocols:
                                protocols[key].extend([subprotocol["tag"] for subprotocol in value])

                        # Handle the possibility of missing protocols
                        for protocol in ["vmess", "vless", "trojan", "shadowsocks"]:
                            try:
                                protocols[protocol].extend([subprotocol["tag"] for subprotocol in all_inbounds[protocol]])
                            except KeyError:
                                pass
                        vmess_inbounds = ", ".join(protocols.get("vmess", []))
                        vless_inbounds = ", ".join(protocols.get("vless", []))
                        trojan_inbounds = ", ".join(protocols.get("trojan", []))
                        shadowsocks_inbounds = ", ".join(protocols.get("shadowsocks", []))
                        add_m_users(M_SESSION, token, user_data,protocols)
                        print("Users transferred to Marzban Succesfuly.")
                # Manual Adding Inbounds
                elif auto_manual == "m":
                        token = m_login(M_SESSION, M_USERNAME, M_PASSWORD)
                        if token:
                            all_inbounds = get_m_inbounds(M_SESSION, token)
                            custom_protocols = {
                            "vmess": [],
                            "vless": [],
                            "trojan": [],
                            "shadowsocks": []
                            }
                            # Loop through the keys in the JSON data
                            for key, value in all_inbounds.items():
                                # Check if the key is one of the supported protocols
                                if key in custom_protocols:
                                    custom_protocols[key].extend([subprotocol["tag"] for subprotocol in value])

                            # Handle the possibility of missing protocols
                            vmess_inbounds = []
                            while True:
                                print("VMESS inbound names. (You Can Type '/' To Select All)")
                                available_inbounds = ", ".join(custom_protocols.get("vmess", []))
                                print("Available Inbounds:", available_inbounds or "No Inbounds Found")
                                vmess_input = input("Enter Inbound Name: (Press Enter While Empty To Skip)")
                                if vmess_input:
                                    if vmess_input == "/":
                                        vmess_inbounds.extend(custom_protocols.get("vmess", []))
                                        break
                                    else:
                                        vmess_inbounds.append(vmess_input)
                                else:
                                    break

                            vless_inbounds = []
                            while True:
                                print("VLESS inbound names. (You Can Type '/' To Select All)")
                                available_inbounds = ", ".join(custom_protocols.get("vless", []))
                                print("Available Inbounds:", available_inbounds or "No Inbounds Found")
                                vless_input = input("Enter Inbound Name: (Press Enter While Empty To Skip)")
                                if vless_input:
                                    if vless_input == "/":
                                        vless_inbounds.extend(custom_protocols.get("vless", []))
                                        break
                                    else:
                                        vless_inbounds.append(vless_input)
                                else:
                                    break

                            trojan_inbounds = []
                            while True:
                                print("TROJAN inbound names. (You Can Type '/' To Select All)")
                                available_inbounds = ", ".join(custom_protocols.get("trojan", []))
                                print("Available Inbounds:", available_inbounds or "No Inbounds Found")
                                trojan_input = input("Enter Inbound Name: (Press Enter While Empty To Skip)")
                                if trojan_input:
                                    if trojan_input == "/":
                                        trojan_inbounds.extend(custom_protocols.get("trojan", []))
                                        break
                                    else:
                                        trojan_inbounds.append(trojan_input)
                                else:
                                    break

                            shadowsocks_inbounds = []
                            while True:
                                print("SHADOWSOCKS inbound names. (You Can Type '/' To Select All)")
                                available_inbounds = ", ".join(custom_protocols.get("shadowsocks", []))
                                print("Available Inbounds:", available_inbounds or "No Inbounds Found")
                                shadowsocks_input = input("Enter Inbound Name: (Press Enter While Empty To Skip)")
                                if shadowsocks_input:
                                    if shadowsocks_input == "/":
                                        shadowsocks_inbounds.extend(custom_protocols.get("shadowsocks", []))
                                        break
                                    else:
                                        shadowsocks_inbounds.append(shadowsocks_input)
                                else:
                                    break
                            while True:
                                print("Do you Want To Use Flow For Vless Inbounds? (xtls-rprx-vision)")
                                fl_ow = input("Enter (y/n) : ").strip().lower()
                                if fl_ow == "y":
                                    flow_status = True
                                    break
                                if fl_ow == "n":
                                    flow_status = False
                                    break
                                else:
                                    print("please enter valid answer")
                            
                            customprotocols = {
                                "vmess": ",".join(vmess_inbounds).split(",") if vmess_inbounds else [],
                                "vless": ",".join(vless_inbounds).split(",") if vless_inbounds else [],
                                "trojan": ",".join(trojan_inbounds).split(",") if trojan_inbounds else [],
                                "shadowsocks": ",".join(shadowsocks_inbounds).split(",") if shadowsocks_inbounds else []
                            }

                            # Filter out empty values
                            customprotocols = {k: v for k, v in customprotocols.items() if v}
                            add_m_custom_users(M_SESSION, token, user_data,customprotocols,flow_status)
                else:
                    print("Invalid choice. Please enter 'a' or 'm'.")

                break
            elif choice == 'n':
                print("Exiting the Script.")
                break
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")

# https://github.com/ItsAML
