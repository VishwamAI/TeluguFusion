#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command):
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info(f"Command executed successfully: {command}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {command}")
        logging.error(f"Error output: {e.stderr}")
        return False

def main():
    logging.info("తెలుగుఫ్యూజన్ బిల్డ్ ప్రక్రియ ప్రారంభమైంది...")

    include_paths = "-I/home/ubuntu/TeluguFusion/src"
    libraries = "-lstdc++fs"  # Add any other required libraries here
    unicode_flags = "-DUNICODE -D_UNICODE"

    # కంపైలర్ బిల్డ్ చేయడం
    logging.info("కంపైలర్ బిల్డ్ చేస్తోంది...")
    if not run_command(f"g++ -std=c++17 -O2 {unicode_flags} {include_paths} compiler/main.cpp {libraries} -o telugufusion_compiler"):
        sys.exit(1)

    # ఇంటర్ప్రెటర్ బిల్డ్ చేయడం
    logging.info("ఇంటర్ప్రెటర్ బిల్డ్ చేస్తోంది...")
    if not run_command(f"g++ -std=c++17 -O2 {unicode_flags} {include_paths} interpreter/main.cpp {libraries} -o telugufusion_interpreter"):
        sys.exit(1)

    # వెబ్ ఫ్రేమ్‌వర్క్ బిల్డ్ చేయడం
    logging.info("వెబ్ ఫ్రేమ్‌వర్క్ బిల్డ్ చేస్తోంది...")
    if not run_command(f"g++ -std=c++17 -O2 {unicode_flags} {include_paths} web_framework.cpp {libraries} -o telugufusion_web_framework"):
        sys.exit(1)

    logging.info("తెలుగుఫ్యూజన్ బిల్డ్ ప్రక్రియ పూర్తయింది.")

if __name__ == "__main__":
    main()
