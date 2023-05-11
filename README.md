# sensitive_extract


This code is a Python script for automating the reconnaissance process in web application security testing. It performs several tasks, including subdomain enumeration, sensitive information extraction from JavaScript files, directory brute-forcing, and searching for sensitive directories and files. The script uses several popular open-source tools such as subfinder, gau, gf, httprobe, nmap, and dirsearch to perform these tasks. It also uses notify-send to send notifications to the user's desktop environment when certain events occur, such as finding sensitive information or discovering an internal website accessible from the external network. The script takes a target domain as an argument and outputs progress information to the terminal.

# Required tools: 

httprobe, subfinder, gau, gf, nmap, notify-send, dirsearch

# Usage: 

python3 sensitive_extract.py <target_domain>


# Installation Guide

Ensure that you have Go installed on your system. You can check this by running go version in your terminal. If Go is not installed, download it from the official Go website and follow the installation instructions specific to your operating system.

Install the required tools using the go install command. Run the following commands one by one to install each tool:

go install github.com/tomnomnom/httprobe@latest

go install github.com/subfinder/subfinder/v2/cmd/subfinder@latest

go install github.com/lc/gau@latest

go install github.com/tomnomnom/gf@latest

go install github.com/nmap/nmap@latest

go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest


If the installation was successful, you should see the version information for each tool.
