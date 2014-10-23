Natural Language Toolkit and Association Rules
===============================================

This repository is for the Natural Language Toolkit and Association Rules talk given at the Pittsburgh Python Meetup on October 22, 2014.

It uses the Accident Injuries data set relased as [Open Government Data](http://www.msha.gov/OpenGovernmentData/OGIMSHA.asp) by the Mine Safety and Health Administration (MSHA). This contains data submitted as part of MSHA Form 7000-1 for all accidents, injuries and illnesses reported by mine operators and contractors since 1/1/2000.  The Accident Injuries Data Set is updated weekly.

To use the repository, 

1. Download the [Accident Injuries data set](http://www.msha.gov/OpenGovernmentData/DataSets/Accidents.zip) and unzip it in this directory. The accident injuries file is encoded as `latin1`.
2. If you haven't used nltk before, after installing you'll need to download some corpora:
 1. Open up python and type `import nltk; nltk.download()` to bring up the downloader GUI.
 2. From the `Corpora` pane, select and download the `stopwords` corpus.
 3. From the `Models` pane, download the `maxent_treebank_pos_tagger` and `punkt` modules.
3. Run `python generate_clean_narrative_pickle.py` to create the pickle `all_narrative_cleanup.txt`
4. Run `python generate_narrative_tag_pickle.py` to create the pickle `all_narrative_tagged.txt`
5. Open `nltk_assocrules_pghpython.ipynb` in the IPython Notebook

Code in this repository was developed by [Haoxian He](https://bitbucket.org/ethan1989111) (https://bitbucket.org/ethan1989111) and [Louis Luangkesor](https://github.com/lluang) (https://github.com/lluang)