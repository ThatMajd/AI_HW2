import itertools

ids = ["111111111", "222222222"]
IMPASSABLE = 'I'





def actions(state):
    def _is_pick_up_action_legal(pick_up_action):
        taxi_name = pick_up_action[1]
        passenger_name = pick_up_action[2]
        # check same position
        if state['taxis'][taxi_name]['location'] != state['passengers'][passenger_name]['location']:
            return False
        # check taxi capacity
        if state['taxis'][taxi_name]['capacity'] <= 0:
            return False
        # check passenger is not in his destination
        if state['passengers'][passenger_name]['destination'] == state['passengers'][passenger_name]['location']:
            return False
        return True

    def _is_drop_action_legal(drop_action):
        taxi_name = drop_action[1]
        passenger_name = drop_action[2]
        # check same position
        if state['taxis'][taxi_name]['location'] != state['passengers'][passenger_name]['destination']:
            return False
        return True

    def _is_refuel_action_legal(refuel_action):
        """
        check if taxi in gas location
        """
        taxi_name = refuel_action[1]
        i, j = state['taxis'][taxi_name]['location']
        if state['map'][i][j] == 'G':
            return True
        else:
            return False

    taxis = state["taxis"]
    passengers = state["passengers"]
    matrix = state["map"]
    rows = len(matrix)
    cols = len(matrix[0])
    acts = {}
    for taxi in taxis:
        acts[taxi] = []
        x, y = state["taxis"][taxi]["location"]
        fuel = state["taxis"][taxi]["fuel"]
        if 0 <= x + 1 < rows and 0 <= y < cols and matrix[x + 1][y] != IMPASSABLE and fuel > 0:
            acts[taxi].append(("move", taxi, (x+1, y)))
        if 0 <= x - 1 < rows and 0 <= y < cols and matrix[x - 1][y] != IMPASSABLE and fuel > 0:
            acts[taxi].append(("move", taxi, (x - 1, y)))
        if 0 <= x < rows and 0 <= y + 1 < cols and matrix[x][y + 1] != IMPASSABLE and fuel > 0:
            acts[taxi].append(("move", taxi, (x, y + 1)))
        if 0 <= x < rows and 0 <= y - 1 < cols and matrix[x][y - 1] != IMPASSABLE and fuel > 0:
            acts[taxi].append(("move", taxi, (x, y - 1)))

        acts[taxi] += [("pick up", taxi, passenger) for passenger in passengers
                         if _is_pick_up_action_legal(("pick up", taxi, passenger))]

        for passenger in passengers:
            if _is_pick_up_action_legal(("pick up", taxi, passenger)):
                acts[taxi].append(("pick up", taxi, passenger))
            if _is_drop_action_legal(("drop off", taxi, passenger)):
                acts[taxi].append(("drop off", taxi, passenger))

        if _is_refuel_action_legal(("refuel", taxi)):
            acts[taxi].append(("refuel", taxi))

    res = ["reset", "terminate"]
    for action in itertools.product(*acts.values()):
        taxis_location_dict = dict([(t, state['taxis'][t]['location']) for t in state['taxis'].keys()])
        move_actions = [a for a in action if a[0] == 'move']
        for move_action in move_actions:
            taxis_location_dict[move_action[1]] = move_action[2]
        if len(set(taxis_location_dict.values())) != len(taxis_location_dict):
            break
        res.append(tuple(action))
    return res


class OptimalTaxiAgent:
    def __init__(self, initial):
        self.initial = initial

    def act(self, state):
        for action in actions(state):
            print(action)

class TaxiAgent:
    def __init__(self, initial):
        self.initial = initial

    def act(self, state):
        pass

