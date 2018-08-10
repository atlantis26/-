# _*_coding:utf-8_*_
# __author__ = 'Alex Li'
import sys
import traceback
from models.db_handler import DatabaseHandler
import datetime
import paramiko

try:
    import interactive
except ImportError:
    from . import interactive


def ssh_login(user_obj, bind_host_obj):
    # now, connect and use paramiko Client to negotiate SSH2 across the connection
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        print('*** Connecting...')
        # client.connect(hostname, port, username, password)
        client.connect(bind_host_obj.host.ip_addr,
                       bind_host_obj.host.port,
                       bind_host_obj.remoteuser.username,
                       bind_host_obj.remoteuser.password,
                       timeout=30)
        chan = client.invoke_shell()
        print(repr(client.get_transport()))
        print('*** Here we go!\n')
        DatabaseHandler.create_audit_log(user_id=user_obj.id,
                                         bind_host_id=bind_host_obj.id,
                                         action='login',
                                         cmd="",
                                         timestamp=datetime.datetime.now())
        interactive.interactive_shell(chan, user_obj, bind_host_obj)
        chan.close()
        client.close()

    except Exception as e:
        print('*** Caught exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
        try:
            client.close()
        except:
            pass
        sys.exit(1)
