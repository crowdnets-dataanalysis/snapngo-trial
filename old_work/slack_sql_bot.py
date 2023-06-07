import os
from sshtunnel import SSHTunnelForwarder
import pymysql
import slack
from slack_bolt.adapter.socket_mode import SocketModeHandler
from bot import *

ssh_host = 'cs.wellesley.edu'
ssh_user = 'crowdnets'
ssh_key_path = '../settings/crowdnets-ssh'


server = SSHTunnelForwarder(
    (ssh_host, 22),
    ssh_username=ssh_user,
    ssh_private_key=ssh_key_path,
    remote_bind_address=('localhost', 3306)
)

server.start()

db_user = 'crowdnets'
db_password = 'your_database_password'
db_name = 'crowdnets_db'

connection = pymysql.connect(
    host='localhost',
    user=db_user,
    password=db_password,
    db=db_name,
    port=server.local_bind_port
)