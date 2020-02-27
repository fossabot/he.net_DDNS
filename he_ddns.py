#!/usr/bin/python3
import requests
import socket
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

url = "https://dyn.dns.he.net/nic/update"
password = "PASSWORD"

rootDomain = "<ROOT-DOMAIN>"


def to_hex(data):
    import binascii
    hex = binascii.hexlify(data.encode('utf-8'))
    return hex.decode('utf-8')


subDomain = "<SUBDOMAIN>"


def get_public_ipv4():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipaddr = s.getsockname()[0]
    s.close()
    return ipaddr


def get_public_ipv6():
    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    s.connect(("2001:4860:4860::8888", 80))
    ipaddr = s.getsockname()[0]
    s.close()
    return ipaddr


def getHostname():
    return socket.gethostname()


def post_address_v4(hostname, password, ip):
    datav4 = {
        'hostname': hostname,
        'password': password,
        'myip': ip
    }
    response = requests.post(url, data=datav4)
    if response.status_code == 200:
        return True
    else:
        return False


def post_address_v6(hostname, password, ip):
    datav6 = {
        'hostname': hostname,
        'password': password,
        'myip': ip
    }
    response = requests.post(url, data=datav6)
    if response.status_code == 200:
        return True
    else:
        return False


machineName = getHostname()

hostname = machineName + "." + subDomain + "." + rootDomain

ipv4Address = get_public_ipv4()
ipv6Address = get_public_ipv6()

if ipv4Address == ipv6Address:
    if post_address_v4(hostname, password, ipv4Address):
        logger.info("ipv4 only, posted ok")
    else:
        logger.debug("ipv4 only, posted bad")
else:
    if post_address_v4(hostname, password, ipv4Address):
        logger.info("ipv4, posted ok")
    else:
        logger.info("ipv4, posted bad")
    if post_address_v6(hostname, password, ipv6Address):
        logger.info("ipv6, posted ok")
    else:
        logger.info("ipv6, posted bad")
