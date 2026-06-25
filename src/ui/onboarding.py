from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QMessageBox,
    QFrame,
)

from core.database import create_initial_profile


class OnboardingPage(QWidget):
    completed = Signal()

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #e5e7eb;
                font-family: Segoe UI;
            }

            QLabel {
                color: #e5e7eb;
            }

            QLineEdit,
            QSpinBox,
            QDoubleSpinBox {
                background-color: #111827;
                color: #ffffff;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }

            QPushButton {
                background-color: #22c55e;
                color: #052e16;
                border: none;
                border-radius: 10px;
                padding: 12px 18px;
                font-size: 14px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #4ade80;
            }
        """)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setMaximumWidth(560)
        card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 18px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 30, 32, 30)
        card_layout.setSpacing(14)

        title = QLabel("Welcome to Rise")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: 800;
            color: #ffffff;
            border: none;
        """)

        subtitle = QLabel("Small steps. Visible progress.")
        subtitle.setStyleSheet("""
            font-size: 15px;
            color: #94a3b8;
            border: none;
        """)

        privacy = QLabel(
            "Everything is stored locally on this computer.\n"
            "No account required. No cloud required."
        )
        privacy.setStyleSheet("""
            font-size: 13px;
            color: #cbd5e1;
            border: none;
        """)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")

        self.age_input = QSpinBox()
        self.age_input.setRange(1, 120)
        self.age_input.setValue(27)
        self.age_input.setSuffix(" years")

        self.height_input = QDoubleSpinBox()
        self.height_input.setRange(50, 250)
        self.height_input.setValue(162)
        self.height_input.setSuffix(" cm")

        self.current_weight_input = QDoubleSpinBox()
        self.current_weight_input.setRange(20, 300)
        self.current_weight_input.setValue(72)
        self.current_weight_input.setSuffix(" kg")

        self.goal_weight_input = QDoubleSpinBox()
        self.goal_weight_input.setRange(20, 300)
        self.goal_weight_input.setValue(65)
        self.goal_weight_input.setSuffix(" kg")

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(privacy)

        card_layout.addSpacing(12)

        card_layout.addWidget(self.create_field_label("Name"))
        card_layout.addWidget(self.name_input)

        card_layout.addWidget(self.create_field_label("Age"))
        card_layout.addWidget(self.age_input)

        card_layout.addWidget(self.create_field_label("Height"))
        card_layout.addWidget(self.height_input)

        card_layout.addWidget(self.create_field_label("Current Weight"))
        card_layout.addWidget(self.current_weight_input)

        card_layout.addWidget(self.create_field_label("Goal Weight"))
        card_layout.addWidget(self.goal_weight_input)

        card_layout.addSpacing(10)

        start_button = QPushButton("Enter Rise")
        start_button.clicked.connect(self.save_profile)
        card_layout.addWidget(start_button)

        center_row = QHBoxLayout()
        center_row.addStretch()
        center_row.addWidget(card)
        center_row.addStretch()

        outer_layout.addStretch()
        outer_layout.addLayout(center_row)
        outer_layout.addStretch()

    def create_field_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
            font-size: 13px;
            font-weight: 600;
            color: #94a3b8;
            border: none;
        """)
        return label

    def save_profile(self):
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Name required", "Please enter your name.")
            return

        age = self.age_input.value()
        height = self.height_input.value()
        current_weight = self.current_weight_input.value()
        goal_weight = self.goal_weight_input.value()

        if current_weight == goal_weight:
            QMessageBox.warning(
                self,
                "Goal needed",
                "Current weight and goal weight should be different."
            )
            return

        create_initial_profile(
            name=name,
            age=age,
            height_cm=height,
            current_weight=current_weight,
            goal_weight=goal_weight,
        )

        self.completed.emit()