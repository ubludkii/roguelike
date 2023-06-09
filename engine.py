﻿from __future__ import annotations

from typing import TYPE_CHECKING
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import EventHandler

if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap


class Engine:
    game_map: GameMap
    def __init__(self, player: Entity):
        self.event_handler: EventHandler = EventHandler(self)
        self.player = player


    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()


    def update_fov(self) -> None:   #A область видимости
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=20,
        )
        #A если плитка исследована то тогда она не будет в ШРАУДЕ
        self.game_map.explored |= self.game_map.visible


    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        context.present(console)
        console.clear()


'''Мы импортировали GameMap класс и теперь передаем его экземпляр в Engine инициализаторе класса. 
    После этого мы используем его двумя способами:
    В handle_events мы используем его, чтобы проверить, является ли плитка “проходимой”, и только после этого перемещаем проигрыватель.
    В render мы вызываем метод GameMap’s render, чтобы отобразить его на экране. '''