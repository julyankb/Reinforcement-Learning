# Modified Pycolab code
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import curses
import sys
import random

from pycolab import ascii_art
from pycolab import human_ui
from pycolab.prefab_parts import sprites as prefab_sprites



# Rules
transition_penalty = 0.0
goal_reward = 1.0
discount_factor = 0.95

GAME_ART_blocking_0 = ['###########',
                       '#         #',
                       '#         #',
                       '#         #',
                       '######### #',
                       '#         #',
                       '#   P     #',
                       '###########']



GAME_ART_blocking_1 = ['###########',
                       '#         #',
                       '#         #',
                       '#         #',
                       '# #########',
                       '#         #',
                       '#   P     #',
                       '###########']




GAME_ART_shortcut_0 = ['###########',
                       '#         #',
                       '#         #',
                       '#         #',
                       '# #########',
                       '#         #',
                       '#   P     #',
                       '###########']


GAME_ART_shortcut_1 = ['###########',
                       '#         #',
                       '#         #',
                       '#         #',
                       '# ####### #',
                       '#         #',
                       '#   P     #',
                       '###########']



def make_blocking_maze(blocked=False):
  if blocked:
    return ascii_art.ascii_art_to_game(
      GAME_ART_blocking_1, what_lies_beneath=' ',
      sprites={'P': PlayerSprite})
  else:
    return ascii_art.ascii_art_to_game(
	GAME_ART_blocking_0, what_lies_beneath=' ',
	sprites={'P': PlayerSprite})

def make_shortcut_maze(shortcut=False):
  if shortcut:
    return ascii_art.ascii_art_to_game(
      GAME_ART_shortcut_1, what_lies_beneath=' ',
      sprites={'P': PlayerSprite})
  else:
    return ascii_art.ascii_art_to_game(
	GAME_ART_shortcut_0, what_lies_beneath=' ',
	sprites={'P': PlayerSprite})


class PlayerSprite(prefab_sprites.MazeWalker):
  def __init__(self, corner, position, character):
    """Inform superclass that we can't walk through walls."""
    super(PlayerSprite, self).__init__(
        corner, position, character, impassable='#')

  def update(self, actions, board, layers, backdrop, things, the_plot):
    del layers, backdrop, things   # Unused.

    the_plot.change_default_discount(discount_factor)

    # Apply motion commands.
    if actions == 0:    # walk upward?
      self._north(board, the_plot)
      the_plot.add_reward(transition_penalty)
    elif actions == 1:  # walk downward?
      self._south(board, the_plot)
      the_plot.add_reward(transition_penalty)
    elif actions == 2:  # walk leftward?
      self._west(board, the_plot)
      the_plot.add_reward(transition_penalty)
    elif actions == 3:  # walk rightward?
      self._east(board, the_plot)
      the_plot.add_reward(transition_penalty)

    # See if we've found the mystery spot.
    if self.position == (1, 9):
      the_plot.add_reward(goal_reward)
      the_plot.terminate_episode()


def main(argv=()):
  del argv  # Unused.

  # Build a four-rooms game.
  game = make_game()

  # Make a CursesUi to play it with.
  ui = human_ui.CursesUi(
      keys_to_actions={curses.KEY_UP: 0, 
			curses.KEY_DOWN: 1,
			curses.KEY_LEFT: 2, 
			curses.KEY_RIGHT: 3,-1: 4},
      			delay=200)

  # Let the game begin!
  ui.play(game)

if __name__ == '__main__':
  main(sys.argv)
