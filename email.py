"""Hi there!

I got a bit carried away with this task and created a full internal email system: slademail.com

Your email address is assessor@slademail.com  password: Password

the admin email address is admin@slademail.com password: adm1n

This has a number of different functions:

1) add new user (only admin)
2) open inbox
    i) read specific email
    ii) see a list of unread emails
    iii) see a list of spam emails
    iv) mark/unmark as spam
    v) delete an email
    vi) return to main menu
3) send email
4) clear inbox
5) log out

The inboxes are objects made of an email address and a list of emails
an email is an object as defined in the task

enjoy!!

"""

#-------------------------------------IMPORT LIBRARIES--------------------------------
import pickle

#-------------------------------------DEFINE CLASSES-----------------------------------------------------
#define class - Email (subject, email contents, from_address, has_been_read, is_spam)

class Email(object):

    has_been_read = False
    is_spam = False
    

    def __init__(self,subject,email_contents,from_address):
        self.subject = subject
        self.email_contents = email_contents
        self.from_address = from_address

    #define methods for Email

    def mark_as_read(self):
        
        self.has_been_read = True

    def mark_as_spam(self):

        self.is_spam = True

# define class User_inbox (user_address, box) where box is a list of emails
class User_inbox(object):

    box = []

    def __init__(self,user_address):
        self.user_address = user_address


#-----------------------------------DEFINE FUNCTIONS----------------------------------

# send email
def send_email(sender_email):


    while True:
        #request destination email
        destination = input("""Enter email address here or type 'e' to exit 
        
To:""")
        
        if destination != 'e':
            #check email address exists
            existing_user = False
            with open ("addressbook.txt","r+") as f:
                    text = f.read()
                    text = text.split("\n")
                    for element in text:
                                current_user = element.split(", ")[0]
                                if  current_user.lower() == destination.lower():
                                    #set existing_user to True if there is a match
                                    existing_user = True 
                                    break
                    #if no match, give error message and return to top of while loop                    
                    if existing_user == False:
                        print("\nI am sorry that email address is not registered\n")
                        continue
                    #else there is a match, so unpickle the inbox and allow the user to enter a subject, and text
                    else:
                        with open(f"inbox_{destination}.dat","rb") as d:
                            dest_inbox = pickle.load(d)
                            email_list = dest_inbox.box
                            subject = input ("\nPlease enter the subject of your email:\n")
                            message = input("Please enter your message:\n")
                            #create a new email instance
                            email = Email(subject, message,sender_email)
                            #update email_list
                            email_list.append(email)
                            #update the inbox object
                            dest_inbox.box = email_list
                            #pickle and dump in the recipient's email file
                        with open(f"inbox_{destination}.dat","wb") as d:
                            pickle.dump(dest_inbox, d)
                            #confirmatory message
                            print("Message sent!\n")
                            return
        else:
            return

#get count(inbox) - this is self explanatory
def get_count(inbox):
    
    return (len(inbox))

#get email from inbox - this function will display the text along with the details of the email and mark it as read
def get_email(inbox,email_num):

    while True:

        try: 
            got_email = inbox[email_num]
            #set spam_yes text for output
            if got_email.is_spam == True:
                spam_yes = "yes"
            else:
                spam_yes = "no"
                #print email contents in a nice format
            got_email_content = (f"""

From:           {got_email.from_address}
Subject:        {got_email.subject}
Spam:           {spam_yes}

Email text:     

{got_email.email_contents}


            """)
            #mark the email as read
            got_email.mark_as_read()
            
            return (got_email_content)

        #if unable to perform, input incorrect so print error message and try again
        except:
            email_num = ("Error, please enter an integer smaller than the size of the inbox:")
            continue
    
#This function returns a list of unread emails
def get_unread_emails(inbox):
    
    unread_list = []

    for email in inbox:
        if email.has_been_read == False:
            #append to list if unread
            unread_list.append(email)

    return (unread_list)


    
#This returns a list spam emails. 
def get_spam_emails(inbox):

    spam_list = []

    for email in inbox:
        if email.is_spam == True:
            #only add to list if spam
            spam_list.append(email)

    return (spam_list)

#This function deletes an email from the inbox
def delete_email(inbox):

    while True:

        num_del = input ("Please enter the number of the above email list you would like to delete or type 'e' to exit:\n")
        
        if num_del != 'e':

            try:
                index = int(num_del)-1
                #delete the designated email
                del inbox[index]
                print (f"\nemail number {num_del} has been deleted\n")

                return
            #error message if incorrect input
            except:
                print("I am sorry, please enter an integer from the list above")
                continue
        #exit if user enters 'e'
        else:
            break
    
        
#This function takes as input inbox, inbox_object and email address and pickledumps inbox_object to the inbox file, updating the inbox
def update_inbox_file (inbox,inbox_object,email_address):

    #put new inbox in inbox_object
    inbox_object.box = inbox

    #write inbox object to the appropriate file    
    with open(f"inbox_{email_address}.dat", "wb") as g:                            
        pickle.dump(inbox_object,g)


#This is a login function similar to that used in the second capstone
def login():

    while True:
        #request input from user (MAKING USERNAME CASE INSENSITIVE AS PER FEEDBACK)
        email_address = input("Please enter email address:\n").lower()
        password = input ("Please enter password:\n")
    

        #open file and check username and password match those in the list
        with open("addressbook.txt","r") as f:
            text = f.read()
            text = text.split("\n")
            match = False
            for element in text:
                if (element.split(", ")[0]).lower() == email_address and element.split(", ")[1] == password:
                    match = True
                    break
            #If no match then return to top
            if match == False:
                print("\nUsername or password is incorrect. Please try again.\n")
                continue
            #Otherwise print message and proceed to menu
            else: 
                print("\nUsername and password correct!\n")
                return (email_address)

#This function registers a new user (code taken from capstone)
def reg_user (username): 
    #Check user is the admin and continue if so
    if username.lower() == "admin@slademail.com":
        #Generate a list of the lines in the file user.txt
        with open ("addressbook.txt","r+") as f:
            text = f.read()
            text = text.split("\n")
            
            #ask for username and confirm in a first nested while loop that the username is not already 
            #registered, and once this condition is met, move on to confirm the username and ensure this 
            #matches
            while True:
            
                while True:
                    user1 = input("You have selected to register a new email address. Please enter the new address in the format\n\
emailaddress@slademail.com or type 'e' to exit:\n").lower()
                    
                    #format check
                    try:
                    
                     if user1.split("@")[1] != "slademail.com":
                        print("Please enter in the correct format")
                        continue
                    except:
                        print("Please enter in the correct format")
                        continue


                    if user1 == "e":
                        return
                    existing_user = False
                    #for each line, split by ", " and compare first element (existing username), with the user1,
                    #the username the user is trying to register. break and display an error message and return to top
                    for element in text:
                        current_user = element.split(", ")[0]
                        if  current_user.lower() == user1.lower():
                            existing_user = True 
                            breakpoint                
                    if existing_user == True:
                        print ("I am sorry but this email address is already in use")
                        continue
                          
                        #request repeat username
                    user2 = input("Please confirm the email address or enter 'e' to exit:\n")
                    #check they match and if they do continue. Else return to the top of user loop
                    if user2 == "e":
                        return
                    
                    if user1.lower() != user2.lower():
                        print("I am sorry these do not match. Please try again")
                        continue

                    else:
                        print("email addresses match!")
                        
                        #ask for password and confirm
                    while True:
                        password1 = input(f"Please enter desired password for {user1} or enter 'e' to exit:\n")
                        if password1 == "e":
                            return
                        password2 = input(f"Please confirm password for {user1} or enter 'e' to exit:\n")
                        if password1 == "e":
                            return
                            #if match continue else return to the top of password loop
                        if password1 != password2:
                            print("Passwords do not match. Try again\n")
                            continue
                        else:
                            print("passwords match!")
                            # if passwords match, continue add username and password to the appropriate file
                            print(f"\n\nA new email address has been added:\nemail address: {user1}\npassword: {password1}\n")
                            f.write(f"\n{user1}, {password1}")
                            inbox_file_name = f"inbox_{user1}"
                            with open(f"{inbox_file_name}.dat", "wb+")as f:
                                user_inbox = User_inbox(f"{user1}")
                               
                                pickle.dump(user_inbox,f)

                            return
    #if user is not the admin display an error message and go back to the menu
    else:
        print("\nI am sorry but only the admin can add new users. Please contact your admin.\n")
        return

#---------------------------------------------------MAIN FUNCTION--------------------------------------------------

#This is the main function, which takes the user through some menus and performs tasks as required
def main():

    while True:
        print ("")
        #login and return the user email address
        email_address = login()
        #email_address = "eirion.slade@slademail.com"
        
        
        while True:

            #MENU 1
            user_choice = input(f"""What would you like to do? (type number next to option)

1) add user (only admin can do this)
2) open inbox
3) send email
4) clear inbox
5) log out

""")
            #---1) register new user ---
            if user_choice == "1":

                reg_user(email_address)
                continue
            #---2) open inbox
            elif user_choice == "2":

                    while True:

                        #open the user's inbox and set that equal to user_inbox
                        with open(f"inbox_{email_address}.dat","rb") as g:
                            inbox_object = pickle.load(g)
                        #inbox_object = User_inbox(email_address)
                            inbox = inbox_object.box    
                        #display message if inbox is empty and return to main menu
                        if get_count(inbox) == 0:
                            print ("\nThe inbox is empty\n")
                            break
                        #if there are messages in the inbox then display inbox and give user options 
                        else:
                            
                            print (f"\nThere are currently {get_count(inbox)} emails in your inbox:\n")
                            #inbox_text = generate_inbox_text(inbox)
                            email_num = 0
                            for email in inbox:
                                email_num +=1
                                if email.is_spam == True:
                                    spam_yes = "yes"
                                else:
                                    spam_yes = "no"
                                if email.has_been_read == True:
                                    read_yes = "yes"
                                else:
                                    read_yes = "no"
                                print (f"{email_num})   Subject: {email.subject}       From: {email.from_address}    Spam: {spam_yes}    Read: {read_yes} ")  
                            print("")
                    
                            #request input from user
                            read_choice = input(f"""Please select from the following options by typing the number of the option:

1 - read a specific email
2 - see a list of unread emails
3 - see a list of spam emails
4 - mark/unmark email as spam
5 - delete an email
6 - return to main menu
""")
                        

                        # -----------2) i) openinbox/read email --------------------
                        if read_choice == "1":
                            
                            while True:
                                #request input from user with error handling
                                try:
                                    email_number = int(input("Please enter the number of the email you would like to view:\n"))-1

                                except: 
                                    print ("\nError: Please enter an integer\n")
                                    continue

                                if email_number >=0 and email_number < get_count(inbox):
                                    #if no issues with user choice then print the email using the get_email function
                                    print(get_email(inbox,email_number))
                                    

                                    #update inbox file (as email is now marked as read)
                                    update_inbox_file (inbox,inbox_object,email_address)
                                    break
                                else:
                                    #error message
                                    print ("\nNumber selected exceed the size of the inbox. Please try again.\n")
                                    continue
                            
                            
                        #---------------2) ii) open inbox/ view list of unread emails--------------------------------------------------------
                        elif read_choice == "2":

                            #get list of unread emails
                            unread_list = get_unread_emails(inbox)
                            #if empty list
                            if unread_list == []:
                                print ("\nThere are no unread emails in your inbox\n")
                            #print list in user friendly format

                            else:
                                count = 0
                                print("\nUnread emails:\n")
                                for email in unread_list:
                                    count +=1
                                    
                                    print (f"{count}) Subject: {email.subject}           From: {email.from_address} ") 

                                print("")
                            
                        #-------------------2) iii) open inbox/read list of spam emails -----------------------------

                        elif read_choice == "3":
                            #get spam list
                            spam_list = get_spam_emails(inbox)
                            #empty spam list
                            if spam_list == []:
                                print ("\nThere are no spam emails in your inbox\n")
                            #else print emails in user-friendly format
                            else:
                                count = 0
                                print("\nSpam emails:\n")
                                for email in spam_list:
                                    count +=1
                                    
                                    print (f"{count}) Subject: {email.subject}           From: {email.from_address} ") 


                        #---2) iv) open inbox/ mark as spam---------

                        elif read_choice == "4":

                            while True:
                            #request input
                                try:
                                    spam_target_num = int(input(f"There are {get_count(inbox)} emails in the inbox.\n\
Please enter the number of the email you would like to change spam setting: "))-1
                                except: 
                                    print ("\nError: please enter an integer\n")
                                    continue

                                #check in range
                                if spam_target_num>=0 and spam_target_num < get_count(inbox):
                                    email = inbox[spam_target_num]
                                    #if email is spam, tell this to user and give option to unmark
                                    if email.is_spam == True:
                                        while True:
                                            unmark = input("\nThis email is marked as spam. Would you like to unmark it? 1) Yes 2) No\n")
                                            if unmark == "1":
                                                email.is_spam = False
                                                print("\nemail unmarked as spam\n")
                                                break
                                            elif unmark == "2":
                                                print("\nemail kept as spam\n")
                                                break
                                            else:
                                                print ("\nError: please enter 1 or 2.\n") 
                                    
                                    #if email is not spam give option to mark as spam
                                    else:
                                        while True:
                                            mark = input("\nThis email is not marked as spam. Would you like to mark it? 1) Yes 2) No\n")
                                            if mark == "1":
                                                email.mark_as_spam()
                                                print("\nemail marked as spam\n")
                                                break
                                            elif mark == "2":
                                                print("\nemail kept as not spam\n")
                                                break
                                            else:
                                                print ("\nError: please enter 1 or 2.\n") 

                                        
                                    #update the inbox file
                                    inbox[spam_target_num] = email
                                    update_inbox_file (inbox,inbox_object,email_address)
                                    break
                                #error message
                                else:
                                    print ("\nNumber selected exceeds size of inbox. Please try again.\n")
                                    continue
                        
                        #---2) v) open inbox/delete email---

                        elif read_choice == "5":

                            #delete email and update inbox file
                            delete_email(inbox)                            
                            update_inbox_file(inbox,inbox_object,email_address)

                        #---2 vi) open inbox/go back to main menu
                        elif read_choice == "6":
                            print ("")
                            break
                        else:
                            print("I am sorry there has been a problem. Please enter 1,2,3,4,5 or 6:\n")

                            continue


            #---3) send email---
            elif user_choice == "3":

                #send email
                send_email(email_address)


            #---4) clear inbox---
            elif user_choice == "4":
                #load inbox
                with open(f"inbox_{email_address}.dat","rb") as g:
                    inbox_object = pickle.load(g)
                

                #confirm user wants to clear the whole inbox
                while True:

                    sure = input(f"""Are you sure you wish to clear the whole inbox?
                    
1) Yes
2) No

""")
                    #if sure, then turn inbox_object.box into an empty list
                    if sure == "1":
                        inbox_object.box = []
                        #dump the empty inbox in the correct data file
                        with open (f"inbox_{email_address}.dat","wb") as g:
                            pickle.dump(inbox_object,g)
                            print ("\nInbox cleared\n")
                        break
                    #else do nothing and return to main menu
                    elif sure == "2":
                        print()
                        break
                    #error message for incorrect input
                    else:
                        print("\nI am sorry that was an incorrect selection. Please try again.\n")
                        continue
            #---5) log out---              
            elif user_choice == "5":
                print ("\nLogging out...\n")
                break

            #input error message for the main menu
            else:
                print ("Error: Please enter 1,2,3,4 or 5")
                continue
            

main()