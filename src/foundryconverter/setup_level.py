import typer
from pydantic import BaseModel


class SetupVariables(BaseModel):
    input_format: str
    export_format: str
    final_location: str
    folder_location: str


def setup_level():
    # take in parameters and then save them to a json file at the oppropirate place
    pass


setup_level_app = typer.Typer()
setup_level_app.command()(setup_level)

if __name__ == "__main__":
    setup_level_app()
