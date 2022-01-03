import os
from subprocess import call
import hashlib
import sys

if sys.platform != "win32":
        sys.exit()

appdataPath = os.getenv("APPDATA")
path = f"{appdataPath}\\Grocery"

if not os.path.isdir(path):
    os.mkdir(f"{path}")

passFileName = "Pass.{21EC2020-3AEA-1069-A2DD-08002B30309D}.txt"
passFile = f"{path}\\{passFileName}"
forgotPassFileName = "ForgotPass.{21EC2020-3AEA-1069-A2DD-08002B30309D}.txt"
forgotPassFile = f"{path}\\{forgotPassFileName}"
hideFileDirName = "Locked Folder.{21EC2020-3AEA-1069-A2DD-08002B30309D}"

# call(["attrib", "-H", "-S", "grocery"]) #for engineering
if os.path.isdir("grocery"):
    call(["attrib", "+H", "+S", "grocery"])

def draw():
    print("-"*24)
    print("| WELCOME TO YOUR GROCERY MANAGEMENT SOFTWARE |")
    print("-"*24)


def hashingData(data):

    data = hashlib.md5(data.encode())
    data = data.hexdigest()
    return data


def passwordData():
    
    if not os.path.isfile(passFile):
        print("Initial Setup:")
        print("-"*24)
        
        while True:
            passwd = input("Create Password: ")
            if passwd:
                break
            else:
                print("Password Cannot be Empty.")
                print('-'*24)
        
        hashedPasswd = hashingData(passwd)
        
        with open(passFile, 'w+') as file:
            file.write(hashedPasswd)
            file.close()
        
        print(f'-'*24)
        call(["attrib", "+H", "+S", passFile])

    if not os.path.isfile(forgotPassFile):
        createForgotPasswordFile()

    with open(passFile, 'r') as file:
        passwdRead = file.read()
        file.close()
    
    return passwdRead


def unlock(password):

    while True:
        passwd = input("Enter Password: ")
        hashedPasswd = hashingData(passwd)
        if hashedPasswd == password:
            break
        else:
            print("Invalid Password. Try Again...")
            print("-"*25)
    call("grocery/grocery.exe")


def changePassword():

    oldPasswdRead = passwordData()
    oldPasswd = input("Enter Old Password: ")
    hashedOldPasswd = hashingData(oldPasswd)
    
    if hashedOldPasswd != oldPasswdRead:
        input("Password did not Match, Press any key to Exit.")
        sys.exit()

    if os.path.isfile(passFile):
        os.remove(passFile)
        
    while True:
        passwd = input("Change/Update Password: ")
        if passwd:
            break
        else:
            print("Password Cannot be Empty.")
            print('-'*24)

    hashedPasswd = hashingData(passwd)

    with open(passFile, "w+") as f:
        f.write(hashedPasswd)
        f.close()
    call(["attrib", "+H", "+S", passFile])
    
            
def createForgotPasswordFile():

    print(f'-'*24)
    
    question = input("Enter Security Question: ")
    answer = input("Enter Answer for security Question: ")
    hashedAnswer = hashingData(answer)

    with open(forgotPassFile, "w+") as f:
        f.write(question)
        f.write("\n")
        f.write(hashedAnswer)
        f.close()
    
    call(["attrib", "+H", "+S", forgotPassFile])


def forgotFileRead():

    with open(forgotPassFile, "r") as f:
        questionData = f.read().splitlines()
        f.close()

    return questionData    


def forgotPassword():
    
    questionData = forgotFileRead()
    print(f"Secutiry Question: {questionData[0]}")
    
    while True:
        answer = input("Answer for the Security Question to change Password: ")
        hashedAnswer = hashingData(answer)
        
        if hashedAnswer == questionData[1]:
            break
        else:
            print("Wrong Password, Try Again...")
            print("-"*24)
    
    while True:
        passwd = input("Enter New Password: ")
        if passwd:
            break
        else:
            print("Password Cannot be Empty.")
            print('-'*24)

    if os.path.isfile(passFile):
        os.remove(passFile)
        
    hashedPasswd = hashingData(passwd)

    with open(passFile, "w+") as f:
        f.write(hashedPasswd)
        f.close()
    
    call(["attrib", "+H", "+S", passFile])


def main():

    os.system("color c0")
    draw()
    password = passwordData()
    options = ['u', 'c', 'f']
    print('-'*24)
    print("1) To start the software  [u]\n3) Change/Update Password [c]\n4) Forgot Password [f]")
    print("-"*24)
    while True:
        opted = input("Choose [u / c / f] >> ")
        if opted.lower() in options:
            break
        else:
            print("Invalid Option, Try Again...")
            print("-"*24)
    
    print("-"*24)

    if opted.lower() == 'u':
        unlock(password)

    elif opted.lower() == 'c':
        changePassword()

    elif opted.lower() == 'f':
        forgotPassword()
  

if __name__ == "__main__":
    main()
