# Scrapper engine for cuba-wheater

The cuban-weather scrapper engine provides a framework 
used for obtain information from different weather services
and send the obtained data to the cuba-weather service 
database.  

## How this work

The cuban-weather scrapper uses services (services are 
located in the services folder). Each service is responsible 
for obtaining data from an specific source and send it to
the cuba-weather service database.

For running all services once you can run:

    python cubaweatherscrapper.py

For creating a new service named "owm" based on the default 
template you can run:

    python cubaweatherscrapper.py -a owm
