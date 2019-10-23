# email_attachments_download_to_s3

Sample lambda (python 3.6) script which would scan an email address and download all attachments. Attachments would then be uploaded to an AWS S3 bucket.

Note: current code is only applicable for email addresses which can be accessed via IMAP

### Lambda setup needed

+ Attached role on lambda function must have write access to S3
    + Reference `<link>` : https://aws.amazon.com/premiumsupport/knowledge-center/lambda-execution-role-s3-bucket/
+ Timeout settings must be increased from the default 3 seconds
    + 1 minute would be fine
    
### Parameters to modify

    EMAIL_USER = 'cbuzon@alumni.ateneo.edu'
    EMAIL_PASS = 'xxxxxxxxxx'
    EMAIL_IMAP_HOST = 'imap.gmail.com'
    EMAIL_IMAP_PORT = '993'
    BUCKET_NAME='clinton-simple-datalake'
