from enum import Enum
import discord
import yaml


class Role(Enum):
    CREWMATE  = 0
    SCIENTIST = 1
    ENGINEER  = 2
    ANGEL     = 3
    IMPOSTOR  = 4

    UNDECIDED = 5


class Player:

    user: discord.User
    role: Role
    location: int

    def __init__(self, user):
        self.user = user
        self.role = Role.UNDECIDED
        self.location = -1


class AmogusException(Exception):
    pass


class GameState:
    is_running: bool = False

    is_vc: bool
    server: discord.Guild

    players: list[Player]

    map_name: str
    room_names: list[str]
    connections: list[list[int]]

    starting_room: int

    def __init__(self, filename: str, is_vc: bool, server: discord.Guild):
        self.is_vc = is_vc
        self.server = server
        self.is_running = False

        self.players = []
        self.room_names = []
        self.connections = []

        with open(f'mapfiles/{filename.replace(".yaml", "")}.yaml') as file:
            map_data = yaml.safe_load(file)

        self.map_name = map_data['name']

        for area in map_data['areas']:
            self.room_names.append(area['name'])
        for area in map_data['areas']:
            link_indices = [self.room_names.index(link) for link in area['links']]
            self.connections.append(link_indices)

        if map_data['start'] not in self.room_names:
            raise AmogusException(f'{map_data["start"]} is not a valid starting area.')

    def add_player(self, user: discord.User):
        if self.is_running:
            raise AmogusException('Cannot add a player while the game is running')
        player = Player(user)
        self.players += [player]

    def start_game(self):
        self.is_running = True

        for player in self.players:
            player.location = self.starting_room


if __name__ == '__main__':
    gs = GameState('test', True, None)
    print(gs.room_names)
    print(gs.connections)
