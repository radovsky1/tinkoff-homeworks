import asyncio
from typing import List

import yaml
from aiohttp import web

from hw_1_12.handlers.handler import Handler
from hw_1_12.node import NodeConfig, NodeNeighborConfig, NodeDaemon
from hw_1_12.repository import Repository
from hw_1_12.service import Service
from hw_1_12.service.webapi import DistributedFileStorage


def init_config(node_name: str):
    with open("configs/config{}.yaml".format(node_name), "r") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    return cfg


def run_node(
        node_config: NodeConfig, node_neighbors_config: List[NodeNeighborConfig]
):
    distributed_file_storages = [
        DistributedFileStorage(neighbor.url)
        for neighbor in node_neighbors_config
    ]

    repository = Repository(node_config.directory)
    service = Service(repository, distributed_file_storages)
    handler = Handler(service)

    app = web.Application()
    handler.init_routes(app)

    node_daemon = NodeDaemon(app, node_config.hostname, node_config.port)
    loop.create_task(node_daemon.start())


if __name__ == "__main__":
    config = init_config("A")

    loop = asyncio.get_event_loop()

    node_cfg = NodeConfig(**config["node"])
    node_neighbors_cfg = [
        NodeNeighborConfig(**neighbor) for neighbor in config["node"]["neighbors"]
    ]

    run_node(node_cfg, node_neighbors_cfg)

    loop.run_forever()
