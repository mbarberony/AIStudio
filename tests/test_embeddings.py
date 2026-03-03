#!/usr/bin/env python3
"""
Quick Embedding Quality Test

Simple script to test the classic "King - Man + Woman = Queen" relationship.

Usage:
    python test_embeddings.py
"""

import sys
from pathlib import Path
import numpy as np

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.ollama_client import ollama_embed


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def test_king_queen():
    """Test the classic King - Man + Woman ≈ Queen relationship"""
    
    print("\n" + "="*60)
    print("EMBEDDING QUALITY TEST: King - Man + Woman = ?")
    print("="*60)
    print(f"Model: {CONFIG.rag.default_embed_model}\n")
    
    # Get embeddings
    print("Getting embeddings...")
    king = np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["king"])[0])
    queen = np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["queen"])[0])
    man = np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["man"])[0])
    woman = np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["woman"])[0])
    
    # Compute: king - man + woman
    print("\nComputing: king - man + woman")
    result = king - man + woman
    result = result / np.linalg.norm(result)  # normalize
    
    # Test candidates
    candidates = {
        "queen": queen,
        "princess": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["princess"])[0]),
        "king": king,  # should not match
        "woman": woman,  # should not match
        "girl": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["girl"])[0]),
        "lady": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["lady"])[0]),
        "empress": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["empress"])[0]),
        "duchess": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["duchess"])[0]),
    }
    
    # Compute similarities
    print("\nSimilarity scores:")
    scores = []
    for word, embedding in candidates.items():
        similarity = cosine_similarity(result, embedding)
        scores.append((word, similarity))
    
    # Sort by similarity
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # Display results
    for i, (word, score) in enumerate(scores, 1):
        bar = "█" * int(score * 50)
        marker = " ✓ CORRECT!" if word == "queen" and i == 1 else ""
        print(f"  {i}. {word:15s} {score:.4f} {bar}{marker}")
    
    # Verdict
    print("\n" + "-"*60)
    if scores[0][0] == "queen":
        print("✓ TEST PASSED: 'queen' is the closest match!")
        print("  This embedding model captures semantic relationships well.")
    else:
        print(f"✗ TEST FAILED: Expected 'queen', got '{scores[0][0]}'")
        print("  This embedding model may not capture semantic relationships well.")
    print("-"*60 + "\n")


def test_geography():
    """Test: Paris - France + Italy = Rome"""
    
    print("\n" + "="*60)
    print("GEOGRAPHY TEST: Paris - France + Italy = ?")
    print("="*60)
    print(f"Model: {CONFIG.rag.default_embed_model}\n")
    
    print("Getting embeddings...")
    paris = np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Paris"])[0])
    france = np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["France"])[0])
    italy = np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Italy"])[0])
    rome = np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Rome"])[0])
    
    print("\nComputing: Paris - France + Italy")
    result = paris - france + italy
    result = result / np.linalg.norm(result)
    
    candidates = {
        "Rome": rome,
        "Milan": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Milan"])[0]),
        "Venice": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Venice"])[0]),
        "Florence": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Florence"])[0]),
        "Naples": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Naples"])[0]),
        "Paris": paris,
        "Madrid": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Madrid"])[0]),
        "Berlin": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Berlin"])[0]),
    }
    
    print("\nSimilarity scores:")
    scores = []
    for word, embedding in candidates.items():
        similarity = cosine_similarity(result, embedding)
        scores.append((word, similarity))
    
    scores.sort(key=lambda x: x[1], reverse=True)
    
    for i, (word, score) in enumerate(scores, 1):
        bar = "█" * int(score * 50)
        marker = " ✓ CORRECT!" if word == "Rome" and i == 1 else ""
        print(f"  {i}. {word:15s} {score:.4f} {bar}{marker}")
    
    print("\n" + "-"*60)
    if scores[0][0] == "Rome":
        print("✓ TEST PASSED: 'Rome' is the closest match!")
    else:
        print(f"✗ TEST FAILED: Expected 'Rome', got '{scores[0][0]}'")
    print("-"*60 + "\n")


def test_tech():
    """Test: Python - Django + JavaScript = ?"""
    
    print("\n" + "="*60)
    print("TECH TEST: Python - Django + JavaScript = ?")
    print("="*60)
    print(f"Model: {CONFIG.rag.default_embed_model}\n")
    
    print("Getting embeddings...")
    python = np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Python"])[0])
    django = np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Django"])[0])
    javascript = np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["JavaScript"])[0])
    
    print("\nComputing: Python - Django + JavaScript")
    result = python - django + javascript
    result = result / np.linalg.norm(result)
    
    candidates = {
        "React": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["React"])[0]),
        "Vue": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Vue"])[0]),
        "Angular": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Angular"])[0]),
        "Express": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Express"])[0]),
        "Node": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Node"])[0]),
        "Flask": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Flask"])[0]),
        "Rails": np.array(ollama_embed(model=CONFIG.rag.default_embed_model, texts=["Rails"])[0]),
        "Django": django,
    }
    
    print("\nSimilarity scores:")
    print("(Looking for JavaScript frameworks like React, Vue, Angular, Express...)")
    scores = []
    for word, embedding in candidates.items():
        similarity = cosine_similarity(result, embedding)
        scores.append((word, similarity))
    
    scores.sort(key=lambda x: x[1], reverse=True)
    
    for i, (word, score) in enumerate(scores, 1):
        bar = "█" * int(score * 50)
        print(f"  {i}. {word:15s} {score:.4f} {bar}")
    
    print("\n" + "-"*60)
    top = scores[0][0]
    if top in ["React", "Vue", "Angular", "Express", "Node"]:
        print(f"✓ TEST PASSED: Got '{top}' (a JavaScript framework)")
    else:
        print(f"? UNCLEAR: Got '{top}' (not a typical JavaScript framework)")
    print("-"*60 + "\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("EMBEDDING MODEL QUALITY TESTS")
    print("="*60)
    print("\nTesting semantic relationships in your embedding model...")
    print("This helps evaluate if your embeddings capture meaning well.\n")
    
    try:
        # Run all tests
        test_king_queen()
        test_geography()
        test_tech()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETE")
        print("="*60)
        print("\nIf most tests passed, your embedding model is working well!")
        print("If tests failed, consider trying a different embedding model.")
        print("\nTo test with a different model:")
        print("  export AISTUDIO_DEFAULT_EMBED_MODEL='bge-large'")
        print("  python test_embeddings.py\n")
        
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        print("\nMake sure:")
        print("  1. Ollama is running: ollama serve")
        print("  2. Model is pulled: ollama pull nomic-embed-text")
        print("  3. You're in the right directory\n")
