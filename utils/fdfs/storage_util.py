from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client

class FDFSStorage(Storage):
    """FDFS文件系统存储类"""
    def __init__(self, client_conf=None, base_url=None):
        """初始化"""
        self.client_conf = settings.FDFS_CLIENT_CONF
        self.base_url = settings.FDFS_URL

    def open(self, name, mode='rb'):
        '''打开文件时使用'''
        pass

    # 重写save方法
    def save(self,name, content):
        # name 上传文件的名称
        # 读取内容
        #创建实例对象 client
        # return dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': local_file_name,
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # } if success else None
        client = Fdfs_client(self.client_conf)
        # 上传内容
        response = client.upload_by_buffer(content.read())
        # 返回响应值
        if response.get('Status') != 'Upload successed.':
            # 上传失败，跑出异常
            raise Exception('上传文件到FDFS系统失败')
        filename = response.get('Remote file_id')
        return filename

    def exists(self, name):
        return False

    def url(self, name):
        return self.base_url + name
