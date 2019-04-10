#!/usr/bin/env python
import pika
import subprocess
import sys

HOST="127.0.0.1"
# Ports are handled in ~/.ssh/config since we use OpenSSH

def util(cmd):
    ssh = subprocess.Popen(["ssh", "%s" % HOST, cmd],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
#    print >>sys.stderr, "ERROR: %s" % error
        return error
    else:
#    print result
        return result


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='compute_util_rpc_q')


def utilization(para):
    if para == 'cpu':
        return util("mpstat") #'cpu %age'
    elif para == 'ram':
        return util("free")
    elif para == 'storage':
        return util("df -h /")
    else:
        return 'Not found'

def on_request(ch, method, props, body):
    print ('received', body)
    response = utilization(body)

    print ('Sending', response)
    #response = 'received'
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, 'compute_util_rpc_q')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
