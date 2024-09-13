from ship.cabin import Cabin
from ship.engine import Engine
from ship.fuel_tank import FuelTank
from ship.radiator import Radiator

def save_ship(ship, filename="ship.txt"):
    with open(filename, "w") as f:
        for module in ship:
            # Save the class name, x, y, and attachment points
            attachment_info = [(point[0], point[1]) for point in module.attachment_points]
            f.write(f"{module.__class__.__name__} {module.x} {module.y} {module.width} {module.height} {attachment_info}\n")

def load_ship(filename="ship.txt"):
    class_map = {
        "Cabin": Cabin,
        "Engine": Engine,
        "FuelTank": FuelTank,
        # Add other module classes as necessary
    }

    ship = []
    with open(filename, "r") as f:
        for line in f:
            parts = line.split(maxsplit=5)
            module_class = class_map.get(parts[0])
            if module_class:
                x, y = int(parts[1]), int(parts[2])
                width, height = int(parts[3]), int(parts[4])
                module = module_class(x, y)
                if len(parts) > 5:
                    attachment_info = eval(parts[5])
                    module.attachment_points = attachment_info
                ship.append(module)

    return ship
