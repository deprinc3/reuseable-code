import boto3

import json


def lambda_handler(event, context):

    secret_name = "RedShiftCluster-Tableau-Creds"  # Replace with your Redshift secret name

    redshift_cluster_id = "tableau-redshift-cluster"  # Replace with your Redshift cluster ID



    # Create a Secrets Manager client

    session = boto3.session.Session()

    client = session.client(service_name='secretsmanager')



    try:

        # Get the current secret value
        print("getting_secret_value")
        get_secret_response = client.get_secret_value(SecretId=secret_name)

        print(get_secret_response)

        # Parse the secret JSON and extract the database username and password

        secret = json.loads(get_secret_response['SecretString'])

        username = secret['username']

        #password = secret['password']
        #password="A68u9lddf"



        # Generate new credentials (e.g., password) for your Redshift cluster

        new_password = generate_new_password()  # Implement your password generation logic
        print("new_password"+new_password)


    #     # Update the Redshift secret with the new password

        new_secret_value = {

            'username': username,

            'password': new_password

        }
        print("putting_secreat_value")
        put_value_response = client.put_secret_value(SecretId=secret_name, SecretString=json.dumps(new_secret_value))
        print(put_value_response)

        # Update the Redshift cluster with the new credentials

        redshift_client = session.client(service_name='redshift')
        print("cluster_modification_using_secreat_value")
        modify_cluster_response = redshift_client.modify_cluster(ClusterIdentifier=redshift_cluster_id , MasterUserPassword=new_password)
        print(modify_cluster_response)


        return {

            'statusCode': 200,

            'body': json.dumps('Secret rotation successful')

        }



    except Exception as e:

        return {

            'statusCode': 500,

            'body': json.dumps(f'Error: {str(e)}')

        }



def generate_new_password():

    # Implement your password generation logic here

    # You can use libraries like random, string, etc. to generate a secure password

    # For example, you can generate a random password of a certain length

    import random

    import string



    password_length = 30

    #characters = string.ascii_letters + string.digits + string.punctuation
    characters = string.ascii_letters + string.digits

    new_password = ''.join(random.choice(characters) for _ in range(password_length))



    return new_password