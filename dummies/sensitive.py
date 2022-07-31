"""Module to store sensitive information such as passwords

Restart the container after editing this file
docker stop <container_name> && docker start <container_name>
"""

# email configurations. These can be empty strings if you do not wish to send e-mails. The send_mail variable should be set to False (in config.py)
smtp_server = ''
sender_email = ''  # address from where the e-mail should be sent
port = None  # should be integer. Intentionally set as None

account = ''  # to login  on SMTP server
pwd = '' # corresponding password

# add jobs you do not wish to remove from your docker instance to the variable below
persistent_jobs = (

                   )
