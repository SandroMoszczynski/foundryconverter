import typer
from foundryconverter.export_formats.dungeon_alchemist.converter import (
    ConvertDAToFoundry,
)
from foundryconverter.export_formats.types import SetupVariables
from foundryconverter.export_formats.dd2vtt.converter import ConvertDD2ToFoundry
import json


def conversion_factory(input_type, output_type):
    converters: dict[str, dict[str, type[ConvertDD2ToFoundry | ConvertDAToFoundry]]] = {
        "foundry": {
            "dungeon_alchemist": ConvertDAToFoundry,
            "dd2vtt": ConvertDD2ToFoundry,
        }
    }
    return converters[input_type][output_type]


def convert(raw_config_data_location: str):
    with open(raw_config_data_location) as json_data:
        setup_data = SetupVariables(**json.load(json_data))
    converter = conversion_factory(setup_data.input_format, setup_data.export_format)
    convert = converter(setup_data.config_dict)
    data = convert.setup_objects()
    convert.save_to_file(
        data=data, file_name=setup_data.config_dict.return_final_name()
    )


convert_app = typer.Typer()
convert_app.command()(convert)

if __name__ == "__main__":
    convert_app()
