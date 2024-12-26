import sys
import time
import random
import string
from enum import Enum
from typing import Tuple

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QSplitter,
    QTextEdit,
    QDoubleSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut

class GameState(Enum):
    GAMESTART = 1
    PLAYING = 2
    PAUSED = 3

class Asteroid:
    existing_ids = set()

    def generate_unique_alphanumeric_id(length=7):
        while True:
            new_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
            if new_id not in Asteroid.existing_ids:
                Asteroid.existing_ids.add(new_id)
                return new_id

    def __init__(self, position: Tuple[float, float, float], velocity: Tuple[float, float, float], raw_mass: float, purity: float):
        self.id = Asteroid.generate_unique_alphanumeric_id()
        self.position = position
        self.velocity = velocity
        self.raw_mass = raw_mass
        self.purity = purity

    @property
    def material_mass(self) -> float:
        return self.raw_mass * self.purity

    def update(self, dt: float):
        x, y, z = self.position
        vx, vy, vz = self.velocity
        self.position = (x + vx * dt, y + vy * dt, z + vz * dt)

    def mine(self, amount: float) -> float:
        mined_mass = min(amount, self.raw_mass)
        self.raw_mass -= mined_mass
        return mined_mass * self.purity

    @classmethod
    def generate_random_asteroid(
        cls,
        position_range: Tuple[float, float] = (-100, 100),
        velocity_range: Tuple[float, float] = (-1, 1),
        mass_range: Tuple[float, float] = (10, 100),
        purity_range: Tuple[float, float] = (0.1, 0.8),
    ) -> "Asteroid":
        position = (
            random.uniform(*position_range),
            random.uniform(*position_range),
            random.uniform(*position_range),
        )
        velocity = (
            random.uniform(*velocity_range),
            random.uniform(*velocity_range),
            random.uniform(*velocity_range),
        )
        mass = random.uniform(*mass_range)
        purity = random.uniform(*purity_range)

        return cls(position, velocity, mass, purity)

# --- Model ---
class SpaceSimModel(QObject):
    game_state_changed = pyqtSignal(GameState)
    time_updated = pyqtSignal(float)
    asteroid_data_updated = pyqtSignal(list)
    fuel_updated = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.fuel = 100
        self.total_seconds = 0.0
        self.time_scale = 1.0
        self.current_game_state = GameState.GAMESTART
        self.asteroids = [Asteroid.generate_random_asteroid() for _ in range(5)]

    def update(self, dt: float):
        if self.current_game_state == GameState.PLAYING:
            self.total_seconds += dt * self.time_scale
            self.time_updated.emit(self.total_seconds)

            for asteroid in self.asteroids:
                asteroid.update(dt * self.time_scale)
            self.asteroid_data_updated.emit(self.asteroids)

    def set_game_state(self, state: GameState):
        self.current_game_state = state
        self.game_state_changed.emit(self.current_game_state)

    def set_time_scale(self, scale: float):
        self.time_scale = scale

    def launch_ship(self):
        if self.fuel > 0:
            self.fuel -= 10
            self.fuel_updated.emit(self.fuel)
            return "Launching ship! Fuel remaining: {}%".format(self.fuel)
        else:
            return "Not enough fuel to launch!"

# --- Controller ---
class SpaceSimController(QObject):
    def __init__(self, model: SpaceSimModel):
        super().__init__()
        self.model = model
        self.target_fps = 60
        self.game_timer = QTimer(self)
        self.game_timer.setInterval(int(1000 / self.target_fps))
        self.game_timer.timeout.connect(self.update_game)
        self.game_timer.start()

    def update_game(self):
        dt = 1 / self.target_fps
        self.model.update(dt)

    def start_pause_game(self):
        if self.model.current_game_state == GameState.PLAYING:
            self.model.set_game_state(GameState.PAUSED)
        elif self.model.current_game_state == GameState.PAUSED:
            self.model.set_game_state(GameState.PLAYING)

    def set_time_scale(self, scale: float):
        self.model.set_time_scale(scale)

    def launch_ship(self):
       message = self.model.launch_ship()
       return message

# --- View ---
class SpaceSimUI(QWidget):
    def __init__(self, controller: SpaceSimController):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Space Simulation Game, v.001")

        # Show welcome message before initializing the UI
        self.show_welcome_message()

        self.init_ui()
        self.connect_signals()

        self.setWindowFlags(
            Qt.WindowType(
                Qt.WindowType.Window
                | Qt.WindowType.WindowMaximizeButtonHint
                | Qt.WindowType.WindowMinimizeButtonHint
                | Qt.WindowType.WindowCloseButtonHint
            )
        )
        self.showMaximized()

    def show_welcome_message(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Welcome!")
        msg_box.setText("Hello! Welcome to the Space Simulation Game!")
        msg_box.exec()

        # Transition to the PLAYING state
        self.controller.model.set_game_state(GameState.PLAYING)

    def init_ui(self):
        # --- Escape Key Shortcut to Exit Fullscreen ---
        self.exit_shortcut = QShortcut(QKeySequence('Escape'), self)
        self.exit_shortcut.activated.connect(self.close)

        # --- Main Layout ---
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # --- Splitter to Divide Main Window into Top (Game) and Bottom (Log) ---
        main_splitter = QSplitter(Qt.Orientation.Vertical)
        main_splitter.setSizes([600, 200])
        main_layout.addWidget(main_splitter)

        # --- Splitter to Divide Game Area into Left (Controls) and Right (Game View) ---
        game_area_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.addWidget(game_area_splitter)

        self.init_control_panel(game_area_splitter)
        self.init_game_panel(game_area_splitter)
        self.init_log_panel(main_splitter)

    def init_control_panel(self, splitter):
        # --- Left Panel (Controls) ---
        self.controls_panel = QFrame()
        self.controls_panel.setFrameShape(QFrame.Shape.Panel)
        self.controls_panel.setMaximumWidth(300)

        # Define the layout FIRST
        controls_layout = QVBoxLayout()
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.controls_panel.setLayout(controls_layout)
        splitter.addWidget(self.controls_panel)

        # --- Start/Pause Button ---
        self.start_pause_button = QPushButton("Pause", self)
        controls_layout.addWidget(self.start_pause_button)

        # --- Time Label ---
        self.time_label = QLabel("Time: 0.00s", self)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        controls_layout.addWidget(self.time_label)

        # --- Time Scale Control ---
        self.time_scale_spinbox = QDoubleSpinBox(self)
        self.time_scale_spinbox.setRange(0, 1000)
        self.time_scale_spinbox.setSingleStep(1)
        self.time_scale_spinbox.setValue(1.0)
        controls_layout.addWidget(self.time_scale_spinbox)

        # --- Fuel Label ---
        self.fuel_label = QLabel("Fuel: 100%")
        controls_layout.addWidget(self.fuel_label)

        # --- Launch Button ---
        self.launch_button = QPushButton("Launch")
        controls_layout.addWidget(self.launch_button)

    def init_log_panel(self, splitter):
        # --- Bottom Panel (Output/Log) ---
        log_frame = QFrame()
        log_frame.setFrameShape(QFrame.Shape.Panel)

        # Define the layout FIRST
        log_layout = QVBoxLayout()
        log_frame.setLayout(log_layout)

        # Populate the layout
        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)
        log_layout.addWidget(self.output_log)

        splitter.addWidget(log_frame)

    def init_game_panel(self, splitter):
        # --- Right Panel (Game View) ---
        game_view_frame = QFrame()
        game_view_frame.setFrameShape(QFrame.Shape.Panel)
        splitter.addWidget(game_view_frame)

        game_view_layout = QVBoxLayout()
        game_view_frame.setLayout(game_view_layout)

        # --- Tab Widget for Detailed Information ---
        self.tab_widget = QTabWidget()
        game_view_layout.addWidget(self.tab_widget)

        self.init_asteroid_tab()

    def init_asteroid_tab(self):
        # --- Asteroid Tab ---
        self.asteroid_tab = QWidget()
        self.tab_widget.addTab(self.asteroid_tab, "Asteroids")

        asteroid_tab_layout = QVBoxLayout()
        self.asteroid_tab.setLayout(asteroid_tab_layout)

        self.asteroid_table = QTableWidget()
        asteroid_tab_layout.addWidget(self.asteroid_table)
        self.create_asteroid_table()

    def create_asteroid_table(self):
        self.asteroid_table.setColumnCount(10)
        self.asteroid_table.setHorizontalHeaderLabels(
            ["X", "Y", "Z", "Velocity", "Raw Mass", "Purity", "dX", "dY","dZ", "ID"]
        )
        self.asteroid_table.horizontalHeader().setStretchLastSection(True)

    def update_asteroid_table(self, asteroids):
        self.asteroid_table.setRowCount(len(asteroids))
        for row, asteroid in enumerate(asteroids):
            velocity_magnitude = (asteroid.velocity[0]**2 + asteroid.velocity[1]**2 + asteroid.velocity[2]**2)**0.5
            self.asteroid_table.setItem(row, 0, QTableWidgetItem(f"{asteroid.position[0]:.2f}"))
            self.asteroid_table.setItem(row, 1, QTableWidgetItem(f"{asteroid.position[1]:.2f}"))
            self.asteroid_table.setItem(row, 2, QTableWidgetItem(f"{asteroid.position[2]:.2f}"))
            self.asteroid_table.setItem(row, 3, QTableWidgetItem(f"{velocity_magnitude:.2f}"))
            self.asteroid_table.setItem(row, 4, QTableWidgetItem(f"{asteroid.raw_mass:.2f}"))
            self.asteroid_table.setItem(row, 5, QTableWidgetItem(f"{asteroid.purity:.2f}"))
            self.asteroid_table.setItem(row, 6, QTableWidgetItem(f"{asteroid.velocity[0]:.2f}"))
            self.asteroid_table.setItem(row, 7, QTableWidgetItem(f"{asteroid.velocity[1]:.2f}"))
            self.asteroid_table.setItem(row, 8, QTableWidgetItem(f"{asteroid.velocity[2]:.2f}"))
            self.asteroid_table.setItem(row, 9, QTableWidgetItem(str(asteroid.id)))

    def connect_signals(self):
        self.start_pause_button.clicked.connect(self.controller.start_pause_game)
        self.time_scale_spinbox.valueChanged.connect(self.controller.set_time_scale)
        self.launch_button.clicked.connect(self.handle_launch_request)

        self.controller.model.game_state_changed.connect(self.update_game_state)
        self.controller.model.time_updated.connect(self.update_time_label)
        self.controller.model.asteroid_data_updated.connect(self.update_asteroid_table)
        self.controller.model.fuel_updated.connect(self.update_fuel_label)

    def update_game_state(self, state):
        if state == GameState.PLAYING:
            self.start_pause_button.setText("Pause")
        else:
            self.start_pause_button.setText("Resume")

    def update_time_label(self, time_value):
        formatted_time = self.format_time(time_value)
        self.time_label.setText(f"Time: {formatted_time}")

    def update_fuel_label(self, fuel):
        self.fuel_label.setText(f"Fuel: {fuel}%")

    def append_to_output_log(self, message):
        current_time = self.format_time(self.controller.model.total_seconds)
        log_message = f"[{current_time}] {message}"
        self.output_log.append(log_message)
    
    def handle_launch_request(self):
        message = self.controller.launch_ship()
        self.append_to_output_log(message)

    def format_time(self, seconds):
        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(days):02d}:{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = SpaceSimModel()
    controller = SpaceSimController(model)
    window = SpaceSimUI(controller)
    sys.exit(app.exec())