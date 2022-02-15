# SWAT APIS & ARSI

2 prezentacije
1 docx




## Analiza
* Python Jypter vizualizacija malicioznih dogadjaja, izrada grafika iz CSV-ova
    * globalni grafik [ APIS ] 
    * podeljeno po procesima gde se desava napad npr (P1, P1 i P3) [ APIS ]
    / dusan/

* Analiza CSV-ova, izrada patterna od kojih ce se posle napraviti Yara pravila
    * Analiza PCAP-ova, i izvlacenje IOC-ova. src ip, src port, dst ip, dst port, raw podaci... [ APIS ]
    * Izrada Yara pravila, (dostavicu primere) [ ARSI ]
    / milos /
    
* Analiza CSV-ova, ML trening; 
    * odabir ML algoritma [ APIS ]
    * trening istog  [ APIS ]
    * verifikacija rezultata tabelarno [ APIS ]
    * reakcija same detekcije anomalije je zapravo [ ARSI ]
    / dusan /

 * Prezentacije i DOCX
    / sandra /

    

## Reakcija i prevencija
 * Izrada statickih pravila (YARA rules) za IDS/IPS
 * Mehanizam detekcije anomalija (heuristika/statistika ili nekakav ML)
 * Rezultati detekcije


## ARSI projekat, reference
 * https://mlad.kaspersky.com/swat-testbed/
 * https://labs.f-secure.com/archive/offensive-ics-exploitation-a-technical-description/
 * https://arxiv.org/pdf/1809.04786.pdf
 * vizualizacija: https://github.com/cbhua/tool-swat-preprocess
 * anomaly detection: https://github.com/eBay/RANSynCoders


