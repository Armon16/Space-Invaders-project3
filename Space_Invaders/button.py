import pygame.font


class Button:

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def update_message(self):
        self.msg_image_rect.center = self.rect.center

    def __init__(self, ai_settings, screen, msg):
        self.msg_image = None
        self.msg_image_rect = None
        self.screen = screen
        self.screen_rect = screen.get_rect()
        ai_settings.log("pass")
        # Set the dimensions and properties of the button.
        self.width = 200
        self.height = 50
        self.button_color = (0, 0, 0)
        self.text_color = (0, 255, 0)
        self.font = pygame.font.SysFont(None, 48)
        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y = 550
        # The button message needs to be prepped only once.
        self.prep_msg(msg)

    def make_high_scores_button(self, msg):
        self.rect.y = 650
        self.prep_msg(msg)
