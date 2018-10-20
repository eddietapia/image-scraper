# Image Scraper

Will allow us to use the Microsoft Bing Search API to scrape images from Bing Search. 
Additionally, this web scaper is based on the following tutorial: 
[Tutorial Link](https://www.pyimagesearch.com/2018/04/09/how-to-quickly-build-a-deep-learning-image-dataset/)


## Getting Started
Make sure you have the requests library installed:
```
pip install requests
```

Additionally, you might have to install other packages if you don't already have 
them installed in your system, such as opencv(for when we import cv2)


### Running
You can run the scirpt `scrape.py` simply by,

```
python scrape.py --query "iphone" --output iphone-dataset/
```

In this example, the item we are searching for is `iphone` and we will be storing 
the images we download into the `iphone-dataset` folder in your current directory.

**Notes**
1. You will have to insert your own Microsoft API key in the `scrape.py` file. 
I included a TODO: comment to show you where to insert your API key

### i-phone Dataset
In addition to the web scraper, I included the `iphone-dataset` that I 
downloaded using this web scraper.


## Contributing

When contributing, please make sure you write clean, efficient code using the PEP8 style guide
* [PEP8](https://www.python.org/dev/peps/pep-0008/) - Style Guide for Python Code


## Questions
* If you have any questions, contact Eddie Tapia at etapiahe@andrew.cmu.edu
* Special thanks to Adrian Rosebrock who created the tutorial for this [web scraper](https://www.pyimagesearch.com/2018/04/09/how-to-quickly-build-a-deep-learning-image-dataset/)


