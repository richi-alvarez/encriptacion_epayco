<?php
require_once('paycaes.php');
class Util
{
    const IV = "0000000000000000";
    const LENGUAGE = "php";

        public function mergeSet($data, $test, $lang, $private_key, $api_key)
        {

            $aes = new PaycoAes($private_key, self::IV, $lang);
            $encryptData = $aes->encryptArray($data);
            $adddata = array(
                "public_key" => $api_key,
                "i" => base64_encode(self::IV),
                "enpruebas" => $aes->encrypt($test),
                "lenguaje" => self::LENGUAGE,
                "p" => "",
            );
            return array_merge($encryptData, $adddata);
        
        }
}

class Client 
{
    public function request(
        $api_key,
        $private_key,
        $data = null,
        $test,
        $lang
    )
    {
         $util = new Util();
         $dataEncripted = $util->mergeSet($data, $test, $lang, $private_key, $api_key);
         $response = json_encode($dataEncripted);
         return $response;
    }

}


 $client = new Client();
 $pse = array(
        "banco" => "1007",
        "factura" => "1472050779",
        "descripcion" => "Pago pruebas 2",
        "valor" => "10000",
        "iva" => "0",
        "baseiva" => "10000",
        "moneda" => "COP",
        "tipo_persona" => "0",
        "tipo_doc" => "CC",
        "documento" => "1214723219",
        "nombres" => "PRUEBAS",
        "apellidos" => "PAYCO",
        "email" => "no-responder@payco.co",
        "pais" => "CO",
        "celular" => "3010000001",
        "ip" => "190.000.000.000",  // This is the client's IP, it is required
        "url_respuesta" => "https://ejemplo.com/respuesta.html",
        "url_confirmacion" => "https://ejemplo.com/confirmacion",
        "metodoconfirmacion" => "GET",
);

 $information=$client->request("c84ad754c728bfb10af2c1c3d1594106","448897b08db8a1ae6e72441fb6101a8b",$pse,false,"ES");
 var_dump($information);