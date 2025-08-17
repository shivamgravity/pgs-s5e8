# Dataset Installation Guide
The dataset is taken from kaggle playground series season 5 episode 8.
You can either download the dataset from [kaggle.com/competitions/playground-series-s5e8/data](https://www.kaggle.com/competitions/playground-series-s5e8/data) or run the setup file to download the files automatically.

## Preparation Before Executing Setup.py
Before executing setup.py, you may need to install some dependencies.
Following Python Libraries:
- os
- zipfile
- time
- threading
- kaggle
- tqdm
Install all these libraries using pip command in cmd.
Before that you need to setup **kaggle api** if you haven't already.

### Kaggle API Setup
Follow these steps to create your first *kaggle api*.
1. Create a folder with name (**.kaggle**) in the directory (**C:/Users/<Your Nanme>**)
2. Go to the **settings** page on your kaggle account and scroll to **API** section
3. Click *Create New Token* and save the kaggle.json file in the same folder you created in step 1 - it will look like C:/Users/<Your Name>/.kaggle/kaggle.json

Now you are ready to run the <ins>setup.py</ins> file.