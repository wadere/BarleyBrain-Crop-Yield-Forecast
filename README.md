![testimage](images/crop_region_2015.png)
# Welcome to Barley Brain!

Barley Brain is a computer model to forecast regional barley yields in Colorado, Wyoming, Idaho and Montana.  The model extracts data from public web sites such as NASA, the US Deparment of Agriculture, and Darksky.net (weather). Aggregating satellite images, county information, historic weather, and reported yield from 2010 to present.  


#### Technology used
*  Python
*  sklearn Adaboost, RandomForests, OLS
*  LANDSAT
*  Darksky.net API



#### Data Collection 
WEATHER: 
Data for Barley Brain comes from a variety places.  Historic weather conditions were downloaded from the Darksky.net (http://www.Darksky.net) weather servers.  Darksky was chosen as it is free (up to 1000 calls per day), and can also handle the task of predicting weather well into the future.  
  
Weather data is downloaded in advance (for ease, data back to 2010 is in data/weather), the only processing of data was to drop unused columns during the download, in an effort to reduce file size. Additionally the weather data is compressed into yearly averages so it can be used with the yield data.

YIELDS:  The USDA (https://www.usda.gov/wps/portal/usda/usdahome) has an online collection of historically reported crop yields.  This data is automatically collected by the model for cleaning and combining with the weather data.
Since Barley was the focus, only the barley data was downloaded.  Note that all state data gets downloaded so that in the future the model can be easily extended to any state or region.

 
#### Model and Performance
Three models were run on the data, Ordinay Least Squares, RandomForests, and Adaboost.
Primary selected model was Adaboost, as it provided the best RMSE (+/- 12 bussels/acre on the test set.)
Data is loaded from the combined file and split into train and test sets.  For training mode, the model discards all information not within the 2010 to 2014 timeframe. Similary the test case drops years less than and including 2014, leaving only 2015 and 2016 data.



#### TEST RESULTS
The model initally way overfit on the train data, and after reviewing in-stage Adaboost scoring, model was 'tuned' to remove over fitting as much as possible.  Resulting RMSE fit was 12.6 bussels/acre.  Not bad given the wide range of things farms can do to their fields in the course of a year.  The following chart shows model predicted yield (green line) and actual yield (blue dots).

![test_image](images/test_results1.png)




#### Repo Organization:
* data   --> Storage for online data and file processing
* eda    --> Holds jupyter notebooks with EDA analysis
* images --> Images for readme and from eda analysis
* web_app -> Just like it says
* src    --> Holds the helper functions, code to extract 
                information from the web

