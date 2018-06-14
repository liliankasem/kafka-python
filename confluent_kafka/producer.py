import sys
import os

from confluent_kafka import Producer

if __name__ == '__main__':
    topic = 'test'

    # Producer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    conf = {
        'bootstrap.servers': os.environ['EVENTHUB_FQDN'],
        'security.protocol': 'SASL_SSL',
	    'sasl.mechanism': 'PLAIN',
        'sasl.username': '$ConnectionString',
        'sasl.password': os.environ['EVENTHUB_CONNECTION_STRING']
    }

    # Create Producer instance
    p = Producer(**conf)

    def delivery_callback(err, msg):
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write('%% Message delivered to %s [%d]\n' %
                             (msg.topic(), msg.partition()))

    for line in sys.stdin:
        try:
            p.produce(topic, line.rstrip(), callback=delivery_callback)
        except BufferError as e:
            sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                             len(p))
        p.poll(0)

    sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
    p.flush()
