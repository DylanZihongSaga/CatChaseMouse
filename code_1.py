import pygame
from sys import exit
import math 

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Cat chase Mouse') 
clock = pygame.time.Clock()
font = pygame.font.Font('Pixeltype.ttf', 50)
game_active = True

ground_surface = pygame.image.load('grass.png').convert()


cat = pygame.image.load('cat.png').convert_alpha()
cat = pygame.transform.scale(cat, (150, 150))
cat_rect = cat.get_rect(center = (100,100))

cat_velocity_x, cat_velocity_y = 0, 0
cat_acceleration = 0.1  # Acceleration value
cat_friction = -0.01  # Friction value
cat_max_speed = 50  # Maximum speed

mouse = pygame.image.load('mouse.png').convert_alpha()
mouse = pygame.transform.scale(mouse, (68, 35))
mouse = pygame.transform.flip(mouse, True, False)
mouse_rect = mouse.get_rect(center = (700,700))
flipped_mouse = pygame.transform.flip(mouse, True, False)

arrow = pygame.transform.scale(pygame.image.load('arrow.png').convert_alpha(), (50,50))
arrow = pygame.transform.flip(arrow, True, False)
arrow_rect = arrow.get_rect()

ground_surface = pygame.transform.scale(ground_surface, (800, 800))

mouse_speed = 6  # Set the speed of the mouse
last_mouse_x = mouse_rect.centerx  # Store the last x-coordinate



# Render the text
text = font.render('Press R to Start', True, (255, 255, 255))  # White color
end_text = font.render('Cat Wins', True, (255, 255, 255))  # White color

# Get the text surface's rect and set its center to the screen's center
text_rect = text.get_rect(center=(400, 500))
end_rect = end_text.get_rect(center=(400, 200))

# screen.blit(ground_surface, (0, 0))
def reset_game():
    mouse_win = False
    global game_active, timer
    game_active = True
    timer = 30  # 60 seconds timer


def calculate_angle(target_pos, source_pos):
    x_diff = target_pos[0] - source_pos[0]
    y_diff = target_pos[1] - source_pos[1]
    return math.degrees(math.atan2(-y_diff, x_diff))

reset_game()

mouse_win = False

while True:
    dt = clock.tick(60) / 1000  # Delta time in seconds
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()
            game_active = True
            cat_rect.center = (100, 100)
            

    if game_active:
        
        timer -= dt
        if timer <= 0:
            game_active = False
            timer = 0

        # Render timer text
        timer_text = font.render(f"Time: {int(timer)}", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(topright=(780, 10))
        screen.blit(timer_text, timer_rect)

        # Game ends when timer reaches zero
        if timer <= 0:
            end_text = font.render("Mouse Wins!", True, (255, 255, 255))
            end_rect = end_text.get_rect(center=(400, 200))
            screen.blit(end_text, end_rect)
            mouse_win = True

        
        pygame.draw.rect(screen, '#4D4845', (0, 0, 800, 800), width=5)

        if cat_rect.left >= 0 and cat_rect.right <= 800 and cat_rect.top >= 0 and cat_rect.bottom <= 800:
            # Cat is inside the display
            inside_display = True
        else:
            # Cat is outside the display
            inside_display = False
            
        cursor_x, cursor_y = pygame.mouse.get_pos()

        # Calculate direction vector and its length
        direction_x = cursor_x - mouse_rect.centerx
        direction_y = cursor_y - mouse_rect.centery
        distance = math.sqrt(direction_x**2 + direction_y**2)

        # Decide which sprite to use based on movement direction
        if mouse_rect.centerx < last_mouse_x:
            current_mouse_sprite = flipped_mouse
        else:
            current_mouse_sprite = mouse

        last_mouse_x = mouse_rect.centerx

        # Move mouse only if cursor is not too close
        if distance > mouse_speed:
            direction_x /= distance  # Normalize
            direction_y /= distance  # Normalize

            # Move the mouse
            mouse_rect.centerx += direction_x * mouse_speed
            mouse_rect.centery += direction_y * mouse_speed

        # Blit the background and sprites
        screen.blit(ground_surface, (5, 5))
        screen.blit(cat, cat_rect)
        screen.blit(current_mouse_sprite, mouse_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            cat_velocity_y -= cat_acceleration
        if keys[pygame.K_s]:
            cat_velocity_y += cat_acceleration
        if keys[pygame.K_a]:
            cat_velocity_x -= cat_acceleration
        if keys[pygame.K_d]:
            cat_velocity_x += cat_acceleration

        # Apply friction
        cat_velocity_x += cat_velocity_x * cat_friction
        cat_velocity_y += cat_velocity_y * cat_friction

        # Limit max speed
        cat_velocity_x = max(-cat_max_speed, min(cat_velocity_x, cat_max_speed))
        cat_velocity_y = max(-cat_max_speed, min(cat_velocity_y, cat_max_speed))

        # Update cat position
        cat_rect.x += cat_velocity_x
        cat_rect.y += cat_velocity_y
        
        if not inside_display:
            angle = calculate_angle(cat_rect.center, (400, 400))
            rotated_arrow = pygame.transform.rotate(arrow, angle)
            arrow_rect = rotated_arrow.get_rect(center=(400, 400))
            screen.blit(rotated_arrow, arrow_rect)


        if cat_rect.colliderect(mouse_rect):
            game_active = False
    else:
        screen.fill((94, 129, 162))
        screen.blit(end_text, end_rect)
        screen.blit(text, text_rect)

        if mouse_win == False:
            screen.blit(cat, (325,255))
        else:
            screen.blit(mouse, (375,305))

    pygame.display.update()

        
    
    pygame.display.update()
'''
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		
		if game_active:
			if event.type == pygame.MOUSEBUTTONDOWN:
				
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
        
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				
				start_time = int(pygame.time.get_ticks() / 1000)

	if game_active:
		screen.blit(sky_surface,(0,0))
		screen.blit(ground_surface,(0,300))

		cat.draw(screen)
		cat.update()

		mouse.draw(screen)
		mouse.update()

		# collision 
		game_active = collision_sprite()
		
	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)
		obstacle_rect_list.clear()
		player_rect.midbottom = (80,300)
		player_gravity = 0
		screen.blit(game_name,game_name_rect)

	pygame.display.update()
	clock.tick(60)
 '''