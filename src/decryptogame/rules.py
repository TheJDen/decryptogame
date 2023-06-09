from functools import partial

# termination conditions

# game ends if a team has k miscomunication tokens
def miscommunication_condition(game_data, k=2):
    return any(miscommunications == k for miscommunications in game_data.miscommunications)

# game ends if a team has k interception tokens
def interception_condition(game_data, k=2):
    return any(interceptions == k for interceptions in game_data.interceptions)

# game ends if k rounds have been played
def round_condition(game_data, k=8):
    return game_data.rounds_played == k

# home rules

home_miscommunication_condition = partial(miscommunication_condition, k=3)

home_interception_condition = partial(interception_condition, k=3)
