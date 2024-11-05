from selenium import webdriver # Selenium kütüphanesi, tarayıcıyı kontrol etmek için kullanılan Python kütüphanesidir.
from selenium.webdriver.common.by import By # Web sayfalarında HTML elementlerini seçmek için By sınıfını kullanırız.
from selenium.webdriver.chrome.service import Service # Selenium ile çalışan Chrome tarayıcısını başlatmak için Service sınıfı kullanılır.
from selenium.webdriver.chrome.options import Options # Tarayıcı için ek seçenekler ayarlamak için Options sınıfı kullanılır.
from selenium.webdriver.support.ui import WebDriverWait # Selenium ile koşullu bekleme işlemleri için WebDriverWait kullanılır.
from selenium.webdriver.support import expected_conditions as EC # Belirli bir koşulun gerçekleşmesini beklemek için expected_conditions sınıfı kullanılır.
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities # Tarayıcı isteği yaparken bazı Selenium izlerini gizlemek için DesiredCapabilities sınıfı kullanılır.
import time

class FlashScoreScraper:
    """ FlashScore internet adresindeki maç verilerini kazımaya yarayan bir sınıf. """
    def __init__(self, platform:str, driverName:str):
        self.platform = platform.lower() # Kullanılacak sürücü için platform bilgisi. Örneğin; Windows, Linux.
        self.driverName = driverName.lower() # Kullanılacak sürücü için tarayıcı bilgisi. Örneğin; Chrome, Firefox.
        self.url = "https://www.flashscore.co.uk/" # FlashScore internet adresi.
        self.driver = self._initializeDriver() # Bir tarayıcı nesnesi oluşturur.
        self.wait = WebDriverWait(self.driver, 10) # JavaScript yüklenmesini beklemek için bir bekleyici oluşturur. Bekleme süresi saniye cinsindendir.

    def _initializeDriver(self):
        """ Tarayıcının başlangıç ayarlarını yapar ve tarayıcıyı tanımlar. """
        driverPath = f"webdrivers/{self.platform}/{self.driverName}/{self.driverName}driver.exe" # Sürücünün dosya konumunu tanımlıyoruz.
        options = self._initializeOptions() # Sürücüyü oluşturmadan önce başlangıç ayarlarını belirliyoruz.
        service = Service(driverPath) # Dosya konumundan alınan sürücüyü kullanarak bir hizmet tanımlıyoruz. Bu hizmet ile tarayıcı nesnesi oluşturacağız.
        driver = None # Tarayıcı nesnesini tutması için bir değişken oluşturuyoruz.
        if self.driverName == "chrome": # Eğer tarayıcı ismi "Chrome" ise koşul sağlanır.
            driver =  webdriver.Chrome(service=service, options=options) # Bir Chrome tarayıcı nesnesi oluşturur.
        driver.maximize_window() # Tarayıcıyı tam ekran yapar.
        return driver
        
    def _initializeOptions(self):
        """ Tarayıcı ayarlarını belirler. """
        options = Options() # Tarayıcı seçenekleri için gerekli nesneyi oluşturur.

        options.add_argument("--log-level=3") # Log seviyesini belirler. Log seviyesi 3 ise; Yalnızca uyarı ve hata mesajları gösterilir ve gereksiz bilgilendirici çıktılar görünmez.

        options.add_argument("--disable-gpu") # GPU hızlandırmasını devre dışı bırak. Headless modda bazen gerekli olabilir.
        options.add_argument("--no-sandbox") # Sandbox modunu devre dışı bırak. Bazı sistemlerde başlatma sorunlarını önleyebilir.

        options.add_argument('--ignore-certificate-errors') # SSL sertifika hatalarını göz ardı eder
        options.add_argument('--allow-insecure-localhost') # Yerel sunucu hatalarını yok say.
        
        options.add_argument("--disable-web-security")  # Web güvenlik önlemlerini devre dışı bırakır.
        options.add_argument("--allow-running-insecure-content")  # Güvensiz içeriği çalıştırmaya izin verir.
        options.add_argument("--disable-features=site-per-process")  # Site başına işlem özelliğini devre dışı bırakır.


        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager" # Hız için "eager" sayfa yükleme stratejisi kullan.

        options.add_experimental_option("excludeSwitches", ["enable-automation"]) # Otomasyonla ilgili bazı switch'leri devre dışı bırak.
        options.add_experimental_option("useAutomationExtension", False) # Otomasyon uzantısını devre dışı bırak.
        options.add_argument("--disable-blink-features=AutomationControlled") # Selenium izlerini gizlemeye yardımcı olur.

        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36") # Tarayıcıya özel bir kullanıcı ajanı ayarla.
    
    def waitJs(self):
        """ Maç sonuçlarının JavaScript ile yüklenmesini bekler. """
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'event__match'))) # JavaScript ile yüklenen içeriklerin tamamlanmasını bekler.

    def scrollTarget(self, targetElement):
        """ Sayfayı hedef öğenin konumuna kaydırır. """
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", targetElement)
        time.sleep(1)

    def open(self):
        """ Tarayıcıyı başlatır. """
        self.driver.get(self.url) # Sürücüyü başlatır.
        self.waitJs() # JavaScript yüklenmesini bekler.
    
    def close(self):
        """ Tarayıcıyı sonlandırır. """
        self.driver.quit() # Sürücüyü sonlandırır.
    
    def getMatches(self):
        """ Maç sonuçlarını web öğesi olarak döndürür. """
        soccerSection = self.driver.find_element(By.CLASS_NAME, 'sportName.soccer') # Maç verilerinin yer aldığı tabloyu seçer.
        matches = soccerSection.find_elements(By.CLASS_NAME, 'event__match') # Seçilen tablodan maç verilerini alır.
        return matches
    
    def clickFilterTab(self, targetTab:str):
        """ Maç sonuçlarının filtre sekmesinde bulunan, 'ODDS' veya 'FINISHED' gibi istenilen filtre seçeneğini seçer. """
        filterTabs = self.driver.find_elements(By.CLASS_NAME, 'filters__tab') # Filtre sekmesini alır.
        for tab in filterTabs: # Filtre sekmesindeki her bir filtreyi sırayla ele alıyoruz.
            if tab.text == targetTab: # Eğer mevcut filtre sekmesinin yazısı, hedef sekme yazısına eşit ise koşul sağlanır.
                self.scrollTarget(tab) # Butonu ortalayacak şekilde sayfayı kaydırır.
                tab.click() # Mevcut filtre sekmesine tıklar.
        self.waitJs() # JavaScript yüklenmesini bekler.
    
    def loadYesterday(self):
        """ Bir önceki günün verilerini yükler. """
        yesterdayButton = self.driver.find_element(By.CLASS_NAME, 'calendar__navigation--yesterday') # Takvim sekmesindeki, bir önceki gün butonunu seçer.
        self.scrollTarget(yesterdayButton) # Butonu ortalayacak şekilde sayfayı kaydırır.
        yesterdayButton.click() # Butona tıklar.
        self.waitJs() # JavaScript yüklenmesini bekler.
    
    def loadTomorrow(self):
        """ Bir sonraki günün verilerini yükler. """
        tomorrowButton = self.driver.find_element(By.CLASS_NAME, 'calendar__navigation--tomorrow') # Takvim sekmesindeki, bir sonraki gün butonunu seçer.
        self.scrollTarget(tomorrowButton) # Butonu ortalayacak şekilde sayfayı kaydırır.
        tomorrowButton.click() # Butona tıklar.
        self.waitJs() # JavaScript yüklenmesini bekler.
    
    def getFinishedData(self) -> list:
        """ Bitmiş (FINISHED) maç verilerini dizi olarak döndürür. """
        matches = self.getMatches() # Maç sonuçlarını alır.
        finishedData = [] # Bitmiş maç verilerini tutar.
        for match in matches: # Maçları sırayla döngüde ele alıyoruz.
            homeTeam = match.find_element(By.CLASS_NAME, "event__homeParticipant").text # Ana takımın adını alır.
            awayTeam = match.find_element(By.CLASS_NAME, "event__awayParticipant").text # Karşı takımın adını alır.
            homeScore = match.find_element(By.CLASS_NAME, "event__score--home").text # Ana takımın maç skorunu alır.
            awayScore = match.find_element(By.CLASS_NAME, "event__score--away").text # Karşı takımın maç skorunu alır.
            finishedData.append({ # Verileri diziye sözlük formatında ekler.
                "Home Team": homeTeam,
                "Away Team": awayTeam,
                "Home Score": homeScore,
                "Away Score": awayScore
            })
        return finishedData

    def getOddsData(self) -> list:
        """ Oranlardaki (ODDS) maç verilerini dizi olarak döndürür. """
        matches = self.getMatches() # Maç sonuçlarını alır.
        oddsData = [] # Oran verilerini tutar.
        for match in matches: # Maçları sırayla döngüde ele alıyoruz.
            homeTeam = match.find_element(By.CLASS_NAME, "event__participant--home").text # Ana takımın adını alır.
            awayTeam = match.find_element(By.CLASS_NAME, "event__participant--away").text # Karşı takımın adını alır.
            odds = match.find_elements(By.CLASS_NAME, "odds__odd") # Maç sonucunun oran verilerini alır.
            oddList = [] # Oranları tutar.
            for odd in odds: # Oranları sırayla döngüde ele alıyoruz.
                oddList.append(odd.text) # Oran verisini diziye ekler.
            oddsData.append({ # Verileri diziye sözlük formatında ekler.
                "Home Team": homeTeam,
                "Away Team": awayTeam,
                "Odds": ', '.join(oddList)
            })
        return oddsData