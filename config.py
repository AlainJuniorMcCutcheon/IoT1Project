AWS_PORT = 8883
AWS_HOST = 'a17bc253rtr4pb-ats.iot.us-east-1.amazonaws.com'
AWS_ROOT_CA = '/home/joeyk/Final_Project/IoT1Project/certs/aws_root.pem'
AWS_CLIENT_CERT = '/home/joeyk/Final_Project/IoT1Project/certs/aws_client.crt'
AWS_PRIVATE_KEY = '/home/joeyk/Final_Project/IoT1Project/certs/aws_private.key'

################## Subscribe / Publish client #################
CLIENT_ID = 'fromPi'
TOPIC = 'house/frontdoor/alarm'
OFFLINE_QUEUE_SIZE = -1
DRAINING_FREQ = 2
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5