# Instagram Topic Classification: Category Discovery and Classification Approach

## Overview

This document outlines an approach to discover and classify topics in Instagram posts with an evolving set of 20-100 categories. The method combines embedding techniques, clustering, and human-in-the-loop refinement to create a robust classification system.

## 1. Text Embedding

### 1.1 Embedding Selection
- Use a state-of-the-art language model for embedding, such as BAAI/bge or other recent advancements.
- Avoid older models like BERT in favor of more recent, powerful alternatives.

### 1.2 Embedding Process
- Embed the full text of each post, not just individual words or hashtags.
- This approach captures the overall meaning of the post, addressing potential ambiguities in individual word meanings.

## 2. Database Design

### 2.1 Embedding Database
- Create a database to store post embeddings.
- Use a system that allows for efficient similarity search, such as Approximate Nearest Neighbor (ANN) indexing.
- Recommended tool: Qdrant (https://github.com/qdrant/qdrant)

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
   - If overlap is statistically significant, merge the categories
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
- Regularly evaluate the quality and coherence of categories
- Monitor for concept drift in category definitions

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

### 7.2 Hardware Considerations
- Ensure the system runs on hardware capable of handling the expected load
- Consider using cloud-based solutions for scalability

## Conclusion

This approach provides a scalable and adaptable solution for discovering and classifying topics in posts. By leveraging modern embedding techniques, efficient similarity search, and dynamic category management, it can handle the scale and evolving nature of social media content. The system allows for continuous refinement and adaptation, ensuring its relevance over time.
