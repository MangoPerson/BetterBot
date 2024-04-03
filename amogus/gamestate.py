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
    channels_generated: bool = False

    is_vc: bool
    server: discord.Guild
    category_name: str
    role_prefix: str

    players: list[Player]

    map_name: str
    room_names: list[str]
    connections: list[list[int]]

    starting_room: int

    def __init__(self, filename: str, is_vc: bool, server: discord.Guild, category_name: str = 'amogus', role_prefix: str = 'amogus'):
        self.is_vc = is_vc
        self.server = server
        self.is_running = False

        self.players = []
        self.room_names = []
        self.connections = []
        self.category_name = category_name
        self.role_prefix = role_prefix

        with open(f'amogus/mapfiles/{filename.replace(".yaml", "")}.yaml') as file:
            map_data = yaml.safe_load(file)

        self.map_name = map_data['name']

        for area in map_data['areas']:
            self.room_names.append(area['name'])
        for area in map_data['areas']:
            link_indices = [self.room_names.index(link) for link in area['links']]
            self.connections.append(link_indices)

        if map_data['start'] not in self.room_names:
            raise AmogusException(f'{map_data["start"]} is not a valid starting area.')

    async def generate_channels(self):
        if self.category_name not in [category.name for category in self.server.categories]:
            category = await self.server.create_category(self.category_name)
        else:
            category = discord.utils.get(self.server.categories, name=self.category_name)
            for channel in category.channels:
                await channel.delete()

        for role in self.server.roles:
            if role.name.startswith(self.role_prefix):
                await role.delete()

        for room in self.room_names:
            channel = await self.server.create_voice_channel(room, category=category)
            await channel.set_permissions(self.server.default_role, view_channel=False)

        for n_room, room in enumerate(self.room_names):
            role = await self.server.create_role(name=self.role_prefix + room)

            connections = [self.room_names[index] for index in self.connections[n_room]]

            print(room, connections)

            for connection in connections + [room]:
                channel = discord.utils.get(self.server.channels, name=connection)

                await channel.set_permissions(role, view_channel=True)

        self.channels_generated = True

    def add_player(self, user: discord.User):
        if self.is_running:
            raise AmogusException('Cannot add a player while the game is running')
        player = Player(user)
        self.players += [player]

    def start_game(self):
        if not self.channels_generated:
            raise AmogusException('Cannot start the game until channels have been generated. This should have happened'
                                  'when the game was created. Try re-running $bb amogus create')

        self.is_running = True

        for player in self.players:
            player.location = self.starting_room


if __name__ == '__main__':
    gs = GameState('test', True, None)
    print(gs.room_names)
    print(gs.connections)
