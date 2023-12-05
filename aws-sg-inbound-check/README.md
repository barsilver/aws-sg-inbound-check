## Table of contents
* [About](#about)
* [Flags](#flags)
* [Workflow](#workflow)
* [Usage](#usage)


# About
The aws-sg-inbound-check.py is a python script which iterates over all of the VPCs in the specified AWS account and checks if there is any `0.0.0.0/0` inbound rule configured in the Security Groups.

All of the Security Groups IDs which contains these inbound rules are printed to the log.txt file during the run and will be uploaded to the specified S3 bucket. 

# Flags
This script should be executed with a few flags:
* `--bucket-name` - (Mandatory) Indicates to which bucket would you like to upload the log.txt file.
* `--profile-name` - (Optional) If you don't have your AWS profiles set, make sure to configure them before running the script with `aws configure`.
* `--log-mode` - (Optional) This parameter should be used for dry run. No rule will be deleted in the account.
* `--access-key` - (Optional) AWS access key ID. Must be set with the --secret-key flag.
* `--secret-key` - (Optional) AWS secret access key. Must be set with the --access-key flag.
* `--session-token` - (Optional) AWS session token. The session token cannot be used without the --access-key and the --secret-key flags, but you can still use both the access key and the secret key without the session token.

If you choose to run the command without the authentication flags above (`--profile-name`, `--access-key`, `--secret-key`), the script would be using the IAM permissions configured locally (default profile, IAM Role connected to the machine, etc.).

# Workflow
The GitHub workflow build the docker image and then push it to the `barsilver/aws-sg-inbound-check` Docker Hub repo every day at 6am and each time a commit is pushed to the `master` branch.

# Usage

Example 1:
```
python3 aws-sg-inbound-check.py --log-mode --bucket-name <bucket> --profile-name <aws_profile_name>
```
Example 2:
```
python3 aws-sg-inbound-check.py --log-mode --bucket-name <bucket> --access-key <aws_access_key_id> --secret-key <aws_secret_access_key>
```
Example 3:
```
python3 aws-sg-inbound-check.py --log-mode --bucket-name <bucket>
```

