# get instance information cross account

import boto3

# create an STS client object that represents a live connection to the
# STS service
sts_client = boto3.client('sts')

def get_instance_name(ec2i):
    # When given an instance ID as str e.g. 'i-1234567', return the instance 'Name' from the name tag.
    instancename = ''
    for tags in ec2i.tags:
        if tags["Key"] == 'Name':
            instancename = tags["Value"]
    return instancename

def get_apptag(ec2i):
    # When given an instance ID as str e.g. 'i-1234567', return the value from the tag "curtin:application-name"
    instanceapptag = ''
    for tags in ec2i.tags:
        if tags["Key"] == "curtin:application-name":
            instanceapptag = tags["Value"]
    return instanceapptag

def get_inst_data():
    for instance in ec2_resource.instances.all():
        name=get_instance_name(instance)
        apptag=get_apptag(instance)
        print(f"{id},{instance.id},{name},{apptag},{instance.platform},{instance.instance_type},{instance.private_ip_address},{instance.image.id},{instance.state['Name']}")

# Call the assume_role method of the STSConnection object and pass the role
# ARN and a role session name.   aws sts assume-role --role-arn arn:aws:iam::428647151701:role/migrationfactory-role --role-session-name ec2-access

accounts = ['941266839542', '678931622771', '778356832056', '774669145013', '654918544985', '863274835299', '501209436976', '715438014192', '754432650346', '913026610106', '940120191464', '282948852859', '358418149203', '023074252191', '313157802381', '015803628719',]
sts_client = boto3.client('sts') #assumes you have a default profile set
for id in accounts:
    assumed_role_object=sts_client.assume_role(
    RoleArn=f"arn:aws:iam::{id}:role/migrationfactory-role",
    RoleSessionName="AssumeRoleSession1"
    )
    credentials=assumed_role_object['Credentials']
    ec2_resource=boto3.resource(
        'ec2',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )
    get_inst_data()