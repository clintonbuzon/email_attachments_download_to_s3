import json
import imaplib
import base64
import os
import email
import boto3
import time

# Please only update parameters below
### Start parameter list ####
EMAIL_USER = 'cbuzon@alumni.ateneo.edu'
EMAIL_PASS = 'xxxxxxxxxx'
EMAIL_IMAP_HOST = 'imap.gmail.com'
EMAIL_IMAP_PORT = '993'
BUCKET_NAME='clinton-simple-datalake'
### End parameter list ####

def lambda_handler(event, context):
    
    # temporary directory on lambda to store downloaded attachments
    dirName = '/tmp'
    
    # create s3 client
    s3 = boto3.client('s3')
    
    # list containing existing s3 items, to be used later
    bucket_items = []                                                                               
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    if 'Contents' in response:
        for obj in response['Contents']:
            bucket_items.append(obj['Key'])

    # for logging purposes
    print("Printing existing s3 items:")
    print(bucket_items)

    # initialize mail code
    mail = imaplib.IMAP4_SSL(EMAIL_IMAP_HOST,EMAIL_IMAP_PORT)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select('Inbox')
    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()

    # scan mail items
    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)' )
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        # downloading attachments
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()
            if bool(fileName) and (fileName not in bucket_items): # only download files which does not exist on s3
                filePath = os.path.join(dirName+'/', fileName)
                if not os.path.isfile(filePath) :
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()

    # for logging purposes
    file_list_to_upload = os.listdir(dirName)
    print("Printing items to upload to s3:")
    print(file_list_to_upload)

    # upload files to s3
    for file in file_list_to_upload:
	    file_full_path = dirName + '/' + file
	    s3.upload_file(file_full_path, BUCKET_NAME, file)
	    os.remove(os.path.join(dirName, file)) # file cleanup

    return {
        'statusCode': 200,
        'body': json.dumps('Job completed successfully')
    }
