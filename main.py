from src.ui.MainWindow import Ui_MainWindow
from src.ui.EventDetailsWindow import Ui_Form
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHeaderView
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel
from src.classes import Log, FlashScoreScraper
from src.utils.helper import getConfig, saveToExcel

CONFIG = getConfig()
log = Log()

class EventDetailsWindow(QWidget, Ui_Form):
    def __init__(self, oddsData:list, h2hData:list):
        try:
            log.debug("The '__init__' function of the 'EventDetailsWindow' class has been executed.")
            super().__init__()
            self.setupUi(self)

            self.setWindowTitle("FlashScore Scraper - Event Details") # Uygulama başlığını belirler. Bu başlık; Uygulama penceresinde, görev yöneticisinde vb. yerlerde görünür.

            icon = QIcon("assets/icons/icon.ico") # Uygulama için ikon tanımlar.
            self.setWindowIcon(icon) # Uygulamaya ikon ekler. Bu ikon; Uygulama penceresinde, görev yöneticisinde vb. yerlerde görülür.

            self.oddsData = oddsData
            self.h2hData = h2hData

            # QStandardItemModel oluşturun ve sütun başlıklarını ayarlayın
            self.eventDetailsModel = QStandardItemModel()

            self.pbtnGetOddsData.clicked.connect(self.showOddsData)
            self.pbtnGetH2hData.clicked.connect(self.showH2hData)
        except Exception as e:
            log.error(f"Unexpected error occurred in '__init__' function of 'EventDetailsWindow' class:\n{e}")

    def showOddsData(self):
        try:
            log.debug("The 'showOddsData' function of the 'EventDetailsWindow' class has been executed.")
            self.eventDetailsModel.clear() # Modeli sıfırlar.

            self.eventDetailsModel.setHorizontalHeaderLabels(["Bahisçi", "Sonuçlar"])
            self.tblvwEventDetails.setModel(self.eventDetailsModel) # Modeli tabloya bağlıyoruz.

            self.eventDetailsModel.removeRows(0, self.eventDetailsModel.rowCount()) # Tablodaki mevcut verileri temizler.
            for rowData in self.oddsData:
                rowItems = [QStandardItem(str(item)) for item in rowData.values()]
                self.eventDetailsModel.appendRow(rowItems)
            
            self.tblvwEventDetails.resizeColumnsToContents() # Tablodaki sütun genişliklerini içeriğe göre düzenler.
        except Exception as e:
            log.error(f"Unexpected error occurred in 'showOddsData' function of 'EventDetailsWindow' class:\n{e}")
    
    def showH2hData(self):
        try:
            log.debug("The 'showH2hData' function of the 'EventDetailsWindow' class has been executed.")
            self.eventDetailsModel.clear() # Modeli sıfırlar.
            
            self.eventDetailsModel.setHorizontalHeaderLabels(["Başlık", "Tarih", "Etkinlik", "Ana Takım", "Karşı Takım", "Ana Takım Skoru", "Karşı Takım Skoru"])
            self.tblvwEventDetails.setModel(self.eventDetailsModel) # Modeli tabloya bağlıyoruz.

            self.eventDetailsModel.removeRows(0, self.eventDetailsModel.rowCount()) # Tablodaki mevcut verileri temizler.
            for rowData in self.h2hData:
                rowItems = [QStandardItem(str(item)) for item in rowData.values()]
                self.eventDetailsModel.appendRow(rowItems)
            
            self.tblvwEventDetails.resizeColumnsToContents() # Tablodaki sütun genişliklerini içeriğe göre düzenler.
        except Exception as e:
            log.error(f"Unexpected error occurred in 'showH2hData' function of 'EventDetailsWindow' class:\n{e}")

class GetLiveMatchesThread(QThread):
    def __init__(self, mainWindow):
        try:
            log.debug("The '__init__' function of the 'GetLiveMatchesThread' class has been executed.")
            super().__init__()
            self.mainWindow = mainWindow
        except Exception as e:
            log.error(f"Unexpected error occurred in '__init__' function of 'GetLiveMatchesThread' class:\n{e}")
        finally:
            log.debug("The '__init__' function of the 'GetLiveMatchesThread' class has completed.")

    def run(self):
        try:
            log.debug("The 'run' function of the 'GetLiveMatchesThread' class has been executed.")
            self.mainWindow.getLiveMatches()
        except Exception as e:
            log.error(f"Unexpected error occurred in 'run' function of 'GetLiveMatchesThread' class:\n{e}")
        finally:
            log.debug("The 'run' function of the 'GetLiveMatchesThread' class has completed.")

class ShowEventDetailsThread(QThread):
    finishedSignal = Signal()  # Thread dışında ana sınıfa sinyal gönderebilmek için bir sinyal tanımlıyoruz.

    def __init__(self, mainWindow, eventLink:str=""):
        try:
            log.debug("The '__init__' function of the 'ShowEventDetailsThread' class has been executed.")
            super().__init__()
            self.mainWindow = mainWindow
            self.eventLink = eventLink
        except Exception as e:
            log.error(f"Unexpected error occurred in '__init__' function of 'ShowEventDetailsThread' class:\n{e}")
        finally:
            log.debug("The '__init__' function of the 'ShowEventDetailsThread' class has completed.")

    def run(self):
        try:
            log.debug("The 'run' function of the 'ShowEventDetailsThread' class has been executed.")
            self.mainWindow.showEventDetails(self.eventLink)
        except Exception as e:
            log.error(f"Unexpected error occurred in 'run' function of 'ShowEventDetailsThread' class:\n{e}")
        finally:
            log.debug("The 'run' function of the 'ShowEventDetailsThread' class has completed.")
            self.finishedSignal.emit() # İşlem bittiğinde sinyal gönderiyoruz.

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

            # QStandardItemModel oluşturun ve sütun başlıklarını ayarlayın
            self.liveMatchesModel = QStandardItemModel()
            self.liveMatchesModel.setHorizontalHeaderLabels(["Ana Takım", "Karşı Takım", "Ana Takım Skoru", "Karşı Takım Skoru", "Etkinlik Linki", "İstatistikler"])
            self.tblvwLiveMatches.setModel(self.liveMatchesModel) # Modeli tabloya bağlıyoruz.
            self.tblvwLiveMatches.clicked.connect(self.onTableClick) # Tıklama olayını dinliyoruz.
            self.isEventLoading = False # Etkinlik detayları yüklenirken bu değişken True olur. Böylece aynı anda birden fazla etkinlik görüntülenemez.

            self.showEventDetailsThread = ShowEventDetailsThread(self)
            self.showEventDetailsThread.finishedSignal.connect(self.onShowEventDetailsFinished) # ShowEventDetailsThread sınıfındaki sinyali bir fonksiyona bağlıyoruz. Fonksiyon, burada Slot olarak kullanılacak.

            self.pbtnGetLiveMatches.clicked.connect(self.clickedPbtnGetLiveMatches)
            self.getLiveMatchesThread = GetLiveMatchesThread(self)
        except Exception as e:
            log.error(f"Unexpected error in '__init__' function of the 'MainWindow' class:\n{e}")
    
    def updateInterface(self):
        """Uygulama arayüzünü günceller."""
        QApplication.processEvents()
    
    def togglePushButton(self, pushButton:QPushButton, status:bool):
        try:
            log.debug("The 'togglePushButton' function of the 'MainWindow' class has been executed.")
            pushButton.setEnabled(status)
            if status:
                pushButton.setStyleSheet("")
            else:
                pushButton.setStyleSheet("QPushButton {background-color: #585858; color: #fff;}") # Buton stilini devre dışı bırakılmış gibi yapar.
        except Exception as e:
            log.error(f"Unexpected error in 'togglePushButton' function of the 'MainWindow' class:\n{e}")
    
    def onTableClick(self, index):
        """Tabloda bir hücreye tıklanması durumunda çalışacak fonksiyon."""
        try:
            log.debug("The 'onTableClick' function of the 'MainWindow' class has been executed.")
            if index.column() == 5 and self.isEventLoading == False: # 5. Index = İstatistikler sütunu
                self.isEventLoading = True
                eventLink = self.liveMatchesModel.index(index.row(), 4).data() # "Etkinlik Linki" sütunundaki veriyi alıyoruz.
                self.clickedShowEventDetails(eventLink)
        except Exception as e:
            log.error(f"Unexpected error in 'onTableClick' function of the 'MainWindow' class:\n{e}")

    def setMessage(self, message:str):
        try:
            log.debug("The 'setMessage' function of the 'MainWindow' class has been executed.")
            self.lblMessage.setText(message)
        except Exception as e:
            log.error(f"Unexpected error in 'setMessage' function of the 'MainWindow' class:\n{e}")
    
    def clickedShowEventDetails(self, eventLink:str):
        try:
            log.debug("The 'clickedShowEventDetails' function of the 'MainWindow' class has been executed.")
            self.showEventDetailsThread.eventLink = eventLink
            self.showEventDetailsThread.start()
        except Exception as e:
            log.error(f"Unexpected error in 'clickedShowEventDetails' function of the 'MainWindow' class:\n{e}")

    def showEventDetails(self, eventLink:str):
        try:
            log.debug("The 'showEventDetails' function of the 'MainWindow' class has been executed.")
            self.setMessage("Seçilen etkinlik detayları getiriliyor...")

            platform = CONFIG["platform"] # Konfigürasyon dosyasından tarayıcının platform bilgisini alır. Örneğin; windows.
            driverName = CONFIG["driverName"] # Konfigürasyon dosyasından tarayıcı bilgisini alır. Örneğin: chrome.
            isHeadless = bool(CONFIG["isHeadless"]) # Konfigürasyon dosyasından tarayıcının görünüp görünmeyeceği bilgisini alır.

            scraper = FlashScoreScraper(platform=platform, driverName=driverName, isHeadless=isHeadless) # FlashScoreScraper sınıfından bir nesne üretiyoruz.
            scraper.open()
            self.oddsData = scraper.getOddsDataFromEvent(eventLink)
            self.h2hData = scraper.getH2HDataFromEvent(eventLink)
            scraper.close()

            self.setMessage("Etkinlik detayları getirildi. Etkinlik detayları görüntüleniyor...")
        except Exception as e:
            self.setMessage("Seçilen etkinlik detayları getirilemedi!")
            log.error(f"Unexpected error in 'showEventDetails' function of the 'MainWindow' class:\n{e}")
        finally:
            self.isEventLoading = False
            self.showEventDetailsThread.quit()
    
    def onShowEventDetailsFinished(self):
        self.eventDetailsWindow = EventDetailsWindow(oddsData=self.oddsData, h2hData=self.h2hData)
        self.eventDetailsWindow.show() # Mod olmayan (non-modal) olarak pencereyi açar, ana pencere açık kalır.
        self.setMessage("Etkinlik detayları görüntülendi.")

    def getLiveMatches(self):
        try:
            log.debug("The 'getLiveMatches' function of the 'MainWindow' class has been executed.")
            self.setMessage("Canlı maç verileri alınıyor...")
            self.liveMatchesModel.removeRows(0, self.liveMatchesModel.rowCount()) # Tablodaki mevcut verileri temizler.
            platform = CONFIG["platform"] # Konfigürasyon dosyasından tarayıcının platform bilgisini alır. Örneğin; windows.
            driverName = CONFIG["driverName"] # Konfigürasyon dosyasından tarayıcı bilgisini alır. Örneğin: chrome.
            isHeadless = bool(CONFIG["isHeadless"]) # Konfigürasyon dosyasından tarayıcının görünüp görünmeyeceği bilgisini alır.

            scraper = FlashScoreScraper(platform=platform, driverName=driverName, isHeadless=isHeadless) # FlashScoreScraper sınıfından bir nesne üretiyoruz.
            scraper.open() # Tarayıcıyı başlatır.
            liveData = scraper.getLiveData() # Canlı maç verilerini alır.
            scraper.close() # Tarayıcıyı sonlandırır.
            self.setMessage("Canlı maç verileri alındı. Maç verileri görüntüleniyor...")

            for rowData in liveData:
                rowItems = [QStandardItem(str(item)) for item in rowData.values()]
                rowItems.append(QStandardItem("Detayları Göster"))
                self.liveMatchesModel.appendRow(rowItems)
            
            self.tblvwLiveMatches.resizeColumnsToContents() # Tablodaki sütun genişliklerini içeriğe göre düzenler.
            self.setMessage("Canlı maç verileri görüntülendi.")
        except Exception as e:
            self.setMessage("Canlı maç verilerini görüntülerken beklenmedik bir hata oluştu!")
            log.error(f"Unexpected error in 'getLiveMatches' function of the 'MainWindow' class:\n{e}")
        finally:
            self.togglePushButton(self.pbtnGetLiveMatches, True)
            self.getLiveMatchesThread.quit()
    
    def clickedPbtnGetLiveMatches(self):
        try:
            log.debug("The 'clickedPbtnGetLiveMatches' function of the 'MainWindow' class has been executed.")
            self.togglePushButton(self.pbtnGetLiveMatches, False)
            self.getLiveMatchesThread.start()
        except Exception as e:
            log.error(f"Unexpected error in 'clickedPbtnGetLiveMatches' function of the 'MainWindow' class:\n{e}")

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