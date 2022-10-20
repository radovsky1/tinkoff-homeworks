import argparse
import socket
import uuid

from datetime import datetime
from enum import Enum
from typing import Optional


class TaskQueueServerConstants(object):
    BACKLOG = 10
    BUFFER_SIZE = 1000000
    DB_FILE = "tasks"


class TaskQueueServerCommands(Enum):
    ADD = b"ADD"
    GET = b"GET"
    ACK = b"ACK"
    IN = b"IN"
    SAVE = b"SAVE"


class TaskQueueServerResponses(Enum):
    YES = b"YES"
    NO = b"NO"
    NONE = b"NONE"
    ERROR = b"ERROR"
    OK = b"OK"


class Task:
    def __init__(
        self,
        task_id: str,
        length: int,
        data: bytes,
        get_at: float = 0.0,
    ):
        self.task_id = task_id
        self.length = length
        self.data = data
        self.get_at = get_at

    def __bytes__(self):
        return b" ".join(
            [self.task_id.encode(), str(self.length).encode(), self.data]
        )

    def get(self):
        self.get_at = datetime.now().timestamp()
        return self


class TaskQueueServer:
    def __init__(self, ip: str, port: int, path: str, timeout: int):
        self.ip = ip
        self.port = port
        self._path = path
        self.timeout = timeout
        self._connection: Optional[socket.socket] = None
        self._queues: dict[str, list[Task]] = {}
        self._load()

    @property
    def path(self) -> str:
        return self._path + TaskQueueServerConstants.DB_FILE

    def _make_connection(self):
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._connection.bind((self.ip, self.port))
        self._connection.listen(TaskQueueServerConstants.BACKLOG)

    def _close_connection(self):
        self._connection.close()

    def _check_timeout(self, task: Task) -> bool:
        if task.get_at == 0.0:
            return False
        return datetime.now().timestamp() - task.get_at < self.timeout

    def _get_task_from_queue(self, name: str) -> Optional[Task]:
        for task in self._queues[name]:
            if not self._check_timeout(task):
                return task
        return None

    def add_task(self, queue_name: str, length: int, data: bytes) -> bytes:
        self._queues.setdefault(queue_name, [])
        task_id = str(uuid.uuid4())
        self._queues[queue_name].append(Task(task_id, length, data))
        return task_id.encode()

    def get_task(self, queue_name: str) -> bytes:
        if (
            queue_name not in self._queues
            or len(self._queues[queue_name]) == 0
        ):
            return TaskQueueServerResponses.NONE.value
        task = self._get_task_from_queue(queue_name)
        if task is None:
            return TaskQueueServerResponses.NONE.value
        else:
            return bytes(task.get())

    def ack_task(self, queue_name: str, task_id: str) -> bytes:
        if queue_name in self._queues:
            for task in self._queues[queue_name]:
                if task.task_id == task_id and task.get_at != 0.0:
                    self._queues[queue_name].remove(task)
                    return TaskQueueServerResponses.YES.value
        return TaskQueueServerResponses.NO.value

    def in_task(self, queue_name: str, task_id: str) -> bytes:
        if queue_name in self._queues:
            for task in self._queues[queue_name]:
                if task.task_id == task_id:
                    return TaskQueueServerResponses.YES.value
        return TaskQueueServerResponses.NO.value

    def save(self) -> bytes:
        with open(self.path, "w") as file:
            for queue_name, tasks in self._queues.items():
                for task in tasks:
                    line = "{} {} {} {} {}\n".format(
                        queue_name,
                        task.task_id,
                        task.length,
                        task.data.decode(),
                        task.get_at,
                    )
                    file.write(line)
        return TaskQueueServerResponses.OK.value

    def _load(self) -> None:
        try:
            with open(self.path, "r") as file:
                for line in file:
                    queue_name, task_id, length, data, get_at = line.split()

                    self._queues.setdefault(queue_name, [])
                    self._queues[queue_name].append(
                        Task(
                            task_id,
                            int(length),
                            data.encode(),
                            float(get_at),
                        )
                    )
        except FileNotFoundError:
            pass

    def run(self):
        self._make_connection()
        while True:
            current_connection = None
            try:
                current_connection, address = self._connection.accept()
                data = current_connection.recv(
                    TaskQueueServerConstants.BUFFER_SIZE
                )
                command, *arg = data.split(b" ")

                if command == TaskQueueServerCommands.ADD.value:
                    response = self.add_task(
                        arg[0].decode(), int(arg[1]), arg[2]
                    )
                elif command == TaskQueueServerCommands.GET.value:
                    response = self.get_task(arg[0].decode())
                elif command == TaskQueueServerCommands.ACK.value:
                    response = self.ack_task(arg[0].decode(), arg[1].decode())
                elif command == TaskQueueServerCommands.IN.value:
                    response = self.in_task(arg[0].decode(), arg[1].decode())
                elif command == TaskQueueServerCommands.SAVE.value:
                    response = self.save()
                else:
                    response = TaskQueueServerResponses.ERROR.value

                current_connection.send(response)
            except KeyboardInterrupt:
                if current_connection:
                    current_connection.close()
                break


def parse_args():
    parser = argparse.ArgumentParser(
        description="This is a simple task queue server with custom protocol"
    )
    parser.add_argument(
        "-p",
        action="store",
        dest="port",
        type=int,
        default=5432,
        help="Server port",
    )
    parser.add_argument(
        "-i",
        action="store",
        dest="ip",
        type=str,
        default="127.0.0.1",
        help="Server ip address",
    )
    parser.add_argument(
        "-c",
        action="store",
        dest="path",
        type=str,
        default="./",
        help="Server checkpoints dir",
    )
    parser.add_argument(
        "-t",
        action="store",
        dest="timeout",
        type=int,
        default=300,
        help="Task maximum GET timeout in seconds",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    server = TaskQueueServer(**args.__dict__)
    server.run()
