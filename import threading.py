import tkinter as tk
import threading
import time

# =====================================================
# GOOGLE PLATFORM SIMULATION LAYERS (LOGICAL ONLY)
# =====================================================

class GoogleMapsPlatform:
    """Simulates real-time navigation & accident alerting"""
    @staticmethod
    def report_accident(location):
        return f"Accident reported at {location} via Google Maps"

class GooglePubSub:
    """Simulates real-time message broadcasting"""
    @staticmethod
    def publish(message):
        return f"Broadcasting: {message}"

class GoogleIoTCore:
    """Simulates vehicle communication"""
    @staticmethod
    def send(vehicle_id, data):
        return f"Vehicle {vehicle_id} sent data to cloud"

class GoogleVisionAI:
    """Simulates crash detection"""
    @staticmethod
    def detect_collision():
        return True

# =====================================================
# CONSTANTS
# =====================================================
WINDOW_W = 1000
WINDOW_H = 650

ACCIDENT_Y = 360
BRAKE_Y = 200
START_Y = 60

CAR_SPEED = 2
ALERT_DELAY = 5
BRAKE_DELAY = 5

# =====================================================
# CAR MODEL
# =====================================================
class Car:
    def __init__(self, car_id, x, y, color):
        self.car_id = car_id
        self.x = x
        self.y = y
        self.color = color
        self.status = "Normal"
        self.moving = True

# =====================================================
# GUI
# =====================================================
class CarGUI:
    def __init__(self, root):
        self.root = root
        root.title("Car-to-Car Accident & Auto-Brake System")

        # LOG PANEL
        self.log = tk.Text(root, width=55, height=18, bg="black", fg="lime")
        self.log.grid(row=0, column=0, padx=10, pady=10)

        # STATUS PANEL
        self.status_frame = tk.Frame(root)
        self.status_frame.grid(row=0, column=1, padx=10, pady=10)
        self.status_labels = {}

        # CANVAS
        self.canvas = tk.Canvas(root, width=900, height=420, bg="black")
        self.canvas.grid(row=1, column=0, columnspan=2, pady=10)

        self.draw_road()
        self.draw_zones()

        # CARS
        self.cars = {
            1: Car(1, 410, ACCIDENT_Y, "red"),
            2: Car(2, 590, ACCIDENT_Y, "red"),
            3: Car(3, 420, START_Y, "orange"),
            4: Car(4, 550, START_Y, "orange"),
        }

        self.car_shapes = {}
        self.draw_cars()

        for cid in self.cars:
            self.update_status(cid, "Normal")

        threading.Thread(target=self.simulation_flow, daemon=True).start()

    # -------------------------------------------------
    # DRAWING
    # -------------------------------------------------
    def draw_road(self):
        for y in range(0, 420, 40):
            self.canvas.create_line(485, y, 485, y + 20, fill="white", dash=(4, 6))

    def draw_zones(self):
        self.canvas.create_rectangle(
            400, ACCIDENT_Y - 40,
            600, ACCIDENT_Y + 40,
            outline="red", dash=(6, 4), width=2
        )
        self.canvas.create_text(
            500, ACCIDENT_Y - 55,
            text="ACCIDENT ZONE", fill="red"
        )

        self.canvas.create_text(
            500, BRAKE_Y - 15,
            text="AUTO BRAKE APPLIED (1 KM FROM ACCIDENT)",
            fill="yellow"
        )

    def draw_cars(self):
        for car in self.cars.values():
            body = self.canvas.create_rectangle(
                car.x - 15, car.y - 25,
                car.x + 15, car.y + 25,
                fill=car.color
            )
            label = self.canvas.create_text(
                car.x, car.y - 35,
                text=f"C{car.car_id}", fill="white"
            )
            self.car_shapes[car.car_id] = (body, label)

    # -------------------------------------------------
    # STATUS & LOG
    # -------------------------------------------------
    def update_status(self, car_id, status):
        colors = {
            "Normal": "green",
            "Accident": "red",
            "Alert": "orange",
            "Stopped": "yellow"
        }
        if car_id not in self.status_labels:
            lbl = tk.Label(
                self.status_frame,
                text=f"Car {car_id}: {status}",
                width=25, bg=colors[status]
            )
            lbl.pack(pady=4)
            self.status_labels[car_id] = lbl
        else:
            self.status_labels[car_id].config(
                text=f"Car {car_id}: {status}", bg=colors[status]
            )

    def log_msg(self, msg):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    # -------------------------------------------------
    # MOVEMENT
    # -------------------------------------------------
    def move_car_xy(self, car_id, dx):
        rect, txt = self.car_shapes[car_id]
        self.canvas.move(rect, dx, 0)
        self.canvas.move(txt, dx, 0)

    def move_car_down(self, car):
        if not car.moving:
            return
        car.y += CAR_SPEED
        rect, txt = self.car_shapes[car.car_id]
        self.canvas.move(rect, 0, CAR_SPEED)
        self.canvas.move(txt, 0, CAR_SPEED)

    # -------------------------------------------------
    # CRASH EFFECT
    # -------------------------------------------------
    def dash_effect(self, car_id):
        rect, txt = self.car_shapes[car_id]
        for _ in range(12):
            self.canvas.move(rect, -6, 0)
            self.canvas.move(txt, -6, 0)
            self.canvas.itemconfig(rect, fill="white")
            time.sleep(0.04)

            self.canvas.move(rect, 12, 0)
            self.canvas.move(txt, 12, 0)
            self.canvas.itemconfig(rect, fill="red")
            time.sleep(0.04)

            self.canvas.move(rect, -6, 0)
            self.canvas.move(txt, -6, 0)

    # -------------------------------------------------
    # MAIN SIMULATION FLOW
    # -------------------------------------------------
    def simulation_flow(self):
        # Cars move toward each other
        for _ in range(18):
            self.move_car_xy(1, +2)
            self.move_car_xy(2, -2)
            time.sleep(0.05)

        # Collision detected (Vision AI)
        if GoogleVisionAI.detect_collision():
            self.log_msg("💥 Collision detected by Google Vision AI")

        self.update_status(1, "Accident")
        self.update_status(2, "Accident")
        self.dash_effect(1)
        self.dash_effect(2)

        # Cloud reporting
        self.log_msg(GoogleMapsPlatform.report_accident("Highway Section A"))
        self.log_msg(GoogleIoTCore.send(1, "Accident Data"))
        self.log_msg(GooglePubSub.publish("Accident Alert to Nearby Vehicles"))

        time.sleep(ALERT_DELAY)

        # Alert nearby cars
        self.update_status(3, "Alert")
        self.update_status(4, "Alert")

        while self.cars[3].y < BRAKE_Y - 30:
            self.move_car_down(self.cars[3])
            self.move_car_down(self.cars[4])
            time.sleep(0.03)

        time.sleep(BRAKE_DELAY)

        # Auto brake
        self.log_msg("🛑 AUTO BRAKE APPLIED – VEHICLES STOPPED")
        self.cars[3].moving = False
        self.cars[4].moving = False
        self.update_status(3, "Stopped")
        self.update_status(4, "Stopped")

# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    root = tk.Tk()
    CarGUI(root)
    root.mainloop()
