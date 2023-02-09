
# Capstone Project: Internal Mail System: slademail.com

## Table of contents

### Section1: Project Description 
### Section 2: Installation Section
### Section 3: Usage Section
### Section 4: Credits


## Section 1: Project Description

<p>This software is an internal email system "@slademail.com". There are a number of existing users, and new users can be added by an admin account<p>

## Section 2: Installation Section

<p>This programme is made up of a single python file email.py, a txt file addressbook.txt and a number of text files: inbox_emailaddress@slademail.com.dat.<br>
These correspond to inboxes of the email addresses in addressbooo.txt. Simply download all these files into a single folder to install.<p>

## Section 3: Usage Section

<p>The file addressbook.txt contains a number of lines of text. These are the email address of a user followed by ", " and then the password.<br>
email.py accesses this file when the user logs in so it is important it is kept in this format.<br>
the inbox files are .dat files containing an inbox object made up of the email address and a list of email objects. email.txt uses pickle to write<br>
these objects directly to this file. They can only be edited through email.py.

<p>email.py when run will give the user a menu of options:<br>
       1) add new user (only admin)<br>
       2) open inbox<br>
    i) read specific email<br>
    ii) see a list of unread emails<br>
    iii) see a list of spam emails <br>
    iv) mark/unmark as spam <br>
    v) delete an email <br>
    vi) return to main menu <br>
3) send email<br>
4) clear inbox<br>
5) log out<br>
        7) exit<br><p>
<p>The user can access these options by typing in the number next to the menu option.<p>

## Section 4: Credits

<p>Eirion Slade<p>

