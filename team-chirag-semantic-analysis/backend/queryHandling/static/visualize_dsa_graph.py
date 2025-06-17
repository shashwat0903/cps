import json
import os
import sys
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.colors as mcolors
import subprocess
import shutil

def parse_arguments():
    """Parse command line arguments for DSA topics"""
    parser = argparse.ArgumentParser(description='DSA Knowledge Graph Generator')
    parser.add_argument('--topics', nargs='+', default=['array'], 
                        help='List of DSA topics to scrape and visualize (e.g., array linked_list binary_tree)')
    parser.add_argument('--scrape', action='store_true', 
                        help='Run the scraper to fetch fresh data (default: use existing data)')
    parser.add_argument('--output', default='dsa_graph.png',
                        help='Output file path for the visualization')
    return parser.parse_args()

def run_scraper(topics):
    """Run the DSA scraper for the specified topics"""
    scraper_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                               'dsa-scraper', 'python-scraper', 'main.py')
    
    print(f"Running scraper for topics: {', '.join(topics)}")
    
    for topic in topics:
        try:
            print(f"Scraping data for '{topic}'...")
            subprocess.run([sys.executable, scraper_path, '--topic', topic], 
                          check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error scraping topic '{topic}': {e}")
            print(f"Error output: {e.stderr}")
            continue
    
    print("Scraping completed")

def load_json_data(json_path):
    """Load the DSA graph data from JSON file"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_path}")
        sys.exit(1)

def create_graph_from_data(data):
    """Create a NetworkX graph from the DSA data"""
    G = nx.DiGraph()
    
    # Node colors by level
    level_colors = {
        "beginner": "#4CAF50",      # Green
        "intermediate": "#2196F3",  # Blue
        "advanced": "#F44336"       # Red
    }
    
    # Keep track of added nodes to avoid duplicates
    added_nodes = set()
    
    # Add all topics as nodes
    for topic in data["concepts"]:
        # Add main topic node
        topic_id = topic["id"]
        if topic_id not in added_nodes:
            G.add_node(
                topic_id, 
                name=topic["name"],
                type="topic",
                level=topic["level"],
                description=topic.get("description", ""),
                color=level_colors.get(topic["level"], "#9E9E9E"),
                resources=topic.get("resources", {})
            )
            added_nodes.add(topic_id)
        
        # Add subtopic nodes
        for subtopic in topic.get("subconcepts", []):
            subtopic_id = subtopic["id"]
            if subtopic_id not in added_nodes:
                G.add_node(
                    subtopic_id,
                    name=subtopic["name"],
                    type="subtopic",
                    level=subtopic["level"],
                    description=subtopic.get("description", ""),
                    color=level_colors.get(subtopic["level"], "#9E9E9E"),
                    resources=subtopic.get("resources", {})
                )
                added_nodes.add(subtopic_id)
            
            # Add edge from topic to subtopic
            G.add_edge(topic_id, subtopic_id, type="parent-child", weight=3)
            
            # Add prerequisite edges
            for prereq_id in subtopic.get("prerequisites", []):
                if prereq_id in G:
                    G.add_edge(prereq_id, subtopic_id, type="prerequisite", weight=2)
            
            # Add suggestion edges
            for suggestion_id in subtopic.get("topic_suggestions", []):
                if suggestion_id in G:
                    G.add_edge(subtopic_id, suggestion_id, type="suggestion", weight=1)
        
        # Add topic prerequisite edges
        for prereq_id in topic.get("prerequisites", []):
            if prereq_id in G:
                G.add_edge(prereq_id, topic_id, type="prerequisite", weight=2)
        
        # Add topic suggestion edges
        for suggestion_id in topic.get("topic_suggestions", []):
            if suggestion_id in G:
                G.add_edge(topic_id, suggestion_id, type="suggestion", weight=1)
    
    return G

def add_resource_nodes(G, data):
    """Add resource nodes (videos, articles) to the graph"""
    # Resource type colors
    resource_colors = {
        "video": "#9C27B0",  # Purple
        "article": "#FF9800"  # Orange
    }
    
    # Process all topics and subtopics
    for concept in data["concepts"]:
        # Process main topic resources
        topic_id = concept["id"]
        resources = concept.get("resources", {})
        
        # Add video resource nodes
        for i, video in enumerate(resources.get("videos", [])[:3]):  # Limit to top 3 resources for clarity
            video_id = f"{topic_id}_video_{i}"
            G.add_node(
                video_id,
                name=video.get("title", "Video Resource"),
                type="resource",
                resource_type="video",
                url=video.get("url", ""),
                color=resource_colors["video"]
            )
            G.add_edge(topic_id, video_id, type="resource", weight=1)
        
        # Add article resource nodes
        for i, article in enumerate(resources.get("articles", [])[:3]):  # Limit to top 3 resources for clarity
            article_id = f"{topic_id}_article_{i}"
            G.add_node(
                article_id,
                name=article.get("title", "Article Resource"),
                type="resource",
                resource_type="article",
                url=article.get("url", ""),
                color=resource_colors["article"]
            )
            G.add_edge(topic_id, article_id, type="resource", weight=1)
        
        # Process subtopic resources
        for subtopic in concept.get("subconcepts", []):
            subtopic_id = subtopic["id"]
            resources = subtopic.get("resources", {})
            
            # Add video resource nodes
            for i, video in enumerate(resources.get("videos", [])[:2]):  # Limit to top 2 resources for clarity
                video_id = f"{subtopic_id}_video_{i}"
                G.add_node(
                    video_id,
                    name=video.get("title", "Video Resource"),
                    type="resource",
                    resource_type="video",
                    url=video.get("url", ""),
                    color=resource_colors["video"]
                )
                G.add_edge(subtopic_id, video_id, type="resource", weight=1)
            
            # Add article resource nodes
            for i, article in enumerate(resources.get("articles", [])[:2]):  # Limit to top 2 resources for clarity
                article_id = f"{subtopic_id}_article_{i}"
                G.add_node(
                    article_id,
                    name=article.get("title", "Article Resource"),
                    type="resource",
                    resource_type="article",
                    url=article.get("url", ""),
                    color=resource_colors["article"]
                )
                G.add_edge(subtopic_id, article_id, type="resource", weight=1)
    
    return G

def visualize_graph(G, output_path, topics=None):
    """Visualize the graph and save as an image"""
    plt.figure(figsize=(24, 18))
    
    # Create a hierarchical layout - use different layout algorithms based on graph size
    if G.number_of_nodes() > 50:
        print("Using spring layout for larger graph...")
        pos = nx.spring_layout(G, seed=42, k=0.5)
    else:
        print("Using kamada kawai layout for smaller graph...")
        pos = nx.kamada_kawai_layout(G)
    
    # Draw nodes with different sizes and colors based on type
    node_colors = []
    node_sizes = []
    node_labels = {}
    
    for node, attrs in G.nodes(data=True):
        node_colors.append(attrs.get('color', '#9E9E9E'))
        
        # Set node size based on node type
        if attrs.get('type') == 'topic':
            node_sizes.append(1500)
        elif attrs.get('type') == 'subtopic':
            node_sizes.append(1000)
        else:  # resource nodes
            node_sizes.append(500)
        
        # Create node labels
        if attrs.get('type') in ['topic', 'subtopic']:
            node_labels[node] = f"{attrs.get('name')}\n({attrs.get('level', '')})"
        else:
            # Truncate resource titles if too long
            title = attrs.get('name', '')
            if len(title) > 30:
                title = title[:27] + '...'
            node_labels[node] = title
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
    
    # Draw edges with different styles based on edge type
    edge_colors = []
    edge_widths = []
    edge_styles = []
    
    for u, v, attrs in G.edges(data=True):
        edge_type = attrs.get('type', '')
        
        if edge_type == 'parent-child':
            edge_colors.append('black')
            edge_widths.append(2.0)
            edge_styles.append('solid')
        elif edge_type == 'prerequisite':
            edge_colors.append('red')
            edge_widths.append(1.5)
            edge_styles.append('dashed')
        elif edge_type == 'suggestion':
            edge_colors.append('blue')
            edge_widths.append(1.0)
            edge_styles.append('dotted')
        else:  # resource edges
            edge_colors.append('gray')
            edge_widths.append(0.5)
            edge_styles.append('solid')
    
    # Draw edges with arrows
    for i, (u, v, attrs) in enumerate(G.edges(data=True)):
        nx.draw_networkx_edges(
            G, pos, 
            edgelist=[(u, v)], 
            width=edge_widths[i],
            edge_color=edge_colors[i],
            style=edge_styles[i],
            arrows=True,
            arrowsize=15,
            connectionstyle='arc3,rad=0.1'  # Curved edges
        )
    
    # Draw labels with better font
    nx.draw_networkx_labels(
        G, pos, 
        labels=node_labels,
        font_size=10,
        font_family='sans-serif',
        font_weight='bold'
    )
    
    # Add a legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4CAF50', markersize=15, label='Beginner'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#2196F3', markersize=15, label='Intermediate'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#F44336', markersize=15, label='Advanced'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#9C27B0', markersize=15, label='Video'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF9800', markersize=15, label='Article'),
        plt.Line2D([0], [0], color='black', lw=2, label='Parent-Child'),
        plt.Line2D([0], [0], color='red', lw=2, linestyle='dashed', label='Prerequisite'),
        plt.Line2D([0], [0], color='blue', lw=2, linestyle='dotted', label='Suggestion')
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=12)
      # Add title
    topics_str = "Array"
    if topics:
        topics_str = ", ".join([t.capitalize() for t in topics])
    plt.title(f'DSA Knowledge Graph: {topics_str} and Related Concepts', fontsize=20, fontweight='bold')
    
    # Remove axes
    plt.axis('off')
    
    # Save figure with high resolution
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Graph visualization saved to {output_path}")
    
    # Display graph
    plt.show()

def main():
    # Parse command line arguments
    args = parse_arguments()
    
    # Set file paths
    json_path = r'c:\Users\Ritesh Singh\OneDrive\Pictures\webs\dsa-scraper\python-scraper\output\dsa_graph.json'
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.output)
    
    # Run scraper for fresh data if requested
    if args.scrape:
        run_scraper(args.topics)
    
    # Load data
    print(f"Loading data from {json_path}")
    data = load_json_data(json_path)
    
    # Create base graph
    print("Creating graph structure...")
    G = create_graph_from_data(data)
    print(f"Created graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    
    # Add resource nodes
    print("Adding resource nodes...")
    G = add_resource_nodes(G, data)
    print(f"Final graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    
    # Visualize graph
    print("Visualizing graph...")
    visualize_graph(G, output_path, args.topics)
    
    print(f"Graph visualization saved to {output_path}")

if __name__ == "__main__":
    main()
