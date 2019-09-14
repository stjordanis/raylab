# pylint: disable=missing-docstring
import os.path as osp
from glob import glob

import click
from ray.tune.analysis import ExperimentAnalysis


def get_last_checkpoint_path(logdir):
    """Retrieve the path of the last checkpoint given a Trial logdir."""
    last_checkpoint_basedir = sorted(
        glob(osp.join(logdir, "checkpoint_*")), key=lambda p: p.split("_")[-1]
    )[-1]
    last_checkpoint_path = osp.join(
        last_checkpoint_basedir, osp.basename(last_checkpoint_basedir).replace("_", "-")
    )
    return last_checkpoint_path


@click.command()
@click.argument(
    "logdir",
    nargs=1,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
)
@click.option("--metric", default="episode_reward_mean")
@click.option("--mode", default="max")
def main(logdir, metric, mode):
    """Find the best experiment checkpoint as measured by a metric."""
    analysis = ExperimentAnalysis(logdir)
    best_logdir = analysis.get_best_logdir(metric, mode=mode)
    last_checkpoint_path = get_last_checkpoint_path(best_logdir)
    click.echo(last_checkpoint_path)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
