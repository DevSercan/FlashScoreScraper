from classes.FlashScoreScraper import FlashScoreScraper # FlashScore internet adresindeki maç verilerini çeken sınıfı içe aktarıyoruz.
import pandas # Python'da veri işleme ve Excel dosyaları oluşturma gibi işlemler için pandas kütüphanesi kullanılır.

def saveToExcel(data, filename):
    """ Bir veri listesini Excel olarak dışa aktarır. """
    dataFrame = pandas.DataFrame(data)
    dataFrame.to_excel(f"{filename}.xlsx", index=False, engine='openpyxl')

def main():
    """ Bütün işlemleri yöneten ana fonksiyondur. """

    scraper = FlashScoreScraper(platform="windows", driverName="chrome", isHeadless=True) # FlashScoreScraper sınıfından bir nesne üretiyoruz.
    print("Tarayıcı çalıştırılıyor...")
    scraper.open() # Tarayıcıyı başlatır.
    print("Tarayıcı çalıştırıldı.")

    liveData = [] # Canlı maç verilerini tutar.
    oddsData = [] # Oran verilerini tutar.
    finishedData = [] # Bitmiş maç verilerini tutar.

    # days = 3 # Son kaç günün verilerinin çekileceği bilgisini tutar.

    # for _ in range(days): # İstenen son günlerin verilerini çekebilmek için bir döngü başlatıyoruz.
    #     print("Bir önceki güne geçiliyor...")
    #     scraper.loadYesterday() # Bir önceki günün verilerini getirir.
    #     print("Bir önceki güne geçildi.")

    print("LIVE verileri alınıyor...")
    liveData.extend(scraper.getLiveData()) # Canlı (LIVE) maç verilerini alır ve diziye ekler.
    print("LIVE verileri alındı.")

    print("ODDS verileri alınıyor...")
    oddsData.extend(scraper.getOddsData()) # Oranlar (ODDS) verilerini alır ve diziye ekler.
    print("ODDS verileri alındı.")

    print("FINISHED verileri alınıyor.")
    finishedData.extend(scraper.getFinishedData()) # Bitmiş maçların verilerini alır ve diziye ekler.
    print("FINISHED verileri alındı.")

    # Verileri Excel'e kaydediyoruz.
    print("Sonuçlar Excel dosyalarına kaydediliyor...")
    saveToExcel(data=liveData, filename="LiveData")
    saveToExcel(data=oddsData, filename="OddsData")
    saveToExcel(data=finishedData, filename="FinishedData")
    print("Sonuçlar Excel dosyalarına kaydedildi.")

    scraper.close()

if __name__ == '__main__':
    main()