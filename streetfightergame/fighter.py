import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)  # Animasyonları yükle
        self.action = 0  # 0:idle #1:run #2:jump #3:attack1 #4:attack2 #5:hit #6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]  # İlk animasyon karesini al
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))  # Dövüşçünün dikdörtgen çerçevesi
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound  # Saldırı ses efekti
        self.hit = False
        self.health = 100
        self.alive = True

        self.invisible = False  # Görünmezlik özelliği
        self.invisible_time = 0  # Görünmezlik süresi

    def set_invisible(self, invisible):
        self.invisible = invisible
        if invisible:
            self.invisible_time = pygame.time.get_ticks()  # Görünmezliği başlat
        else:
            self.invisible_time = 0  # Görünmezliği durdur

    def load_images(self, sprite_sheet, animation_steps):
        # Sprite sheet'ten resimleri çıkar ve animasyon listesi oluştur
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
#EK
    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # Tuşlara basma durumlarını al
        key = pygame.key.get_pressed()

        # Sadece saldırmıyorsa diğer eylemleri gerçekleştirebilir
        if self.attacking == False and self.alive == True and round_over == False:
            # Oyuncu 1 kontrollerini kontrol et
            if self.player == 1:
                # Hareket
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                # Zıplama
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # Saldırı
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    # Hangi saldırı türünün kullanıldığını belirle
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

            # Oyuncu 2 kontrollerini kontrol et
            if self.player == 2:
                # Hareket
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                # Zıplama
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # Saldırı
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    # Hangi saldırı türünün kullanıldığını belirle
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

        # Yerçekimini uygula
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Oyuncunun ekranda kalmasını sağla
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # Oyuncuların birbirine bakmasını sağla
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # Saldırı bekleme süresini uygula
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Oyuncunun pozisyonunu güncelle
        self.rect.x += dx
        self.rect.y += dy
#EY
    # Animasyon güncellemelerini yönet
    def update(self):
        # Oyuncunun hangi eylemi yaptığını kontrol et
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # 6:ölüm
        elif self.hit == True:
            self.update_action(5)  # 5:yaralandı
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)  # 3:saldırı1
            elif self.attack_type == 2:
                self.update_action(4)  # 4:saldırı2
        elif self.jump == True:
            self.update_action(2)  # 2:zıplama
        elif self.running == True:
            self.update_action(1)  # 1:koşma
        else:
            self.update_action(0)  # 0:boşta

        animation_cooldown = 50
        # Görüntüyü güncelle
        self.image = self.animation_list[self.action][self.frame_index]
        # Son güncellemeden bu yana yeterli zaman geçti mi kontrol et
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # Animasyon tamamlandı mı kontrol et
        if self.frame_index >= len(self.animation_list[self.action]):
            # Oyuncu öldüyse animasyonu sonlandır
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # Saldırı yapıldı mı kontrol et
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                # Hasar alındı mı kontrol et
                if self.action == 5:
                    self.hit = False
                    # Oyuncu bir saldırı ortasındaysa saldırıyı durdur
                    self.attacking = False
                    self.attack_cooldown = 20
        if self.invisible:
            if pygame.time.get_ticks() - self.invisible_time >= 10000:
                self.set_invisible(False)
            else:
                return  # Görünmezlik süresi dolmadıysa saldırı yapma
        else:
            self.can_attack = True
#EK
    def attack(self, target):
        if self.attack_cooldown == 0 and not target.invisible:
            # Saldırıyı gerçekleştir
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,
                                         2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True

    def update_action(self, new_action):
        # Yeni eylem önceki eylemden farklı mı kontrol et
        if new_action != self.action:
            self.action = new_action
            # Animasyon ayarlarını güncelle
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        if not self.invisible or pygame.time.get_ticks() - self.invisible_time >= 10000:
            img = pygame.transform.flip(self.image, self.flip, False)
            surface.blit(img, (
                self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))  # Görüntüyü ekrana çiz
