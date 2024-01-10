# README

# Overview

MassEmailChecker is an advanced tool designed to streamline and automate the process of managing and validating email accounts and proxy servers.

This script simplifies tasks such as credential verification, email server mapping, and proxy management. It's an essential tool for efficiently handling large volumes of email accounts and ensuring smooth network operations.

# Disclaimer

This software is intended for educational and professional use only. Any misuse or application of MassEmailChecker in illegal activities is strictly prohibited.

Users must adhere to ethical standards and comply with all applicable laws and regulations.

# Features of MassEmailChecker

Automated Credential Reading: The script starts by automatically reading user credentials from a predefined file (credentials.txt).

# Account Shuffling 

(Basically trying to avoid connecting to the same email provider twice a row, if so it introduces a random delay up to 60 seconds)


Randomization Logic: To mitigate the risk of pattern detection by email service providers, the script employs a randomization strategy. 
This shuffling of accounts minimizes the chances of triggering security alerts that can arise from systematic access patterns.

Delay Insertion: The script intelligently introduces variable delays between processing consecutive accounts from the same domain.
These random time intervals further disguise the script's activities, making it less likely to be flagged by automated monitoring systems.

# IMAP Server Mapping

Parsing IMAP Server Details: The script reads and parses IMAP server mappings from imap_server_mappings.txt. 

This file should contain mappings in the format domain:server:port, enabling the script to identify the correct server and port for each email domain.

Dynamic Server Retrieval: Upon processing an email, the script dynamically retrieves the corresponding IMAP server details, ensuring accurate and efficient email server connections.

# SSL in IMAP Server Connection

When the script connects to an IMAP server to access email accounts, it uses a very basic SSL implementation to ensure that the connection is secure. 

Customization of SSL Context: Depending on the security requirements and the server's specifications, you might need to adjust the SSL context's properties, such as the SSL version, ciphers, and verification modes.

Example:

    ssl_context.set_ciphers('DEFAULT@SECLEVEL=1')
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

This allows for the specification of various SSL settings, such as the SSL protocol version, ciphers, and whether to verify the server's certificate.

# Proxy Management

Proxy Reading and Validation: Proxies are read from proxies.txt and validated through a series of checks. This includes testing each proxy for connectivity and response.

Intelligent Proxy Selection: The script employs a strategy to randomly select proxies from the validated list, reducing the likelihood of usage patterns that could trigger network security mechanisms.

# Advanced Proxy Management

Multi-Source Proxy Gathering: Beyond reading proxies from a local file, the script can fetch proxies from external sources, adding a layer of dynamism to the proxy pool.

Proxy Validation and Testing: Each proxy is rigorously tested for validity and responsiveness. The script ensures that only functioning proxies are used, enhancing the reliability of connections.

Adaptive Proxy Usage: The script adapts its proxy usage based on previous successes and failures. It avoids proxies that previously resulted in connection issues, thereby optimizing the success rate of email logins and operations.

# Email Analysis

Bulk Email Login: Leveraging the IMAP protocol, the script logs into each email account from the verified credentials list.

Data Retrieval and Analysis: Once logged in, it navigates to the inbox, retrieving and analyzing email data, such as sender information, to gather relevant insights about unique correspondents.

# Data Organization

Efficient Data Extraction: The script extracts crucial data from each email account, focusing on unique sender information.

Organized Data Output: Extracted data is neatly organized and written into output files named after the respective account, including the accounts credentials, facilitating easy access and review.

# Notification System

Post-Execution Alerts: One of the script's standout features is its ability to send notifications upon completion of its tasks. This is crucial for long-running scripts where continuous monitoring isn't feasible.

Email-Based Notifications: The notification system is configured to send an email alert, detailing the completion status of the script. This feature is particularly useful for users who need to be informed remotely.

# Customization Steps for Email-Based Notifications

Although almost everything is self-expaining inside the script, here is a little guide how to..

# Setting Up Email Credentials for the Sender:

Locate the section in the script where the sender's email credentials are defined. This typically involves specifying the sender's email address and password.

Modify the sender_email and password variables with the appropriate credentials. These credentials will be used to log in to the email server for sending the notification.

Example:

    sender_email = "your_sender_email@example.com"
    password = "your_email_password"

# Configuring the SMTP Server Details:

Find the part of the script where the SMTP server and port are defined. This is necessary for establishing a connection to the email server.

Update the smtp_server and smtp_port variables with the correct server details for the sender's email provider.
    
Example:

    smtp_server = "smtp.example.com"
    smtp_port = 587  # Common port for SMTP

# Setting the Receiver's Email Address:

Look for the variable that defines the recipient of the notification email. This could be the same as the sender or a different email address.

Change the receiver_email variable to the desired recipient's email address.

Example:

    receiver_email = "your_receiver_email@example.com"

# Customizing the Email Content:

The script will have a section where the email's subject and body are defined. This is where you can customize the content of the notification email to include specific details or summaries.

Modify the message["Subject"] and the body of the email as per your requirements.

Example:

    message["Subject"] = "Script Notification: Completion Status"
    body = "The MassEmailChecker script has completed its execution."


# Example Code Snippet

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

By customizing these sections of the script, users can set up personalized email notifications that inform them about the script's execution status, making remote monitoring more efficient and convenient.

# Installation

Clone the MassEmailChecker repository to your local machine.

    git clone https://github.com/WhiteyCookie/MassEmailChecker.git

Ensure that Python 3 is installed on your system.

Install necessary Python libraries:

    pip install requests imaplib email socket smtplib ssl

# Usage

Ensure that the credentials.txt, imap_server_mappings.txt, and proxies.txt files are properly formatted and located in the same directory as the MassEmailChecker script.

Run the script with:

    python MassEmailCheckerGPTv3.py

File Formats

Credentials File: Should contain email credentials in username:password format.

IMAP Server Mappings File: Must have lines in domain:server:port format.

Proxy File: Should list proxies in host:port format.
(By default, already provided with a list of Proxies)


# Contribution

We welcome contributions to enhance MassEmailChecker. Please fork the repository and submit your pull requests with any proposed changes.

# License

This project is released under the GNU General Public License (GPL), which provides copyleft for the distribution of free software. For more details, see the LICENSE file.

# Acknowledgments

This project owes its inspiration and success to several key influences and sources of motivation:

OpenAI and Its Team: A special thanks to OpenAI and its team for providing invaluable resources and support. Their contributions in the field of AI and technology have been a guiding light and an essential part of the development process for this project.

The Movie "Hackers": Heartfelt gratitude goes to the cult classic film "Hackers" for its influential role. The movie has been a significant source of inspiration, providing not only entertaining content but also thought-provoking quotes and perspectives on the digital world and its endless possibilities.

The Open-Source Community: Immense appreciation is extended to the open-source community. Their collaborative spirit, resource sharing, and innovative approach to problem-solving have been instrumental in the development of this project.
