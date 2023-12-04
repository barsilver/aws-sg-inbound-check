## Table of contents
* [About](#about)
* [Flags](#flags)
* [Usage](#usage)

# About
The aws-sg-inbound-check.py is a python script which iterates over all of the VPCs in the specified AWS account and checks if there is any `0.0.0.0/0` inbound rule configured in the security groups.

All of the marked for deletion rule IDs are printed to the log.txt file during the run and will be uploaded to the specified S3 bucket at the end of it. 

# Flags
This script should be executed with a few flags:
* `--bucket-name` - (Mandatory) Indicates to which bucket would you like to upload the log.txt file.
* `--profile-name` - (Optional) The default of this parameter is set to the `default` AWS profile name in your terminal. If you don't have your AWS profiles set, make sure to add them before running the script with `aws configure`.
* `--log-mode` - (Optional) This parameter should be used for dry run. No rule will be deleted in the account.

If you choose to run the command without the flags, the parameters will be prompted and you won't be able to run the script in log mode.

# Usage

```
python3 aws-sg-inbound-check.py --log-mode --bucket-name <bucket> --profile-name <aws_profile_name>
```

```
$ python3 aws-sg-inbound-check.py
Bucket name: <bucket>
Profile name [default]:
```
