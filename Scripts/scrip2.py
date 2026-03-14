# prod_script.py
import click

@click.command()
@click.option("--name", default="mario")
def main(name: str):
    click.echo(f"Soy el script de PRO2, hola {name}")

if __name__ == "__main__":
    main()