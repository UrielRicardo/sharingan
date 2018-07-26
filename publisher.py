#!/usr/bin/env python
import pika
import time
credentials = pika.PlainCredentials('user', 'pass')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials))
channel = connection.channel()

f = open("domains.txt")
lines = f.readlines()
for line in lines:
    payload = line.replace('\n','')
    channel.basic_publish(exchange='', routing_key='domain', body=payload)
