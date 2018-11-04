import base64
with open('./images/button.png', 'rb') as imgFile:
    imageFile = base64.b64encode(imgFile.read())