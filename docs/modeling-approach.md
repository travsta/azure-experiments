# Social Media Post Topic Classification: Category Discovery and Classification Approach

The problem requires us to develop a system that can label Instagram posts by topic. The key requirement is:

Categorize all posts from a collection of 20-100 topics with confidence scores

## Assumptions
Our approach to Instagram topic classification is based on the following key assumption:

### Hard vs Soft Clustering
There is a trade-off between category breadth/overlap and post coverage, which can be adjusted based on user requirements:

1. **High Coverage Approach**: 
   - Prioritize broad, potentially overlapping categories.
   - This maximizes the number of posts classified with relatively high confidence.
   - May result in posts being assigned to multiple categories.

2. **High Distinctness Approach**:
   - Prioritize more distinct, non-overlapping categories.
   - This increases the likelihood of posts being mapped to a single, specific category.
   - May result in fewer posts being classified with high confidence, and more posts either unclassified or classified with lower confidence.

The choice between these approaches depends on the specific needs of the end-users and the intended application of the classification system. Given the low number of categories permitted and because it makes for the more interesting approach, we will assume the use case suggests a preference for distinct categories of interest and can tolerate posts being mapped with low confidence. The below approach could be modified to instead use soft clustering techniques to manage categories/clusters through an initial sampling of the post corpus and then periodic recalibrations using new data.

### Additional Assumptions in Classification Approach

**Data Availability and Access**
   - We have access to a large volume of posts (500+ billion) and can process them without significant legal or technical barriers.

**Text Sufficiency**
   - The textual content of Instagram posts (captions, comments, hashtags) provides sufficient information for meaningful topic classification, even without analyzing images or videos.

**Scalability of Cloud Infrastructure**
   - Azure cloud services (or similar platforms) can scale to handle the processing and storage requirements of billions of posts and real-time classification requests and users will accept the costs.

**Dynamic Nature of Topics**
   - Post topics are not static and new trends can emerge rapidly, necessitating a system that can adapt and evolve its categories over time even though our approach should result in relatively slow changing categories.

**Multi-label Relevance**
   - Many Instagram posts are relevant to multiple topics, making a multi-label classification approach more appropriate than strict single-label classification.

**User Feedback Value**
   - End-users of the system (or a subset of expert users) can provide valuable feedback for improving classification accuracy and identifying new topics.

**Ethical Compliance**
   - The classification system can be implemented and operated in compliance with relevant data protection regulations and ethical guidelines.

**Computational Efficiency**
   - Approximate Nearest Neighbor (ANN) search and other optimization techniques can provide sufficient speed for real-time classification without significant loss of accuracy.

**Category Stability**
   - While allowing for dynamic updates, the core set of categories will remain relatively stable over time, not requiring complete retraining of the system too frequently.

**Multilingual Capability**
   - The posts are all in english.

**Acceptable Confidence Levels**
   - There exists a range of confidence levels that balances the trade-off between classification coverage and accuracy, which will be acceptable for the intended use cases.

## Overview of Approach

This document outlines an approach to discover and classify topics in Instagram posts with an evolving set of 20-100 categories. The method combines embedding techniques, clustering, and human-in-the-loop refinement to create a robust classification system.

## 1. Text Embedding

### 1.1 Embedding Selection
- Use a state-of-the-art language model for embedding, such as [BAAI/bge](https://huggingface.co/collections/BAAI/bge-66797a74476eb1f085c7446d) or other recent advancements.
- Avoid older models like BERT in favor of more recent, powerful alternatives.

### 1.2 Embedding Process
- Embed the full text of each post, not just individual words or hashtags.
- This approach captures the overall meaning of the post, addressing potential ambiguities in individual word meanings.

## 2. Database Design

### 2.1 Embedding Database
- Create a database to store post embeddings.
- Use a system that allows for efficient similarity search, such as Approximate Nearest Neighbor (ANN) indexing.
- Recommended tool: [Qdrant](https://github.com/qdrant/qdrant)

### 2.2 Category Database
- Maintain a separate database for categories.
- Store for each category:
  - Representative posts (both embeddings and original text)
  - Average embedding of the category
  - Standard deviation from the average embedding

## 3. Category Discovery Process

### 3.1 Initial Category Creation
- For the first 20 posts (or until the minimum required categories are reached):
  - Create a new category for each post
  - Use the post as the representative for its category
  - Set the category's average embedding to the post's embedding
  - Set the standard deviation to zero

### 3.2 Sampling to Improve Initial Categorization
- We will use an incremntal sampling approach to improve the list of categories until we have processed the initial data set
- The classification model can begin to be used once a sufficient sample has been used to train the model

### 3.3 Subsequent Post Processing
- For each new post after the initial training and incremental updates during training:
  1. Compare the post's embedding to existing categories
  2. If significantly more similar to one category than others:
    - Add to that category
  3. If not similar to any existing categories:
    - Create a new category

### 3.4 Category Updates
- When adding a post to a category:
  1. Decide if it should be a representative post
    - Keep a fixed number of representative posts per category
    - Replace the closest-to-average representative if needed
  2. Update the category's average embedding
  3. Recalculate the standard deviation

### 3.5 Category Refinement
Periodically:
1. Calculate distances between categories using average embeddings
2. Identify overlapping categories:
   - To determine if the overlap is statistically significant:
     a. Calculate the Euclidean distance between the average embeddings of two categories
     b. Compare this distance to the sum of the standard deviations of both categories
     c. If the distance is less than X times the sum of standard deviations, consider it significant
        (X could be determined empirically, starting with a value like 2 or 3)
   - Additionally, use a t-test or ANOVA to compare the distribution of posts in both categories
   - If p-value < 0.05 (or another chosen threshold), consider the overlap significant
   - Consider the number of posts that could be classified into either category with high confidence
   - If overlap is statistically significant, consider a merge of the categories
3. Ensure the total number of categories stays within the desired range (20-100)

## 4. Classification System

### 4.1 Similarity Search
- Use the ANN index to quickly find the most similar embeddings for a given post

### 4.2 Classification Process
For a new post to be classified:
1. Embed the post text
2. Use the ANN index to find the most similar existing embeddings
3. Assign the post to the most frequent category among these similar embeddings
4. Calculate a confidence score based on the similarity and category consistency of the nearest neighbors

## 5. Scalability Considerations

### 5.1 Distributed Computing
- Implement the system using distributed computing frameworks (e.g., Apache Spark)
- Shard the embedding database

### 5.2 Incremental Updates
- Design the system to handle incremental updates without full reprocessing
- Periodically rebalance and optimize the ANN index:
  a. Monitor the distribution of data points across the index
  b. If distribution becomes uneven, trigger a rebalancing process:
     - Rebuild sub-trees or reorganize data points within the index
     - This may involve re-inserting a portion of the data points
  c. Optimize by adjusting index parameters:
     - Tune the number of trees or the depth of the index based on performance metrics
     - Adjust the number of nearest neighbors checked during search
  d. Implement a background process for continuous, incremental index optimization:
     - Regularly sample and re-index a small portion of the data
     - Gradually improve index quality without disrupting the main system
  e. Consider using techniques like Progressive Dimensional Reordering to improve ANN performance over time

## 6. Continuous Improvement

### 6.1 Monitoring and Evaluation
Effective monitoring and evaluation are crucial for maintaining the quality and relevance of the Instagram topic classification system. This section outlines a comprehensive strategy for ongoing assessment and improvement.

#### 6.1.1 Quality Metrics
##### a. Topic Coherence
- Implement automated coherence scoring using metrics like Normalized Pointwise Mutual Information (NPMI) or UCI coherence.
- Periodically calculate coherence scores for each topic.
- Set threshold values for acceptable coherence; flag topics falling below this threshold for review or automated recalibration of categories.

##### b. Classification Confidence
- Track the average confidence score of classifications over time.
- Implement alerts for sudden drops in confidence, which may indicate emerging topics or shifts in language use.

##### c. Inter-Topic Distance
- Regularly compute and monitor the distance between topic centroids in the embedding space.
- Flag topics that are becoming too close, indicating potential redundancy or need for merging.

#### 6.1.2 Performance Monitoring
##### a. Classification Speed
- Monitor the average time taken to classify posts.
- Set up alerts for significant increases in classification time, which may indicate indexing or scaling issues.

##### b. System Load
- Track CPU, memory, and storage utilization.
- Implement auto-scaling triggers based on load metrics to maintain consistent performance.

##### c. API Response Times
- Monitor and log response times for the classification API.
- Set up alerts for response times exceeding predetermined thresholds.

#### 6.1.3 Data Distribution Analysis
##### a. Topic Distribution
- Regularly analyze the distribution of posts across topics.
- Flag unusually large or small topics for human review.
- Monitor for the emergence of new significant clusters that don't fit existing topics.

##### b. Temporal Analysis
- Track topic popularity over time to identify trending and declining topics.
- Implement visualizations (e.g., heat maps) to easily spot temporal patterns.

##### c. Geographic Distribution (if applicable)
- Analyze topic distribution across different geographic regions.
- Identify region-specific topics that may require special handling.

#### 6.1.4 Concept Drift Detection
##### a. Embedding Drift
- Periodically compare the distribution of post embeddings to a baseline distribution.
- Use techniques like Kullback-Leibler divergence to quantify drift.

##### b. Topic Centroid Shift
- Track the movement of topic centroids in the embedding space over time.
- Implement alerts for significant or sudden shifts in topic centroids.

##### c. Classification Stability
- Monitor the stability of classifications for a set of benchmark posts over time.
- Flag topics with high classification volatility for review.

#### 6.1.5 Continuous Improvement Process
##### a. Regular Retraining Schedule
- Establish a regular schedule for retraining the model with recent data.
- Monitor improvements or degradations in performance after each retraining.

##### b. Automated Refinement Pipeline
- Implement an automated pipeline that uses monitoring data to suggest refinements:
  - Merging of similar topics
  - Splitting of overly broad topics
  - Retirement of obsolete topics
  - Creation of new topics for emerging trends

#### 6.1.6 Reporting and Visualization
##### a. Dashboard Development
- Create a comprehensive dashboard displaying key metrics, trends, and alerts.
- Include visualizations of topic distributions, performance metrics, and data flow.

##### b. Automated Reporting
- Set up automated weekly/monthly reports summarizing system performance, notable changes, and areas needing attention.
- Include trend analysis to highlight long-term changes in topic landscape.

##### c. Anomaly Highlighting
- Implement automated anomaly detection in all key metrics.
- Ensure that anomalies are prominently displayed in dashboards and included in reports.

#### 6.1.7 External Validation
##### a. Benchmark Against External Sources
- Periodically compare topic trends with external sources if available (e.g., top historical hashtags, etc.) to validate relevance.

### 6.2 Human-in-the-Loop Refinement
- Periodically involve human experts to review and refine category definitions
- Use active learning techniques to efficiently incorporate human feedback:
  a. Uncertainty Sampling: Present posts with low classification confidence for human review
  b. Diversity Sampling: Select a diverse set of posts from each category for validation
  c. Query-By-Committee: Use multiple classifiers and present posts with high disagreement
  d. Expected Model Change: Select posts that would cause the largest update to the model
  e. Error Reduction: Choose posts that are expected to reduce classification error the most
  f. Implement an interface for experts to easily review and correct classifications
  g. Use the feedback to retrain the model and update category definitions

## 7. Performance Optimization

### 7.1 Accuracy Tuning
- Experiment with different accuracy levels in the ANN search (e.g., 95-99.5% range)
- Balance between speed and accuracy based on specific use case requirements:
  a. Start with a high accuracy setting (e.g., 99.5%) and measure system performance
  b. Gradually reduce accuracy and observe the impact on:
     - Classification accuracy (compare to results from exact nearest neighbor search)
     - Query speed (measure improvement in query time)
     - Resource utilization (monitor CPU and memory usage)
  c. Identify the "knee point" where a small decrease in accuracy leads to a large increase in speed
  d. Consider different accuracy levels for different use cases:
     - Higher accuracy for critical applications or when classifying trending posts
     - Lower accuracy for bulk processing of historical data
  e. Implement adaptive accuracy:
     - Use higher accuracy for posts that fall in uncertain regions between categories
     - Use lower accuracy for posts that are clearly within a category's core
  f. Regularly re-evaluate the accuracy-speed trade-off as the dataset grows and evolves

### 7.2 Infrastructure Considerations
- Using cluster or cloud-based solutions for scalability and streaming data for storage efficient processing

## Conclusion

This approach provides a scalable and adaptable solution for discovering and classifying topics in posts. By leveraging modern embedding techniques, efficient similarity search, and dynamic category management, it can handle the scale and evolving nature of social media content. The system allows for continuous refinement and adaptation, ensuring its relevance over time.
