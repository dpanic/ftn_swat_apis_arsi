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
* ✅ Find IOC's: src ip, src port, dst ip, dst port, raw data... [ APIS ] 
    * ✅ isolate where attacks are 
    * ✅ set skip files
    * ✅ set precision window (process every N rows)
    * ✅ parse big data 
    * extract patterns
* Create Yara rules [ ARSI ] 
* Test patterns on data with test results

[ knowledge based IDS ]
/ dusan /

>>>
The attacks were performed at level 1 of the SWaT network as discussed in Section 2. The network data captures the communication between the SCADA system and the PLCs. Hence, the attacks were launched by hijacking the packets as they communicate between the SCADA system and the PLCs. During the process, the network packets are altered to reflect the spoofed values from the sensors.
<<<

<br>

## Machine Learning and Response
Analysis of CSV files and ML training:
* implement moving window stats with k nearest 
* show tests results in notebook

[ behaviour based IDS ]
/ sandra and milos /

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


