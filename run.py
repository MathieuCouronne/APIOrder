import click
from src import create_app
from src.config.database import init_db
from src.services.product_service import fetch_and_store_products

app = create_app()

@click.command("init-db")
def init_db_command():
    init_db()
    fetch_and_store_products()


app.cli.add_command(init_db_command)


if __name__ == "__main__":
    app.run(debug=True)