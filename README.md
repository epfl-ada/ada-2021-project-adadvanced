# A Short Story of the Long Road to Brexit

## Abstract
In the last few years, Brexit has been one of the most trending topics in the world. Between 2015 and Britain's official EU exit in February 2020, countless discussions and debates have been generated around the subject. People coming from different backgrounds had a take on the matter, where views and opinions diversified and contrasted. Opponents speculated that the influence of Brexit would have negative impacts on certain sectors while supporters claimed the opposite. The aim of the study is to analyze the evolution of the perception of Brexit throughout the years (2015 - 2020). It would be interesting to look at this perception by aggregating the views by sector as well as by counrty, age, gender, ethnicity and educational level of the speakers. 

## Research Questions
The project aims at answering the following questions:
Main Question: 
- How did the perception of Brexit evolved over time?
Supporting Questions:
- Which sectors had the most negative take on Brexit?
- Which sectors had a significant change in perception (from negative to positive or vise versa) throughout the years?
- Is it true that older people were more in favor of Brexit than younger people?
- Which countries were the most supportive of the exit decisions and which ones opposed it?
- What was the perception of European countries with regards to Brexit?
- Which ethnicities were the most supportive of the exit decisions and which ones opposed it?
- Do genders have different perception of Brexit?
- Is the global take on Brexit rather positive or negative?
- Did the UK's view on Brexit switch much from 2015 until its exit in 2020? When did the turnarounds of perception happen?

## Proposed additional datasets 
Wikidata

## Methods
1. Data preprocessing: 
Before diving into the analysis of the data, it is crucial to have a look at the data itself and process it. A preprocessing task was performed on the data and it consisted of the following steps:
 - Data Exploration and Sanity Checks : Exploring the dataset, checking its consistency and getting familiar with the different features/information provided.
 - Data Extraction : Pulling out the quotes of interest that discuss Brexit.
 - Data Augmentation : Attributes related to the speaker & sentiment labelling of the quote (positive/neutral/negative):
     - Attributes of interest are extracted from Wikidata knowledge base using the speaker_attributes.parquet file
     - Mapping QIDs to meaningful labels
     - Labelling was performed using [NLTK's Vader Neural network](https://www.nltk.org/_modules/nltk/sentiment/vader.html) 
 - Final Cleaning of the data & Merging:
   - Eliminating duplicated quotations using Sentence BERT
   - Removing quotations that do not have pertinent references
   - Aggregation of the data based on sectors, countries, gender and age categories
   - Merging similar speakers
   - One hot-encoding of attributes
 - Quotations and speakers clustering : Clustering the quotations and the speakers
   - Converting quotations into vectors using [SentenceTransformer](https://www.sbert.net/docs/usage/semantic_textual_similarity.html) deep neural network.
   - Reducing the dimension of the data frame using [T-stochastic neighbors embeddings](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html)
   - Perform aggregation to attribute a vector to each speaker.
   - Performing clustering using [Spectral Clustering](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.SpectralClustering.html#sklearn.cluster.SpectralClustering) method.

2. Data Analysis:
- Generate Results: statistics and general description of the data
- Data Visualization using maps, histograms, scatter plots, interactive time map and plots, 

## Timeline
By the end of Milestone 2:
- The data has been properly explored, augmented and cleaned. 
- Additional data describing the attributes of the speakers have been processed (dealing with missing values), cleaned and one-hot encoded.
- Sentiment analysis has been performed. 
- Full merge of the dataset. 
- Clustering has been performed.
- Initial results/plots have been generated.

For Milestone 3:
- Focus on proper visualizazion of the results in order to make conjectures that answer our research questions. 
- Deep and elaborate analysis of the results to write the final story. 
- Set up the platform.
- Propose recommendations for future work.

## Organization within the Team
- Milestone 2:
  Arnaud: Data exploration and Sanity check, Data extraction, Data cleaning, Quotations and speakers   clustering, Initial results. 
  Rafaelle: Data exploration and Sanity check, Quotations and speakers clustering, 
  Jean: Data exploration and Sanity check, Data augmentation, Quotations and speakers clustering, 
  Gaelle: Data exploration and Sanity check, Data augmentation, Data merging and cleaning, writing the     readme file.

- Milestone 3 (Tentative):
  Arnaud & Rafaelle: Visualisation of the results.
  Gaelle & Jean: Analysis of the results and writing the final story.

 
