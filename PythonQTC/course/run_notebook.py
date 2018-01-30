import logging
import click
import os
import json


KEY = "cells"
TYPE = "cell_type"
CODE = "code"
SOURCE = "source"


def run(path):
    with open(path) as f:
        notebook = json.load(f)
        variables = {}
        for cell in notebook[KEY]:
            if cell.get(TYPE, None) == CODE:
                for source in cell[SOURCE]:
                    exec(source, variables)

    return 1


def execute(path, interrupt=True):
    if interrupt:
        result = run(path)
        logging.warning("%s | %s", path, result)
    else:
        try:
            result = run(path)
        except Exception as e:
            logging.error("%s | %s", path, e)
        else:
            logging.warning("%s | %s", path, result)



@click.command()
@click.argument("path", nargs=-1)
@click.option("--config", '-c', default=None)
@click.option("--interrupt", "-i", is_flag=True, default=False)
@click.option("--log", "-l", default=None)
@click.option("--mode", "-m", default="w")
def run_notebook(config=None, path=None, interrupt=False, log=None, mode="w"):
    if log:
        logging.basicConfig(
            handlers=[logging.StreamHandler(),
                      logging.FileHandler(log, mode)]
        )

    if config and os.path.isfile(config):
        with open(config) as f:
            for line in f.readlines():
                execute(line, interrupt)
    else:
        for p in path:
            if os.path.isfile(p):
                execute(p, interrupt)


if __name__ == '__main__':
    run_notebook()