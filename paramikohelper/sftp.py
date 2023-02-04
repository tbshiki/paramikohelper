import paramiko


def ssh_connect(hostname: str, portnumber: int, username: str, key_path: str, passphrase: str = "", timeout: int = 10, auth_timeout: int = 30):

    """ Connect to the server via SSH

    Sample code:
        With paramikohelper.ssh_connect(hostname, portnumber, username, key_path, passphrase, timeout, auth_timeout) as client
            with client.open_sftp() as sftp:
                for img in dimg_list:
                    remotepath = remotedir + img  # upload to the remote path
                    localpath = localdir + img  # local img path
                    sftp.put(remotepath=remotepath, localpath=localpath)  # upload

    Args:
        hostname (str): Host name of the server to connect to
        portnumber (int): Port number of the server to connect to
        username (str): User name of the server to connect to
        key_path (str): Authentication key path of the server to connect to
        passphrase (str, optional): Passphrase for the authentication key oh the server to connect to. Defaults to "".
        timeout (int, optional): Timeout time of the connection. Defaults to 10.
        auth_timeout (int, optional): Aauthentication timeout time of the connection. Defaults to 30.

    Returns:
        SSHClient: SSHClient object

    """

    if passphrase != "":  # パスフレーズがある場合
        rsakey = paramiko.RSAKey.from_private_key_file(key_path, passphrase)
    else:  # パスフレーズがない場合
        rsakey = paramiko.RSAKey.from_private_key_file(key_path)

    client = paramiko.client.SSHClient()  # SSHClientオブジェクトを作成
    client.load_system_host_keys()  # host_keysを読み込み
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())  # host_keysがない場合は自動で追加するように設定
    try:
        client.connect(hostname=hostname, port=portnumber, username=username, pkey=rsakey, timeout=timeout, auth_timeout=auth_timeout)
    except:

        raise Exception("Exception raised when authentication failed for some reason")  # 認証に失敗したのでErrorを返す

    return client
