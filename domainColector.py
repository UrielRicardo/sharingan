#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import os
import sys
import requests
import subprocess
from bs4 import BeautifulSoup
import json
import pika

credentials = pika.PlainCredentials('user', 'pass')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))

def tryAgain(retries=0):
    if retries > 3: return
    try:
		channel = connection.channel()
        def callback(ch, method, properties, body):
            url = str(body)
        
            if not (re.search(r'^https?://', url, re.IGNORECASE)):
                    url = 'http://'+url
        
        
            try:
                response = requests.get(url,timeout=3)
                soup = BeautifulSoup(response.text, 'html.parser')
                images_src = []
                for image in soup.findAll('img')[0:5]:
                    image_path = image.get('src', image.get('data-src'))
                    if image_path is not None:
        
                        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', image_path)
                        if 'http' not in image_path:
                            image_path = '{}{}'.format(url, image_path)
        
                        images_src.append(image_path)
        
                if len(images_src) > 0:
                   message = {"DomainUrl": url, "images": images_src }
                   payload = json.dumps(message)
                   channel.basic_publish(exchange='', routing_key='imageurls', body=payload)
        
                ch.basic_ack(delivery_tag = method.delivery_tag)
        
            except requests.exceptions.RequestException as err:
                ch.basic_ack(delivery_tag = method.delivery_tag)
            except requests.exceptions.HTTPError as errh:
                ch.basic_ack(delivery_tag = method.delivery_tag)
            except requests.exceptions.ConnectionError as errc:
                ch.basic_ack(delivery_tag = method.delivery_tag)
            except requests.exceptions.Timeout as errt:
                ch.basic_ack(delivery_tag = method.delivery_tag)
        
        
        channel.basic_consume(callback,
                              queue='domain',
                              no_ack=False)
        
        channel.start_consuming()
        channel.basic_qos(prefetch_count=1)
		
    except:
        retries+=1
        tryAgain(retries)

tryAgain()
