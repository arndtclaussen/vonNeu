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
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QKeySequence, QShortcut

class GameState(Enum):
    PLAYING = 2
    PAUSED = 3

class GameLoop(QThread):
    updateSignal = pyqtSignal(float)

    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.target_fps = 60
        self.running = True

    def run(self):
        clock = time.perf_counter()
        dt = 1 / self.target_fps
        while self.running:
            new_time = time.perf_counter()
            frame_time = new_time - clock
            clock = new_time

            if self.backend.current_game_state == GameState.PLAYING:
                self.updateSignal.emit(dt)

            sleep_time = dt - (time.perf_counter() - clock)
            if sleep_time > 0:
                time.sleep(sleep_time)

    def stop(self):
        self.running = False
        self.wait()

class Asteroid:
    existing_ids = set()  # Use a set to store existing IDs for fast lookup

    def generate_unique_alphanumeric_id(length=7):
        """Generates a unique alphanumeric ID of a given length."""
        while True:
            new_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
            if new_id not in Asteroid.existing_ids:
                Asteroid.existing_ids.add(new_id)
                return new_id
    
    def __init__(
        self,
        position: Tuple[float, float, float],
        velocity: Tuple[float, float, float],
        raw_mass: float,
        purity: float,
    ):
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

class SpaceSimBackend:
    def __init__(self):
        self.fuel = 100
        self.total_seconds = 0.0
        self.time_scale = 1.0
        self.current_game_state = GameState.PLAYING
        self.asteroids = [Asteroid.generate_random_asteroid() for _ in range(5)]

    def launch_ship(self):
        if self.fuel > 0:
            self.fuel -= 10
            return "Launching ship! Fuel remaining: {}%".format(self.fuel)
        else:
            return "Not enough fuel to launch!"

    def update(self, dt):
        if self.current_game_state == GameState.PLAYING:
            self.total_seconds += dt * self.time_scale
            self.window.time_label.setText(f"Time: {self.total_seconds:.2f}s")

            # Update asteroid positions
            for asteroid in self.asteroids:
                asteroid.update(dt * self.time_scale)

            # Update the asteroid table in the UI
            self.window.update_asteroid_table()

    def get_time(self):
        return f"Time: {self.total_seconds:.2f}s"

    def set_time_scale(self, scale):
        self.time_scale = scale

class SpaceSimUI(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.backend.window = self
        self.setWindowTitle("Space Simulation Game, v.001")
        self.init_ui()

        # Make the window movable in "fullscreen"
        self.setWindowFlags(
            Qt.WindowType(
                Qt.WindowType.Window 
                | Qt.WindowType.WindowMaximizeButtonHint 
                | Qt.WindowType.WindowMinimizeButtonHint
                | Qt.WindowType.WindowCloseButtonHint
            )
        )
        self.showMaximized()  

        self.game_loop = GameLoop(backend)
        self.game_loop.updateSignal.connect(backend.update)
        self.game_loop.start()

    def init_ui(self):
        # --- Gameplay Layout ---
        # --- Start/Pause Button ---
        self.start_pause_button = QPushButton("Pause", self)
        self.start_pause_button.clicked.connect(self.toggle_start_pause)

        self.time_label = QLabel("Time: 0.00s", self)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        # --- Time Scale Control ---
        self.time_scale_spinbox = QDoubleSpinBox(self)
        self.time_scale_spinbox.setRange(0.1, 10.0)
        self.time_scale_spinbox.setSingleStep(0.1)
        self.time_scale_spinbox.setValue(1.0)
        self.time_scale_spinbox.valueChanged.connect(self.update_time_scale)

        # --- Left Panel (Controls) ---
        controls_layout = QVBoxLayout()
        controls_layout.addWidget(self.start_pause_button)
        controls_layout.addWidget(self.time_label)
        controls_layout.addWidget(self.time_scale_spinbox)
        self.fuel_label = QLabel("Fuel: 100%")
        self.launch_button = QPushButton("Launch")
        self.launch_button.clicked.connect(self.launch_ship)
        controls_layout.addWidget(self.fuel_label)
        controls_layout.addWidget(self.launch_button)

        self.controls_panel = QFrame()
        self.controls_panel.setFrameShape(QFrame.Shape.Panel)
        self.controls_panel.setMaximumWidth(300)
        self.controls_panel.setLayout(controls_layout)

        # --- Right Panel (Game View) ---
        game_view_layout = QVBoxLayout()  # Layout for game view and table
        self.game_view = QLabel("Game View Area")
        self.game_view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        game_view_layout.addWidget(self.game_view)

        # --- Asteroid Table ---
        self.asteroid_table = QTableWidget()
        self.create_asteroid_table()
        game_view_layout.addWidget(self.asteroid_table) 

        game_view_panel = QWidget()  # Widget to hold game view elements
        game_view_panel.setLayout(game_view_layout)

        # --- Bottom Panel (Output/Log) ---
        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)

        # --- Layout ---
        splitter1 = QSplitter(Qt.Orientation.Horizontal)
        splitter1.addWidget(self.controls_panel)
        splitter1.addWidget(game_view_panel)  

        splitter2 = QSplitter(Qt.Orientation.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.output_log)

        self.gameplay_layout = QHBoxLayout()
        self.gameplay_layout.addWidget(splitter2)

        splitter2.setSizes([600, 200])

        # --- Escape Key Shortcut to Exit Fullscreen ---
        self.exit_shortcut = QShortcut(QKeySequence('Escape'), self)
        self.exit_shortcut.activated.connect(self.close)
        # --- Main Layout ---
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.gameplay_layout)
        self.setLayout(main_layout)

    def create_asteroid_table(self):
        self.asteroid_table.setColumnCount(10)
        self.asteroid_table.setHorizontalHeaderLabels(
            ["X", "Y", "Z", "Velocity", "Raw Mass", "Purity", "dX", "dY","dZ", "ID"]
        )
        self.asteroid_table.horizontalHeader().setStretchLastSection(True)

    def update_asteroid_table(self):
        self.asteroid_table.setRowCount(len(self.backend.asteroids))
        for row, asteroid in enumerate(self.backend.asteroids):
            velocity_magnitude = (asteroid.velocity[0]**2 + asteroid.velocity[1]**2 + asteroid.velocity[2]**2)**0.5
            self.asteroid_table.setItem(row, 0, QTableWidgetItem(f"{asteroid.position[0]:.2f}"))
            self.asteroid_table.setItem(row, 1, QTableWidgetItem(f"{asteroid.position[1]:.2f}"))
            self.asteroid_table.setItem(row, 2, QTableWidgetItem(f"{asteroid.position[2]:.2f}"))
            self.asteroid_table.setItem(row, 3, QTableWidgetItem(f"{velocity_magnitude:.2f}"))
            self.asteroid_table.setItem(row, 4, QTableWidgetItem(f"{asteroid.raw_mass:.2f}"))
            self.asteroid_table.setItem(row, 5, QTableWidgetItem(f"{asteroid.purity:.2f}"))
            self.asteroid_table.setItem(row, 6, QTableWidgetItem(f"{asteroid.velocity[0]:.2f}")) # vx
            self.asteroid_table.setItem(row, 7, QTableWidgetItem(f"{asteroid.velocity[1]:.2f}")) # vy
            self.asteroid_table.setItem(row, 8, QTableWidgetItem(f"{asteroid.velocity[2]:.2f}")) # vz 
            self.asteroid_table.setItem(row, 9, QTableWidgetItem(str(asteroid.id))) # Add ID to the table
            

    def toggle_start_pause(self):
        if self.backend.current_game_state == GameState.PLAYING:
            self.backend.current_game_state = GameState.PAUSED
            self.start_pause_button.setText("Resume")
        elif self.backend.current_game_state == GameState.PAUSED:
            self.backend.current_game_state = GameState.PLAYING
            self.start_pause_button.setText("Pause")

    def update_time_scale(self):
        new_scale = self.time_scale_spinbox.value()
        self.backend.set_time_scale(new_scale)
        print(f"Time scale changed to: {new_scale}")

    def launch_ship(self):
        launch_message = self.backend.launch_ship()
        if launch_message:
            self.output_log.append(launch_message)
        self.fuel_label.setText("Fuel: {}%".format(self.backend.fuel))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    backend = SpaceSimBackend()
    window = SpaceSimUI(backend)
    sys.exit(app.exec())