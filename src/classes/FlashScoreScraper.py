from selenium import webdriver # Selenium kütüphanesi, tarayıcıyı kontrol etmek için kullanılan Python kütüphanesidir.
from selenium.webdriver.common.by import By # Web sayfalarında HTML elementlerini seçmek için By sınıfını kullanırız.
from selenium.webdriver.chrome.service import Service # Selenium ile çalışan Chrome tarayıcısını başlatmak için Service sınıfı kullanılır.
from selenium.webdriver.chrome.options import Options # Tarayıcı için ek seçenekler ayarlamak için Options sınıfı kullanılır.
from selenium.webdriver.support.ui import WebDriverWait # Selenium ile koşullu bekleme işlemleri için WebDriverWait kullanılır.
from selenium.webdriver.support import expected_conditions as EC # Belirli bir koşulun gerçekleşmesini beklemek için expected_conditions sınıfı kullanılır.
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities # Tarayıcı isteği yaparken bazı Selenium izlerini gizlemek için DesiredCapabilities sınıfı kullanılır.
import time
from fractions import Fraction

from src.classes import Log
log = Log()

class FlashScoreScraper:
    """ FlashScore internet adresindeki maç verilerini kazımaya yarayan bir sınıf. """
    def __init__(self, platform:str, driverName:str, isHeadless:bool):
        try:
            log.debug("The '__init__' function of the 'FlashScoreScraper' class has been executed.")
            self.platform = platform.lower() # Kullanılacak sürücü için platform bilgisi. Örneğin; Windows, Linux.
            self.driverName = driverName.lower() # Kullanılacak sürücü için tarayıcı bilgisi. Örneğin; Chrome, Firefox.
            self.isHeadless = isHeadless # Tarayıcının görünmez olarak çalışıp çalışmayacağı bilgisini tutar.
            self.url = "https://www.flashscore.co.uk/" # FlashScore internet adresi.
        except Exception as e:
            log.error(f"Unexpected error in '__init__' function of the 'FlashScoreScraper' class:\n{e}")

    def _initializeDriver(self):
        """ Tarayıcının başlangıç ayarlarını yapar ve tarayıcıyı tanımlar. """
        try:
            log.debug("The '_initializeDriver' function of the 'FlashScoreScraper' class has been executed.")
            driverPath = f"webdrivers/{self.platform}/{self.driverName}/{self.driverName}driver.exe" # Sürücünün dosya konumunu tanımlıyoruz.
            options = self._getOptions() # Sürücüyü oluşturmadan önce başlangıç ayarlarını belirliyoruz.
            service = Service(driverPath) # Dosya konumundan alınan sürücüyü kullanarak bir hizmet tanımlıyoruz. Bu hizmet ile tarayıcı nesnesi oluşturacağız.
            driver = None # Tarayıcı nesnesini tutması için bir değişken oluşturuyoruz.
            if self.driverName == "chrome": # Eğer tarayıcı ismi "Chrome" ise koşul sağlanır.
                driver =  webdriver.Chrome(service=service, options=options) # Bir Chrome tarayıcı nesnesi oluşturur.
            driver.maximize_window() # Tarayıcıyı tam ekran yapar.
            return driver
        except Exception as e:
            log.error(f"Unexpected error in '_initializeDriver' function of the 'FlashScoreScraper' class:\n{e}")
            return None
        
    def _getOptions(self):
        """ Tarayıcı ayarlarını belirler. """
        try:
            log.debug("The '_getOptions' function of the 'FlashScoreScraper' class has been executed.")
            options = Options() # Tarayıcı seçenekleri için gerekli nesneyi oluşturur.

            if self.isHeadless:
                options.add_argument("--headless") # Tarayıcı, arka planda görünmez olarak çalışır.

            options.add_argument("--log-level=3") # Log seviyesini belirler. Log seviyesi 3 ise; Yalnızca uyarı ve hata mesajları gösterilir ve gereksiz bilgilendirici çıktılar görünmez.

            options.add_argument("--disable-gpu") # GPU hızlandırmasını devre dışı bırak. Headless modda bazen gerekli olabilir.
            options.add_argument("--no-sandbox") # Sandbox modunu devre dışı bırak. Bazı sistemlerde başlatma sorunlarını önleyebilir.

            options.add_argument("--mute-audio") # Tarayıcı sesini kapatır.

            options.add_argument('--ignore-certificate-errors') # SSL sertifika hatalarını göz ardı eder
            options.add_argument('--allow-insecure-localhost') # Yerel sunucu hatalarını yok say.

            options.add_argument("--enable-unsafe-swiftshader") # WebGL uyarılarını almamak için gereklidir.
            
            options.add_argument("--disable-web-security")  # Web güvenlik önlemlerini devre dışı bırakır.
            options.add_argument("--allow-running-insecure-content")  # Güvensiz içeriği çalıştırmaya izin verir.
            options.add_argument("--disable-features=site-per-process")  # Site başına işlem özelliğini devre dışı bırakır.
            options.add_argument("start-maximized")  # Tarayıcıyı tam ekran başlatır.

            caps = DesiredCapabilities().CHROME
            caps["pageLoadStrategy"] = "eager" # Hız için "eager" sayfa yükleme stratejisi kullan.

            options.add_experimental_option("excludeSwitches", ["enable-automation"]) # Otomasyonla ilgili bazı switch'leri devre dışı bırak.
            options.add_experimental_option("useAutomationExtension", False) # Otomasyon uzantısını devre dışı bırak.
            options.add_argument("--disable-blink-features=AutomationControlled") # Selenium izlerini gizlemeye yardımcı olur.

            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36") # Tarayıcıya özel bir kullanıcı ajanı ayarla.
            
            return options
        except Exception as e:
            log.error(f"Unexpected error in '_getOptions' function of the 'FlashScoreScraper' class:\n{e}")
            return None

    def waitJs(self, className:str) -> bool:
        """ Maç sonuçlarının JavaScript ile yüklenmesini bekler. """
        try:
            log.debug(f"[className={className}] The 'waitJs' function of the 'FlashScoreScraper' class has been executed.")
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, className))) # JavaScript ile yüklenen içeriklerin tamamlanmasını bekler.
            return True
        except Exception as e:
            log.error(f"[className={className}] Unexpected error in 'waitJs' function of the 'FlashScoreScraper' class:\n{e}")
            return False

    def scrollTarget(self, targetElement) -> bool:
        """ Sayfayı hedef öğenin konumuna kaydırır. """
        try:
            log.debug("The 'scrollTarget' function of the 'FlashScoreScraper' class has been executed.")
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", targetElement)
            time.sleep(1)
            return True
        except Exception as e:
            log.error(f"Unexpected error in 'scrollTarget' function of the 'FlashScoreScraper' class:\n{e}")
            return False
    
    def scrollBottom(self) -> bool:
        """ Mevcut tarayıcı sayfasını en aşağı kaydırır. """
        try:
            log.debug("The 'scrollBottom' function of the 'FlashScoreScraper' class has been executed.")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            return True
        except Exception as e:
            log.error(f"Unexpected error in 'scrollBottom' function of the 'FlashScoreScraper' class:\n{e}")
            return False
    
    def scrollTop(self) -> bool:
        """ Mevcut tarayıcı sayfasını en yukarı kaydırır. """
        try:
            log.debug("The 'scrollTop' function of the 'FlashScoreScraper' class has been executed.")
            self.driver.execute_script("window.scrollTo(0, 0);")
            return True
        except Exception as e:
            log.error(f"Unexpected error in 'scrollTop' function of the 'FlashScoreScraper' class:\n{e}")
            return False

    def open(self) -> bool:
        """ Tarayıcıyı başlatır. """
        try:
            log.debug("The 'open' function of the 'FlashScoreScraper' class has been executed.")
            self.driver = self._initializeDriver() # Bir tarayıcı nesnesi oluşturur.
            self.wait = WebDriverWait(self.driver, 10) # JavaScript yüklenmesini beklemek için bir bekleyici oluşturur. Bekleme süresi saniye cinsindendir.
            self.driver.get(self.url) # Sürücüyü başlatır.
            self.waitJs('event__match') # JavaScript yüklenmesini bekler.
            return True
        except Exception as e:
            log.error(f"Unexpected error in 'open' function of the 'FlashScoreScraper' class:\n{e}")
            return False
    
    def close(self) -> bool:
        """ Tarayıcıyı sonlandırır. """
        try:
            log.debug("The 'close' function of the 'FlashScoreScraper' class has been executed.")
            self.driver.quit() # Sürücüyü sonlandırır.
            return True
        except Exception as e:
            log.error(f"Unexpected error in 'close' function of the 'FlashScoreScraper' class:\n{e}")
            return False
    
    def getMatches(self):
        """ Maç sonuçlarını web öğesi olarak döndürür. """
        try:
            log.debug("The 'getMatches' function of the 'FlashScoreScraper' class has been executed.")
            soccerSection = self.driver.find_element(By.CLASS_NAME, 'sportName.soccer') # Maç verilerinin yer aldığı tabloyu seçer.
            matches = soccerSection.find_elements(By.CLASS_NAME, 'event__match') # Seçilen tablodan maç verilerini alır.
            return matches
        except Exception as e:
            log.error(f"Unexpected error in 'getMatches' function of the 'FlashScoreScraper' class:\n{e}")
            return None
    
    def clickFilterTab(self, targetTab:str) -> bool:
        """ Maç sonuçlarının filtre sekmesinde bulunan, 'ODDS' veya 'FINISHED' gibi istenilen filtre seçeneğini seçer. """
        try:
            log.debug(f"[targetTab={targetTab}] The 'clickFilterTab' function of the 'FlashScoreScraper' class has been executed.")
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'filters__tab'))) # 'filters__tab' sınıfının yüklenmesini bekler.
            filterTabs = self.driver.find_elements(By.CLASS_NAME, 'filters__tab') # Filtre sekmesini alır.
            for tab in filterTabs: # Filtre sekmesindeki her bir filtreyi sırayla ele alıyoruz.
                if tab.text == targetTab: # Eğer mevcut filtre sekmesinin yazısı, hedef sekme yazısına eşit ise koşul sağlanır.
                    self.scrollTarget(tab) # Butonu ortalayacak şekilde sayfayı kaydırır.
                    tab.click() # Mevcut filtre sekmesine tıklar.
                    break
            self.waitJs('event__match') # JavaScript yüklenmesini bekler.
            return True
        except Exception as e:
            log.error(f"[targetTab={targetTab}] Unexpected error in 'clickFilterTab' function of the 'FlashScoreScraper' class:\n{e}")
            return False
    
    def clickEventFilterTab(self, targetTab:str) -> bool:
        """ Etkinliklerde filtre sekmesinde bulunan, 'ODDS' veya 'H2H' gibi istenilen filtre seçeneğini seçer. """
        try:
            log.debug(f"[targetTab={targetTab}] The 'clickEventFilterTab' function of the 'FlashScoreScraper' class has been executed.")
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@data-testid="wcl-tab"]'))) # 'wcl-tab ' ögesinin yüklenmesini bekler.
            filterTabs = self.driver.find_elements(By.XPATH, '//button[@data-testid="wcl-tab"]') # Filtre sekmesini alır.
            for tab in filterTabs: # Filtre sekmesindeki her bir filtreyi sırayla ele alıyoruz.
                if tab.text == targetTab: # Eğer mevcut filtre sekmesinin yazısı, hedef sekme yazısına eşit ise koşul sağlanır.
                    self.scrollTarget(tab) # Butonu ortalayacak şekilde sayfayı kaydırır.
                    tab.click() # Mevcut filtre sekmesine tıklar.
                    break
            return True
        except Exception as e:
            log.error(f"[targetTab={targetTab}] Unexpected error in 'clickEventFilterTab' function of the 'FlashScoreScraper' class:\n{e}")
            return False
    
    def loadYesterday(self) -> bool:
        """ Bir önceki günün verilerini yükler. """
        try:
            log.debug("The 'loadYesterday' function of the 'FlashScoreScraper' class has been executed.")
            yesterdayButton = self.driver.find_element(By.CLASS_NAME, 'calendar__navigation--yesterday') # Takvim sekmesindeki, bir önceki gün butonunu seçer.
            self.scrollTarget(yesterdayButton) # Butonu ortalayacak şekilde sayfayı kaydırır.
            yesterdayButton.click() # Butona tıklar.
            self.waitJs('event__match') # JavaScript yüklenmesini bekler.
            return True
        except Exception as e:
            log.error(f"Unexpected error in 'loadYesterday' function of the 'FlashScoreScraper' class:\n{e}")
            return False
    
    def loadTomorrow(self) -> bool:
        """ Bir sonraki günün verilerini yükler. """
        try:
            log.debug("The 'loadTomorrow' function of the 'FlashScoreScraper' class has been executed.")
            tomorrowButton = self.driver.find_element(By.CLASS_NAME, 'calendar__navigation--tomorrow') # Takvim sekmesindeki, bir sonraki gün butonunu seçer.
            self.scrollTarget(tomorrowButton) # Butonu ortalayacak şekilde sayfayı kaydırır.
            tomorrowButton.click() # Butona tıklar.
            self.waitJs('event__match') # JavaScript yüklenmesini bekler.
            return True
        except Exception as e:
            log.error(f"Unexpected error in 'loadTomorrow' function of the 'FlashScoreScraper' class:\n{e}")
            return False
    
    def getLiveData(self) -> list:
        """ Canlı maç verilerini dizi olarak döndürür. """
        try:
            log.debug("The 'getLiveData' function of the 'FlashScoreScraper' class has been executed.")
            self.clickFilterTab("LIVE") # Maç filtrelerinden "FINISHED" sekmesini seçer.
            matches = self.getMatches() # Maç sonuçlarını alır.
            liveData = []
            for match in matches: # Maçları sırayla döngüde ele alıyoruz.
                homeTeam = match.find_element(By.CLASS_NAME, "event__homeParticipant").text # Ana takımın adını alır.
                awayTeam = match.find_element(By.CLASS_NAME, "event__awayParticipant").text # Karşı takımın adını alır.
                homeScore = match.find_element(By.CLASS_NAME, "event__score--home").text # Ana takımın maç skorunu alır.
                awayScore = match.find_element(By.CLASS_NAME, "event__score--away").text # Karşı takımın maç skorunu alır.
                eventLink = match.find_element(By.CLASS_NAME, "eventRowLink").get_attribute("href") # Etkinliğin linkini alır.
                liveData.append({ # Verileri diziye sözlük formatında ekler.
                    "Home Team": homeTeam,
                    "Away Team": awayTeam,
                    "Home Score": homeScore,
                    "Away Score": awayScore,
                    "Event Link": eventLink
                })
            return liveData
        except Exception as e:
            log.error(f"Unexpected error in 'getLiveData' function of the 'FlashScoreScraper' class:\n{e}")
            return []

    def getFinishedData(self) -> list:
        """ Bitmiş (FINISHED) maç verilerini dizi olarak döndürür. """
        try:
            log.debug("The 'getFinishedData' function of the 'FlashScoreScraper' class has been executed.")
            self.clickFilterTab("FINISHED") # Maç filtrelerinden "FINISHED" sekmesini seçer.
            matches = self.getMatches() # Maç sonuçlarını alır.
            finishedData = [] # Bitmiş maç verilerini tutar.
            for match in matches: # Maçları sırayla döngüde ele alıyoruz.
                homeTeam = match.find_element(By.CLASS_NAME, "event__homeParticipant").text # Ana takımın adını alır.
                awayTeam = match.find_element(By.CLASS_NAME, "event__awayParticipant").text # Karşı takımın adını alır.
                homeScore = match.find_element(By.CLASS_NAME, "event__score--home").text # Ana takımın maç skorunu alır.
                awayScore = match.find_element(By.CLASS_NAME, "event__score--away").text # Karşı takımın maç skorunu alır.
                eventLink = match.find_element(By.CLASS_NAME, "eventRowLink").get_attribute("href") # Etkinliğin linkini alır.
                finishedData.append({ # Verileri diziye sözlük formatında ekler.
                    "Home Team": homeTeam,
                    "Away Team": awayTeam,
                    "Home Score": homeScore,
                    "Away Score": awayScore,
                    "Event Link": eventLink
                })
            return finishedData
        except Exception as e:
            log.error(f"Unexpected error in 'getFinishedData' function of the 'FlashScoreScraper' class:\n{e}")
            return []

    def getOddsData(self) -> list:
        """ Oranlardaki (ODDS) maç verilerini dizi olarak döndürür. """
        try:
            log.debug("The 'getOddsData' function of the 'FlashScoreScraper' class has been executed.")
            self.clickFilterTab(targetTab="ODDS") # Maç filtrelerinden "ODDS" sekmesini seçer.
            matches = self.getMatches() # Maç sonuçlarını alır.
            oddsData = [] # Oran verilerini tutar.
            for match in matches: # Maçları sırayla döngüde ele alıyoruz.
                homeTeam = match.find_element(By.CLASS_NAME, "event__participant--home").text # Ana takımın adını alır.
                awayTeam = match.find_element(By.CLASS_NAME, "event__participant--away").text # Karşı takımın adını alır.
                odds = match.find_elements(By.CLASS_NAME, "odds__odd") # Maç sonucunun oran verilerini alır.
                oddList = [] # Oranları tutar.
                for odd in odds: # Oranları sırayla döngüde ele alıyoruz.
                    oddList.append(str(float(Fraction(odd.text))+1)) # Oran verisini diziye ekler.
                oddsData.append({ # Verileri diziye sözlük formatında ekler.
                    "Home Team": homeTeam,
                    "Away Team": awayTeam,
                    "Odds": ', '.join(oddList)
                })
            return oddsData
        except Exception as e:
            log.error(f"Unexpected error in 'getOddsData' function of the 'FlashScoreScraper' class:\n{e}")
            return []
    
    def getOddsDataFromEvent(self, eventLink:str) -> list:
        """ Bir etkinlikteki oran verilerini alır. """
        try:
            log.debug("The 'getOddsDataFromEvent' function of the 'FlashScoreScraper' class has been executed.")
            self.driver.get(eventLink) # Sürücüyü başlatır.
            self.waitJs('detailOver') # JavaScript yüklenmesini bekler.
            self.clickEventFilterTab(targetTab="ODDS") # Maç filtrelerinden "ODDS" sekmesini seçer.
            self.waitJs('ui-table') # JavaScript yüklenmesini bekler.
            bodyUiTable = self.driver.find_element(By.CLASS_NAME, 'ui-table__body') # Verilerin yer aldığı tabloyu seçer.
            odds = bodyUiTable.find_elements(By.CLASS_NAME, 'ui-table__row') # Seçilen tablodan ODDS verilerini alır.
            oddsData = [] # Oran verilerini tutar.
            for odd in odds: # Maçları sırayla döngüde ele alıyoruz.
                bookmaker = odd.find_element(By.CLASS_NAME, "prematchLink").get_attribute("title") # Ana takımın adını alır.
                odds = odd.find_elements(By.CLASS_NAME, "oddsCell__odd") # Maç sonucunun oran verilerini alır.
                oddList = [] # Oranları tutar.
                for odd in odds: # Oranları sırayla döngüde ele alıyoruz.
                    oddList.append(str(float(Fraction(odd.text))+1)) # Oran verisini diziye ekler.
                oddsData.append({ # Verileri diziye sözlük formatında ekler.
                    "Bookmaker": bookmaker,
                    "Odds": ', '.join(oddList)
                })
            return oddsData
            
        except Exception as e:
            log.error(f"Unexpected error in 'getOddsDataFromEvent' function of the 'FlashScoreScraper' class:\n{e}")
            return []
    
    def showMoreH2H(self) -> bool:
        """ H2H Sayfasında daha fazla maç gösteren seçeneğe tıklar. """
        try:
            log.debug("The 'showMoreH2H' function of the 'FlashScoreScraper' class has been executed.")
            while True:
                try:
                    showMoreButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "showMore")))
                    self.scrollTarget(showMoreButton)
                    showMoreButton.click()
                    time.sleep(0.4)
                except:
                    break
            return True
        except Exception as e:
            log.error(f"Unexpected error in 'showMoreH2H' function of the 'FlashScoreScraper' class:\n{e}")
            return False

    def getH2HDataFromEvent(self, eventLink:str) -> list:
        """ Bir etkinlikteki H2H verilerini alır. """
        try:
            log.debug("The 'getH2HDataFromEvent' function of the 'FlashScoreScraper' class has been executed.")
            self.driver.get(eventLink) # Sürücüyü başlatır.
            self.waitJs('detailOver') # JavaScript yüklenmesini bekler.
            self.clickEventFilterTab(targetTab="H2H") # Maç filtrelerinden "H2H" sekmesini seçer.
            self.waitJs('h2h') # JavaScript yüklenmesini bekler.
            self.showMoreH2H()
            h2hTable = self.driver.find_element(By.CLASS_NAME, 'h2h') # H2H Verilerinin yer aldığı tabloyu seçer.
            h2hSections = h2hTable.find_elements(By.CLASS_NAME, "h2h__section") # Seçilen tablodan grupları seçer.
            h2hData = [] # Oran verilerini tutar.
            for section in h2hSections: # Seçilen grupları sırayla döngüde ele alıyoruz.
                h2hList = section.find_elements(By.CLASS_NAME, 'h2h__row') # Seçilen gruplardan H2H verilerini alır.
                for h2h in h2hList: # Maçları sırayla döngüde ele alıyoruz.
                    title = section.find_element(By.CLASS_NAME, "section__title").text
                    date = h2h.find_element(By.CLASS_NAME, "h2h__date").text
                    event = h2h.find_element(By.CLASS_NAME, "h2h__event").text
                    homeTeam = h2h.find_element(By.CLASS_NAME, "h2h__homeParticipant").text
                    awayTeam = h2h.find_element(By.CLASS_NAME, "h2h__awayParticipant").text
                    result = h2h.find_element(By.CLASS_NAME, "h2h__result")
                    scoreList = result.find_elements(By.TAG_NAME, "span")
                    homeScore = scoreList[0].text
                    awayScore = scoreList[1].text
                    h2hData.append({ # Verileri diziye sözlük formatında ekler.
                        "Title": title,
                        "Date": date,
                        "Event": event,
                        "Home Team": homeTeam,
                        "Away Team": awayTeam,
                        "Home Score": homeScore,
                        "Away Score": awayScore
                    })
            return h2hData
        except Exception as e:
            log.error(f"Unexpected error in 'getH2HDataFromEvent' function of the 'FlashScoreScraper' class:\n{e}")
            return []