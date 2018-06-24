import pika
import uuid
import json


class RpcClient(object):
    def __init__(self, host, port, virtual_host, username, password):
        self.task_id = None
        self.response = None
        # 声明mq连接用户、连接实例、声明使用管道
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,
                                                                            port=port,
                                                                            virtual_host=virtual_host,
                                                                            credentials=credentials))
        self.channel = self.connection.channel()
        # 生成一个随机队列callback_queue,用于告诉服务端将请求结果发送到哪里
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.get_response, queue=self.callback_queue)
        self.channel.queue_declare(queue='rpc_queue')

    def get_response(self, ch, method, props, body):
        print(props.__dict__, body)
        if self.task_id == props.correlation_id:
            self.response = body
        return body

    def run_cmd(self, cmds):
        task_id = str(uuid.uuid4())
        req_data = {"task_id": task_id, "check_task": False, "cmd": cmds}
        req_data = json.dumps(req_data)
        properties = pika.BasicProperties(reply_to=self.callback_queue, correlation_id=task_id)
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=properties,
                                   body=req_data)
        self.connection.process_data_events()  # 非阻塞发送请求
        return task_id

    def check_task(self, task_id):
        req_data = {"task_id": task_id, "check_task": True}
        req_data = json.dumps(req_data)
        properties = pika.BasicProperties(reply_to=self.callback_queue, correlation_id=task_id)
        print(self.callback_queue)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.callback_queue,
                                   properties=properties,
                                   body=req_data)
        # self.connection.process_data_events()  # 非阻塞发送请求
        self.channel.start_consuming()

        return self.response

    def close(self):
        self.connection.close()


if __name__ == "__main__":
    client = RpcClient("localhost", 5672, "/", "alex", "123456")
    # task_id = client.run_cmd("ls,pwd")
    # print(task_id)
    # rsp = client.check_task(task_id)
    rsp = client.check_task("082b61a0-7ed4-42a2-bcb8-d48e03b0c389")
    print(rsp)
    client.close()

