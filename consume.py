from confluent_kafka import Consumer
import time
import json
import re

BOOTSTRAP_SERVERS = 'localhost:9094'
GROUP_ID = 'kafka-cdc'
GROUP_INSTANCE_ID = 'consumer-1'
INTERVAL_SECONDS = 5
TOPIC_PREFIX = 'test'

def generate_consumer():
    conf = {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'group.id': GROUP_ID,
        'group.instance.id': GROUP_INSTANCE_ID,
        'enable.auto.commit': 'false',
        'auto.offset.reset': 'earliest',
    }
    consumer = Consumer(conf)
    return consumer



def start():
    consumer = generate_consumer()
    consumer.subscribe([f'{TOPIC_PREFIX}.public.cities', f'{TOPIC_PREFIX}.public.users'])

    now = time.time()
    now += INTERVAL_SECONDS

    while True:
        try:
            res = consumer.consume(num_messages=100, timeout=5)
            for msg in res:
                if not msg:
                    continue

                if err:= msg.error():
                    print(err)
                    continue

                if key_raw := msg.key():
                    key = json.loads(key_raw.decode())
                    pk = key['payload']
                else:
                    key = key_raw
                    pk = None
                value = json.loads(msg.value().decode())
                table = re.findall(f'^{TOPIC_PREFIX}\\.(.*)', msg.topic())[0]
                op = value['payload']['op']
                
                before = value['payload']['before']
                after = value['payload']['after']
                # print({'key': json.loads(msg.key().decode()), 'val': {'table': table, 'pk': pk, 'op': op, 'before': before, 'after': after}, 'headers': msg.headers()})
                print(json.dumps(key))
                print(json.dumps(value))

            dt = time.time()
            if dt > now:
                consumer.commit()
                now += INTERVAL_SECONDS
                print('committed')

        except KeyboardInterrupt:
            print('bye')
            consumer.commit()
            consumer.close()
            break

        except Exception as err:
            raise (err)

if __name__ == '__main__':
    start()