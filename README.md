![testimage](images/crop_region_2015.png)
# Welcome to Barley Brain!

Barley Brain is a computer model to forecast regional barley yields in Colorado, Wyoming, Idaho and Montana.  The model first  extracts data from public web sites such as NASA, USGOV, Darksky.net, aggregating satellite images, county information, historic weather, and reported yield from 2010 to present.


#### Technology used
*  Python
*  sklearn Adaboost, RandomForests, ElasticNet
*  LANDSAT


#### Data Collection
  WEATHER: 
  Data for Barley Brain is comes from a variety places.  For historic weather conditions (daily back to 2010) were downloaded from the Darksky.net (http://www.Darksky.net) weather servers.  Darksky was chosen as it is free (up to 1000 calls per day).  
  
 YIELDS:  The US government has an online collection of historical crops yields.  For each location in the 4 state region, data is downloaded and processed for useage.  Since Barley was the focus, only the barley data was downloaded. 


#### Model



#### Model Performance




#### Next Steps
* Integrate NDVI into Public Model
*


#### Repo Organization:
* data   --> Storage for online data and file processing
* eda    --> Holds jupyter notebooks with EDA analysis
* images --> Images for readme and from eda analysis
* web_app -> Just like it says
* src    --> Holds the helper functions, code to extract 
                information from the web

