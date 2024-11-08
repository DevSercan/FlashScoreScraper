from src.ui.MainWindow import Ui_MainWindow
from PySide6.QtWidgets import QStyledItemDelegate, QApplication, QMainWindow, QPushButton
from PySide6.QtCore import Qt, QTimer, QThread, QCoreApplication
from PySide6.QtGui import QPixmap, QIcon, QBrush, QColor, QMovie
from src.classes import Log, FlashScoreScraper
from src.utils.helper import getConfig, saveToExcel

CONFIG = getConfig()
log = Log()

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Bu sınıf; Programın ana sınıfıdır. Ana pencereyi görüntüler ve ana işlemleri gerçekleştirir.
    """
    def __init__(self):
        try:
            log.debug("The '__init__' function of the 'MainWindow' class has been executed.")
            super().__init__()
            self.setupUi(self)

            self.setWindowTitle("FlashScore Scraper") # Uygulama başlığını belirler. Bu başlık; Uygulama penceresinde, görev yöneticisinde vb. yerlerde görünür.

            icon = QIcon("assets/icons/icon.ico") # Uygulama için ikon tanımlar.
            self.setWindowIcon(icon) # Uygulamaya ikon ekler. Bu ikon; Uygulama penceresinde, görev yöneticisinde vb. yerlerde görülür.
        except Exception as e:
            log.error(f"Unexpected error in '__init__' function of the 'MainWindow' class:\n{e}")
    
    def updateInterface(self):
            """Uygulama arayüzünü günceller."""
            QApplication.processEvents()
    
    def main(self):
        try:
            log.debug("The 'main' function of the 'MainWindow' class has been executed.")

            platform = CONFIG["platform"] # Konfigürasyon dosyasından tarayıcının platform bilgisini alır. Örneğin; windows.
            driverName = CONFIG["driverName"] # Konfigürasyon dosyasından tarayıcı bilgisini alır. Örneğin: chrome.
            isHeadless = bool(CONFIG["isHeadless"]) # Konfigürasyon dosyasından tarayıcının görünüp görünmeyeceği bilgisini alır.

            scraper = FlashScoreScraper(platform=platform, driverName=driverName, isHeadless=isHeadless) # FlashScoreScraper sınıfından bir nesne üretiyoruz.
            print("Tarayıcı çalıştırılıyor...")
            scraper.open() # Tarayıcıyı başlatır.
            print("Tarayıcı çalıştırıldı.")

            eventLink = "https://www.flashscore.co.uk/match/AHtiptfM/#/match-summary"

            eventOddsData = []
            eventOddsData.extend(scraper.getOddsDataFromEvent(eventLink=eventLink))
            saveToExcel(data=eventOddsData, filename="EventOddsData")

            eventH2HData = []
            eventH2HData.extend(scraper.getH2HDataFromEvent(eventLink=eventLink))
            saveToExcel(data=eventH2HData, filename="EventH2HData")

            # liveData = [] # Canlı maç verilerini tutar.
            # oddsData = [] # Oran verilerini tutar.
            # finishedData = [] # Bitmiş maç verilerini tutar.

            # days = 3 # Son kaç günün verilerinin çekileceği bilgisini tutar.

            # for _ in range(days): # İstenen son günlerin verilerini çekebilmek için bir döngü başlatıyoruz.
            #     print("Bir önceki güne geçiliyor...")
            #     scraper.loadYesterday() # Bir önceki günün verilerini getirir.
            #     print("Bir önceki güne geçildi.")

            # print("LIVE verileri alınıyor...")
            # liveData.extend(scraper.getLiveData()) # Canlı (LIVE) maç verilerini alır ve diziye ekler.
            # print("LIVE verileri alındı.")

            # print("ODDS verileri alınıyor...")
            # oddsData.extend(scraper.getOddsData()) # Oranlar (ODDS) verilerini alır ve diziye ekler.
            # print("ODDS verileri alındı.")

            # print("FINISHED verileri alınıyor.")
            # finishedData.extend(scraper.getFinishedData()) # Bitmiş maçların verilerini alır ve diziye ekler.
            # print("FINISHED verileri alındı.")

            # # Verileri Excel'e kaydediyoruz.
            # print("Sonuçlar Excel dosyalarına kaydediliyor...")
            # saveToExcel(data=liveData, filename="LiveData")
            # saveToExcel(data=oddsData, filename="OddsData")
            # saveToExcel(data=finishedData, filename="FinishedData")
            # print("Sonuçlar Excel dosyalarına kaydedildi.")

            scraper.close()
        except Exception as e:
            log.error(f"Unexpected error in 'main' function of the 'MainWindow' class:\n{e}")

def main():
    try:
        log.createLogFile()
        log.debug("The 'main' function of main class has been executed.")
        app = QApplication([])
        mainWindow = MainWindow()
        mainWindow.show()
        app.exec()
    except Exception as e:
        log.error(f"Unexpected error occurred in 'main' function of main class:\n{e}")
    finally:
        log.debug("The 'main' function of main class has completed.")

if __name__ == '__main__':
    main()