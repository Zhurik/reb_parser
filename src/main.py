import sys
import os

RESOURCES_PATH = None

# Определяем, что проект запускается из EXEшника
# Необходимо делать это перед импортом PyQt5, иначе не будет запускаться
# без установленного Qt на компьютере
if hasattr(sys, "frozen") and hasattr(sys, "_MEIPASS"):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
    RESOURCES_PATH = "./resources/"
else:
    RESOURCES_PATH = "../resources/"

import argparse

import matplotlib
matplotlib.use("Qt5Agg")

from typing import List

from PyQt5 import QtWidgets

from window import MainWindow, CustomGridLayout


def process_arguments(argv: List[str]) -> argparse.Namespace:
    """Обрабатываем параметры командной строки"""

    parser = argparse.ArgumentParser(
        prog="REB Parser",
        description="Программа для обработки REB файлов"
    )

    parser.add_argument(
        "--light",
        dest="light",
        nargs="?",
        default=False,
        const=True,
        help="Запуск программы в легковесном режиме",
        metavar=""
    )

    return parser.parse_args(argv)


def recources_exist(
    argv: argparse.Namespace,
    resources: str
) -> bool:
    """Проверяем существование необходимых для работы файлов и папок"""

    if not os.path.exists(resources):
        print("Не найдена папка ресурсов!")
        print("Заканчиваю работу")
        return False

    if not os.path.exists(resources + "stations.json"):
        print("Не найдена база станций!")
        print("Заканчиваю работу!")
        return False

    if not os.path.exists(resources + "chunks"):
        print("Не найдена папка с частями карты!")
        print("Запускаю программу в легковесном режиме!")
        argv.light = True

    return True


def main():
    argv = process_arguments(sys.argv[1:])

    if not recources_exist(
        argv,
        RESOURCES_PATH
    ):
        input()
        return

    qt_app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow(
        "REB Parser",
        CustomGridLayout,
        argv,
        RESOURCES_PATH
    )

    main_window.show()
    sys.exit(qt_app.exec_())


if __name__ == "__main__":
    main()
