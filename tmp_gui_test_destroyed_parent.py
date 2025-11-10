import tkinter as tk
from client.views.game_ai_view import GameAIView

class DummyClient:
    pass

# Create a temporary window and then destroy it to simulate HomeView being destroyed
temp = tk.Tk()
temp.title('TEMP HOME')
temp.geometry('200x100')
# Destroy immediately to simulate the scenario
temp.destroy()

dummy = DummyClient()
# attach the destroyed window as current_view.window
dummy.current_view = type('V',(object,),{'window':temp})();
# also provide a user
dummy.user = type('U',(object,),{'nickname':'Tester','num_games':0,'num_wins':0,'num_draws':0,'rank':1})();

print('Instantiating GameAIView with destroyed parent...')
view = GameAIView(dummy)
print('Resulting window:', 'exists' if view.window and view.window.winfo_exists() else 'no window')
# clean up
if view.window and view.window.winfo_exists():
    view.window.after(500, view.window.destroy)
    view.window.mainloop()

print('done')
