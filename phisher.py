#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pika
import sys
import argparse
import io
import re
import ast
from google.cloud import vision
from google.cloud.vision import types
reload(sys)
sys.setdefaultencoding('utf-8')

lista=['term1','term2','term3','term4','term5','term6']
credentials = pika.PlainCredentials('user', 'pass')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))


# [START def_detect_web_uri]
def detect_web_uri(uri, site):
    """Detects web annotations in the file located in Google Cloud Storage."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()

    image.source.image_uri = str(uri)
    images_analized = []


    response = client.web_detection(image=image)
    notes = response.web_detection

    if notes.web_entities:
        #print ('\n{} Web entities found: '.format(len(notes.web_entities)))

        for entity in notes.web_entities:
            #print('Score      : {}'.format(entity.score))
            #print('Description: {}'.format(entity.description))

                scoreMatch = (entity.score)
                descri = str(entity.description)

                for i in lista:
                        if re.search(i, descri, re.IGNORECASE):
                                images_analized.append(i)




    if len(images_analized) > 0:
       message = {"Encontrado": images_analized, "Site": site, "Onde": uri}
       payload = json.dumps(message)
       channel.basic_publish(exchange='', routing_key='phisher', body=payload)
# [END def_detect_web_uri]


def tryAgain(retries=0):
    if retries > 3: return
    try:   
        
        channel = connection.channel()
        
        
        def callback(ch, method, properties, body):
            image = str(body)
        
            loaded_json = (json.loads(image))
        
        
        
            imagem = loaded_json['images']
            imagem = ast.literal_eval(json.dumps(imagem))
            site = loaded_json['DomainUrl']
            site = ast.literal_eval(json.dumps(site))
        
            for element in loaded_json['images']:
                detect_web_uri(element, site)
        
        
        
            ch.basic_ack(delivery_tag = method.delivery_tag)
        
        channel.basic_consume(callback,
                              queue='imageurls',
                              no_ack=False)
        
        channel.start_consuming()
        channel.basic_qos(prefetch_count=1)
    except:
        retries+=1
        tryAgain(retries)

tryAgain()
