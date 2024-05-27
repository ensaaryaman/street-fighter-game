import pygame

# Buton sınıfı
class Button():
    def __init__(self, x, y, image, scale):
        # Resmin orijinal genişlik ve yüksekliğini alır
        width = image.get_width()
        height = image.get_height()
        # Resmi ölçek faktörüne göre ölçeklendirir  (scale)
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        # Ölçeklendirilmiş resmin dikdörtgen alanını alır get_rect()
        self.rect = self.image.get_rect()
        # Dikdörtgenin sol üst köşesini belirtilen (x, y) pozisyonuna ayarla
        self.rect.topleft = (x, y)
        # Tıklanma durumunu False olarak başlat
        self.clicked = False

    def draw(self, surface):

        action = False

        pos = pygame.mouse.get_pos()

        # Fare butonun üzerindeyse ve tıklandıysa kontrol et
        if self.rect.collidepoint(pos):  # Fare butonun üzerindeyse kontrol et
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:  # Sol fare butonuna basıldıysa ve buton daha önce tıklanmadıysa kontrol et
                self.clicked = True  # Tıklanma durumunu True yap
                action = True  # Butonun tıklandığını belirten action değişkenini True yap


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Buton resmini belirtilen yüzeye çiz
        surface.blit(self.image, (self.rect.x, self.rect.y))


        return action
