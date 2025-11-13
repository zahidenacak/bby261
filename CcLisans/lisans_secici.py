import sys

class LicenseChooser:
    """
    Kullanıcıya sorular sorarak Creative Commons lisansını belirleyen
    ve atıf metni oluşturan bir sınıf.
    """

    def __init__(self):
        """
        Sınıfın 'constructor' (kurucu) metodu.
        Bir 'LicenseChooser' nesnesi yaratıldığında çalışır.
        Başlangıç verilerini (nitelikleri) ayarlar.
        """
        # Kullanıcı seçimlerini saklamak için nitelikler (attributes)
        self.adapt_choice = None
        self.commercial_choice = None
        
        # Hesaplanan lisans bilgilerini saklamak için nitelikler
        self.license_code = "CC BY"  # Tüm lisanslar 'BY' (Atıf) ile başlar
        self.license_name = ""
        self.license_url = ""

    def _get_user_choice(self, prompt: str, options: dict) -> str:
        """
        Kullanıcıya bir soru sorar ve geçerli bir yanıt alır.
        Bu bir 'yardımcı' metottur (internal helper method).
        """
        print(f"\n{prompt}")
        valid_keys = []
        for key, description in options.items():
            print(f"  [{key}] {description}")
            valid_keys.append(key.lower())

        while True:
            choice = input("Seçiminiz: ").lower().strip()
            if choice and choice[0] in valid_keys:
                return choice[0]
            
            print(f"Hatalı seçim. Lütfen şu seçeneklerden birini girin: {', '.join(valid_keys)}")

    def _ask_questions(self):
        """
        Kullanıcıya lisans belirleme sorularını sorar ve
        cevapları 'self' niteliklerinde saklar.
        """
        # 1. Soru: Uyarlamalar
        adapt_prompt = "1. Eserinizin uyarlanmasına (remix, dönüştürme, üzerine inşa etme) izin veriyor musunuz?"
        adapt_options = {
            'e': 'Evet',
            's': 'Evet, başkaları da aynı şekilde paylaştığı sürece (ShareAlike)',
            'h': 'Hayır (Türetilemez - NoDerivs)'
        }
        # Cevabı 'self.adapt_choice' niteliğine kaydet
        self.adapt_choice = self._get_user_choice(adapt_prompt, adapt_options)

        # 2. Soru: Ticari Kullanım
        commercial_prompt = "2. Eserinizin ticari kullanımına izin veriyor musunuz?"
        commercial_options = {
            'e': 'Evet',
            'h': 'Hayır (Ticari Olmayan - NonCommercial)'
        }
        # Cevabı 'self.commercial_choice' niteliğine kaydet
        self.commercial_choice = self._get_user_choice(commercial_prompt, commercial_options)

    def _calculate_license(self):
        """
        'self' içinde saklanan kullanıcı cevaplarına göre
        lisans kodunu, adını ve URL'sini hesaplar.
        """
        # Ticari kullanım kontrolü
        if self.commercial_choice == 'h':
            self.license_code += "-NC"  # NonCommercial

        # Uyarlama kontrolü
        if self.adapt_choice == 's':
            self.license_code += "-SA"  # ShareAlike
        elif self.adapt_choice == 'h':
            self.license_code += "-ND"  # NoDerivs

        # Hesaplanan sonuçları 'self' niteliklerine kaydet
        self.license_name = f"{self.license_code} 4.0"
        self.license_url = f"https://creativecommons.org/licenses/{self.license_code.lower().replace('cc ', '')}/4.0/"

    def _display_license(self):
        """
        Hesaplanan lisans sonuçlarını ekrana basar.
        """
        print("\n" + "="*30)
        print("--- ÖNERİLEN LİSANS ---")
        print(f"Seçimlerinize göre önerilen lisans: {self.license_name}")
        print(f"Lisans hakkında detaylı bilgi: {self.license_url}")
        print("="*30 + "\n")

    def _generate_attribution(self):
        """
        Kullanıcıya atıf metni oluşturmayı teklif eder ve gerekirse
        gerekli bilgileri alır.
        """
        print("Lisansınız için önerilen atıf metnini oluşturmak ister misiniz?")
        if self._get_user_choice("Devam edilsin mi?", {'e': 'Evet', 'h': 'Hayır'}) == 'e':
            work_title = input("Eserinizin Adı: ")
            author_name = input("Sizin Adınız (veya Varlık Adı): ")
            
            print("\n--- ÖNERİLEN ATIF METNİ (Kopyalayıp kullanabilirsiniz) ---")
            print(
                f'"{work_title}" © {author_name}, {self.license_name} lisansı altında lisanslanmıştır. '
                f'Bu lisansın bir kopyasını görüntülemek için {self.license_url} adresini ziyaret edin.'
            )
            print("---------------------------------------------------------")

    def run(self):
        """
        Programı çalıştıran ana 'public' metot.
        Tüm iş akışını sırayla yönetir.
        """
        print("--- Creative Commons Lisans Seçme Aracı (OOP Versiyonu) ---")
        print("Eseriniz için en uygun Creative Commons lisansını bulmak için")
        print("lütfen aşağıdaki soruları yanıtlayın.")
        
        try:
            self._ask_questions()      # 1. Adım: Soruları sor
            self._calculate_license()  # 2. Adım: Cevaplara göre hesapla
            self._display_license()    # 3. Adım: Sonucu göster
            self._generate_attribution() # 4. Adım: Atıf oluştur (isteğe bağlı)
            
            print("\nİşlem tamamlandı. Programdan çıkılıyor.")
        
        except KeyboardInterrupt:
            print("\n\nProgram kullanıcı tarafından sonlandırıldı.")
            sys.exit()

# --- Programın Başlangıç Noktası ---
if __name__ == "__main__":
    """
    Bu blok, dosya doğrudan 'python dosya_adi.py' komutuyla
    çalıştırıldığında yürütülür.
    """
    # 1. LicenseChooser sınıfından bir 'nesne' (örnek) oluştur
    chooser = LicenseChooser()
    
    # 2. Oluşturulan bu nesnenin 'run' metodunu çağırarak programı başlat
    chooser.run()