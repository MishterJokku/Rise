from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
)
from PySide6.QtCore import Qt


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(22)

        header = QLabel("Good Morning, Jishnu")
        header.setStyleSheet("""
            font-size: 30px;
            font-weight: 700;
            color: #ffffff;
        """)

        tagline = QLabel("Small steps. Visible progress.")
        tagline.setStyleSheet("""
            font-size: 15px;
            color: #94a3b8;
        """)

        layout.addWidget(header)
        layout.addWidget(tagline)

        next_step = self.create_card(
            "Next Step",
            "Walk for 15 minutes",
            "Reason: This keeps your health goal moving forward.\nImpact: +1 Health XP"
        )
        layout.addWidget(next_step)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(18)

        cards_row.addWidget(self.create_card(
            "Health",
            "72.0 kg → 65.0 kg",
            "Progress: 0%\nCalories: Not logged today"
        ))

        cards_row.addWidget(self.create_card(
            "Mind",
            "Daily check-in pending",
            "Mood: -- / 10\nEnergy: -- / 10\nSleep: -- hours"
        ))

        cards_row.addWidget(self.create_card(
            "Projects",
            "Rise App",
            "Today: 0 minutes\nWeekly XP: 0"
        ))

        layout.addLayout(cards_row)
        layout.addStretch()

    def create_card(self, title, main_text, detail_text):
        card = QFrame()
        card.setMinimumHeight(150)
        card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 14px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #94a3b8;
        """)

        main_label = QLabel(main_text)
        main_label.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #ffffff;
        """)

        detail_label = QLabel(detail_text)
        detail_label.setWordWrap(True)
        detail_label.setStyleSheet("""
            font-size: 13px;
            color: #cbd5e1;
            line-height: 1.4;
        """)

        layout.addWidget(title_label)
        layout.addWidget(main_label)
        layout.addWidget(detail_label)
        layout.addStretch()

        return card