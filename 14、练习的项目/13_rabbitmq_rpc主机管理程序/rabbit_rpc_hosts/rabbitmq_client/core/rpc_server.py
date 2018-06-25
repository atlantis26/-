# _*_coding:utf-8_*_
import pika


class RpcServer(object):
    def __init__(self, host, port, virtual_host, username, password):
        # 声明mq连接用户、连接实例、声明使用管道、声明使用的队列名称
        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,
                                                                       port=port,
                                                                       virtual_host=virtual_host,
                                                                       credentials=credentials))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='rpc_queue')

    @staticmethod
    def handler(req_data):
        """
        :param req_data: 请求数据，1个或多个可执行的命令，以逗号连接
        :return: 请求返回结果，命令的执行结果
        """
        return req_data + b"response1"

    def get_response(self, ch, method, props, body):
        """
        :param ch: 队列管道channel对象
        :param method:请求方法对象
        :param props:请求属性对象
        :param body:请求数据
        :return: 请求处理结果
        """
        # 处理请求
        response = self.handler(body)
        # 请求返回数据通过客户端指定的队列（reply_to）返回给客户端
        response_queue = props.reply_to
        print(response_queue)
        # 客户端发送的请求task_id
        task_id = props.correlation_id
        print(task_id, body)
        # 执行推送消息
        ch.basic_publish(exchange='',
                         routing_key=response_queue,
                         properties=pika.BasicProperties(correlation_id=task_id),
                         body=response)
        # 确认推送的消息被处理完成ack
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.channel.basic_consume(self.get_response, queue='rpc_queue')
        self.channel.start_consuming()


if __name__ == "__main__":

    server = RpcServer("localhost", 5672, "/", "alex", "123456")
    server.run()
