import typer
from pathlib import Path
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QGridLayout,
    QPushButton,
    QListWidget,
    QLabel,
    QFileDialog,
    QWidget,
    QApplication,
    QListWidgetItem,
    QLineEdit,
)
import os
from foundryconverter.export_formats.types import (
    BaseConverterConfig,
    FloorObject,
    SetupVariables,
)
import sys
import json
from foundryconverter.convert import conversion_factory, convert


class MainWindow(QWidget):
    config_object: BaseConverterConfig
    setup_variables: SetupVariables
    setup_file = "setup_data.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("PyQt File Dialog")
        self.setGeometry(100, 100, 300, 150)
        layout = QGridLayout()
        self.setLayout(layout)

        # various buttons
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)

        convert_button = QPushButton("Convert")
        convert_button.clicked.connect(self.convert)

        # height inputs
        self.start_height = QLineEdit()
        self.start_height.setValidator(QIntValidator())
        start_label = QLabel("Enter start height:", self)
        self.wall_height = QLineEdit()
        self.wall_height.setValidator(QIntValidator())
        height_label = QLabel("Enter wall height:", self)

        # file selection
        file_browser_btn = QPushButton("Browse")
        file_browser_btn.clicked.connect(self.open_file_dialog)
        self.file_list = QListWidget(self)

        # import/export choices
        self.import_choice, import_label = self.create_import_choice()
        self.export_choice, export_label = self.create_export_choice()

        # layout setup
        layout.addWidget(QLabel("Files:"), 0, 0)
        layout.addWidget(self.file_list, 1, 0, 1, 2)
        layout.addWidget(file_browser_btn, 2, 0, 1, 2)
        layout.addWidget(start_label, 3, 0)
        layout.addWidget(height_label, 3, 1)
        layout.addWidget(self.start_height, 4, 0)
        layout.addWidget(self.wall_height, 4, 1)
        layout.addWidget(import_label, 5, 0)
        layout.addWidget(export_label, 5, 1)
        layout.addWidget(self.import_choice, 6, 0)
        layout.addWidget(self.export_choice, 6, 1)
        layout.addWidget(save_button, 7, 0, 1, 2)
        layout.addWidget(convert_button, 8, 0, 1, 2)

        self.show()

    def create_import_choice(self):
        list_widget = QListWidget(self)
        list_widget.setGeometry(50, 70, 150, 60)
        current_choices = [{"label": "foundry", "value": "foundry"}]
        for choice in current_choices:
            list_widget.addItem(QListWidgetItem(choice["label"]))
        label = QLabel("Select to what file type to create", self)
        return list_widget, label

    def create_export_choice(self):
        list_widget = QListWidget(self)
        list_widget.setGeometry(50, 70, 150, 60)
        current_choices = [
            {"label": "dungeon_alchemist", "value": "json"},
            {"label": "dd2vtt", "value": "dd2vtt"},
        ]
        for choice in current_choices:
            list_widget.addItem(QListWidgetItem(choice["label"]))
        label = QLabel("Select which file type you have", self)
        return list_widget, label

    def save(self):
        start_height = int(self.start_height.text())
        wall_height = int(self.wall_height.text())
        import_choice = self.import_choice.takeItem(0).text()
        export_choice = self.export_choice.takeItem(0).text()
        floors = []
        for i in range(self.file_list.count()):
            floor = FloorObject(
                json_location=self.file_list.takeItem(0).text(),
                start_height=start_height + (i * wall_height),
                end_height=start_height + ((i + 1) * wall_height),
            )
            floors.append(floor)

        converter = conversion_factory(import_choice, export_choice)
        self.config_object = converter.config_class(
            file_name="test.json",
            final_location=os.getcwd(),
            floors=self.file_list.count(),
            initial_level=0,
            wall_height=wall_height,
            map_name="test combined maps",
            floor_objects=floors,
        )
        variables = SetupVariables(
            input_format=import_choice,
            export_format=export_choice,
            final_location=os.getcwd(),
            config_dict=self.config_object,
        )
        with open(self.setup_file, "w") as final_write:
            json.dump(variables.model_dump(), final_write)

    def convert(self):
        convert(self.setup_file)

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Files (*.json *.dd2vtt)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            if filenames := dialog.selectedFiles():
                self.file_list.addItems([str(Path(filename)) for filename in filenames])


def setup_level():
    # take in parameters and then save them to a json file at the oppropirate place
    app = QApplication([])

    widget = MainWindow()
    widget.resize(1200, 800)
    widget.show()

    sys.exit(app.exec())


setup_level_app = typer.Typer()
setup_level_app.command()(setup_level)

if __name__ == "__main__":
    setup_level_app()
