"""
═══════════════════════════════════════════════════════════════════════════════
SOVEREIGN CINEMA ENGINE - CHROMADB SETUP
Semantic Memory & RAG Foundation
═══════════════════════════════════════════════════════════════════════════════
"""

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

CHROMA_DATA_PATH = Path("./chroma_data")
CHROMA_DATA_PATH.mkdir(exist_ok=True)

# OpenAI Embedding Function (best quality)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"  # Cost: $0.02 per 1M tokens (very cheap)
)

# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def get_chroma_client():
    """Initialize persistent ChromaDB client"""
    client = chromadb.PersistentClient(
        path=str(CHROMA_DATA_PATH),
        settings=Settings(
            anonymized_telemetry=False,
            allow_reset=True
        )
    )
    return client

# ═══════════════════════════════════════════════════════════════════════════════
# COLLECTION SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

COLLECTIONS = {
    "research_intelligence": {
        "description": "Research reports, web scraping results, intelligence gathered",
        "metadata_schema": {
            "project_id": "UUID of related project",
            "topic": "Research topic",
            "source_urls": "List of source URLs",
            "date": "Date of research",
            "viability_score": "0-100 score",
            "agent": "Agent that created this"
        }
    },
    
    "user_memory": {
        "description": "Learned preferences, style choices, feedback patterns",
        "metadata_schema": {
            "type": "style_preference | content_preference | feedback | pattern",
            "confidence": "0.0-1.0 confidence score",
            "learned_from": "project_id or 'feedback_loop'",
            "category": "aesthetic | tone | technical | creative",
            "date": "When this was learned"
        }
    },
    
    "ideas_pool": {
        "description": "AI-generated content ideas, suggestions, trending topics",
        "metadata_schema": {
            "idea_type": "original | trending | recreate | inspired",
            "viability_score": "0-100",
            "target_audience": "Audience description",
            "suggested_by": "agent | user | trend_analysis",
            "date": "Suggestion date",
            "status": "new | reviewed | approved | rejected"
        }
    },
    
    "source_knowledge": {
        "description": "Knowledge extracted from high-performing sources",
        "metadata_schema": {
            "source_id": "UUID from PostgreSQL sources table",
            "domain": "Source domain",
            "category": "news | youtube | blog | paper",
            "extracted_date": "When content was extracted",
            "relevance_topics": "List of relevant topics"
        }
    },
    
    "rag_documents": {
        "description": "Your RAG project - technical docs, references, knowledge base",
        "metadata_schema": {
            "doc_type": "technical | reference | tutorial | api_doc",
            "source": "Source of document",
            "date_added": "When added",
            "tags": "List of tags",
            "language": "Programming language if applicable"
        }
    },
    
    "project_artifacts": {
        "description": "Scripts, storyboards, prompts from completed projects",
        "metadata_schema": {
            "project_id": "UUID of project",
            "artifact_type": "script | storyboard | prompt | dialogue",
            "success_score": "Project success score",
            "date": "Creation date",
            "reusable": "true | false"
        }
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# COLLECTION INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def initialize_collections(client=None, reset=False):
    """
    Create all collections with proper schemas
    
    Args:
        client: ChromaDB client (creates new if None)
        reset: If True, deletes and recreates all collections
    
    Returns:
        dict: Dictionary of collection objects
    """
    if client is None:
        client = get_chroma_client()
    
    collections = {}
    
    for name, schema in COLLECTIONS.items():
        if reset:
            try:
                client.delete_collection(name=name)
                print(f"✓ Deleted existing collection: {name}")
            except:
                pass
        
        try:
            collection = client.get_or_create_collection(
                name=name,
                embedding_function=openai_ef,
                metadata={"description": schema["description"]}
            )
            collections[name] = collection
            print(f"✓ Initialized collection: {name}")
        except Exception as e:
            print(f"✗ Error initializing {name}: {str(e)}")
    
    return collections

# ═══════════════════════════════════════════════════════════════════════════════
# COLLECTION HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

class ChromaManager:
    """Manager class for all ChromaDB operations"""
    
    def __init__(self):
        self.client = get_chroma_client()
        self.collections = {}
        self._load_collections()
    
    def _load_collections(self):
        """Load all collections"""
        for name in COLLECTIONS.keys():
            try:
                self.collections[name] = self.client.get_collection(
                    name=name,
                    embedding_function=openai_ef
                )
            except:
                # Create if doesn't exist
                self.collections[name] = self.client.create_collection(
                    name=name,
                    embedding_function=openai_ef
                )
    
    def add_research(self, project_id, topic, content, metadata=None):
        """Add research intelligence"""
        meta = {
            "project_id": str(project_id),
            "topic": topic,
            "date": str(datetime.now().date()),
            "agent": "01_intelligence_agent"
        }
        if metadata:
            meta.update(metadata)
        
        doc_id = f"research_{project_id}_{int(time.time())}"
        
        self.collections["research_intelligence"].add(
            documents=[content],
            metadatas=[meta],
            ids=[doc_id]
        )
        return doc_id
    
    def add_user_memory(self, memory_text, memory_type, confidence=1.0, metadata=None):
        """Add learned user preference"""
        meta = {
            "type": memory_type,
            "confidence": confidence,
            "date": str(datetime.now().date())
        }
        if metadata:
            meta.update(metadata)
        
        doc_id = f"memory_{memory_type}_{int(time.time())}"
        
        self.collections["user_memory"].add(
            documents=[memory_text],
            metadatas=[meta],
            ids=[doc_id]
        )
        return doc_id
    
    def add_idea(self, idea_text, viability_score, metadata=None):
        """Add content idea to pool"""
        meta = {
            "viability_score": viability_score,
            "date": str(datetime.now().date()),
            "status": "new",
            "suggested_by": "agent"
        }
        if metadata:
            meta.update(metadata)
        
        doc_id = f"idea_{int(time.time())}"
        
        self.collections["ideas_pool"].add(
            documents=[idea_text],
            metadatas=[meta],
            ids=[doc_id]
        )
        return doc_id
    
    def search_similar(self, collection_name, query_text, n_results=5, filters=None):
        """
        Semantic search in any collection
        
        Args:
            collection_name: Name of collection to search
            query_text: Search query
            n_results: Number of results
            filters: Metadata filters (e.g., {"type": "style_preference"})
        
        Returns:
            dict: Query results with documents, metadatas, distances
        """
        collection = self.collections.get(collection_name)
        if not collection:
            raise ValueError(f"Collection {collection_name} not found")
        
        where_filter = filters if filters else None
        
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where_filter
        )
        return results
    
    def get_collection_stats(self):
        """Get statistics for all collections"""
        stats = {}
        for name, collection in self.collections.items():
            try:
                count = collection.count()
                stats[name] = {
                    "count": count,
                    "description": COLLECTIONS[name]["description"]
                }
            except:
                stats[name] = {"count": 0, "description": "Error"}
        return stats
    
    def delete_by_metadata(self, collection_name, filters):
        """Delete documents matching metadata filters"""
        collection = self.collections.get(collection_name)
        if not collection:
            return
        
        collection.delete(where=filters)

# ═══════════════════════════════════════════════════════════════════════════════
# MAINTENANCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def cleanup_old_ideas(days_threshold=30):
    """Remove old rejected ideas"""
    manager = ChromaManager()
    
    from datetime import datetime, timedelta
    cutoff_date = (datetime.now() - timedelta(days=days_threshold)).strftime("%Y-%m-%d")
    
    # This is a simple example - ChromaDB doesn't support date comparison in where clause
    # In production, you'd need to fetch all, filter in Python, then delete by IDs
    print(f"Cleanup: Remove ideas older than {cutoff_date} with status='rejected'")

def export_collection(collection_name, output_path):
    """Export collection to JSON for backup"""
    import json
    
    manager = ChromaManager()
    collection = manager.collections.get(collection_name)
    
    if not collection:
        print(f"Collection {collection_name} not found")
        return
    
    data = collection.get(include=["documents", "metadatas", "embeddings"])
    
    with open(output_path, 'w') as f:
        json.dump({
            "collection_name": collection_name,
            "count": len(data['ids']),
            "data": data
        }, f, indent=2)
    
    print(f"✓ Exported {collection_name} to {output_path}")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN - SETUP SCRIPT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    from datetime import datetime
    import time
    
    print("═" * 70)
    print("SOVEREIGN CINEMA ENGINE - ChromaDB Setup")
    print("═" * 70)
    
    # Check for reset flag
    reset = "--reset" in sys.argv
    
    if reset:
        print("\n⚠️  RESET MODE: All collections will be deleted and recreated")
        confirm = input("Type 'YES' to confirm: ")
        if confirm != "YES":
            print("Aborted.")
            sys.exit(0)
    
    # Initialize
    print("\n📦 Initializing ChromaDB client...")
    client = get_chroma_client()
    
    print("\n🏗️  Creating collections...")
    collections = initialize_collections(client, reset=reset)
    
    # Test manager
    print("\n🧪 Testing ChromaManager...")
    manager = ChromaManager()
    
    # Add test data
    if reset:
        print("\n📝 Adding test data...")
        
        # Test memory
        manager.add_user_memory(
            "User prefers minimalist aesthetic with neon green accents",
            memory_type="style_preference",
            confidence=0.95,
            metadata={"learned_from": "manual_setup"}
        )
        
        # Test idea
        manager.add_idea(
            "Create Hinglish explanation of Docker containers for Indian developers",
            viability_score=88,
            metadata={"idea_type": "trending", "target_audience": "Indian developers"}
        )
        
        print("✓ Test data added")
    
    # Show stats
    print("\n📊 Collection Statistics:")
    stats = manager.get_collection_stats()
    for name, info in stats.items():
        print(f"  • {name}: {info['count']} documents")
    
    print("\n✅ ChromaDB setup complete!")
    print(f"📁 Data stored in: {CHROMA_DATA_PATH}")
    print("\nUsage in your code:")
    print("  from database.chroma_setup import ChromaManager")
    print("  manager = ChromaManager()")
    print("  manager.add_research(...)")
    print("  results = manager.search_similar('user_memory', 'style preferences')")