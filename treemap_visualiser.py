"""Assignment 2: Treemap Visualiser

=== CSC148 Fall 2020 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code to run the treemap visualisation program.
It is responsible for initializing an instance of AbstractTree (using a
concrete subclass, of course), rendering it to the user using pygame,
and detecting user events like mouse clicks and key presses and responding
to them.
"""
import pygame
from tree_data import FileSystemTree, AbstractTree
from population import PopulationTree

# Screen dimensions and coordinates

ORIGIN = (0, 0)
WIDTH = 1024
HEIGHT = 768
FONT_HEIGHT = 30  # The height of the text display.
TREEMAP_HEIGHT = HEIGHT - FONT_HEIGHT  # The height of the treemap display.

# Font to use for the treemap program.
FONT_FAMILY = 'Consolas'


def run_visualisation(tree: AbstractTree) -> None:
    """Display an interactive graphical display of the given tree's treemap."""
    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Render the initial display of the static treemap.
    render_display(screen, tree, '')

    # Start an event loop to respond to events.
    event_loop(screen, tree)


def render_display(screen: pygame.Surface, tree: AbstractTree,
                   text: str) -> None:
    """Render a treemap and text display to the given screen.

    Use the constants TREEMAP_HEIGHT and FONT_HEIGHT to divide the
    screen vertically into the treemap and text comments.
    """
    # First, clear the screen
    pygame.draw.rect(screen, pygame.color.THECOLORS['black'],
                     (0, 0, WIDTH, HEIGHT))

    rect1 = (0, 0, WIDTH, HEIGHT)
    tupple = tree.generate_treemap(rect1)
    for tup in tupple:
        color = tup[1]
        tangle = tup[0]
        pygame.draw.rect(screen, color, tangle)
    rect2 = (0, TREEMAP_HEIGHT, WIDTH, FONT_HEIGHT)
    pygame.draw.rect(screen, pygame.color.THECOLORS['black'], rect2)
    _render_text(screen, text)

    # This must be called *after* all other pygame functions have run.
    pygame.display.flip()


def _render_text(screen: pygame.Surface, text: str) -> None:
    """Render text at the bottom of the display."""
    # The font we want to use
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)
    text_surface = font.render(text, 1, pygame.color.THECOLORS['white'])

    # Where to render the text_surface
    text_pos = (0, HEIGHT - FONT_HEIGHT + 4)
    screen.blit(text_surface, text_pos)


def event_loop(screen: pygame.Surface, tree: AbstractTree) -> None:
    """Respond to events (mouse clicks, key presses) and update the display.

    Note that the event loop is an *infinite loop*: it continually waits for
    the next event, determines the event's type, and then updates the state
    of the visualisation or the tree itself, updating the display if necessary.
    This loop ends when the user closes the window.
    """
    # We strongly recommend using a variable to keep track of the currently-
    # selected leaf (type AbstractTree | None).
    # But feel free to remove it, and/or add new variables, to help keep
    # track of the state of the program.
    selected_leaf = None

    while True:
        # Wait for an event
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            return

        # Remember to call render_display if any data_sizes change,
        # as the treemap will change in this case.

        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            rect = tree.generate_treemap((0, 0, WIDTH, HEIGHT))
            subtrees = tree.leaf_list()
            pos = tree.get_rect(x, y, rect, subtrees)
            if event.button == 1 and selected_leaf == pos:
                render_display(screen, tree, "")
                selected_leaf = None
            if event.button == 1 and selected_leaf != pos:
                selected_leaf = pos
                render_display(screen, tree, tree.l_text(selected_leaf))
            elif event.button == 3:
                selected_leaf = pos
                tree.delete_leaf(selected_leaf)
                render_display(screen, tree, "")
                selected_leaf = None

        elif event.type == pygame.KEYUP and selected_leaf is not None:
            if event.key == pygame.K_UP:
                tree.l_up(selected_leaf)
                render_display(screen, tree, tree.l_text(selected_leaf))
            elif event.key == pygame.K_DOWN:
                tree.l_down(selected_leaf)
                render_display(screen, tree, tree.l_text(selected_leaf))


def run_treemap_file_system(path: str) -> None:
    """Run a treemap visualisation for the given path's file structure.

    Precondition: <path> is a valid path to a file or folder.
    """
    file_tree = FileSystemTree(path)
    run_visualisation(file_tree)


def run_treemap_population() -> None:
    """Run a treemap visualisation for World Bank population data."""
    pop_tree = PopulationTree(True)
    run_visualisation(pop_tree)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(
        config={
            'extra-imports': ['pygame', 'tree_data', 'population'],
            'generated-members': 'pygame.*'})

    # To check your work for Tasks 1-4, try uncommenting the following function
    # call, with the '' replaced by a path like
    # 'C:\\Users\\David\\Documents\\csc148\\assignments' (Windows) or
    # '/Users/dianeh/Documents/courses/csc148/assignments'
    run_treemap_file_system(
        '/Users/SeungAJung/Desktop/sandbox/csc148/csc148/assignments/')

    # To check your work for Task 5, uncomment the following function call.
    run_treemap_population()
