"""{{cookiecutter.project_slug}} commands."""

import subprocess

from toil.common import Toil
from toil.job import Job
import click

from {{cookiecutter.project_slug}} import jobs
from {{cookiecutter.project_slug}} import parsers


def run_toil(options):
    """Toil implementation for {{cookiecutter.project_slug}}."""
    helloworld = jobs.HelloWorld(
        cores=4,
        memory="12G",
        options=options,
        unitName="Hello World",
        lsf_tags=["SHORT"]
        )

    helloworld_message = jobs.HelloWorldMessage(
        message=options.message,
        cores=4,
        memory="12G",
        options=options,
        unitName="Hello World with Message",
        lsf_tags=["INTERNET"]
        )

    # Build pipeline DAG.
    helloworld.addChild(helloworld_message)

    # Execute the pipeline.
    with Toil(options) as pipe:
        if not pipe.options.restart:
            pipe.start(helloworld)
        else:
            pipe.restart()


def get_parser():
    """Get pipeline configuration using toil's."""
    parser = parsers.ToilArgumentParser()

    # Add description to parser.
    parser.description = "Run {{cookiecutter.project_slug}} pipeline."

    # We need to add a group of arguments specific to the pipeline.
    settings = parser.add_argument_group("{{cookiecutter.project_slug}} configuration")

    settings.add_argument(
        "--message",
        help="A message to be echoed to the Universe.",
        required=False,
        default="Hello Universe, this text is used in the pipeline tests.",
        )

    settings.add_argument(
        "--total",
        help="Total times message should be printed.",
        required=False,
        default=1,
        type=int,
        )

    settings.add_argument(
        "--outfile",
        help="Outfile to print message to.",
        required=True,
        type=click.Path(file_okay=True, writable=True),
        )

    return parser


def process_parsed_options(options):
    """Perform validations and add post parsing attributes to `options`."""
    if options.writeLogs is not None:
        subprocess.check_call(["mkdir", "-p", options.writeLogs])

    # This is just an example of how to post process variables after parsing.
    options.message = options.message * options.total

    return options


def main():
    """Parse options and run toil."""
    options = get_parser().parse_args()
    options = process_parsed_options(options=options)
    run_toil(options=options)

if __name__ == "__main__":
    main()
