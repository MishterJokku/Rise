from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
)
from PySide6.QtCore import Qt

from core.database import get_dashboard_data


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.data = get_dashboard_data() or {}

        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
            }

            QLabel {
                border: none;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(22)

        user_name = self.data.get("user_name") or "there"

        header = QLabel(f"Good Morning, {user_name}")
        header.setStyleSheet("""
            font-size: 30px;
            font-weight: 700;
            color: #ffffff;
            border: none;
        """)

        tagline = QLabel("Small steps. Visible progress.")
        tagline.setStyleSheet("""
            font-size: 15px;
            color: #94a3b8;
            border: none;
        """)

        layout.addWidget(header)
        layout.addWidget(tagline)

        next_step = self.create_card(
            "Next Step",
            "Complete today's check-in",
            "Reason: Rise needs today's data to show real progress.\nImpact: Keeps your roadmap accurate."
        )
        layout.addWidget(next_step)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(18)

        cards_row.addWidget(self.create_card(
            "Health",
            self.get_health_main_text(),
            self.get_health_detail_text()
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

    def get_health_main_text(self):
        current_weight = self.data.get("current_weight")
        goal_weight = self.data.get("goal_weight")

        if current_weight is None or goal_weight is None:
            return "No weight goal"

        return f"{current_weight:.1f} kg → {goal_weight:.1f} kg"

    def get_health_detail_text(self):
        progress = self.data.get("weight_progress", 0)
        calories = self.data.get("calories")
        protein = self.data.get("protein")

        calorie_text = f"{calories} kcal" if calories is not None else "Not logged today"
        protein_text = f"{protein}g" if protein is not None else "Not logged today"

        return (
            f"Progress: {progress}%\n"
            f"Calories: {calorie_text}\n"
            f"Protein: {protein_text}"
        )

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
            border: none;
        """)

        main_label = QLabel(main_text)
        main_label.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #ffffff;
            border: none;
        """)

        detail_label = QLabel(detail_text)
        detail_label.setWordWrap(True)
        detail_label.setStyleSheet("""
            font-size: 13px;
            color: #cbd5e1;
            border: none;
        """)

        layout.addWidget(title_label)
        layout.addWidget(main_label)
        layout.addWidget(detail_label)
        layout.addStretch()

        return card