from wsgiref.simple_server import make_server
from webstuff.main import *
#import webstuff.main

##  test environment !Production environment   ##
PORT=8080
DEBUG=True

if __name__ == '__main__':
    app.run(debug=DEBUG,port=PORT,host='0.0.0.0')
    #app.run()

# if __name__ == '__main__':
#     server = make_server('127.0.0.1', PORT, app)
#     server.serve_forever()

    