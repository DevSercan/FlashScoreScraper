from classes.FlashScoreScraper import FlashScoreScraper # FlashScore internet adresindeki maç verilerini çeken sınıfı içe aktarıyoruz.
import pandas # Python'da veri işleme ve Excel dosyaları oluşturma gibi işlemler için pandas kütüphanesi kullanılır.

def saveToExcel(data, filename):
    """ Bir veri listesini Excel olarak dışa aktarır. """
    dataFrame = pandas.DataFrame(data)
    dataFrame.to_excel(f"{filename}.xlsx", index=False, engine='openpyxl')

def main():
    """ Bütün işlemleri yöneten ana fonksiyondur. """

    scraper = FlashScoreScraper(platform="windows", driverName="chrome") # 
    scraper.open() # Tarayıcıyı başlatır.

    oddsData = [] # Oran verilerini tutar.
    finishedData = [] # Bitmiş maç verilerini tutar.

    days = 3 # Son kaç günün verilerinin çekileceği bilgisini tutar.

    for _ in range(days): # İstenen son günlerin verilerini çekebilmek için bir döngü başlatıyoruz.
        scraper.clickFilterTab(targetTab="ODDS") # Maç filtrelerinden "ODDS" sekmesini seçer.
        oddsData.extend(scraper.getOddsData()) # Oranlar (ODDS) verilerini alır ve diziye ekler.

        scraper.clickFilterTab(targetTab="FINISHED") # Maç filtrelerinden "FINISHED" sekmesini seçer.
        finishedData.extend(scraper.getFinishedData()) # Bitmiş maçların verilerini alır ve diziye ekler.

        scraper.loadYesterday() # Bir önceki günün verilerini getirir.

    # Verileri Excel'e kaydediyoruz.
    saveToExcel(data=oddsData, filename="OddsData")
    saveToExcel(data=finishedData, filename="FinishedData")

    scraper.close()

if __name__ == '__main__':
    main()