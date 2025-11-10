import tkinter as tk
from client.views.game_ai_view import GameAIView

class DummyClient:
    pass

root = tk.Tk()
root.title('HOME')
root.geometry('300x200')

dummy = DummyClient()
dummy.current_view = type('V',(object,),{'window':root})()
dummy.user = type('U',(object,),{'nickname':'Tester','num_games':0,'num_wins':0,'num_draws':0,'rank':1})();

view = GameAIView(dummy)
print('AI view created with view_size=', view.view_size, 'origin=', view.origin_x, view.origin_y)
# simulate some pans
view.pan(5,0)
print('After pan right origin=', view.origin_x, view.origin_y)
view.zoom_out()
print('After zoom_out view_size=', view.view_size)
view.zoom_in()
print('After zoom_in view_size=', view.view_size)

# show briefly
if view.window and view.window.winfo_exists():
    view.window.after(800, view.window.destroy)
    view.window.mainloop()
print('done')
