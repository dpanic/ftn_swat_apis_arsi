# SWAT APIS & ARSI

## Authors:
* Sandra Čoralić (I9 5/2021)
* Miloš Milovanović (I9 6/2021)
* Dušan Panić (I9 7/2021)

## Profesor:
* PhD, Imre Lendak

## Institution:
* UNIVERZITET U NOVOM SADU, Fakultet tehničkih nauka

<br>

## Environment 

``` 
Python Version: 3.6 or later
Python Packages: jupyterlab, torch, numpy, pandas, matplotlib
```

<br>

## Visualization
 Python Jypter visulization of malicious events:
* ✅ Bootstrap data, download data from external source (because of licence)
* ✅ Global chart [ APIS ] 
* ✅ Plot and divide per stage (P1, P2, P3, P4, P5, P6) [ APIS ]
* ✅ Plot and divide per process where attack occurs (MV101, P101, P102 and AIT201) [ APIS ]
/ dusan/

<br>

## Analysis
Analysis of CSV files, determine patterns from which Yara rules will be built 
* ✅ Refactor python files to separate folder 
* Find IOC's: src ip, src port, dst ip, dst port, raw data... [ APIS ] - 6h
* Create Yara rules [ ARSI ] - 3h
* Test patterns on data 
/ dusan /

<br>

## Machine Learning and Response
Analysis of CSV files and ML training:
* choose ML algorithm [ APIS ]
* perform training on control set [ APIS ]
* perform training on whole set [ APIS ]
* show results of ML anomaly detection [ APIS ]
/ dusan /

<br>

## Documentation
* 2 Presentations
* 1 Word document
    

<br>

## References
 * https://mlad.kaspersky.com/swat-testbed/
 * https://labs.f-secure.com/archive/offensive-ics-exploitation-a-technical-description/
 * https://arxiv.org/pdf/1809.04786.pdf
 * vizualizacija: https://github.com/cbhua/tool-swat-preprocess
 * anomaly detection: https://github.com/eBay/RANSynCoders


