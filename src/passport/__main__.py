"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Passport."""


if __name__ == "__main__":
    main(prog_name="passport")  # pragma: no cover
