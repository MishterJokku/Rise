import sys
from PySide6.QtWidgets import QApplication

from core.database import initialize_database, has_user_profile
from ui.main_window import MainWindow


def main():
    initialize_database()

    app = QApplication(sys.argv)

    window = MainWindow(show_onboarding=not has_user_profile())
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()