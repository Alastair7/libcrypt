import click


@click.group()
def main() -> None:
    """Test CLI group."""
    pass


@click.command("sum")
@click.argument("x")
@click.argument("y")
def sum_command(x: str, y: str) -> None:
    """Add two numbers."""
    result = int(x) + int(y)
    click.echo(f"Result: {result}")


@click.command("hello")
@click.argument("name")
def hello_command(name: str) -> None:
    """Greet a person."""
    click.echo(f"Hello, {name}!")


main.add_command(sum_command)
main.add_command(hello_command)


if __name__ == "__main__":
    main()