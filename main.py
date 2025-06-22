from backend import Backend
from ui import UI

if __name__ == "__main__":
    backend = Backend()
    ui = UI(controller=backend.start, backend_stop=backend.stop)

    ui.start()
    backend.prediction_thread.join()
