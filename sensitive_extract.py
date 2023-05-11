#!/usr/bin/env python3

import os
import subprocess
import sys
import re

# Required tools: httprobe, subfinder, gau, gf, nmap, notify-send, dirsearch
# Usage: python3 sensitive_extract.py <target_domain>

# Check if target domain is provided
if len(sys.argv) < 2:
    print("Please provide the target domain as an argument")
    sys.exit(1)

# Set target domain
TARGET_DOMAIN = sys.argv[1]

# Set wordlist for bruteforcing directories
WORDLIST = "/usr/share/dirb/wordlists/common.txt"

# Set Nmap options for checking if internal websites are accessible
NMAP_OPTIONS = "-sS -p 80,443"

# Function to extract subdomains
def extract_subdomains():
    print("[+] Extracting subdomains...")
    # Extract subdomains
    os.system(f"subfinder -d {TARGET_DOMAIN} -silent > subdomains.txt")

# Function to extract sensitive information from JS files
def extract_sensitive_info():
    print("[+] Extracting sensitive information from JS files...")
    # Extract JS files from subdomains
    subdomains = open("subdomains.txt", "r").read().splitlines()
    js_files = []
    for subdomain in subdomains:
        output = subprocess.check_output(f"echo {subdomain} | httpx -silent | gau -subs | grep '\.js$' | sort -u", shell=True)
        js_files.extend(output.decode().strip().split("\n"))
    js_files = list(set(js_files))

    sensitive_info = []
    # Extract sensitive information from JS files
    for js_file in js_files:
        output = subprocess.check_output(f"subjs -u {js_file} | grep -Ei 'password|api|secret|key'", shell=True)
        if output:
            sensitive_info.extend(output.decode().strip().split("\n"))

    # Extract internal URLs from JS files and check if accessible
    internal_urls = []
    for line in sensitive_info:
        urls = re.findall(r"(http|https)://[a-zA-Z0-9./?=_-]*", line)
        internal_urls.extend(urls)
    internal_urls = list(set(internal_urls))
    for url in internal_urls:
        result = subprocess.run(f"nmap {NMAP_OPTIONS} {url}", shell=True, stdout=subprocess.PIPE)
        if "open" in result.stdout.decode():
            os.system(f"notify-send 'Internal website accessible: {url}'")

    # Check for hardcoded credentials in JS files
    sensitive_info = list(set(sensitive_info))
    if sensitive_info:
        os.system(f"notify-send 'Sensitive information found: {','.join(sensitive_info)}'")

# Function to bruteforce directories
def bruteforce_directories():
    print("[+] Bruteforcing directories...")
    # Bruteforce directories for each subdomain
    subdomains = open("subdomains.txt", "r").read().splitlines()
    for subdomain in subdomains:
        output = subprocess.check_output(f"echo {subdomain} | httprobe -c 50 -t 5 -p https:443 -p http:80", shell=True)
        urls = output.decode().strip().split("\n")
        for url in urls:
            print(f"Bruteforcing directories for {url}")
            os.system(f"dirsearch -u {url} -w {WORDLIST} -e php,html,js,json,txt,md")

    # Check for sensitive folders or files
    output = subprocess.check_output(f"cat directory_results.txt | grep -Ei 'admin|login|database|backup'", shell=True)
    if output:
        os.system(f"notify-send 'Sensitive directories or files found: {output.decode().strip()}'")

# Run functions
extract_subdomains()
extract_sensitive_info()
bruteforce_directories()
