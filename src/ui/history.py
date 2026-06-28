from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.database import get_checkin_history


class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.entries = get_checkin_history()

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

        title = QLabel("History")
        title.setStyleSheet("""
            font-size: 30px;
            font-weight: 700;
            color: #ffffff;
            border: none;
        """)

        subtitle = QLabel("Your recent daily check-ins.")
        subtitle.setStyleSheet("""
            font-size: 15px;
            color: #94a3b8;
            border: none;
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        if not self.entries:
            layout.addWidget(self.create_empty_state())
        else:
            layout.addWidget(self.create_history_table())

        layout.addStretch()

    def create_empty_state(self):
        card = QFrame()
        card.setMinimumHeight(150)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)

        message = QLabel("No check-ins yet. Save your first daily check-in from the dashboard.")
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

    def create_history_table(self):
        columns = [
            "Date",
            "Weight",
            "Calories",
            "Protein",
            "Mood",
            "Energy",
            "Stress",
            "Sleep",
            "Notes",
        ]

        table = QTableWidget(len(self.entries), len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setAlternatingRowColors(False)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(True)

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.Stretch)

        for row_index, entry in enumerate(self.entries):
            values = [
                entry["date"],
                self.format_decimal(entry["weight"], " kg"),
                self.format_integer(entry["calories"], " kcal"),
                self.format_decimal(entry["protein"], " g"),
                self.format_score(entry["mood"]),
                self.format_score(entry["energy"]),
                self.format_score(entry["stress"]),
                self.format_decimal(entry["sleep_hours"], " hours"),
                entry["notes"] or "",
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                if column_index != 8:
                    item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_index, column_index, item)

        table.resizeRowsToContents()

        return table

    def format_decimal(self, value, suffix):
        if value is None:
            return "--"

        return f"{value:.1f}{suffix}"

    def format_integer(self, value, suffix):
        if value is None:
            return "--"

        return f"{value}{suffix}"

    def format_score(self, value):
        if value is None:
            return "--"

        return f"{value} / 10"
