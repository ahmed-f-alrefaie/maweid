"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Maweid."""


if __name__ == "__main__":
    main(prog_name="maweid")  # pragma: no cover
