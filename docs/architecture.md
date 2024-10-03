# System Architecture

## Overview
This document describes the architecture of the Instagram Topic Classification system. The system is designed to classify the topics of Instagram posts using a machine learning model deployed on Azure.

## Components

### 1. Azure Function (API Endpoint)
- Hosted on Azure Functions
- Built using Microsoft's recommended approach for Python Azure functions
- Receives HTTP POST requests with Instagram post text content
- Communicates with the Azure ML model for classification
- Returns classification results as JSON
- https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python?pivots=python-mode-decorators

### 2. Topic Classification Model
- Deployed on Azure Machine Learning
- Receives text input from the Azure Function
- Performs (trivial) topic classification
- Returns classification probabilities

## Data Flow
1. Client sends a POST request with Instagram post text to the Azure Function endpoint
2. Azure Function preprocesses the text and sends it to the Azure ML model
3. Azure ML model performs classification and returns probabilities
4. Azure Function formats the response and sends it back to the client

## Azure Services Used
- Azure Functions: Hosts the API endpoint
- Azure Machine Learning: Hosts the classification model
- Azure Monitor: Provides logging and monitoring capabilities

## Security Considerations
- Azure Function is secured with function-level authentication
- All communications use HTTPS
- Azure ML workspace is configured with private endpoints

## Scaling
- Azure Functions can automatically scale based on demand
- Azure ML can be configured to auto-scale for high-throughput scenarios

## Future Improvements
- Implement evlauation capabilities for future model updates
- Add a caching layer to improve response times for frequent requests

