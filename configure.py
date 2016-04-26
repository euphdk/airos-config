#!/usr/bin/env python

from argparse import ArgumentParser

import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException, BadHostKeyException

from scp import SCPClient

import time
import re

def main(host=None, username=None, password=None, hostname=None, ipaddress=None):

    final_config = []

    with open('system.cfg') as f:
        config = f.read().splitlines()

    for line in config:

        if re.match(r'^resolv.host.1.name=.*', line):
            line = 'resolv.host.1.name=%s' % hostname

        if re.match(r'^netconf.3.ip=.*', line):
            line = 'netconf.3.ip=%s' % ipaddress


        print line;


        final_config.append(line)

    with open('temp-system.cfg', 'w') as outfile:
        outfile.write("\n".join(final_config))


    try:
        ssh = paramiko.SSHClient()
        #ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)

        with SCPClient(ssh.get_transport()) as scp:
            scp.put('temp-system.cfg', '/tmp/system.cfg')

        ssh.exec_command('cfgmtd -f /tmp/system.cfg -w')
        time.sleep(5)
        ssh.exec_command('reboot')

    except AuthenticationException:
        print("Authentication failed, please verify your credentials: %s")
    except SSHException as sshException:
        print("Unable to establish SSH connection: %s" % sshException)
    except BadHostKeyException as badHostKeyException:
        print("Unable to verify server's host key: %s" % badHostKeyException)
    except Exception as e:
        print("Operation error: %s" % e)




if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        action='store',
        dest='host',
        help='The address of your device.',
    )
    parser.add_argument(
        action='store',
        dest='hostname',
        help='The hostname you want to configure.',
    )
    parser.add_argument(
        action='store',
        dest='ipaddress',
        help='IP adress.',
    )
    parser.add_argument(
        '-u', '--username',
        action='store',
        default='ubnt',
        dest='username',
        help='The username. Default \'ubnt\'.',
    )
    parser.add_argument(
        '-p', '--password',
        action='store',
        default='ubnt',
        dest='password',
        help='The password. Default \'ubnt\'.',
    )

    args = parser.parse_args()
    main(host=args.host, username=args.username, password=args.password, hostname=args.hostname, ipaddress=args.ipaddress)
