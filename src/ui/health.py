from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QGridLayout,
    QHeaderView,
    QLabel,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.database import get_health_summary, get_weight_history


class HealthPage(QWidget):
    def __init__(self):
        super().__init__()

        self.summary = get_health_summary()
        self.weight_history = get_weight_history()

        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #e5e7eb;
                font-family: Segoe UI;
            }

            QLabel {
                border: none;
            }

            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 14px;
            }

            QProgressBar {
                background-color: #111827;
                border: 1px solid #334155;
                border-radius: 8px;
                color: #ffffff;
                height: 20px;
                text-align: center;
                font-weight: 700;
            }

            QProgressBar::chunk {
                background-color: #22c55e;
                border-radius: 7px;
            }

            QTableWidget {
                background-color: #111827;
                color: #e5e7eb;
                border: 1px solid #334155;
                border-radius: 8px;
                gridline-color: #334155;
                selection-background-color: #334155;
                selection-color: #ffffff;
            }

            QHeaderView::section {
                background-color: #1e293b;
                color: #94a3b8;
                border: none;
                border-bottom: 1px solid #334155;
                padding: 8px;
                font-size: 13px;
                font-weight: 700;
            }

            QTableWidget::item {
                border: none;
                padding: 6px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 20, 28, 20)
        layout.setSpacing(14)

        title = QLabel("Health")
        title.setStyleSheet("""
            font-size: 30px;
            font-weight: 700;
            color: #ffffff;
            border: none;
        """)

        subtitle = QLabel("Body weight progress from your local check-ins.")
        subtitle.setStyleSheet("""
            font-size: 15px;
            color: #94a3b8;
            border: none;
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        if self.summary is None:
            layout.addWidget(self.create_empty_state())
        else:
            layout.addWidget(self.create_progress_card())
            layout.addWidget(self.create_weight_history_section())

        layout.addStretch()

    def create_empty_state(self):
        card = QFrame()
        card.setMinimumHeight(160)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)

        message = QLabel("No weight goal yet. Complete onboarding to create your first body weight goal.")
        message.setWordWrap(True)
        message.setAlignment(Qt.AlignCenter)
        message.setStyleSheet("""
            font-size: 15px;
            color: #cbd5e1;
            border: none;
        """)

        layout.addStretch()
        layout.addWidget(message)
        layout.addStretch()

        return card

    def create_progress_card(self):
        card = QFrame()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        title = QLabel("Weight Progress")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #ffffff;
            border: none;
        """)
        layout.addWidget(title)

        progress = QProgressBar()
        progress.setRange(0, 100)
        progress.setValue(round(self.summary["weight_progress"]))
        progress.setFormat(f"{self.summary['weight_progress']}%")
        layout.addWidget(progress)

        details = QGridLayout()
        details.setHorizontalSpacing(18)
        details.setVerticalSpacing(12)

        details.addWidget(self.create_metric("Current Weight", self.format_weight(self.summary["current_weight"])), 0, 0)
        details.addWidget(self.create_metric("Start Weight", self.format_weight(self.summary["start_weight"])), 0, 1)
        details.addWidget(self.create_metric("Goal Weight", self.format_weight(self.summary["goal_weight"])), 0, 2)
        details.addWidget(self.create_metric("Remaining", self.format_weight(self.summary["remaining_weight"])), 1, 0)
        details.addWidget(self.create_metric("Latest Log", self.summary["latest_weight_date"] or "--"), 1, 1)
        details.addWidget(self.create_metric("Progress", f"{self.summary['weight_progress']}%"), 1, 2)

        layout.addLayout(details)

        return card

    def create_metric(self, label_text, value_text):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        label = QLabel(label_text)
        label.setStyleSheet("""
            font-size: 13px;
            font-weight: 600;
            color: #94a3b8;
            border: none;
        """)

        value = QLabel(value_text)
        value.setStyleSheet("""
            font-size: 21px;
            font-weight: 700;
            color: #ffffff;
            border: none;
        """)

        layout.addWidget(label)
        layout.addWidget(value)

        return container

    def create_weight_history_section(self):
        card = QFrame()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        title = QLabel("Recent Weight Entries")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #ffffff;
            border: none;
        """)
        layout.addWidget(title)

        if not self.weight_history:
            empty = QLabel("No weight entries yet.")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("""
                font-size: 14px;
                color: #cbd5e1;
                border: none;
            """)
            layout.addWidget(empty)
        else:
            layout.addWidget(self.create_weight_table())

        return card

    def create_weight_table(self):
        table = QTableWidget(len(self.weight_history), 2)
        table.setHorizontalHeaderLabels(["Date", "Weight"])
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(True)

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        for row_index, entry in enumerate(self.weight_history):
            values = [
                entry["date"],
                self.format_weight(entry["weight"]),
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_index, column_index, item)

        table.resizeRowsToContents()

        return table

    def format_weight(self, value):
        if value is None:
            return "--"

        return f"{value:.1f} kg"
