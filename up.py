import boto3


def get_all_instances():
    """
    Filter stopped instances by a tag.
    :return: Return array instances id
    """
    try:
        client = boto3.client('ec2')
        custom_filter = [{
            'Name': 'tag:start',
            'Values': ['true']}, {
            'Name': 'instance-state-name',
            'Values': ['stopped']}]
        response = client.describe_instances(Filters=custom_filter)
        turn_ons = []
        reservations = response.get('Reservations') if response else []
        for res in reservations:
            for item in res.get('Instances'):
                instance = item.get('InstanceId')
                turn_ons.append(instance)
        print(turn_ons)
        return turn_ons
    except Exception as ex0:
        print(ex0)

def turn_on(instances):
    """
    Start instances
    :param instances:
    :return:
    """
    try:
        my_session = boto3.Session()
        region = my_session.region_name
        ec2 = boto3.client('ec2', region_name=region)
        ec2.start_instances(InstanceIds=instances)
        print('Instances started: ' + str(instances))
    except Exception as ex1:
        print(ex1)

def run(event, context):
    print("Getting instances ..")
    instances = get_all_instances()
    print(f"Count: {len(instances) if instances else 0}")
    if instances and len(instances) > 0:
        print("Starting instances")
        turn_on(instances)
    else:
        print("No instances to start")
