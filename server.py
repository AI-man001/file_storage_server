# API Name      : SplitStorage
# API Version   : 1.0.0
# Developed By  : Divine Zvenyika
# Date          : Sunday, Augast ‎16, ‎2020, ‏‎08:36:30 AM  #
import os
from procesor import FileProcessor
from flask import Flask, request, jsonify
from flask.helpers import send_from_directory

app = Flask(__name__)


@app.route('/savefiles', methods=['POST'])
def saveFiles():
  processor = FileProcessor(request)
  response = processor.saveFiles()
  return jsonify(response)


@app.route('/deletefiles', methods=['POST'])
def deleteFiles():
  processor = FileProcessor(request)
  response = processor.deleteFiles()
  return jsonify(response)


@app.route('/deleteroot', methods=['POST'])
def deleteRoot():
  processor = FileProcessor(request)
  response = processor.deleteRoot()
  return jsonify(response)


@app.route('/uploads/<rootnode>/<filename>', methods=['GET'])
def getFilesWithOutParentNode(rootnode, filename):
  return send_from_directory(os.path.join('uploads', rootnode), filename)


@app.route('/uploads/<rootnode>/<parentnode>/<filename>', methods=['GET'])
def getFilesWithParentNode(rootnode, parentnode, filename):
  return send_from_directory(os.path.join('uploads', rootnode, parentnode), filename)


if __name__ == "__main__":
  app.run(debug=True, port=5001)
