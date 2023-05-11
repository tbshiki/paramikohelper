import paramiko
import urllib
import os
from pathlib import Path


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

def upload_files(list_upload_files, dct_sftp, tmp_dir :str = str(Path(__file__).parent)):
    UPLOAD_HOSTNAME: str = dct_sftp["upload_hostname"]
    UPLOAD_PORT: int = int(dct_sftp["upload_port"])
    UPLOAD_FTPUSERNAME: str = dct_sftp["upload_ftpusername"]
    UPLOAD_PKEYSTR: str = dct_sftp["upload_pkeystr"]
    UPLOAD_PASSPHRASE: str = dct_sftp["upload_passphrase"]
    UPLOAD_REMOTEDIR: str = dct_sftp["upload_remotedir"]

    # パスフレーズをもとにパスキーを生成
    key_path = os.path.join(tmp_dir, "id_rsa")
    with open(key_path, "w") as f:
        f.write(UPLOAD_PKEYSTR)

    print(f"アップロード開始")
    remotepath_list = []
    with ssh_connect(UPLOAD_HOSTNAME, UPLOAD_PORT, UPLOAD_FTPUSERNAME, key_path, UPLOAD_PASSPHRASE) as client:
        with client.open_sftp() as sftp:
            for file in list_upload_files:
                parsed_file_name = urllib.parse.urlparse(str(file))  # ファイル名を取得するためにパース
                file_name = os.path.basename(parsed_file_name.path)  # ファイル名のみを取得
                remotepath = UPLOAD_REMOTEDIR + file_name  # アップロード先のパス(リモート)
                remotepath_list.append(remotepath) # アップロード先のパスをリストに追加
                localpath = str(file)  # アップロードしたいファイルのパス(ローカル)
                sftp.put(localpath=localpath, remotepath=remotepath)  # アップロード

    print(f"アップロード完了")

    # パスキーを削除する
    os.remove(key_path)

    return remotepath_list
