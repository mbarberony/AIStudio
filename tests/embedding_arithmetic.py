#!/usr/bin/env python3
"""
Embedding Arithmetic Explorer

Test semantic relationships in embeddings like:
- King - Man + Woman ≈ Queen
- Paris - France + Italy ≈ Rome
- Good - Bad + Ugly ≈ Beautiful

Usage:
    python embedding_arithmetic.py
    python embedding_arithmetic.py --model nomic-embed-text
    python embedding_arithmetic.py --interactive
"""

from __future__ import annotations

import argparse
import numpy as np
from typing import List, Tuple
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.ollama_client import ollama_embed


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_embedding(text: str, model: str = None) -> np.ndarray:
    """Get embedding vector for text"""
    model = model or CONFIG.rag.default_embed_model
    # ollama_embed returns list[list[float]], we want the first one
    embedding = ollama_embed(model=model, texts=[text])[0]
    return np.array(embedding)


def find_closest_words(
    target_embedding: np.ndarray,
    word_list: List[str],
    model: str,
    top_k: int = 5,
    exclude: List[str] = None
) -> List[Tuple[str, float]]:
    """
    Find words in word_list closest to target_embedding.
    
    Returns list of (word, similarity_score) tuples.
    """
    exclude = exclude or []
    exclude_lower = [w.lower() for w in exclude]
    
    results = []
    for word in word_list:
        if word.lower() in exclude_lower:
            continue
        
        word_embedding = get_embedding(word, model)
        similarity = cosine_similarity(target_embedding, word_embedding)
        results.append((word, similarity))
    
    # Sort by similarity (descending)
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]


def embedding_arithmetic(
    positive: List[str],
    negative: List[str],
    model: str = None,
    verbose: bool = True
) -> np.ndarray:
    """
    Perform embedding arithmetic: sum(positive) - sum(negative)
    
    Example:
        positive = ["king", "woman"]
        negative = ["man"]
        → king - man + woman
    """
    model = model or CONFIG.rag.default_embed_model
    
    if verbose:
        pos_str = " + ".join(positive)
        neg_str = " - ".join(negative)
        print(f"\nComputing: {pos_str} - {neg_str}")
    
    # Get embeddings
    # Initialize result with proper dimension (get from first embedding)
    first_word = positive[0] if positive else negative[0]
    first_emb = get_embedding(first_word, model)
    result = np.zeros_like(first_emb)
    
    for word in positive:
        emb = get_embedding(word, model)
        result += emb
        if verbose:
            print(f"  + {word}")
    
    for word in negative:
        emb = get_embedding(word, model)
        result -= emb
        if verbose:
            print(f"  - {word}")
    
    # Normalize
    result = result / np.linalg.norm(result)
    
    return result


def test_analogy(
    a: str, b: str, c: str,
    candidates: List[str],
    model: str = None,
    top_k: int = 5
) -> List[Tuple[str, float]]:
    """
    Test analogy: a is to b as c is to ?
    
    Example: "king" is to "queen" as "man" is to ?
    → woman
    
    This computes: c + (b - a)
    """
    model = model or CONFIG.rag.default_embed_model
    
    print(f"\n{'='*60}")
    print(f"Analogy: '{a}' is to '{b}' as '{c}' is to ?")
    print(f"{'='*60}")
    
    # Compute: c + (b - a)
    result = embedding_arithmetic(
        positive=[c, b],
        negative=[a],
        model=model,
        verbose=True
    )
    
    # Find closest candidates
    print(f"\nSearching for closest matches...")
    matches = find_closest_words(
        result,
        candidates,
        model,
        top_k=top_k,
        exclude=[a, b, c]
    )
    
    print(f"\nTop {top_k} matches:")
    for i, (word, score) in enumerate(matches, 1):
        bar = "█" * int(score * 50)
        print(f"  {i}. {word:20s} {score:.4f} {bar}")
    
    return matches


# Predefined test cases
CLASSIC_ANALOGIES = [
    {
        "name": "King-Queen-Man-Woman",
        "a": "king",
        "b": "queen", 
        "c": "man",
        "expected": "woman",
        "candidates": ["woman", "girl", "lady", "female", "boy", "prince", "princess", "child"]
    },
    {
        "name": "Paris-France-Rome-Italy",
        "a": "paris",
        "b": "france",
        "c": "rome", 
        "expected": "italy",
        "candidates": ["italy", "spain", "germany", "england", "greece", "milan", "venice", "florence"]
    },
    {
        "name": "Good-Better-Bad-Worse",
        "a": "good",
        "b": "better",
        "c": "bad",
        "expected": "worse",
        "candidates": ["worse", "worst", "terrible", "awful", "poor", "great", "excellent", "best"]
    },
    {
        "name": "Walk-Walking-Swim-Swimming",
        "a": "walk",
        "b": "walking",
        "c": "swim",
        "expected": "swimming",
        "candidates": ["swimming", "swam", "swims", "walker", "running", "runner", "jumped", "jumping"]
    },
    {
        "name": "Dog-Puppy-Cat-Kitten",
        "a": "dog",
        "b": "puppy",
        "c": "cat",
        "expected": "kitten",
        "candidates": ["kitten", "kitty", "feline", "pet", "meow", "puppy", "doggy", "animal"]
    }
]


TECH_ANALOGIES = [
    {
        "name": "Python-Django-JavaScript-Framework",
        "a": "python",
        "b": "django",
        "c": "javascript",
        "expected": "react",
        "candidates": ["react", "vue", "angular", "node", "express", "flask", "rails", "spring"]
    },
    {
        "name": "CPU-Intel-GPU-NVIDIA",
        "a": "cpu",
        "b": "intel",
        "c": "gpu",
        "expected": "nvidia",
        "candidates": ["nvidia", "amd", "qualcomm", "arm", "apple", "samsung", "geforce", "radeon"]
    },
    {
        "name": "Code-GitHub-Design-Figma",
        "a": "code",
        "b": "github",
        "c": "design",
        "expected": "figma",
        "candidates": ["figma", "sketch", "adobe", "canva", "gitlab", "bitbucket", "photoshop", "illustrator"]
    }
]


BUSINESS_ANALOGIES = [
    {
        "name": "CEO-Company-President-Country",
        "a": "ceo",
        "b": "company",
        "c": "president",
        "expected": "country",
        "candidates": ["country", "nation", "government", "state", "business", "corporation", "firm", "organization"]
    },
    {
        "name": "Product-Engineer-Marketing-Marketer",
        "a": "product",
        "b": "engineer",
        "c": "marketing",
        "expected": "marketer",
        "candidates": ["marketer", "designer", "analyst", "manager", "developer", "specialist", "expert", "consultant"]
    }
]


def run_test_suite(model: str = None, category: str = "all"):
    """Run a suite of analogy tests"""
    model = model or CONFIG.rag.default_embed_model
    
    print(f"\n{'='*60}")
    print(f"EMBEDDING ARITHMETIC TEST SUITE")
    print(f"Model: {model}")
    print(f"{'='*60}")
    
    # Select test cases
    if category == "classic":
        tests = CLASSIC_ANALOGIES
    elif category == "tech":
        tests = TECH_ANALOGIES
    elif category == "business":
        tests = BUSINESS_ANALOGIES
    elif category == "all":
        tests = CLASSIC_ANALOGIES + TECH_ANALOGIES + BUSINESS_ANALOGIES
    else:
        print(f"Unknown category: {category}")
        return
    
    results = []
    
    for test in tests:
        matches = test_analogy(
            a=test["a"],
            b=test["b"],
            c=test["c"],
            candidates=test["candidates"],
            model=model,
            top_k=5
        )
        
        # Check if expected answer is in top matches
        expected = test["expected"]
        top_words = [w for w, _ in matches]
        
        if expected in top_words:
            rank = top_words.index(expected) + 1
            status = "✓ PASS"
            color = "\033[92m"  # Green
        else:
            rank = None
            status = "✗ FAIL"
            color = "\033[91m"  # Red
        
        print(f"\n{color}[{status}]\033[0m Expected: '{expected}'" + 
              (f" (ranked #{rank})" if rank else " (not in top 5)"))
        
        results.append({
            "name": test["name"],
            "expected": expected,
            "actual": top_words[0],
            "rank": rank,
            "passed": rank is not None
        })
        
        print("\n" + "-"*60)
    
    # Summary
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    accuracy = passed / total * 100
    
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Accuracy: {accuracy:.1f}%")
    print()
    
    # Show failed tests
    failed = [r for r in results if not r["passed"]]
    if failed:
        print("\nFailed tests:")
        for r in failed:
            print(f"  ✗ {r['name']}")
            print(f"    Expected: {r['expected']}, Got: {r['actual']}")


def interactive_mode(model: str = None):
    """Interactive exploration of embeddings"""
    model = model or CONFIG.rag.default_embed_model
    
    print(f"\n{'='*60}")
    print(f"INTERACTIVE EMBEDDING ARITHMETIC")
    print(f"Model: {model}")
    print(f"{'='*60}")
    print("\nEnter arithmetic operations on words.")
    print("Format: word1 + word2 - word3")
    print("Example: king + woman - man")
    print("\nType 'quit' to exit.\n")
    
    while True:
        try:
            expr = input(">>> ").strip()
            
            if expr.lower() in ['quit', 'exit', 'q']:
                break
            
            if not expr:
                continue
            
            # Parse expression
            positive = []
            negative = []
            
            # Simple parser: split by + and -
            current = ""
            current_sign = "+"
            
            for char in expr + " ":
                if char in ['+', '-']:
                    word = current.strip()
                    if word:
                        if current_sign == '+':
                            positive.append(word)
                        else:
                            negative.append(word)
                    current = ""
                    current_sign = char
                elif char != ' ' or current:
                    current += char
            
            if not positive:
                print("Error: Need at least one positive term")
                continue
            
            # Compute result
            result = embedding_arithmetic(positive, negative, model, verbose=False)
            
            # Show formula
            pos_str = " + ".join(positive)
            neg_str = " - ".join(negative) if negative else ""
            formula = f"{pos_str} {('- ' + neg_str) if neg_str else ''}"
            print(f"\nComputed: {formula}")
            
            # Find similar words
            print("\nEnter candidate words (comma-separated) or press Enter for common words:")
            candidates_input = input("Candidates: ").strip()
            
            if candidates_input:
                candidates = [w.strip() for w in candidates_input.split(',')]
            else:
                # Use a default word list
                candidates = [
                    "king", "queen", "man", "woman", "boy", "girl",
                    "prince", "princess", "duke", "duchess",
                    "emperor", "empress", "lord", "lady",
                    "father", "mother", "son", "daughter",
                    "brother", "sister", "husband", "wife"
                ]
            
            matches = find_closest_words(
                result,
                candidates,
                model,
                top_k=10,
                exclude=positive + negative
            )
            
            print("\nClosest matches:")
            for i, (word, score) in enumerate(matches, 1):
                bar = "█" * int(score * 50)
                print(f"  {i}. {word:20s} {score:.4f} {bar}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue


def main():
    parser = argparse.ArgumentParser(
        description="Explore embedding arithmetic and analogies"
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Embedding model to use (default: from config)"
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Interactive mode"
    )
    parser.add_argument(
        "--category",
        choices=["all", "classic", "tech", "business"],
        default="all",
        help="Test category to run"
    )
    parser.add_argument(
        "--custom",
        nargs=4,
        metavar=("A", "B", "C", "CANDIDATES"),
        help="Custom analogy: A is to B as C is to ? (candidates comma-separated)"
    )
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode(args.model)
    elif args.custom:
        a, b, c, candidates_str = args.custom
        candidates = [w.strip() for w in candidates_str.split(',')]
        test_analogy(a, b, c, candidates, args.model)
    else:
        run_test_suite(args.model, args.category)


if __name__ == "__main__":
    main()
