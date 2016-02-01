"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._totalcookies = 0.0
        self._currentcookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "\nTime: "+str(self._time)+"\nCurrent cookies: "+str(self._currentcookies)+"\nCPS: "+str(self._cps)+"\nTotal cookies: "+str(self._totalcookies)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._currentcookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self._currentcookies: 
            return 0.0
        return math.ceil((cookies - self._currentcookies)/self._cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time <= 0:
            return
        self._time += time
        self._currentcookies += self._cps * time
        self._totalcookies += self._cps * time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if (cost > self._currentcookies) or (additional_cps <= 0):
            return        
        self._currentcookies -= cost
        self._cps += additional_cps
        self._history.append((self._time, item_name, cost, self._totalcookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    ugrades = build_info.clone()
    state = ClickerState()
    strname = strategy(state.get_cookies(), state.get_cps(), duration - state.get_time(), ugrades)
    while state.get_time() <= duration :
        strname = strategy(state.get_cookies(), state.get_cps(), duration - state.get_time(), ugrades)
        if strname == None :
            state.wait(duration - state.get_time())
            return state
        elif ugrades.get_cost(strname) > state.get_cookies() + (duration - state.get_time()) * state.get_cps():
            state.wait(duration - state.get_time())
            return state
        else:
            cost = ugrades.get_cost(strname)
            state.wait(state.time_until(cost))
            state.buy_item(strname, cost, ugrades.get_cps(strname))
            ugrades.update_item(strname)
    strname = strategy(state.get_cookies(), state.get_cps(), duration - state.get_time(), ugrades)
    state.wait(duration - state.get_time())
    state.buy_item(strname, ugrades.get_cost(strname), ugrades.get_cps(strname))
    ugrades.update_item(strname)
    
    return state


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Builds items and return the cheaper one
    Searches over the list of items
    """
    
    itemlist = build_info.build_items()
    cheaper = itemlist[0]
    for item in itemlist:
        if 	build_info.get_cost(item) < build_info.get_cost(cheaper) :
            cheaper = item
    if build_info.get_cost(cheaper) > cookies + time_left * cps:
        return None            
    return cheaper

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Builds items and return the more expensive one
    Searches over the list of items
    """
    itemlist = build_info.build_items()
    expen = ""
    for item in itemlist:
        if build_info.get_cost(item) <= cookies + time_left * cps:
            expen = item
            break
    if expen == "":
        return None
    for item in itemlist:
        if 	build_info.get_cost(item) > build_info.get_cost(expen) and build_info.get_cost(item) < cookies + time_left * cps:
            expen = item
    return expen

def strategy_best(cookies, cps, time_left, build_info):
    """
    Best strategy choses the item with the lowest cost/cps
    """
    itemlist = build_info.build_items()
    best = ""
    for item in itemlist:
        if build_info.get_cost(item) <= cookies + time_left * cps:
            best = item
            break
    if best == "":
        return None
    for item in itemlist:
        if build_info.get_cost(item)/ build_info.get_cps(item) < build_info.get_cost(best)/ build_info.get_cps(best) and build_info.get_cost(item) < cookies + time_left * cps:
            best = item
    return best
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    #state = simulate_clicker(provided.BuildInfo(), time, strategy)
    state1 = simulate_clicker(provided.BuildInfo(), time, strategy_cheap)
    print strategy_name, ":", state1
    print state1.get_history()
    print "#########"
    state2 = simulate_clicker(provided.BuildInfo(), time, strategy_expensive)

    print strategy_name, ":", state2
    print state2.get_history()
    print "#########"
    state = simulate_clicker(provided.BuildInfo(), time, strategy_best)
    print strategy_name, ":", state
    print state.get_history()

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history1 = state1.get_history()
    # history1 = [(item[0], item[3]) for item in history1]
    # history2 = state2.get_history()
    # history2 = [(item[0], item[3]) for item in history2]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history2], True)

def run():
    """
    Run the simulator.
    """  
    run_strategy("Cursor", SIM_TIME, strategy_best)

    
    
#run()


