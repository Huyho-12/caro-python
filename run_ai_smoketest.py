import sys
import os

# ensure project root on path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from client.views.game_ai_view import GameAIView

# Minimal dummy client with required attributes/methods
class DummyUser:
    def __init__(self):
        self.nickname = 'TestUser'

class DummyClient:
    def __init__(self):
        self.user = DummyUser()
    def open_home_view(self):
        print('Returning to home (dummy)')

if __name__ == '__main__':
    client = DummyClient()
    view = GameAIView(client, difficulty='medium')
    view.show()
