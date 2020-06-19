import logging
from Controllers.HueInterfaceController import HueInterfaceController

class Main:
    def __init__(self):
        logging.info("[Main] Starting up main operation...")  

        # Create a new instance of the Hue Controller
        self.hueController = HueInterfaceController()

        # Initialise Hue Controller parameters.
        self.hueController.initialiseController()
        
if __name__ == '__main__':
    Main()
