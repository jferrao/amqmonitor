import time
import datetime
import sys
import sqlite3

import stomp

from amqmonitor import parser



class StatsListener(object):
    def __init__(self, sqlconn):
        self.sqlconn = sqlconn
        
    def on_error(self, headers, message):
        print('received an error %s' % message)
        
    def on_message(self, headers, content):

        date_time = datetime.datetime.fromtimestamp(int(headers['timestamp'][:10]))
        data = parser.parse(content)

        sql = 'INSERT INTO queues VALUES ("{timestamp}","{queue}",{size},{consumers},{enqueue},{dequeue},{avg_enqueue_time},{max_enqueue_time})'.format(
            timestamp=date_time,
            queue=data.get('destinationName'),
            size=data.get('size'),
            consumers=data.get('consumerCount'),
            enqueue=data.get('enqueueCount'),
            dequeue=data.get('dequeueCount'),
            avg_enqueue_time=data.get('averageEnqueueTime'),
            max_enqueue_time=data.get('maxEnqueueTime'),
        )

        c = self.sqlconn.cursor()
        c.execute(sql)
        self.sqlconn.commit()

        

conn = stomp.Connection(host_and_ports=[('172.16.32.88', 61613)])
sqlconn = sqlite3.connect('data/amqstats.sqlite', check_same_thread=False)

conn.set_listener('', StatsListener(sqlconn))
conn.start()
conn.connect()

conn.subscribe(destination='/queue/stats.results', id=1, ack='auto', headers={'client-id': 'amqstats'})


while 1:
    # Broker information
    #conn.send(body='', destination='/queue/ActiveMQ.Statistics.Broker', headers={'reply-to': '/queue/stats.results'})
    # Queue information
    conn.send(body='', destination='/queue/ActiveMQ.Statistics.Destination.stomp.test', headers={'reply-to': '/queue/stats.results'})#
    # Subscription statistics
    #conn.send(body='', destination='/queue/ActiveMQ.Statistics.Subscription', headers={'reply-to': '/queue/stats.results'})#
    time.sleep(30)
    
if conn.connected:
    conn.disconnect()

