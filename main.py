import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

class ImageGenerator:
    def __init__(self, scale=5, text_main="SnehulakTV_"):
        # Nastavení rozměrů
        self.scale = scale
        self.side_x = int(2048 * scale)
        self.side_y = int(2048 * scale)
        self.center_x = self.side_x // 2
        self.center_y = self.side_y // 2
        self.image_scale = (self.side_x, self.side_y)

        # Hlavní text a barvy
        self.text_main = text_main
        self.color_bg = (25, 25, 25)
        self.text_color_shadow = (150, 150, 150)
        self.text_color = (255, 255, 255)
        
        # Defaultní limity pro šum
        self.r_limit = (20, 50)
        self.g_limit = (20, 50)
        self.b_limit = (20, 50)
        
        # Inicializace proměnných pro velký text (aby neházelo chybu, když se nenačte config)
        self.text_big_text = ""
        self.text_big_scale = 0.5
        self.text_big_color = (255, 255, 255)
        self.text_big_color_shadow = (100, 100, 100)

    def LoadConfig(self, ver, app_name):
        if ver == 1.0:
            configs = {
                "ig": {
                    "limits": ((25, 50), (10, 30), (20, 40)),
                    "text": "INSTA",
                    "scale": 0.38,
                    "colors": ((220, 0, 150), (180, 0, 100)), # (Main, Shadow)
                    "icon": "Icon/ig.png"
                },
                "git": {
                    "limits": ((20, 50), (20, 50), (20, 50)),
                    "text": "GIT",
                    "scale": 0.6,
                    "colors": ((225, 225, 225), (200, 200, 200)),
                    "icon": "Icon/git.png"
                },
                "disc": {
                    "limits": ((0, 0), (0, 0), (20, 60)),
                    "text": "DISC",
                    "scale": 0.49,
                    "colors": ((15, 0, 200), (5, 0, 100)),
                    "icon": "Icon/discord.png"
                },
                "osu": {
                    "limits": ((40, 70), (0, 0), (20, 40)),
                    "text": "OSU",
                    "scale": 0.54,
                    "colors": ((250, 0, 169), (200, 0, 100)),
                    "icon": "Icon/osu.png"
                }
            }

            # Vyhledání aplikace v deníku (pokud neexistuje, hodí to chybu nebo default)
            app_name = app_name.lower()
            if app_name in configs:
                conf = configs[app_name]
                
                # Rozřazení hodnot do proměnných třídy
                self.r_limit, self.g_limit, self.b_limit = conf["limits"]
                self.text_big_text = conf["text"]
                self.text_big_scale = conf["scale"]
                self.text_big_color, self.text_big_color_shadow = conf["colors"]
                self.icon_path = conf["icon"] # Cesta k ikoně pro budoucí použití
            else:
                print(f"⚠️ Konfigurace pro '{app_name}' nebyla nalezena!")
                return

            # Načtení fontů (vždy po nastavení scale a textu)
            try:
                font_path = "Fonts\\RussoOne-Regular.ttf"
                self.font = ImageFont.truetype(font_path, int(235 * self.scale))
                self.big_font = ImageFont.truetype(font_path, int(1500 * self.scale * self.text_big_scale))
            except OSError:
                print("⚠️ Font 'RussoOne' nenalezen, používám default.")
                self.font = self.big_font = ImageFont.load_default()
      
    def GetTools(self):
        self.img = Image.new("RGB", self.image_scale, self.color_bg)
        self.draw = ImageDraw.Draw(self.img)

    def AddNoise(self):
        small_size = 205
        noise_array = np.random.randint(
            [self.r_limit[0], self.g_limit[0], self.b_limit[0]],
            [self.r_limit[1] + 1, self.g_limit[1] + 1, self.b_limit[1] + 1],
            (small_size, small_size, 3), 
            dtype=np.uint8
        )
        noise_img = Image.fromarray(noise_array)
        noise_img = noise_img.filter(ImageFilter.GaussianBlur(radius=2))
        bg_texture = noise_img.resize((self.side_x, self.side_y), resample=Image.BILINEAR)
        self.img.paste(bg_texture)
    
    def AddBigText(self):
        text_pos_x = self.center_x
        text_pos_y = int(self.side_y // 8 * 3)

        shadow_offset = int(15 * self.scale)
        
        # Shadow
        self.draw.text((text_pos_x + shadow_offset, text_pos_y + shadow_offset), 
                       self.text_big_text, font=self.big_font, fill=self.text_big_color_shadow, anchor="mm")
        # Main
        self.draw.text((text_pos_x, text_pos_y), 
                       self.text_big_text, font=self.big_font, fill=self.text_big_color, anchor="mm")
        
    def Addtext(self):
        # Opraveno text_pos_x z center_y na center_x
        text_pos_x = self.center_x 
        text_pos_y = int(self.side_y // 4 * 3)

        shadow_offset = int(15 * self.scale)

        # Shadow
        self.draw.text((text_pos_x + shadow_offset, text_pos_y + shadow_offset), 
                       self.text_main, font=self.font, fill=self.text_color_shadow, anchor="mm")
        # Main
        self.draw.text((text_pos_x, text_pos_y), 
                       self.text_main, font=self.font, fill=self.text_color, anchor="mm")
    

    def SaveShow(self, save=False, show=True, path="Save/"):
        if show:
            self.img.show()
        if save:
            self.img.save(f"{path}Picture-{self.text_big_text}.png")


if __name__ == "__main__":
    u_scale = 1
    u_ver = 1.0
    u_app = "ig"
    u_save = True
    u_path = "Save/"
    while True:
        while True:
            print("\n--- Banner Generator Settings ---")
            print(f"1. Verze      = {u_ver}")
            print(f"2. Aplikace   = {u_app}")
            print(f"3. Škálování  = {u_scale}")
            print(f"4. Uložení    = {'ANO' if u_save else 'NE'}")
            print(f"5. Složka     = {u_path}")
            print("6. SPUSTIT GENEROVÁNÍ")
            print("7. Konec")

            inp = input("Pro změnu zvolte 1-5, pro start 5: ")

            if inp == "1":
                u_ver = float(input("Nová verze (např. 1.0): "))
            elif inp == "2":
                u_app = input("Nová aplikace (ig, git, disc, osu): ")
            elif inp == "3":
                u_scale = int(input("Nové škálování (1-10): "))    
            elif inp == "4":
                val = input("Uložit? (y/n): ").lower()
                u_save = val == 'y' or val == 'ano' or val == ''
            elif inp == "5":
                u_path = input("Nová složka: ")
            elif inp == "6":
                break
            elif inp == "7":
                exit()
            else:
                print("Neplatná volba, zkus to znovu.")

        # === Spuštění generátoru ===
        print(f"\n🚀 Spouštím generování pro {u_app.upper()}...")
        time_start = time.time()
        
        generator = ImageGenerator(scale=u_scale)
        generator.LoadConfig(u_ver, u_app)
        generator.GetTools()
        generator.AddNoise()
        generator.AddBigText()
        generator.Addtext()
        
        time_end = time.time()
        print(f"✅ Hotovo za {round(time_end - time_start, 2)}s!")
        
        generator.SaveShow(save=u_save, show=True, path=u_path)


