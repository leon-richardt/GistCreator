#!/bin/python3

import requests
import pyperclip
import sys

opts = {"clipboard": False, "description": "", "public": False, "quiet": False}


def send_request(file_names):
    POST_URL = "https://api.github.com/gists"

    token = ""
    with open("token.txt", "r") as reader:
        token = reader.read().rstrip("\n")

    if not token:
        exit("Failed to read token from token.txt")

    auth_header = {"Authorization": f"token {token}"}
    payload = build_payload(opts["description"], opts["public"], file_names)

    return requests.post(POST_URL, headers=auth_header, json=payload)


def build_payload(description, public, file_names):
    payload = {}

    payload["description"] = description
    payload["public"] = public

    files_json = {}

    # Read all files into list, skipping those that can not be found
    for name in file_names:
        # TODO: Handle stdin
        try:
            with open(name, "r") as reader:
                files_json[name] = {"content": reader.read()}
        except FileNotFoundError:
            log(f"File {name} could not be found, skipping ...")
            continue

    payload["files"] = files_json

    return payload


def parse_args():
    file_names = []

    # Skip program name when parsing arguments
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]

        if arg.startswith("--"):
            # Long opts
            if arg == "--clipboard":
                opts["clipboard"] = True
            elif arg == "--description":

                if i + 1 >= len(sys.argv):
                    log("--description passed, but no description string was"
                        " found")
                    exit(1)

                opts["description"] = sys.argv[i + 1]
                # One additional increment for the description string
                i = i + 1
            elif arg == "--public":
                opts["public"] = True
            elif arg == "--quiet":
                opts["quiet"] = True
            elif arg == "--secret":
                opts["public"] = False

            i = i + 1
        elif arg.startswith("-"):
            if arg == "-":
                # stdin
                file_names.append("-")
            else:
                # TODO: Short opts
                pass
        else:
            # Files
            file_names.append(arg)
            i = i + 1

    return file_names


def log(string):
    if not opts["quiet"]:
        print(string)


if __name__ == "__main__":

    file_list = parse_args()

    response = send_request(file_list)

    # Response code 201 means that the gist was created
    if response.status_code == 201:
        data = response.json()
        html_url = data["html_url"]

        log(f"Gist successfully created at {html_url}")
        if opts["clipboard"]:
            pyperclip.copy(html_url)
            log("(Also copied to clipboard.)")
    else:
        log(response.text)
        exit(f"Request was not successful, received status code"
             " {response.status_code}")
