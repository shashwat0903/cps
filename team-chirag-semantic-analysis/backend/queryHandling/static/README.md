# DSA Knowledge Graph Scraper

This directory contains a comprehensive DSA (Data Structures and Algorithms) knowledge graph generator system. It scrapes information from multiple educational resources, creates a structured knowledge graph, and provides visualization capabilities.

## Components

- `dsa-scraper/` - The main Python scraper module that collects DSA information from various sources
- `update_dsa_relationships.py` - Script to update relationships between DSA topics
- `visualize_dsa_graph.py` - Script to visualize the knowledge graph

## Features

- Scrapes DSA topics from GeeksForGeeks, LeetCode, W3Schools, NPTEL, YouTube, Coursera, Stack Overflow, Medium, and Dev.to
- Extracts resources (videos, articles, courses, forum posts) for each topic
- Organizes topics into a hierarchical knowledge graph with relationships
- Visualizes the graph to show connections between topics

## Usage

1. Run the scraper to collect information:
   ```
   cd dsa-scraper
   python main.py
   ```

2. Update relationships between topics:
   ```
   python update_dsa_relationships.py
   ```

3. Visualize the knowledge graph:
   ```
   python visualize_dsa_graph.py
   ```

## Integration

This module is designed to be integrated into the queryHandling system to provide comprehensive DSA knowledge for question answering and semantic analysis.
