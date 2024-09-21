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
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
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

class SpaceSimBackend(QObject):
    game_state_changed = pyqtSignal(GameState)
    time_updated = pyqtSignal(float)
    asteroid_data_updated = pyqtSignal(list)
    fuel_updated = pyqtSignal(int)
    launch_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.fuel = 100
        self.total_seconds = 0.0
        self.time_scale = 1.0
        self.current_game_state = GameState.PLAYING
        self.asteroids = [Asteroid.generate_random_asteroid() for _ in range(5)]
        self.game_loop = GameLoop(self)
        self.game_loop.updateSignal.connect(self.update)
        self.game_loop.start()

    def update(self, dt):
        if self.current_game_state == GameState.PLAYING:
            self.total_seconds += dt * self.time_scale
            self.time_updated.emit(self.total_seconds)

            for asteroid in self.asteroids:
                asteroid.update(dt * self.time_scale)
            self.asteroid_data_updated.emit(self.asteroids)

    def start_pause_game(self):
        if self.current_game_state == GameState.PLAYING:
            self.current_game_state = GameState.PAUSED
        elif self.current_game_state == GameState.PAUSED:
            self.current_game_state = GameState.PLAYING
        self.game_state_changed.emit(self.current_game_state)

    def set_time_scale(self, scale):
        self.time_scale = scale

    def launch_ship(self):
        if self.fuel > 0:
            self.fuel -= 10
            self.launch_message.emit("Launching ship! Fuel remaining: {}%".format(self.fuel))
        else:
            self.launch_message.emit("Not enough fuel to launch!")
        self.fuel_updated.emit(self.fuel)

class SpaceSimUI(QWidget):
    start_pause_toggled = pyqtSignal()
    time_scale_changed = pyqtSignal(float)
    launch_requested = pyqtSignal()

    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.setWindowTitle("Space Simulation Game, v.001")
        self.init_ui()
        self.connect_signals()

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
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Align all to the top

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
        self.time_scale_spinbox.setRange(0.1, 10.0)
        self.time_scale_spinbox.setSingleStep(0.1)
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
        log_frame = QFrame()  # Create the frame
        log_frame.setFrameShape(QFrame.Shape.Panel) # Add the panel border

        # Define the layout FIRST
        log_layout = QVBoxLayout()  # Define its layout
        log_frame.setLayout(log_layout)  # Link them

        # Populate the layout
        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)
        log_layout.addWidget(self.output_log) 

        splitter.addWidget(log_frame)  # Add the FRAME to the splitter


    def init_game_panel(self, splitter):
        # --- Right Panel (Game View) ---
        game_view_frame = QFrame()  # Create the QFrame
        game_view_frame.setFrameShape(QFrame.Shape.Panel)  # Add the panel border
        splitter.addWidget(game_view_frame)  # Add the FRAME to the splitter

        game_view_layout = QVBoxLayout()
        game_view_frame.setLayout(game_view_layout)  # Set layout on the frame

        # --- Tab Widget for Detailed Information ---
        self.tab_widget = QTabWidget()
        game_view_layout.addWidget(self.tab_widget)

        self.init_asteroid_tab()
        # Add more tabs as needed... 

    
    
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
        self.start_pause_button.clicked.connect(self.start_pause_toggled.emit)
        self.time_scale_spinbox.valueChanged.connect(self.time_scale_changed.emit)
        self.launch_button.clicked.connect(self.launch_requested.emit)

        # Connect backend signals to frontend slots
        self.backend.game_state_changed.connect(self.update_game_state)
        self.backend.time_updated.connect(self.update_time_label)
        self.backend.asteroid_data_updated.connect(self.update_asteroid_table)
        self.backend.fuel_updated.connect(self.update_fuel_label)
        self.backend.launch_message.connect(self.append_to_output_log)

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
        current_time = self.format_time(self.backend.total_seconds)
        log_message = f"[{current_time}] {message}"
        self.output_log.append(log_message)


    def format_time(self, seconds):
        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(days):02d}:{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"





if __name__ == "__main__":
    app = QApplication(sys.argv)
    backend = SpaceSimBackend()
    window = SpaceSimUI(backend)

    # Connect frontend signals to backend slots
    window.start_pause_toggled.connect(backend.start_pause_game)
    window.time_scale_changed.connect(backend.set_time_scale)
    window.launch_requested.connect(backend.launch_ship)

    sys.exit(app.exec())