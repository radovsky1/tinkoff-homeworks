import os
from unittest import TestCase

import time
import socket

import subprocess

from server import TaskQueueServer


class ServerTestCase(TestCase):
    def send(self, command):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 5432))
        s.send(command)
        data = s.recv(1000000)
        s.close()
        return data


class ServerBaseTest(ServerTestCase):
    def setUp(self):
        self.server = subprocess.Popen(["python3", "server.py"])
        # даем серверу время на запуск
        time.sleep(0.5)

    def tearDown(self):
        self.server.terminate()
        self.server.wait()

    def test_base_scenario(self):
        task_id = self.send(b"ADD 1 5 12345")
        self.assertEqual(b"YES", self.send(b"IN 1 " + task_id))

        self.assertEqual(task_id + b" 5 12345", self.send(b"GET 1"))
        self.assertEqual(b"YES", self.send(b"IN 1 " + task_id))
        self.assertEqual(b"YES", self.send(b"ACK 1 " + task_id))
        self.assertEqual(b"NO", self.send(b"ACK 1 " + task_id))
        self.assertEqual(b"NO", self.send(b"IN 1 " + task_id))

    def test_two_tasks(self):
        first_task_id = self.send(b"ADD 1 5 12345")
        second_task_id = self.send(b"ADD 1 5 12345")
        self.assertEqual(b"YES", self.send(b"IN 1 " + first_task_id))
        self.assertEqual(b"YES", self.send(b"IN 1 " + second_task_id))

        self.assertEqual(first_task_id + b" 5 12345", self.send(b"GET 1"))
        self.assertEqual(b"YES", self.send(b"IN 1 " + first_task_id))
        self.assertEqual(b"YES", self.send(b"IN 1 " + second_task_id))
        self.assertEqual(second_task_id + b" 5 12345", self.send(b"GET 1"))

        self.assertEqual(b"YES", self.send(b"ACK 1 " + second_task_id))
        self.assertEqual(b"NO", self.send(b"ACK 1 " + second_task_id))

    def test_long_input(self):
        data = "12345" * 1000
        data = "{} {}".format(len(data), data)
        data = data.encode("utf")
        task_id = self.send(b"ADD 1 " + data)
        self.assertEqual(b"YES", self.send(b"IN 1 " + task_id))
        self.assertEqual(task_id + b" " + data, self.send(b"GET 1"))

    def test_wrong_command(self):
        self.assertEqual(b"ERROR", self.send(b"ADDD 1 5 12345"))

    def test_wrong_task_id(self):
        self.assertEqual(b"NO", self.send(b"IN 1 12345"))
        self.assertEqual(b"NO", self.send(b"ACK 1 12345"))
        self.assertEqual(b"NONE", self.send(b"GET 1 12345"))

    def test_wrong_queue_id(self):
        self.assertEqual(b"NONE", self.send(b"GET UNDEF 1"))


class ServerTimeoutTest(ServerTestCase):
    def setUp(self):
        self.server = subprocess.Popen(["python3", "server.py", "-t", "2"])
        # даем серверу время на запуск
        time.sleep(0.5)

    def tearDown(self):
        self.server.terminate()
        self.server.wait()

    def test_timeout(self):
        task_id = self.send(b"ADD 1 5 12345")
        self.send(b"GET 1 " + task_id)
        self.assertEqual(b"YES", self.send(b"IN 1 " + task_id))
        time.sleep(1)
        self.assertEqual(b"NONE", self.send(b"GET 1"))
        time.sleep(2)
        self.assertEqual(task_id + b" 5 12345", self.send(b"GET 1"))


class ServerSaveTest(TestCase):
    def _start_server(self):
        self.server = subprocess.Popen(["python3", "server.py", "-c", "./"])
        # даем серверу время на запуск
        time.sleep(0.5)

    def setUp(self):
        self._start_server()

    def tearDown(self):
        self.server.terminate()
        self.server.wait()
        os.remove("./tasks")

    def send(self, command):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 5432))
        s.send(command)
        data = s.recv(1000000)
        s.close()
        return data

    def test_save(self):
        task_id = self.send(b"ADD 1 5 12345")
        self.assertEqual(b"YES", self.send(b"IN 1 " + task_id))
        self.send(b"SAVE")
        self.server.terminate()
        self.server.wait()
        self.server = subprocess.Popen(["python3", "server.py", "-c", "./"])
        # даем серверу время на запуск
        time.sleep(0.5)
        self.assertEqual(b"YES", self.send(b"IN 1 " + task_id))
        self.assertEqual(task_id + b" 5 12345", self.send(b"GET 1"))


if __name__ == "__main__":
    unittest.main()
