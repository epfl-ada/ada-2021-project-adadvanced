# A Short Story on the Long Road to Brexit

## Abstract
In the last few years, Brexit has been one of the most trending topics around the world. Between 2015 and Britain's official EU exit in February 2020, countless discussions and debates have been generated around the subject. Opponents speculated that the influence of Brexit would have negative impacts on certain sectors while supporters claimed the opposite. People coming from different backgrounds had a take on the matter, where views and opinions diversified and contrasted. This made it hard to determine which side was majoritarian and had an edge on the debate and who was the losing side until the EU referdum that declared, in numbers, those in favor of Brexit as the winning side. 

The problem with the referudum is that it is anonymous and therefore does not tell much about the attributes of the people who voted. On the other hand, analyzing data sets that reveal the identity of individuals such as quotations or surveys that are not anonymous, makes it possible to obtain such information. In contrast to surveys or polls, quotations span over a period of time and allow therefore to track the evolution of opinions about Brexit. In fact, the debates around Brexit did not end with the referdum: they were just yet to start.

The study aims at analyzing the evolution of the perception of Brexit throughout the years (2016 - 2020) using a quantitative approach that aggregates the views about Brexit by sector, country, age, gender and profession of speakers. 

## Research Questions
And therefore we ask ourselves:
<br/>
**How did the perception of Brexit evolve over time after the referundum?** 
<br/>
<br/>
Supporting Questions:
<br/>
- Did the UK's view on Brexit switch much from 2016 until its exit in 2020?
- Which countries were the most supportive of the exit decision and which ones opposed it? What was the perception of European countries with regards to Brexit?
- Which sectors had the most negative take on Brexit? Which sectors had a significant change in perception (from negative to positive or vise versa) throughout the years?
- What do the attributes of people tell about their opinions with respect to Brexit?
- Did Brexit discussions influence the british stock market?

## Proposed additional datasets 
To enrich the quotebank data, we used additional information about the speakers that was provided by the `speaker_attributes.parquet` file. The source of the information is Wikidata. To complement the Quotebank data set, a sentiment analysis has been performed so to label the sentiment carried by the quote. Another dataset of interest is the FTSE100. This data set is accessible using the package [YFinance](https://pypi.org/project/yfinance/) and it gives the daily evolution of the stock actions throughout the years. 

## Methods
1. Data preprocessing: 
Before diving into the analysis of the data, it is crucial to have a look at the data itself and process it. A preprocessing task was performed on the data and it consisted of the following steps:
 - Data Exploration and Sanity Checks : Exploring the dataset, checking its consistency and getting familiar with the different features/information provided.
 - Data Extraction : Pulling out the quotes of interest that discuss Brexit.
 - Data Augmentation : Attributes related to the speaker & sentiment labelling of the quote (positive/neutral/negative):
     - Attributes of interest are extracted from Wikidata knowledge base using the speaker_attributes.parquet file
     - Mapping QIDs to meaningful labels
     - Sentiment labelling was performed using [NLTK's Vader Neural network](https://www.nltk.org/_modules/nltk/sentiment/vader.html) 
 - Final Cleaning of the data & Merging:
   - Eliminating very similar quotations using Sentence BERT 
       - Converting quotations into vectors using [SentenceTransformer](https://www.sbert.net/docs/usage/semantic_textual_similarity.html) deep neural network.
       - Computing [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity) between each pair of quotations
       - Removing quotations that are too similar from the dataset
   - Removing quotations that do not have pertinent references (ambiguity regarding the speakers)
   - Thresholding to remove categories with low number of occurences (categories: nationality, party, academic_degree, religion and gender)
   - Manual grouping of different categories:
      - For the academic degree grouping into 5 categories: Professor, Phd, Master, Bachelor and 		  others
      - For religions grouping into 4 categories: Christianity, Hinduism, Islam, Judaism, Atheism
   - Aggregation of the data based on sectors, countries, gender and age categories
   - Identify time periods distributed on an almost uniform number of quotations
   - One hot-encoding of attributes
 - Quotations and speakers clustering :
   - Converting quotations into vectors using [SentenceTransformer](https://www.sbert.net/docs/usage/semantic_textual_similarity.html) deep neural network, encoding with the [multi-qa-mpnet-base-dot-v1](https://huggingface.co/sentence-transformers/multi-qa-mpnet-base-dot-v1) algorithm.
   - Reducing the dimension of the data frame using [Locally Linear Embeddings](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.LocallyLinearEmbedding.html#sklearn.manifold.LocallyLinearEmbedding). This algorithm aims at preserving the neighbouring points. First, for each point, its nearest neighbors are determined. Then it tries to project the new point in the embedded space such that its neighbors are preserved
This spectral dimensionality reduction technique is non-linear, fast and reliable enough to handle big and complex dataset.
   - Perform aggregation to attribute a vector to each speaker.
   - Performing clustering using [Spectral Clustering](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.SpectralClustering.html#sklearn.cluster.SpectralClustering) method.
   - Validate the temporal coherence, hence the decision boundaries should comprehend almost the same speakers along time.
   - Compare with the sentiment score.

2. Data Analysis:
- Generate Results: statistics and general description of the data
- Data visualisation:
    - Evolution of the way Brexit is perceived in the UK using pie charts to represent sentiment distribution across years.
    - Evolution of the way Brexit is perceived in European countries using a color-encoded worldmap that reflects the position of the country towards Brexit.
    - Evolution of the way Brexit is perceived in different sectors using dynamic pie charts (dash application) that represent sentiment distribution across years per sector.
    - Perception of Brexit by age using dynamic histograms (dash application), for the world and UK.
    - Perception of Brexit by gender using histograms. <br/>

Except for the analysis of the european country, we assessed the differences between pairs (for instance art and health for the sectors) by comparing the means of the sentiment distribution using a Welch's t-test. 

Dynamic graph were deployed via the [Heroku](https://www.heroku.com/home) platform.
- Influence of Brexit on the stock exchange: to measure the correlation between the emergence of new events related to Brexit and movements in the stock exchange, the absolute value of the derivate was computed, in addition to the derivate of the number of quotations, both with respect to time. The derivatives are then used to compute the Pearson's correlation coefficient. For further information please check the stock market section in the Jupyter notebook.
- Clustering: in order to find further correlations among the speakers, a discrete classification was performed basing on the speaker vectorization. A vectorized speaker is composed by the one-hot vectorization of its basic properties corresponding to the parameters mapped by the list `columns_to_map` (see Jupyter notebook, cell [1]) attached to the average over the vectorized quotations obtained by the *Sentence transformer* (see cell [32]). The resulting vectors were then embedded, clustered and, at last, the decision boundaries were evaluated by their temporal coherence and compared to the results obtained by the sentiment analysis. For further informations check the clustering section in the Jupyter notebook.

## Organization within the Team
- Milestone 2:
    - Arnaud: Data exploration and Sanity check, Data extraction, Data cleaning, Quotations and speakers clustering, Initial results.
    - Raffaele: Data exploration and Sanity check, Quotations and speakers clustering, 
    - Jean: Data exploration and Sanity check, Data augmentation, Quotations and speakers clustering, 
    - Gaelle: Data exploration and Sanity check, Data augmentation, Data merging and cleaning, writing the readme file.
    
- Milestone 3:
    - Arnaud: data cleaning and wrangling, generation of plotly graphs as way as dash applications, deployment of these apps on Heroku, stock market analysis.
    - Raffaele: data cleaning and analysis, generation of plotly graphs, speakers clustering task.
    - Gaelle: Website tuning and deployement, data story writing, embedding graphs into the website.
    - Jean: Website tuning and deployement, data story writing, embedding heroku applications into the website.

## Here is the final story ;)

[Final story link](https://jeannafta.github.io/brexit_story)
