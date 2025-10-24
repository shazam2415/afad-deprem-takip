# deprem/views.py

from django.shortcuts import render
import requests
import datetime

# --- AFAD API AYARLARI ---
AFAD_API_URL = "https://deprem.afad.gov.tr/EventData/GetEventsByFilter"

def afad_verilerini_cek():
    """AFAD'dan veriyi çeken ve temizleyen Python fonksiyonu."""
    
    end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    
    payload = {
        "EventSearchFilterList": [
            {"FilterType": 8, "Value": start_date},
            {"FilterType": 9, "Value": end_date},
        ],
        "Skip": 0,
        "Take": 15, # Daha fazla veri çekelim
        "SortDescriptor": {"field": "eventDate", "dir": "desc"},
    }
    headers = { 'Content-Type': 'application/json' }
    
    try:
        response = requests.post(AFAD_API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status() 
        data = response.json()
        
        # Sadece 1.0 ve üzeri depremleri alalım
        filtrelenmis_depremler = [
            event for event in data.get('eventList', []) if event.get('magnitude', 0) >= 1.0
        ]
        
        return filtrelenmis_depremler

    except requests.exceptions.RequestException as e:
        print(f"AFAD API İsteği Başarısız: {e}")
        return []

def deprem_listesi(request):
    """HTML şablonunu render eden view."""
    
    depremler = afad_verilerini_cek()
    
    # Çekilen deprem listesini 'depremler' adıyla şablona gönderiyoruz
    context = {
        'depremler': depremler
    }
    
    return render(request, 'deprem/deprem_tablosu.html', context)
