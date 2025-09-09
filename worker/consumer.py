import os
import pika
import time

from callback import callback

user = os.getenv("RABBITMQ_DEFAULT_USER")
pwd = os.getenv("RABBITMQ_DEFAULT_PASS")


def consume(host):
    print(host)
    for attempt in range(10):
        try:
            print(f"Connecting to RabbitMQ (try {attempt})...")
            creds = pika.PlainCredentials(user, pwd)
            conn = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host,
                    credentials=creds,
                    # blocked_connection_timeout=300,
                    # heartbeat=1
                )
            )
            break
        except Exception as e:
            print(f"Failed: {e}")
            time.sleep(5)
    else:
        print("Could not connect after 10 attempts")
        exit(1)

    ch = conn.channel()
    ch.queue_declare(queue="router_jobs", durable=True)
    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(queue="router_jobs", on_message_callback=callback, auto_ack=True)
    ch.start_consuming()


if __name__ == "__main__":
    consume("localhost")
