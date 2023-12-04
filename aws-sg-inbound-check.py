import boto3
import logging
import click
 
@click.command()
@click.option('--log-mode', is_flag=True)

def main(log_mode):
    ec2_client = boto3.client('ec2')
    logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

 
    vpcs = ec2_client.describe_vpcs(Filters=[{'Name':'tag:Name', 'Values':['*']}])['Vpcs']
    for vpc in vpcs:
        vpc_id = vpc['VpcId']
        security_groups = ec2_client.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}, {'Name': 'ip-permission.cidr', 'Values': ['0.0.0.0/0']}])
        for sg in security_groups['SecurityGroups']:
            sg_id = sg['GroupId']
            # Log the security group to the log.txt file
            logging.warning('%s contains 0.0.0.0/0 inboud rule', sg_id)
            # Delete the rule from the inbound rules
            if not log_mode:
                logging.info('log mode is set to false')



if __name__ == '__main__':
    main()
        