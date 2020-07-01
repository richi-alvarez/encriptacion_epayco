import ssl
import json
import base64
import hashlib
from Crypto.Cipher import AES
from pathlib import Path
import sys

# No verificar el certifcado para los request
ssl._create_default_https_context = ssl._create_unverified_context

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-(s[-1])]

BASE_DIR = Path(__file__).resolve().parent.parent
EPAYCO_KEY_LANG_FILE = str(BASE_DIR.joinpath('key_lang.json'))

class AESCipher:
    def __init__( self, key,iv  ):
        self.key = key
        self.iv = iv    

    def encrypt( self, row ):

        raw = pad(row).encode("utf8")
        cipher = AES.new( self.key.encode("utf8"), AES.MODE_CBC, self.iv.encode("utf8"))
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc)


    def decrypt( self, enc ):
       
        enc = base64.b64decode(enc)
        cipher = AES.new( self.key.encode("utf8"), AES.MODE_CBC, self.iv.encode("utf8"))
        dec = cipher.decrypt(enc)
        return unpad(dec).decode('utf-8')

    def encryptArray(self,data):
        aux = {}
        for key, value in data.items():
            aux[key] = self.encrypt(value)
        return aux


class Util():

    def setKeys(self, array={},sp=''):
        #print('/setKeys/',sp)
        #sys.exit()
            file = open(EPAYCO_KEY_LANG_FILE, 'r').read()
            values = json.loads(file)
            aux = {}
            for key, value in array.items():
                if key in values:
                    aux[values[key]] = value
                else:
                    aux[key] = value
            return aux


class Client:

    IV = "0000000000000000"
    LANGUAGE = "python"
    SWITCH= False

    def __init__(self):
        pass

    """
    Make request and return a Python object from the JSON response. If
    HTTP method is DELETE return True for 204 response, false otherwise.
    :param api_key: String with the API key
    :param data: Dictionary with query strings
    :param private_key: String with the Private key Api
    :param test: String TRUE O FALSE transaction in pruebas or production
    :param lang: String languaje response errors
    :return: Native python object resulting of the JSON deserialization of the API response
    """
    def request(self,api_key="",data={}, private_key="",test=""):
            if(test):
                test= "TRUE"
            else:
                test= "FALSE"

            aes = AESCipher(private_key,self.IV)
            enpruebas = aes.encrypt(test)
            encryptData = None
            encryptData = aes.encryptArray(data)
            addData = {
                'public_key': api_key,
                'i': base64.b64encode(self.IV.encode('ascii')),
                'enpruebas': enpruebas,
                'lenguaje': self.LANGUAGE,
                'p': ''
            }
            enddata = {}
            enddata.update(encryptData)
            enddata.update(addData)
            data=enddata
           
            return data



class Resource(Client):
    """
     * Instance epayco class
     * @param array $epayco
     */
    """
    def __init__(self, epayco):
        self.epayco = epayco
"""
 * Constructor resource requests
"""

class Encript(Resource):
    """
     * Instance epayco class
     * @param array $epayco
     */
    """
    def create(self, options=None):
        return self.request(
            self.epayco.api_key,
            options,
            self.epayco.private_key,
            self.epayco.test
        )


class Epayco:

    public_key = ""
    api_key = ""
    test = False
    lang = "ES"

    def __init__(self, options):
        self.api_key = options["apiKey"]
        self.private_key = options["privateKey"]
        self.test = options["test"]
        self.lang = options["lenguage"]

        self.encript = Encript(self)


apiKey = "c84ad754c728bfb10af2c1c3d1594106"
privateKey = "448897b08db8a1ae6e72441fb6101a8b"
test = False
lenguage = "ES"
options={"apiKey":apiKey,"privateKey":privateKey,"test":test,"lenguage":lenguage}
objepayco = Epayco(options)

pse_info = {
     "bank": "1007",
    "invoice": "1a47asxsdsdd205asasdd0s778",
    "description": "pay test",
    "value": "10000",
    "tax": "0",
    "tax_base": "10000",
    "currency": "COP",
    "type_person": "0",
    "doc_type": "CC",
    "doc_number": "10000000",
    "name": "testing",
    "last_name": "PAYCO",
    "email": "no-respondser@payco.co",
    "country": "CO",
    "cell_phone": "3010000001",
    "ip": "181.129.40.114",
    "url_response": "https://tudominio.com/respuesta.php",
    "url_confirmation": "https://tudominio.com/confirmacion.php",
    "method_confirmation": "GET"
        }


pse = objepayco.encript.create(pse_info)
print(pse)