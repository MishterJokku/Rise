from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
    QDoubleSpinBox,
    QSpinBox,
    QTextEdit,
    QPushButton,
    QMessageBox,
)

from core.database import get_dashboard_data, get_today_checkin_data, save_daily_checkin


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.data = get_dashboard_data() or {}
        self.today_data = get_today_checkin_data() or {}

        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #e5e7eb;
                font-family: Segoe UI;
            }

            QLabel {
                border: none;
            }

            QDoubleSpinBox,
            QSpinBox,
            QTextEdit {
                background-color: #111827;
                color: #ffffff;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
            }

            QTextEdit {
                min-height: 54px;
            }

            QPushButton {
                background-color: #22c55e;
                color: #052e16;
                border: none;
                border-radius: 10px;
                padding: 11px 18px;
                font-size: 14px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #4ade80;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 20, 28, 20)
        layout.setSpacing(14)

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
        layout.addWidget(self.create_card_frame(
            "Next Step",
            "Complete today's check-in",
            "Reason: Rise needs today's data to show real progress.\nImpact: Keeps your roadmap accurate."
        ))
        layout.addWidget(self.create_checkin_card())

        cards_row = QHBoxLayout()
        cards_row.setSpacing(18)

        self.health_card = self.create_card(
            "Health",
            self.get_health_main_text(),
            self.get_health_detail_text()
        )
        cards_row.addWidget(self.health_card["frame"])

        self.mind_card = self.create_card(
            "Mind",
            self.get_mind_main_text(),
            self.get_mind_detail_text()
        )
        cards_row.addWidget(self.mind_card["frame"])

        cards_row.addWidget(self.create_card_frame(
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

        return f"{current_weight:.1f} kg -> {goal_weight:.1f} kg"

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

    def get_mind_main_text(self):
        mood = self.data.get("mood")

        if mood is None:
            return "Daily check-in pending"

        return f"Mood: {mood} / 10"

    def get_mind_detail_text(self):
        energy = self.data.get("energy")
        stress = self.data.get("stress")
        sleep_hours = self.data.get("sleep_hours")

        energy_text = f"{energy} / 10" if energy is not None else "-- / 10"
        stress_text = f"{stress} / 10" if stress is not None else "-- / 10"
        sleep_text = f"{sleep_hours:.1f} hours" if sleep_hours is not None else "-- hours"

        return (
            f"Energy: {energy_text}\n"
            f"Stress: {stress_text}\n"
            f"Sleep: {sleep_text}"
        )

    def create_checkin_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 14px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(10)

        title = QLabel("Daily Check-In")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #ffffff;
            border: none;
        """)
        layout.addWidget(title)

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(14)
        form_layout.setVerticalSpacing(10)

        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(20, 300)
        self.weight_input.setDecimals(1)
        self.weight_input.setSuffix(" kg")

        self.calories_input = QSpinBox()
        self.calories_input.setRange(0, 10000)
        self.calories_input.setSuffix(" kcal")

        self.protein_input = QDoubleSpinBox()
        self.protein_input.setRange(0, 500)
        self.protein_input.setDecimals(1)
        self.protein_input.setSuffix(" g")

        self.mood_input = self.create_score_input()
        self.energy_input = self.create_score_input()
        self.stress_input = self.create_score_input()

        self.sleep_input = QDoubleSpinBox()
        self.sleep_input.setRange(0, 24)
        self.sleep_input.setDecimals(1)
        self.sleep_input.setSingleStep(0.5)
        self.sleep_input.setSuffix(" hours")

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notes")

        self.add_form_field(form_layout, 0, 0, "Weight", self.weight_input)
        self.add_form_field(form_layout, 0, 1, "Calories", self.calories_input)
        self.add_form_field(form_layout, 0, 2, "Protein", self.protein_input)
        self.add_form_field(form_layout, 1, 0, "Mood", self.mood_input)
        self.add_form_field(form_layout, 1, 1, "Energy", self.energy_input)
        self.add_form_field(form_layout, 1, 2, "Stress", self.stress_input)
        self.add_form_field(form_layout, 2, 0, "Sleep", self.sleep_input)

        notes_column = QVBoxLayout()
        notes_column.setSpacing(6)
        notes_column.addWidget(self.create_field_label("Notes"))
        notes_column.addWidget(self.notes_input)
        form_layout.addLayout(notes_column, 2, 1, 1, 2)

        layout.addLayout(form_layout)

        button_row = QHBoxLayout()
        button_row.addStretch()
        save_button = QPushButton("Save Today")
        save_button.clicked.connect(self.save_today)
        button_row.addWidget(save_button)
        layout.addLayout(button_row)

        self.prefill_checkin_form()

        return card

    def create_score_input(self):
        score_input = QSpinBox()
        score_input.setRange(1, 10)
        score_input.setSuffix(" / 10")
        return score_input

    def create_field_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
            font-size: 13px;
            font-weight: 600;
            color: #94a3b8;
            border: none;
        """)
        return label

    def add_form_field(self, form_layout, row, column, label_text, widget):
        field_layout = QVBoxLayout()
        field_layout.setSpacing(6)
        field_layout.addWidget(self.create_field_label(label_text))
        field_layout.addWidget(widget)
        form_layout.addLayout(field_layout, row, column)

    def prefill_checkin_form(self):
        weight = self.today_data.get("weight")
        if weight is None:
            weight = self.data.get("current_weight")

        if weight is not None:
            self.weight_input.setValue(weight)

        if self.today_data.get("calories") is not None:
            self.calories_input.setValue(self.today_data["calories"])

        if self.today_data.get("protein") is not None:
            self.protein_input.setValue(self.today_data["protein"])

        if self.today_data.get("mood") is not None:
            self.mood_input.setValue(self.today_data["mood"])

        if self.today_data.get("energy") is not None:
            self.energy_input.setValue(self.today_data["energy"])

        if self.today_data.get("stress") is not None:
            self.stress_input.setValue(self.today_data["stress"])

        if self.today_data.get("sleep_hours") is not None:
            self.sleep_input.setValue(self.today_data["sleep_hours"])

        self.notes_input.setPlainText(self.today_data.get("notes") or "")

    def save_today(self):
        save_daily_checkin(
            weight=self.weight_input.value(),
            calories=self.calories_input.value(),
            protein=self.protein_input.value(),
            mood=self.mood_input.value(),
            energy=self.energy_input.value(),
            stress=self.stress_input.value(),
            sleep_hours=self.sleep_input.value(),
            notes=self.notes_input.toPlainText().strip(),
        )

        self.refresh_dashboard_data()
        QMessageBox.information(self, "Saved", "Today's check-in has been saved.")

    def refresh_dashboard_data(self):
        self.data = get_dashboard_data() or {}
        self.today_data = get_today_checkin_data() or {}

        self.health_card["main"].setText(self.get_health_main_text())
        self.health_card["detail"].setText(self.get_health_detail_text())
        self.mind_card["main"].setText(self.get_mind_main_text())
        self.mind_card["detail"].setText(self.get_mind_detail_text())

    def create_card_frame(self, title, main_text, detail_text):
        return self.create_card(title, main_text, detail_text)["frame"]

    def create_card(self, title, main_text, detail_text):
        card = QFrame()
        card.setMinimumHeight(120)
        card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 14px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(6)

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

        return {
            "frame": card,
            "main": main_label,
            "detail": detail_label,
        }
