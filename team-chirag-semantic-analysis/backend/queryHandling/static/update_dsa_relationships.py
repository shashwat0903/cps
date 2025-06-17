import json
import os
import sys

# Path to the DSA knowledge graph JSON file
JSON_PATH = r'c:\Users\Ritesh Singh\OneDrive\Pictures\webs\dsa-scraper\python-scraper\output\dsa_graph.json'

# Define relationships between data structures
# Format: 
# {
#   "source_data_structure": {
#     "prerequisites": ["data_structure1", "data_structure2"],
#     "topic_suggestions": ["data_structure3", "data_structure4"]
#   }
# }
DSA_RELATIONSHIPS = {
    # Array and related data structures
    "array": {
        "prerequisites": [],
        "topic_suggestions": ["dynamic_array", "linked_list", "stack", "queue", "matrix", "hash_table"]
    },
    "dynamic_array": {
        "prerequisites": ["array"],
        "topic_suggestions": ["linked_list", "vector"]
    },
    
    # Linked List and related data structures
    "linked_list": {
        "prerequisites": ["array"],
        "topic_suggestions": ["doubly_linked_list", "circular_linked_list", "stack", "queue", "hash_table"]
    },
    "doubly_linked_list": {
        "prerequisites": ["linked_list"],
        "topic_suggestions": ["circular_linked_list", "deque"]
    },
    "circular_linked_list": {
        "prerequisites": ["linked_list"],
        "topic_suggestions": ["doubly_linked_list"]
    },
    
    # Stack and Queue
    "stack": {
        "prerequisites": ["array", "linked_list"],
        "topic_suggestions": ["queue", "expression_evaluation", "recursion", "dfs"]
    },
    "queue": {
        "prerequisites": ["array", "linked_list"],
        "topic_suggestions": ["stack", "deque", "priority_queue", "bfs"]
    },
    "deque": {
        "prerequisites": ["queue", "doubly_linked_list"],
        "topic_suggestions": ["priority_queue"]
    },
    "priority_queue": {
        "prerequisites": ["queue", "heap"],
        "topic_suggestions": ["binary_heap", "graph_algorithms"]
    },
    
    # Tree data structures
    "tree": {
        "prerequisites": ["recursion"],
        "topic_suggestions": ["binary_tree", "binary_search_tree", "avl_tree", "heap", "trie", "graph"]
    },
    "binary_tree": {
        "prerequisites": ["tree"],
        "topic_suggestions": ["binary_search_tree", "heap", "tree_traversal"]
    },
    "binary_search_tree": {
        "prerequisites": ["binary_tree", "binary_search"],
        "topic_suggestions": ["avl_tree", "red_black_tree", "b_tree"]
    },
    "avl_tree": {
        "prerequisites": ["binary_search_tree"],
        "topic_suggestions": ["red_black_tree", "self_balancing_tree"]
    },
    "red_black_tree": {
        "prerequisites": ["binary_search_tree"],
        "topic_suggestions": ["avl_tree", "self_balancing_tree"]
    },
    "heap": {
        "prerequisites": ["binary_tree", "array"],
        "topic_suggestions": ["priority_queue", "heap_sort"]
    },
    "trie": {
        "prerequisites": ["tree"],
        "topic_suggestions": ["string_algorithms", "autocomplete"]
    },    
    # Graph data structures
    "graph": {
        "prerequisites": ["array", "linked_list"],
        "topic_suggestions": ["dfs", "bfs", "shortest_path", "spanning_tree", "network_flow"]
    },
    "directed_graph": {
        "prerequisites": ["graph"],
        "topic_suggestions": ["topological_sort", "strongly_connected_components"]
    },
    "undirected_graph": {
        "prerequisites": ["graph"],
        "topic_suggestions": ["minimum_spanning_tree", "connected_components"]
    },
    "weighted_graph": {
        "prerequisites": ["graph"],
        "topic_suggestions": ["shortest_path", "minimum_spanning_tree"]
    },
    
    # Hash-based data structures
    "hash_table": {
        "prerequisites": ["array", "linked_list"],
        "topic_suggestions": ["hash_set", "hash_map", "bloom_filter"]
    },
    "hash_set": {
        "prerequisites": ["hash_table"],
        "topic_suggestions": ["hash_map"]
    },
    "hash_map": {
        "prerequisites": ["hash_table"],
        "topic_suggestions": ["hash_set", "lru_cache"]
    },
    
    # Advanced data structures
    "segment_tree": {
        "prerequisites": ["binary_tree", "array"],
        "topic_suggestions": ["fenwick_tree", "range_queries"]
    },
    "fenwick_tree": {
        "prerequisites": ["array"],
        "topic_suggestions": ["segment_tree", "range_queries"]
    },
    "disjoint_set": {
        "prerequisites": ["array", "tree"],
        "topic_suggestions": ["kruskal", "minimum_spanning_tree"]
    },
    
    # String data structures
    "string": {
        "prerequisites": ["array"],
        "topic_suggestions": ["string_matching", "trie", "suffix_tree"]
    },
    "suffix_tree": {
        "prerequisites": ["string", "tree"],
        "topic_suggestions": ["suffix_array", "string_matching"]
    },
    "suffix_array": {
        "prerequisites": ["string", "array"],
        "topic_suggestions": ["suffix_tree", "string_matching"]
    },
    
    # Algorithmic techniques
    "recursion": {
        "prerequisites": [],
        "topic_suggestions": ["dynamic_programming", "divide_and_conquer", "backtracking"]
    },
    "dynamic_programming": {
        "prerequisites": ["recursion"],
        "topic_suggestions": ["greedy", "memoization"]
    },
    "greedy": {
        "prerequisites": [],
        "topic_suggestions": ["dynamic_programming"]
    },
    "divide_and_conquer": {
        "prerequisites": ["recursion"],
        "topic_suggestions": ["merge_sort", "quick_sort", "binary_search"]
    },
    "backtracking": {
        "prerequisites": ["recursion"],
        "topic_suggestions": ["branch_and_bound", "combinatorial_search"]
    }
}

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

def save_json_data(json_path, data):
    """Save the DSA graph data to JSON file"""
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Successfully updated DSA relationships in {json_path}")
    except Exception as e:
        print(f"Error saving JSON data: {e}")
        sys.exit(1)

def get_topic_id_by_name(data, topic_name):
    """Find a topic ID by name (case-insensitive partial match)"""
    for topic in data["concepts"]:
        if topic_name.lower() in topic["name"].lower():
            return topic["id"]
    return None

def update_relationships(data):
    """Update relationships between data structures in the graph"""
    # Create a mapping of topic names to IDs
    topic_name_to_id = {}
    
    print("Found the following concepts in the data:")
    for topic in data["concepts"]:
        # Use the lowercase name as key for easier matching
        name_lower = topic["name"].lower()
        topic_name_to_id[name_lower] = topic["id"]
        print(f"  - {topic['name']} (ID: {topic['id']})")
    
    # Count the relationships added
    added_prerequisites = 0
    added_suggestions = 0
    
    # Process each topic in the data
    for topic in data["concepts"]:
        topic_name = topic["name"].lower()
        
        # Try to find a matching relationship definition
        relationship_key = None
        for key in DSA_RELATIONSHIPS:
            if key in topic_name:
                relationship_key = key
                break
        
        if relationship_key:
            print(f"\nProcessing relationships for {topic['name']} (matching with '{relationship_key}'):")
            relationship = DSA_RELATIONSHIPS[relationship_key]
            
            # Process prerequisites
            for prereq_name in relationship["prerequisites"]:
                # Find topics that match this prerequisite
                for name, topic_id in topic_name_to_id.items():
                    if prereq_name in name and topic_id != topic["id"]:
                        if topic_id not in topic["prerequisites"]:
                            topic["prerequisites"].append(topic_id)
                            added_prerequisites += 1
                            print(f"  Added prerequisite: {name} (ID: {topic_id})")
            
            # Process topic suggestions
            for suggestion_name in relationship["topic_suggestions"]:
                # Find topics that match this suggestion
                for name, topic_id in topic_name_to_id.items():
                    if suggestion_name in name and topic_id != topic["id"]:
                        if topic_id not in topic["topic_suggestions"]:
                            topic["topic_suggestions"].append(topic_id)
                            added_suggestions += 1
                            print(f"  Added suggestion: {name} (ID: {topic_id})")
    
    print(f"\nAdded {added_prerequisites} prerequisites and {added_suggestions} topic suggestions")
    return data

def add_missing_relationships(data):
    """Add specific relationships that might be missed by the automatic matching"""
    # Map of topic IDs
    topic_id_map = {topic["id"]: topic for topic in data["concepts"]}
    
    # Find IDs for common data structures if they exist
    array_id = get_topic_id_by_name(data, "array")
    linked_list_id = get_topic_id_by_name(data, "linked list")
    stack_id = get_topic_id_by_name(data, "stack")
    queue_id = get_topic_id_by_name(data, "queue")
    
    # Add specific relationships between core data structures
    if linked_list_id and stack_id:
        if linked_list_id not in topic_id_map[stack_id]["prerequisites"]:
            topic_id_map[stack_id]["prerequisites"].append(linked_list_id)
            print(f"Added linked list as prerequisite for stack")
    
    if linked_list_id and queue_id:
        if linked_list_id not in topic_id_map[queue_id]["prerequisites"]:
            topic_id_map[queue_id]["prerequisites"].append(linked_list_id)
            print(f"Added linked list as prerequisite for queue")
    
    if array_id and stack_id:
        if array_id not in topic_id_map[stack_id]["prerequisites"]:
            topic_id_map[stack_id]["prerequisites"].append(array_id)
            print(f"Added array as prerequisite for stack")
    
    if array_id and queue_id:
        if array_id not in topic_id_map[queue_id]["prerequisites"]:
            topic_id_map[queue_id]["prerequisites"].append(array_id)
            print(f"Added array as prerequisite for queue")
    
    return data

def main():
    print(f"Loading DSA knowledge graph from {JSON_PATH}")
    data = load_json_data(JSON_PATH)
    
    print(f"Updating relationships between data structures...")
    data = update_relationships(data)
    
    print(f"Adding missing specific relationships...")
    data = add_missing_relationships(data)
    
    print(f"Saving updated DSA knowledge graph...")
    save_json_data(JSON_PATH, data)
    
    print(f"Done! Now you can visualize the updated graph with:")
    print(f"python visualize_dsa_graph.py")

if __name__ == "__main__":
    main()
