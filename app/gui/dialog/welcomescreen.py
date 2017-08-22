
from app.gui.dialog import BaseDialogWindow


class WelcomeScreen(BaseDialogWindow):
    def __init__(self, root, app):
        super().__init__(root)
        self.app = app
