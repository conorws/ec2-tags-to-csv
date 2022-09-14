#!/usr/bin/env python
# run tag-to-csv across multiple accounts
import boto3
import botocore
import argparse
import csv

# parse command line argumetns
def parse_args():
    parser = argparse.ArgumentParser(prog='tags-to-csv', description='Get instance tags in CSV format.')
    # required
    parser.add_argument('-o', '--out', required=True, action='store', dest='output_file', type=str, help='path to where the output should be written')

    # optional
    parser.add_argument('-r', '--region',action='store', default='ap-southeast-2', dest='aws_region', type=str, help='AWS region to use.')
    parser.add_argument('-v', '--version', action='version', version='0.2')

    args = parser.parse_args()
    return args

def get_instances(filters=[]):
    reservations = {}
    try:
        reservations = ec2.describe_instances(
            Filters=filters
        )
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])

    instances = []
    for reservation in reservations.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            instances.append(instance)
    return instances



#
# Main
#
def main():
    global args
    global ec2

    accounts = ['941266839542', '678931622771', '778356832056', '774669145013', '654918544985', '863274835299', '501209436976', '715438014192', '754432650346', '913026610106', '940120191464', '282948852859', '358418149203', '023074252191', '313157802381', '015803628719',]
    sts_client = boto3.client('sts')
    args = parse_args()
    
    for id in accounts:
        assumed_role_object=sts_client.assume_role(
        RoleArn=f"arn:aws:iam::{id}:role/migrationfactory-role",
        RoleSessionName="AssumeRoleSession1"
        )
        credentials=assumed_role_object['Credentials']
        ec2=boto3.resource(
            'ec2',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
        )
        instances = get_instances() 

        tag_set = []
        for instance in instances:
            for tag in instance.get('Tags', []):
                if tag.get('Key'):
                    tag_set.append(tag.get('Key'))
        tag_set = list(set(tag_set))

        with open(args.output_file, 'w') as csvfile:
            fieldnames = ['InstanceId'] + tag_set
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for instance in instances:
                row = {}
                for tag in instance.get('Tags', []):
                    row[tag.get('Key')] = tag.get('Value')
                row['InstanceId'] = instance.get('InstanceId')
                writer.writerow(row) 

if __name__ == "__main__":
    main()