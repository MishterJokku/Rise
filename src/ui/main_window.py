from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt

from ui.dashboard import DashboardPage
from ui.health import HealthPage
from ui.history import HistoryPage
from ui.onboarding import OnboardingPage


class MainWindow(QMainWindow):
    def __init__(self, show_onboarding=False):
        super().__init__()

        self.setWindowTitle("Rise")
        self.setMinimumSize(1100, 700)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }

            QLabel {
                color: #e5e7eb;
                font-family: Segoe UI;
            }

            QPushButton {
                background-color: transparent;
                color: #cbd5e1;
                border: none;
                text-align: left;
                padding: 12px 16px;
                font-size: 14px;
                border-radius: 8px;
            }

            QPushButton:hover {
                background-color: #1e293b;
                color: #ffffff;
            }
        """)

        if show_onboarding:
            self.show_onboarding()
        else:
            self.show_main_app()

    def show_onboarding(self):
        onboarding = OnboardingPage()
        onboarding.completed.connect(self.show_main_app)
        self.setCentralWidget(onboarding)

    def show_main_app(self):
        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = self.create_sidebar()
        self.page_container = QWidget()
        self.page_layout = QVBoxLayout(self.page_container)
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.page_layout.setSpacing(0)

        root_layout.addWidget(sidebar)
        root_layout.addWidget(self.page_container, 1)

        self.setCentralWidget(root)
        self.show_dashboard()

    def show_dashboard(self):
        self.set_page(DashboardPage())

    def show_health(self):
        self.set_page(HealthPage())

    def show_history(self):
        self.set_page(HistoryPage())

    def set_page(self, page):
        while self.page_layout.count():
            item = self.page_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.page_layout.addWidget(page)

    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(230)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #020617;
                border-right: 1px solid #1e293b;
            }
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 24, 18, 24)
        layout.setSpacing(10)

        title = QLabel("Rise")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
        """)

        subtitle = QLabel("Life Progress System")
        subtitle.setStyleSheet("""
            font-size: 12px;
            color: #94a3b8;
            margin-bottom: 20px;
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        nav_items = [
            "Dashboard",
            "Health",
            "Mind",
            "Projects",
            "Finance",
            "History",
            "Settings",
        ]

        for item in nav_items:
            button = QPushButton(item)
            if item == "Dashboard":
                button.clicked.connect(self.show_dashboard)
            elif item == "Health":
                button.clicked.connect(self.show_health)
            elif item == "History":
                button.clicked.connect(self.show_history)
            layout.addWidget(button)

        layout.addStretch()

        footer = QLabel("Offline First")
        footer.setAlignment(Qt.AlignLeft)
        footer.setStyleSheet("""
            color: #64748b;
            font-size: 12px;
        """)

        layout.addWidget(footer)

        return sidebar
