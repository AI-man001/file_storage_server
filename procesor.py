import os
import random
import string
import shutil
from urllib.parse import urlparse
from werkzeug.utils import secure_filename


class FileProcessor:

  def __init__(self, request):
    self.urlList = []
    self.root = request.form.get('root')
    self.files = request.files.getlist('files')
    self.procedure = request.form.get('procedure')
    self.fileowner = request.form.get('fileowner')
    self.fileurls = request.form.getlist('fileurls')
    self.host = f'http://10.0.2.2:5001/uploads/{self.root}'

  def saveFiles(self):
    #delete existing file if procedure is replace
    self.deleteFiles() if self.procedure == 'replace' else False
    #!-----------------------------------start saving new files------------------------------------
    for _file in self.files:
      _filename, _extension = os.path.splitext(_file.filename)
      _prefix = ''.join(random.choice(f'{string.ascii_letters}{string.digits}') for _ in range(20))
      _filename = secure_filename(f'{self.fileowner}_{_prefix}{_extension}').lower()
      _file.save(os.path.join(self.get_parent_dir(), _filename))
      _fileURL = f'{self.host}/{self.fileowner}/{_filename}'
      self.urlList.append(_fileURL)
    return {'urls': self.urlList}

  def deleteRoot(self):
    return {'status': True} if shutil.rmtree(self.get_parent_dir()) else {'status': False}

  def deleteFiles(self):
    for _fileurl in self.fileurls:
      _filename = os.path.basename(urlparse(_fileurl).path).lower()
      _filepath = os.path.join(self.get_parent_dir(), _filename)
      os.remove(_filepath) if os.path.isfile(_filepath) else {'status': False}
    return {'status': True}

  def get_parent_dir(self):
    _parent = os.path.join('uploads', self.root, self.fileowner)
    os.makedirs(_parent) if not os.path.exists(_parent) else {'status': False}
    return _parent