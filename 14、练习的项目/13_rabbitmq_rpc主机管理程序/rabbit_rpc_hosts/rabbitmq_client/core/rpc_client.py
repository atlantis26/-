# coding:utf-8
from core.db_handler import save_task, load_task
import pika
import uuid


class RpcClient(object):
    def __init__(self, host, port, virtual_host, username, password, server_queue_name):
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.username = username
        self.password = password
        self.server_queue_name = server_queue_name
        self.response = None

        # 声明mq连接用户、连接实例、声明使用管道
        credentials = pika.PlainCredentials(self.username, self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,
                                                                            port=self.port,
                                                                            virtual_host=self.virtual_host,
                                                                            credentials=credentials))
        self.channel = self.connection.channel()
        # 声明服务端的队列queue_name
        self.channel.queue_declare(queue=server_queue_name)
        # 再生成一个随机队列callback_queue,用于告诉服务端将请求结果发送到哪里
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.get_response, queue=self.callback_queue)

    def get_response(self, ch, method, props, body):
        task_id = props.correlation_id
        queue = props.reply_to
        save_task(task_id, queue, body)

    def run_cmd(self, cmds):
        task_id = str(uuid.uuid4())
        properties = pika.BasicProperties(reply_to=self.callback_queue, correlation_id=task_id)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.server_queue_name,
                                   properties=properties,
                                   body=cmds)
        self.connection.process_data_events()  # 非阻塞发送请求
        # 记录下task相关信息
        save_task(task_id, self.callback_queue, None)

        return task_id

    def check_task(self, task_id):
        properties = pika.BasicProperties(reply_to=self.callback_queue, correlation_id=task_id)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.callback_queue,
                                   properties=properties,
                                   body=task_id)
        self.connection.process_data_events()  # 非阻塞发送请求
        task_data = load_task(task_id)

        return task_data["data"]

    def close(self):
        self.connection.close()
