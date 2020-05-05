import sys
from mcipc.rcon import Client as CRcon
from time import sleep
import paramiko

class mcManage:
    def __init__(self, ip, port, VPSpasswd):
        #information about current server
        self.status = False
        self.max = 0
        self.online = 0
        self.ip = ip
        self.port = port
        self.login = 'root'

        #current virtual server
        self.VPSUser = 'root'
        self.VPSpasswd = VPSpasswd
        self.VPSport = 22

    def command(self, command):
        #   Run rcon command
        with CRcon(self.ip, self.port) as rcon:
            rcon.login(self.login)
            message = rcon.run(command)
        return message

    def runServer(self):
        # Run server
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.ip, self.VPSport, self.VPSUser, self.VPSpasswd)
            stdin, stdout, stderr = client.exec_command('cd /home/MC;sh start.sh', get_pty=True)
            sleep(10)
            client.close()
        except Exception as e:
            return (e)

    def closeServer(self):
        # Closing the server
        try:
            cmd = 'stop'
            message = self.command(cmd)
            return message
        except Exception:
            return "Serwer jest aktualnie wylaczony"

    def stats(self):
        #  Server stats
        try:
            with CRcon(self.ip, self.port) as rcon:
                rcon.login(self.login)
                self.status = True
                self.max = rcon.players.max
                self.online = rcon.players.online
        except Exception as e:
            self.stats = False
            return

    def kick(self, nickname, reasonse):
        #   Kick the player
        cmd = 'kick {} {}'.format(nickname, reasonse)
        self.command(cmd)

    def giveItemsToPlayer(self, nickname, item, value):
        #   Give items for player
        cmd = 'give {} minecraft:{} {}'.format(nickname, item, value)
        self.command(cmd)

    def teleportPlayer(self, nickname, target):
        #   Teleport player somewhere
        cmd = 'tp {} {}'.format(nickname, target)
        self.command(cmd)

    def getPlayerCords(self, nickname):
        #  Return player cords
        cmd = 'data get entity {} Pos'.format(nickname)
        cords = self.command(cmd)
        return cords

    def getPlayerMoney(self, nickname):
        # Give money for player
        cmd = 'gmoney {}'.format(nickname)
        money = self.command(cmd)
        money = 'Money: {}'.format(money[36:])
        return money

    def downloadLogs(self):
        # Download last log from .log file
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.ip, self.VPSport, self.VPSUser, self.VPSpasswd)
        stdin, stdout, stderr = client.exec_command('cat /home/MC/logs/latest.log ', get_pty=True)
        sleep(0.5)
        net_dump = stdout.readlines()
        sleep(0.5)
        client.close()
        return  net_dump[len(net_dump)-1]
