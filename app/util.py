import os

def load_config():
    mysql_uname = os.environ.get('MYSQL_USER')
    mysql_passd = os.environ.get('MYSQL_PASS')
    mysql_addr  = os.environ.get('MYSQL_ADDR')
    mysql_port  = os.environ.get('MYSQL_PORT')
    mysql_db  = os.environ.get('MYSQL_DB')
    server_addr = os.environ.get('SERVER_ADDR')
    server_port = os.environ.get('SERVER_PORT')
    debug = os.environ.get('DEBUG')

    ret = {
        "uname": mysql_uname,
        "passw": mysql_passd,
        "addr": mysql_addr,
        "port": mysql_port,
        "db": mysql_db,
        'sv_addr': server_addr,
        'sv_port': server_port,
        'debug': debug
    }

    if any(not v for v in ret.values()):
        return None
    
    return ret