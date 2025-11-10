import tkinter as tk
import time

# Ensure we import the updated GameAIView
from client.views.game_ai_view import GameAIView

class DummyClient:
    pass

root = tk.Tk()
root.title('FAKE HOME WINDOW')
root.geometry('300x200')

dummy = DummyClient()
dummy.current_view = type('V',(object,),{'window':root})()
dummy.user = type('U',(object,),{'nickname':'Tester','num_games':0,'num_wins':0,'num_draws':0,'rank':1})()

print('Creating GameAIView...')
view = GameAIView(dummy)
print('Created. window title ->', view.window.title())

# show for a short moment then destroy
root.update()
root.after(800, root.destroy)
root.mainloop()
print('Done')
