from django.core.files.storage import Storage

from fdfs_client.client import Fdfs_client

from django.conf import settings
# 文件上传操作

class FDFStorage(Storage):
    '''fast dfs自定义存储类'''
    def __init__(self,client_config=None,base_url=None):
        '''初始化'''
        if client_config is None:
            client_config =settings.FDFS_FILE_CONFIG
        self.client_config = client_config
        if base_url is None:
            base_url =settings.FDFS_URL
        self.base_url = base_url

    def _open(self,name,mode='rb'):
        # 打开文件
        pass

    def _save(self,name,content):
        '''
        原有方法说明:
        使用存储系统保存新文件，最好使用指定的名称。如果已经存在具有此名称的文件，
        存储系统可以根据需要修改文件名以获得唯一名称。将返回存储文件的实际名称。
        保存文件时使用
        :param name: 上传文件的名称
        :param content: 包含上传文件内容的File对象
        :return:
        '''
        # 1. 创建Fdfs_client对象
        client = Fdfs_client(self.client_config)
        # 2. # 上传文件至fsat dfs系统中
        res = client.upload_by_buffer(filebuffer=content.read())
        # 返回值
        # dict = {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # }
        if res.get('Status') !='Upload successed.':
            # 上传失败
            raise Exception('上传文件到fast dfs失败')
        # 获取返回的文件ID
        filename= res.get('Remote file_id')
        return filename

    def exists(self, name):
        '''
        # 原有方法说明:如果指定名称引用的文件已经存在于存储系统中，则返回True;如果名称对新文件可用，则返回False。
        判断文件名是否可用,在项目中重写exists方法
        :param name:
        :return:
        '''
        return False

    def url(self, name):
        '''
        返回访问的URL文件路径
        :param name:
        :return:
        '''

        return self.base_url+name

