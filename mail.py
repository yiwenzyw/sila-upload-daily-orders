# Make sure you have valid network connection and IMAP enabled in your gmail settings.
# Make sure you have turned on the less secure mode https://myaccount.google.com/lesssecureapps
# The script not able to download the same filename twice even if their contents are different.
import email
import getpass
import imaplib
import os
import sys
import datetime

# if folder 'template' does not exist create a 'template 'folder on desktop
upload_folder = '.'
if 'template' not in os.listdir(upload_folder):
    os.mkdir('template')
# input gmail address and password
mail_address = raw_input('Enter your Gmail address :')
mail_pwd = getpass.getpass('Enter your password: ')
#date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
# get today's date
date = (datetime.date.today()).strftime("%d-%b-%Y")
# establish a connection to an IMAP4 server
imap_service = imaplib.IMAP4_SSL('imap.gmail.com',993)

#result, accountDetails = imap_service.login(mail_address, mail_pwd)
#print(result)

try:
    # parse the login credentials
    result, accountDetails = imap_service.login(mail_address, mail_pwd)
    if result == 'OK':
        print 'Login OK!'

except imaplib.IMAP4.error:
    print "Unable to login to: " + mail_address + ". Account not verified\n"

else:
    try:
        # Limit by today's date, search for a subject and sender from 'yiwen@yojee.com'
        imap_service.select('[Gmail]/All Mail')
        result, data = imap_service.search(
            None, '(SENTSINCE {date} FROM "yiwentest123@gmail.com" SUBJECT "YOJEE TASK - Container")'.format(date=date))
        if result == 'OK':
            print 'Search OK!\n'

        for msgId in data[0].split():
            result, messageParts = imap_service.fetch(msgId, '(RFC822)')
            # fetch the email body (RFC 822) from the given ID
            # here's the body, which is raw text of the whole email
            # including headers and alternate payloads
            emailBody = messageParts[0][1]
            mail = email.message_from_string(emailBody)
            subject = mail['subject']
            if result == 'OK':
                print 'Subject Found:' + subject

            # Body details
            for part in mail.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                # print part.as_string()
                if part.get('Content-Disposition') is None:
                    continue
                # print part.as_string()
                fileName = part.get_filename()

                if bool(fileName):
                    filePath = os.path.join(upload_folder, 'template', fileName)
                    if os.path.isfile(filePath):
                        print 'Download Failed!!! Same filename already exists\n'
                    if not os.path.isfile(filePath):
                        print 'CSV downloaded successfully: ' + fileName + '\n'
                        fp = open(filePath, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()
        imap_service.close()
        imap_service.logout()

    except imaplib.IMAP4.error:
        print 'Unable to fetch attachments!'
