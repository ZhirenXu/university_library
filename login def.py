from getpass import getpass

## ask user login info
# @return   loginDict
#           a dictionary contains user name and password
def login()
    userName = ""
    password = ""
    loginDict= {}
    
    print("Please enter user name(lastname.#): ")
    userName = input()
    password = getpass(prompt = 'Please enter password: ')
    loginDict['j_username'] = userName
    loginDict['j_password'] = password

    return loginDict
