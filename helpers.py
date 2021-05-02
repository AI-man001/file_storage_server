import requests, pymongo

host = ""
api_cursor = pymongo.MongoClient().storage


class Products:
  def saveImage(api_key, _imagefiles):
    _imageList = []
    for _imagefile in _imagefiles:
      _imageList.append(('files', (_imagefile.filename, _imagefile.read())))
    _params = {'root': 'foldername', 'fileowner': api_key}
    _imagererouter = requests.post(f'{host}/savefiles', data=_params, files=_imageList)
    _imageurs = _imagererouter.json()
    return _imageurs.get('urls')

  def deleteImage(api_key, product):
    images = api_cursor.products.find_one({'$and': [{
        'owner': api_key,
        'product': product
    }]}, {
        '_id': False,
        'image': True
    })
    if images:
      params = {'root': 'foldername', 'fileurls': images['image'], 'fileowner': api_key}
      imagererouter = requests.post(f'{host}/deletefiles', data=params)
      return imagererouter.json()


class Stores:
  def saveImage(self, api_key, **kwargs):
    _imagefile = self.request.files.get('file')
    _images = {'files': (_imagefile.filename, _imagefile.read())}
    _params = {
        'root': 'foldername',
        'fileowner': api_key,
        'fileurls': [kwargs.get('current')],
        'procedure': kwargs.get('procedure')
    }
    _imagererouter = requests.post(f'{host}/savefiles', data=_params, files=_images)
    _imageurs = _imagererouter.json()
    return _imageurs.get('urls')[0]

  def updateLogo(self):
    api_key = self.request.form.get('api_key')
    currentimage = api_cursor.stores.find_one({'api_key': api_key}, {'image': True, '_id': False})
    imageURL = self.saveImage(api_key, procedure='replace', current=currentimage['image'])
    api_cursor.stores.update_one({'api_key': api_key}, {'$set': {'image': imageURL}})
