#!/usr/bin/env python
import pika
import uuid

class UtilizationRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='10.138.77.176'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare('', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue,
            on_message_callback=self.on_response, auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='', routing_key='compute_util_rpc_q',
            properties=pika.BasicProperties(reply_to=self.callback_queue,
            correlation_id=self.corr_id,),body=n)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

utilization_rpc = UtilizationRpcClient()
def cpu_util():
    print (' [x]Get CPU utilization')
    response = utilization_rpc.call('cpu')
#   print(" [.] Got", response)
    li = list(response.split('\\n'))
#
#debug
#   print len(li)
#   for num in range (0,len(li)):
#    print li[num]
    if len(li) > 3:
        title_list = list(li[2].split(' '))
        title_list_f = []
        for num in range (0, len(title_list)):
             if title_list[num]:
                 title_list_f.append(title_list[num]) 
#debug        
#       for num in range (0, len(title_list_f)):
#            print title_list_f[num]

        value_list = list(li[3].split(' '))
        value_list_f = []
        for num in range (0, len(value_list)):
             if value_list[num]:
                 value_list_f.append(value_list[num]) 
#debug        
#       for num in range (0, len(value_list_f)):
#           print value_list_f[num]

        print title_list_f[4], value_list_f[4]
        print title_list_f[13], value_list_f[13]

def ram_util():
#    utilization_rpc = UtilizationRpcClient()
    print (' [x]Get RAM utilization')
    response = utilization_rpc.call('ram')
#debug
#    print(" [.] Got", response)
    li = list(response.split('\\n'))
    #print li

#debug
#    print len(li)
#    for num in range (0,len(li)):
#        print li[num]
    if len(li) > 3:
        title_list = list(li[0].split(' '))
        title_list_f = []
        for num in range (0, len(title_list)):
             if title_list[num]:
                 title_list_f.append(title_list[num])
#debug        
#        for num in range (0, len(title_list_f)):
#             print title_list_f[num]
 
        value_list = list(li[1].split(' '))
        value_list_f = []
        for num in range (0, len(value_list)):
             if value_list[num]:
                 value_list_f.append(value_list[num]) 
#debug        
#        for num in range (0, len(value_list_f)):
#             print value_list_f[num]
        print title_list_f[1], value_list_f[2]
        print title_list_f[2], value_list_f[3]
        print title_list_f[6], value_list_f[7]

def storage_util():
#    utilization_rpc = UtilizationRpcClient()
    print (' [x]Get Storage utilization')
    response = utilization_rpc.call('storage')
#    print(" [.] Got", response)
    li = list(response.split('\\n'))
#    print li
#debug
#    print len(li)
#    for num in range (0,len(li)):
#        print li[num]
    if len(li) > 2:
        title_list = list(li[0].split(' '))
        title_list_f = []
        for num in range (0, len(title_list)):
             if title_list[num]:
                 title_list_f.append(title_list[num])
#debug        
#        for num in range (0, len(title_list_f)):
#             print title_list_f[num]
    
        value_list = list(li[1].split(' '))
        value_list_f = []
        for num in range (0, len(value_list)):
             if value_list[num]:
                 value_list_f.append(value_list[num])
#debug        
#        for num in range (0, len(value_list_f)):
#             print value_list_f[num]
 
        print title_list_f[1], value_list_f[2]
        print title_list_f[2], value_list_f[3]
        print title_list_f[3], value_list_f[4]

cpu_util()
ram_util()
storage_util()
