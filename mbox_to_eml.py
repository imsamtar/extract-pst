import email
from email import policy
import mailbox
import os
from pathlib import Path
import sys

def has_attachments_eml(eml_file):
    with open(eml_file, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)
        for part in msg.iter_attachments():
            filename = part.get_filename()
            if filename:
                return 1
    return 0

def extract_attachments_from_eml(eml_file, attachments_dir):
    os.makedirs(attachments_dir, exist_ok=True)
    with open(eml_file, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)
        for part in msg.iter_attachments():
            filename = part.get_filename()
            if filename:
                attachment_path = Path(attachments_dir) / filename
                with open(attachment_path, 'wb') as af:
                    data = part.get_payload(decode=True)
                    if data is not None:
                        af.write(data)
                    else:
                        print(f"Skipping empty or undecodable part: {filename}")

def mbox_to_eml(mbox_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    mbox = mailbox.mbox(mbox_file)
    
    for i, message in enumerate(mbox):
        eml_path = os.path.join(output_dir, f"message_{i+1}.eml")
        with open(eml_path, 'wb') as f:
            f.write(message.as_bytes())
        if has_attachments_eml(eml_path):
            attachments = eml_path.replace(".eml", "-attachments")
            os.path.isdir(attachments) or os.makedirs(attachments)
            extract_attachments_from_eml(eml_path, attachments)

for mbox_file in Path(".").rglob("**/*.mbox"):
    output_dir = str(mbox_file).replace(".mbox", "")
    os.path.isdir(output_dir) or os.makedirs(output_dir)
    mbox_to_eml(str(mbox_file), output_dir)
