from client.views.game_ai_view import GameAIView

class DummyClient:
    pass

c = DummyClient()
c.current_view = None
c.user = type('U',(object,),{'nickname':'Tester','num_games':0,'num_wins':0,'num_draws':0,'rank':1})();

v = GameAIView(c)
print('Starting timer with small value...')
v.timer_seconds = 2
v.start_timer()
# simulate immediate stop (like when switching to AI)
v.stop_timer()
print('Stopped timer, _timer_after_id=', getattr(v,'_timer_after_id', None))
# restart to ensure it schedules
v.start_timer()
print('Restarted timer, _timer_after_id=', getattr(v,'_timer_after_id', None))
# clean up
if v.window and v.window.winfo_exists():
    v.window.after(500, v.window.destroy)
    v.window.mainloop()
print('done')
