"""
Модуль OPC_Client
"""

from opcua import Client
from opcua.ua import NodeClass, AttributeIds


class ClientApp(Client):
    """
        Клиент высокого уровня для подключения к серверу OPC-UA.
        Данный клиент является потомком класса Client библиотеки opcua
    """

    def __init__(self, url='opc.tcp://192.168.56.102:62544', timeout=4):
        """
        Функция инициализирует подключение к OPC UA серверу.
        :param url: url для подключения к OPC UA серверу
        :type url: str
        :param timeout: время, в течение которого клиент ожидает ответ сервера в секундах
        :type timeout: int 
        """

        super().__init__(url, timeout)
        self.url = url
        self.node_list = list()
        self.object_node_list = list()
        self.NodeClass_Variable = NodeClass(2)  # тип узла - переменная
        self.NodeClass_Object = NodeClass(1)  # тип узла - объект

    def get_nodes_from_tags(self, tags):
        nodes = list()
        for tag in tags:
            try:
                nodes.append(self.get_node('ns=1;s=' + tag))
            except:
                print('!!!! Нет тега', tag)
        return nodes

    def set_value(self, node, value):
        """
        Функция обновляет значения узла
        :param node: узел
        :type node: opcua.common.node.Node 
        :param value: значение
        :type value: float 
        """
        node.set_value(value, varianttype=node.get_data_type_as_variant_type())

    def set_values(self, node_list, values):
        """
        Функция обновляет значения узлов
        :param node_list: список узлов
        :type node_list: list 
        :param values: список значений
        :type values: list 
        """
        for node, value in zip(node_list, values):
            node.set_value(
                value, varianttype=node.get_data_type_as_variant_type())


if __name__ == '__main__':

    client = ClientApp()
    try:
        client.connect()
        tags = ['root.Sensors_A.Sensor_1.Pressure', 'root.Sensors_A.Sensor_100.Pressure',
                'root.Sensors_A.Sensor_2.Pressure', 'root.Sensors_A.Sensor_101.Pressure']
        nodes = client.get_nodes_from_tags(tags)
        print(client.get_values(nodes))
        client.set_values(nodes, [10, 10, 10, 10])
        print(client.get_values(
            nodes))  # nodes - список, хочешь получить значение одного узла закидывай его в список и обращайся к этой функции
    finally:
        client.disconnect()