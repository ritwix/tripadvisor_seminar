# Creating a sentiment analysis model using Scrapy and Monkeylearn
This is about building a Monkeylearn sentiment analysis model using scraped Tripadvisor hotel reviews.
The items to be saved are in hotel_sentiment/items.py. The spider to be used is tripadvisor.py .
To run the spider,
```shell
scrapy crawl tripadvisor -o scrapedData.csv -s CLOSESPIDER_ITEMCOUNT=15000
```
This is the scraped data stored in file scrapedData.csv. This needs to be preprocessed using csv_monkey_converter.py .
The outcome of this step will be a .csv file which will be fed to the Monkeylearn model. Once the model is trained, we can test with our inputs.
