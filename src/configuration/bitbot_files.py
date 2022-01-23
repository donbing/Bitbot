
from os.path import join as pjoin, exists
import errno, os

def use_config_dir(base_config_path):
    return BitBotFiles(base_config_path)

class BitBotFiles():
    def __init__(self, base_path):
        self.log_file_path = pjoin(base_path, 'debug.log')

        self.config_folder = pjoin(base_path, 'config/') 
        self.fonts_folder = pjoin(base_path, 'src/resources')

        self.logging_ini = self.existing_file_path('logging.ini')
        self.config_ini = self.existing_file_path('config.ini')
        self.base_style = self.existing_file_path('base.mplstyle') 
        self.inset_style = self.existing_file_path('inset.mplstyle') 
        self.default_style = self.existing_file_path('default.mplstyle') 
        self.volume_style = self.existing_file_path('volume.mplstyle') 
    
    def existing_file_path(self, file_name):
        file_path =  pjoin(self.config_folder, file_name)
        if not exists(file_path): 
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_name)
        return file_path