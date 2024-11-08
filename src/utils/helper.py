import json # Json formatında işlemler gerçekleştirebilmek için kullanılır.
import os # İşletim sistemi (Operating System) işlemleri için kullanılır.
import pandas # Python'da veri işleme ve Excel dosyaları oluşturma gibi işlemler için pandas kütüphanesi kullanılır.

def getConfig() -> dict:
    """ Konfigürasyon dosya içeriğini Json formatında okur ve sözlük olarak döndürür. """
    with open("config.json", 'r', encoding='utf-8') as file:
        configDict = json.load(file)
    return configDict

def saveToExcel(data, filename):
    """ Bir veri listesini Excel olarak dışa aktarır. """
    dataFrame = pandas.DataFrame(data)
    dataFrame.to_excel(f"{filename}.xlsx", index=False, engine='openpyxl')

def clear():
    """ Konsolu temizler. """
    if os.name == 'nt': # İşletim sistemi Windows ise koşul sağlanır.
        os.system('cls') # CMD'nin 'cls' komutu ile konsol temizlenir.
    else: # İşletim sistemi Windows değil ise koşul sağlanır.
        os.system('clear') # Terminal'in 'clear' komutu ile konsol temizlenir.