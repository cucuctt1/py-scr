import pygame
import sys

class Block:
    def __init__(self, x, y, size, color, isheader=False):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.isheader = isheader
        self.parent = None
        self.children = []
        self.slot = None

    def draw(self, screen):
        if self.isheader:
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.size, self.size))  # Green header block
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

# Check if two blocks overlap
def check_overlap(block1, block2):
    return (block1.x < block2.x + block2.size and
            block1.x + block1.size > block2.x and
            block1.y < block2.y + block2.size and
            block1.y + block1.size > block2.y)

# Find the topmost block in the hierarchy
def find_topmost(block):
    while block.parent:
        block = block.parent
    return block

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sticky Blocks")

# Create three blocks with different properties
header_block = Block(100, 100, 50, (255, 0, 0), isheader=True)  # Red header block
block1 = Block(200, 200, 50, (0, 0, 255))  # Blue block
block2 = Block(300, 300, 50, (255, 0, 255))  # Purple block

# List to hold all blocks
blocks = [header_block, block1, block2]

# Variable to track whether a block is being dragged
dragging_block = None

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if a block is clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for block in blocks:
                if block.x <= mouse_x <= block.x + block.size and block.y <= mouse_y <= block.y + block.size:
                    dragging_block = block
                    offset_x = mouse_x - block.x
                    offset_y = mouse_y - block.y
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_block:
                # Check if the block is over a slot
                for block in blocks:
                    if block != dragging_block and check_overlap(dragging_block, block) and not block.isheader:
                        # Stick the dragging block to the non-header block
                        if dragging_block.parent:
                            dragging_block.parent.children.remove(dragging_block)
                        block.add_child(dragging_block)
                        dragging_block.slot = block

                        # Adjust the position to align with the slot
                        dragging_block.x = block.x
                        dragging_block.y = block.y - dragging_block.size

            dragging_block = None
        elif event.type == pygame.MOUSEMOTION and dragging_block:
            # Update block position based on mouse movement
            dragging_block.x, dragging_block.y = pygame.mouse.get_pos()
            dragging_block.x -= offset_x
            dragging_block.y -= offset_y

    # Fill the background
    screen.fill((255, 255, 255))

    # Draw all blocks
    for block in blocks:
        block.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
