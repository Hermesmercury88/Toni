import pygame, sys, random

class ParticlePrinciple:
    def __init__(self):
        self.particles = []

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= 0.2
                pygame.draw.circle(screen, pygame.Color('White'), particle[0], int(particle[1]))

    def add_particles(self):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1]
        radius = 10
        direction_x = random.randint(-3, 3)
        direction_y = random.randint(-3, 3)
        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
        self.particles.append(particle_circle)

    def delete_particles(self):
        self.particles = [particle for particle in self.particles if particle[1] > 0]


class ParticleNyan:
    def __init__(self):
        self.particles = []
        self.size = 12
        self.image1 = pygame.image.load('pic/Pavar1.png').convert_alpha()
        self.image2 = pygame.image.load('pic/Pavar2.png').convert_alpha()
        self.current_image = self.image1  # ตั้งค่าเริ่มต้นเป็นภาพแรก
        self.switch = False  # ใช้สำหรับสลับภาพ
        
    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0].x -= 1
                pygame.draw.rect(screen, particle[1], particle[0])

        self.draw_nyancat()

    def add_particles(self, offset, color):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1] + offset
        particle_rect = pygame.Rect(int(pos_x - self.size / 2), int(pos_y - self.size / 2), self.size, self.size)
        self.particles.append((particle_rect, color))

    def delete_particles(self):
        self.particles = [particle for particle in self.particles if particle[0].x > 0]

    def draw_nyancat(self):
        nyan_rect = self.current_image.get_rect(center=pygame.mouse.get_pos())
        screen.blit(self.current_image, nyan_rect)

    def switch_image(self):
        self.current_image = self.image1 if self.switch else self.image2
        self.switch = not self.switch


pygame.init()

# ตั้งค่าขนาดหน้าจอมือถือ
screen_width, screen_height = 360, 640
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# โหลด background images และปรับขนาด
bg_image1 = pygame.image.load('pic/bg1.png').convert()
bg_image1 = pygame.transform.scale(bg_image1, (screen_width, screen_height))
bg_image2 = pygame.image.load('pic/bg2.png').convert()
bg_image2 = pygame.transform.scale(bg_image2, (screen_width, screen_height))

current_bg = bg_image1  # เริ่มต้นด้วยพื้นหลังแรก

# Particle Objects
particle1 = ParticlePrinciple()
particle2 = ParticleNyan()

# โหลดเสียงพื้นหลัง
pygame.mixer.init()
pygame.mixer.music.load('wave/Nyan_Cat1.wav')  # แทนที่ด้วยชื่อไฟล์เสียงของคุณ
pygame.mixer.music.set_volume(0.5)  # ตั้งระดับเสียง (0.0 ถึง 1.0)
pygame.mixer.music.play(-1)  # เล่นแบบลูป (-1 คือเล่นซ้ำไม่มีที่สิ้นสุด)

PARTICLE_EVENT = pygame.USEREVENT + 1
IMAGE_SWITCH_EVENT = pygame.USEREVENT + 2  # อีเวนต์สำหรับสลับภาพ
BG_SWITCH_EVENT = pygame.USEREVENT + 3  # อีเวนต์สำหรับสลับพื้นหลัง

pygame.time.set_timer(PARTICLE_EVENT, 40)
pygame.time.set_timer(IMAGE_SWITCH_EVENT, 300)  # สลับภาพทุก 200ms
pygame.time.set_timer(BG_SWITCH_EVENT, 2000)  # สลับพื้นหลังทุก 2 วินาที

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()  # หยุดเสียงเมื่อโปรแกรมปิด
            pygame.quit()
            sys.exit()
        if event.type == PARTICLE_EVENT:
            particle1.add_particles()
            particle2.add_particles(-30, pygame.Color("Red"))
            particle2.add_particles(-18, pygame.Color("Orange"))
            particle2.add_particles(-6, pygame.Color("Yellow"))
            particle2.add_particles(6, pygame.Color("Green"))
            particle2.add_particles(18, pygame.Color("Blue"))
            particle2.add_particles(30, pygame.Color("Purple"))
        if event.type == IMAGE_SWITCH_EVENT:
            particle2.switch_image()  # สลับภาพ
        if event.type == BG_SWITCH_EVENT:
            # สลับพื้นหลัง
            current_bg = bg_image1 if current_bg == bg_image2 else bg_image2

    # วาดพื้นหลัง
    screen.blit(current_bg, (0, 0))

    # วาดวัตถุ
    particle1.emit()
    particle2.emit()

    pygame.display.update()
    clock.tick(120)

