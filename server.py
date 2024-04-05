import os
import datetime
import json
import socket


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def get_root(self):
        return self.root

    def add(self, val):
        if not self.root:
            self.root = Node(val)
        else:
            self._add(val, self.root)

    def _add(self, val, node):
        if val < node.value:
            if node.left:
                self._add(val, node.left)
            else:
                node.left = Node(val)
        else:
            if node.right:
                self._add(val, node.right)
            else:
                node.right = Node(val)

    def tree_to_dict(self):
        return self._tree_dict(self.root)

    def _tree_dict(self, node):
        if node == None:
            return None
        else:
            return {"value": node.value,
                    "left": self._tree_dict(node.left),
                    "right": self._tree_dict(node.right)}


def save_binary_tree(tree_dicted, filename):
    with open(filename, 'a') as file:
        json.dump(tree_dicted, file)

def create_directory():
    now = datetime.datetime.now()
    folder_name = now.strftime("%d-%m-%Y_%H-%M-%S")
    os.mkdir(folder_name)
    return folder_name

def handle_client(client_socket):
    folder_name = create_directory()
    file_counter = 0
    Tree = BinaryTree()

    while True:
        data = client_socket.recv(1024).decode()
        print(data)
        '''if data == 'END':
            break'''
        if not data:
            file_counter += 1
            filename = f"{folder_name}/{file_counter}.json"
            save_binary_tree(Tree.tree_to_dict(), filename)
            break
        if data == "GET_FILE":
            file_info = client_socket.recv(1024).decode().split(",")
            folder_name = file_info[0]
            file_number = file_info[1]
            filename = f"{folder_name}/{file_number}.json"
            with open(filename, 'r') as file:
                file_data = file.read()
            client_socket.send(file_data.encode())
        else:
            number = int(data)
            Tree.add(number)

    client_socket.close()


def main():
    host = "127.0.0.1"
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Ожидание подключения клиента...")

    client_socket, addr = server_socket.accept()
    print("Клиент подключен:", addr)

    handle_client(client_socket)

    server_socket.close()
    print("Файл сохранен.")

if __name__ == "__main__":
    main()
