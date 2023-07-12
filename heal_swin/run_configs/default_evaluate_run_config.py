#!/usr/bin/env -S python3 -u
# fmt: off
#SBATCH -t 4-00:00:00  # noqa: E265
#SBATCH -o ../../slurm/slurm-%j.out  # for array jobs, this should be slurm-%A_%a.out # noqa: E265
# this is needed to prevent black from formatting the above SBATCH comments...
dummy="dummy"  # noqa: E225
# fmt: on

import os  # noqa: E402
import subprocess  # noqa: E402
from pathlib import Path  # noqa: E402


RUN_ID = os.getenv("RUN_ID", default="")
EPOCH = "best"


def get_eval_run_config():
    from heal_swin.utils import utils
    from heal_swin.evaluation.evaluate_config import EvaluateConfig

    train_run_config = utils.load_config(RUN_ID, "run_config")
    data_config = train_run_config.data
    train_config = train_run_config.train

    return EvaluateConfig(
        path=RUN_ID, epoch=EPOCH, data_config=data_config, train_config=train_config
    )


def get_pl_config():
    from heal_swin.utils import utils

    import torch

    train_pl_config = utils.load_config(RUN_ID, "pl_config")

    if torch.cuda.is_available():
        train_pl_config.gpus = 1
    else:
        train_pl_config.gpus = 0
    return train_pl_config


def main():
    this_path = str(Path(__file__).absolute())

    if "SLURM_SUBMIT_DIR" in os.environ:
        base_path = str(Path(os.environ["SLURM_SUBMIT_DIR"]).parents[1])
    else:
        base_path = str(Path(this_path).parents[2])

    run_py_path = os.path.join(base_path, "run.py")

    command = ["python3", "-u", run_py_path]
    command += ["--env", "singularity"]
    command += ["evaluate"]
    command += ["--config_path", this_path]
    print(" ".join(command))

    subprocess.run(command)


if __name__ == "__main__":
    main()
