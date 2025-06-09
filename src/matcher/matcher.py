# src/matcher/matcher.py

import json
import os
from typing import Dict, List

def load_metadata() -> Dict:
    """Load metadata from JSON file"""
    try:
        # Get the path relative to the project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        metadata_path = os.path.join(project_root, "metadata", "metadata.json")

        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            print(f"✅ Loaded {len(metadata)} metadata entries.")
            return metadata
    except FileNotFoundError:
        print(f"❌ metadata.json not found at {metadata_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing metadata.json: {e}")
        return {}

def extract_keywords_from_query(query: str) -> List[str]:
    """Extract relevant keywords from user query"""
    query_lower = query.lower()

    # Keywords related to different datasets
    keyword_mappings = {
        'soil': ['soil', 'erosion', 'texture', 'productivity', 'sandy', 'alluvial', 'loam'],
        'roads': ['road', 'highway', 'path', 'track', 'transport', 'national highway', 'state highway'],
        'forest': ['forest', 'tree', 'vegetation', 'evergreen', 'deciduous', 'plantation'],
        'drainage': ['river', 'stream', 'canal', 'drain', 'water', 'drainage', 'tributary'],
        'lulc': ['land use', 'lulc', 'urban', 'rural', 'agriculture', 'built', 'settlement'],
        'earthquake': ['earthquake', 'seismic', 'zone', 'fault', 'thrust'],
        'flood': ['flood', 'plain', 'flooding'],
        'folds': ['fold', 'anticline', 'syncline', 'geology'],
        'contour': ['elevation', 'contour', 'height', 'altitude', 'topography'],
        'districts': ['district', 'administrative', 'boundary', 'almora', 'dehradun', 'nainital'],
        'irrigation': ['irrigation', 'irrigated', 'farming', 'agriculture'],
        'glacier': ['glacier', 'ice', 'glacial', 'snow'],
        'glacial_lakes': ['glacial lake', 'lake', 'pond', 'water body', 'moraine', 'supra']
    }

    matched_categories = []

    for category, keywords in keyword_mappings.items():
        for keyword in keywords:
            if keyword in query_lower:
                matched_categories.append(category)
                break

    return matched_categories

def get_relevant_metadata(query: str) -> str:
    """
    Get relevant dataset metadata based on user query
    Returns formatted context for LLM or empty string if no match
    """
    if not query.strip():
        return ""

    metadata = load_metadata()
    if not metadata:
        return ""

    matched_categories = extract_keywords_from_query(query)

    query_lower = query.lower()
    districts = ['almora', 'tehri garhwal', 'udham singh nagar', 'uttarkashi', 
                'haridwar', 'nainital', 'chamoli', 'bageshwar', 'champawat', 
                'pithoragarh', 'pauri garhwal', 'rudraprayag', 'dehradun']

    has_uttarakhand_context = any(d in query_lower for d in districts) or \
                               'uttarakhand' in query_lower or \
                               'uttrakhand' in query_lower

    relevant_datasets = []

    category_to_dataset = {
        'soil': ['Uttarakhand Soil Data'],
        'roads': ['Uttarakhand Roads Data'],
        'forest': ['Uttarakhand Forest Data'],
        'drainage': ['Uttarakhand Drainage Data'],
        'lulc': ['Uttarakhand LULC (Land Use Land Cover) Data - 2015'],
        'earthquake': ['Uttarakhand earthqake Zone Data', 'Uttarakhand Fault Data'],
        'flood': ['Uttarakhand Flood Plains Data'],
        'folds': ['Uttarakhand Folds Data'],
        'contour': ['Uttarakhand Contour 100 meter Data', 'Uttarakhand Contour 200 meter Data', 'Uttarakhand Contour 500 meter Data'],
        'districts': ['Uttarakhand Districts Data'],
        'irrigation': ['Uttarakhand Irrigation Data'],
        'glacier': ['Uttarakhand Glacier area 2020', 'Uttarakhand Glacier area 2021', 'Uttarakhand Glacier area 2022', 'Uttarakhand Glacier area 2023'],
        'glacial_lakes': ['Uttarakhand Glacial Lakes Data', 'Pre Monsoon Glacial Lakes 2020', 'Pre Monsoon Glacial Lakes 2021', 'Pre Monsoon Glacial Lakes 2022', 'Pre Monsoon Glacial Lakes 2023', 'Post Monsoon Glacial Lakes 2020', 'Post Monsoon Glacial Lakes 2021', 'Post Monsoon Glacial Lakes 2022', 'Post Monsoon Glacial Lakes 2023']
    }

    for category in matched_categories:
        if category in category_to_dataset:
            relevant_datasets.extend(category_to_dataset[category])

    if not relevant_datasets and has_uttarakhand_context:
        relevant_datasets = list(metadata.keys())

    if not relevant_datasets:
        return ""

    relevant_datasets = list(dict.fromkeys(relevant_datasets))

    context_parts = []
    for dataset_name in relevant_datasets:
        if dataset_name in metadata:
            dataset_info = metadata[dataset_name]
            context_part = f"""
Dataset: {dataset_name}
Table: {dataset_info.get('table_name', 'N/A')}
Description: {dataset_info.get('description', 'N/A')}
Columns:"""

            for col_name, col_desc in dataset_info.get('columns', {}).items():
                context_part += f"\n  - {col_name}: {col_desc}"

            context_parts.append(context_part)

    return "\n" + "="*50 + "\n".join(context_parts) + "\n" + "="*50

def test_matcher():
    test_queries = [
        "What types of soil are found in Uttarakhand?",
        "Tell me about roads in Dehradun",
        "What is the weather like today?",
        "Show me forest data",
        "What are the earthquake zones?",
        "Hello, how are you?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        context = get_relevant_metadata(query)
        if context:
            print(f"Context:\n{context}")
        else:
            print("No relevant context found")

if __name__ == "__main__":
    test_matcher()
