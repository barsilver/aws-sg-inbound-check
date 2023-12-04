import boto3
import logging
import click
from botocore.exceptions import ClientError
 
@click.command()
@click.option('--log-mode', is_flag=True)
@click.option('--bucket-name', required=True, type=str, prompt=True)
@click.option('--profile-name', type=str, prompt=True, default='default')

def main(log_mode, bucket_name, profile_name):
    session = boto3.session.Session(profile_name=profile_name)

    ec2_client = session.client('ec2')
    s3_client = session.client('s3')

    logging.basicConfig(
        filename='log.txt',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    vpcs = ec2_client.describe_vpcs(
        Filters=[
            {'Name':'tag:Name', 'Values':['*']}
        ]
    )
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
            logging.info('%s contains 0.0.0.0/0 inboud rule', sg_id)

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
                    logging.warning('Delete rule ID for 0.0.0.0/0 inbound rule in %s: %s', sg_id, rule_id)
                    #ec2_client.revoke_security_group_ingress(
                        #GroupId = sg_id,
                        #SecurityGroupRuleIds = [rule_id]
                    #)

        # Upload the log file to S3 bucket.
        try:
            res = s3_client.upload_file('log.txt', bucket_name, 'log.txt')
        except ClientError as e:
            logging.error('Error uploading file to S3: %s', e)
            return False
        return True

    click.echo('Script finished successfully.')
    return True



if __name__ == '__main__':
    main()
        