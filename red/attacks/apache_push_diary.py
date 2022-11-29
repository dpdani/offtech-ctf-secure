# pip3 install hyper
#
# cat /etc/apache2/sites-enabled/default-ssl.conf | grep Link -B1 -A1
#		<Location />
#		Header add Link "</foo.css>;rel=preload"
#		</Location>

import hyper
import ssl
import base64

from red.config import config


def run():
    c = hyper.tls.init_context()
    c.check_hostname = False
    c.verify_mode = ssl.CERT_NONE

    conn = hyper.HTTPConnection(f'{config.server_host}:{config.server_port}', enable_push=True, ssl_context=c)
    print(conn.request('GET', '/', headers={"Cache-Digest": "EA9BQQ=="}))
