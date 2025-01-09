import sys, pygame, math, random

pygame.init()

# ------Values------------
# Canvas setup
size = width, height = 600, 400
screen = pygame.display.set_mode(size)

# Colors
black = 0, 0, 0
white = 255, 255, 255
baby_blue = 137, 207, 240
red = 255, 0, 0
dark_red = 200, 0, 0

# Outer circle values
circle_position = (300, 200)  # (x, y) position of the circle
circle_radius = 190  # Radius of the circle
border_thickness = 2  # Thickness of the circle border

# Ball values
ball_position = [300, 200]
default_radius = 15
ball_radius = default_radius

# ------Physics--------
# Gravity
gravity = 0.0005  # Acceleration due to gravity

# Randomized initial velocity
velocity = [random.uniform(.01, .03), random.uniform(-.02, .02)]  # Random x and y velocities

# Button values
button_rect = pygame.Rect(10, 10, 100, 30)  # Position and size of the button

def reset_simulation():
    """Resets the ball position and velocity."""
    global ball_position, velocity
    ball_position = [300, 200]
    velocity = [random.uniform(0.1, 0.3), random.uniform(-0.2, 0.2)]

# ------Gameplay------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                reset_simulation()

    screen.fill(black)

    # Draw the outer circle
    pygame.draw.circle(screen, white, circle_position, circle_radius, border_thickness)

    # Apply gravity
    velocity[1] += gravity  # Apply gravity to vertical velocity
    ball_position[0] += velocity[0]  # Update x-coordinate
    ball_position[1] += velocity[1]  # Update y-coordinate

    # Get the ball position relative to the circle center
    posx = ball_position[0] - circle_position[0]
    posy = ball_position[1] - circle_position[1]
    distance_from_center = math.sqrt(posx**2 + posy**2)

    # Check for collision
    if distance_from_center + ball_radius >= circle_radius:
        #print("collision detected")
        ball_radius = ball_radius * 1.1

        # Calculate the normal vector at the collision point
        normal_x = posx / distance_from_center
        normal_y = posy / distance_from_center

        # Reflect the velocity vector using the normal
        dot_product = velocity[0] * normal_x + velocity[1] * normal_y
        velocity[0] -= 2 * dot_product * normal_x
        velocity[1] -= 2 * dot_product * normal_y

        # Dampening effect to simulate energy loss
        # velocity[0] *= 0.9
        # velocity[1] *= 0.9

        # Reposition the ball just inside the circle boundary to prevent sticking
        overlap = (distance_from_center + ball_radius) - circle_radius
        ball_position[0] -= overlap * normal_x
        ball_position[1] -= overlap * normal_y

    #make sure the ball isn't bigger than the circle
    if ball_radius >= circle_radius:
        ball_radius = default_radius

    # Draw the ball
    pygame.draw.circle(screen, baby_blue, (int(ball_position[0]), int(ball_position[1])), ball_radius)

    # restart button
    pygame.draw.rect(screen, red if button_rect.collidepoint(pygame.mouse.get_pos()) else dark_red, button_rect)
    font = pygame.font.Font(None, 24)
    text = font.render("Restart", True, white)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)


    # Refresh the display
    pygame.display.flip()
