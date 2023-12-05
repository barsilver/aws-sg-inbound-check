import boto3
import logging
import click
from botocore.exceptions import ClientError
 
@click.command()
@click.option('--log-mode', is_flag=True)
@click.option('--bucket-name', required=True, type=str)
@click.option('--profile-name', type=str)
@click.option('--access-key', type=str)
@click.option('--secret-key', type=str)


def main(log_mode, bucket_name, profile_name, access_key, secret_key):

    # Configure the logger for file output
    file_logger = logging.getLogger('file_logger')
    file_logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler('log.txt')
    file_handler.setFormatter(formatter)
    file_logger.addHandler(file_handler)

    # Configure the logger for console output
    console_logger = logging.getLogger("console_logger")
    console_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_logger.addHandler(console_handler)

    if access_key and secret_key:
        console_logger.info('Logging in using Access key pair...')
        try:
            session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key
            )
            ec2_client = session.client('ec2')
            s3_client = session.client('s3')
        except ClientError as e:
            console_logger.error('Authentication Error: %s', e)
            return False

    elif profile_name:
        try:
            console_logger.info('Logging in using AWS Profile...')
            session = boto3.session.Session(profile_name=profile_name)
            ec2_client = session.client('ec2')
            s3_client = session.client('s3')
        except ClientError as e:
            console_logger.error('Authentication Error: %s', e)
            return False

    else:
        try:
            console_logger.info('No key pair or profile provided. Logging in using IAM role...')
            ec2_client = boto3.client('ec2')
            s3_client = boto3.client('s3')
        except ClientError as e:
            console_logger.error('Authentication Error: %s', e)
            return False

    console_logger.info('Successfully authenticated. Proceeding to describe VPCs in order to get Security Groups.')

    try:
        vpcs = ec2_client.describe_vpcs(
            Filters=[
                {'Name':'tag:Name', 'Values':['*']}
            ]
        )
    except ClientError as e:
        console_logger.error('Error describing VPCs: %s', e)
        return False

    for vpc in vpcs['Vpcs']:
        vpc_id = vpc['VpcId']
        security_groups = ec2_client.describe_security_groups(
            Filters=[
                {'Name': 'vpc-id', 'Values': [vpc_id]},
                {'Name': 'ip-permission.cidr', 'Values': ['0.0.0.0/0']}
            ]
        )
        for sg in security_groups['SecurityGroups']:
            sg_id = sg['GroupId']
            # Log the security group to the log.txt file.
            file_logger.info('%s contains 0.0.0.0/0 inboud rule', sg_id)

            inbound_rules = ec2_client.describe_security_group_rules(
                Filters=[
                    {'Name': 'group-id', 'Values': [sg_id]}
                ]
            )
        
            matching_rules = [
                rule['SecurityGroupRuleId']
                for rule in inbound_rules['SecurityGroupRules']
                if rule.get('CidrIpv4') == '0.0.0.0/0' and not rule.get('IsEgress', False)
            ]

            # Delete the rule from the inbound rules.
            if not log_mode:
                for rule_id in matching_rules:
                    try:
                        ec2_client.revoke_security_group_ingress(
                            GroupId=sg_id,
                            SecurityGroupRuleIds=[rule_id]
                        )
                        console_logger.info('Successfully deleted rule ID %s in security group %s', rule_id, sg_id)
                    except ClientError as e:
                        console_logger.error('Error deleting rule ID %s in security group %s: %s', rule_id, sg_id, e)

    # Upload the log file to S3 bucket.
    try:
        res = s3_client.upload_file('log.txt', bucket_name, 'log.txt')
    except ClientError as e:
        console_logger.error('Error uploading file to S3: %s', e)
        return False

    console_logger.info('Script finished successfully.')
    return True



if __name__ == '__main__':
    main()
        