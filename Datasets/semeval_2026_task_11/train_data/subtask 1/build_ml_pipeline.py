import json
import numpy as np
import pandas as pd
import spacy
from sentence_transformers import SentenceTransformer

# 1. Initialize models
print("Loading spaCy and SentenceTransformer (this may take a moment)...")
nlp = spacy.load('en_core_web_sm')
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Load Dataset
with open('train_data.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Hardcoded structural configuration rules from Phase 2 & 4
NEGATION_TOKENS = {'no', 'not', 'none', 'never', 'nothing', 'neither', 'cannot', 'separate'}
PARTICULAR_TOKENS = {'some', 'portion', 'number', 'least', 'few', 'many', 'certain', 'subset'}
UNIVERSAL_TOKENS = {'all', 'every', 'everything', 'anything', 'each', 'any', 'without'}

def get_quantifier_type(sentence_text):
    lowered = sentence_text.lower().strip()
    words = [w.strip(",.?!\"()").lower() for w in lowered.split()]
    if not words: return 0 # Unknown/Empty
    has_neg = any(t in words or t in lowered for t in NEGATION_TOKENS)
    
    if words[0] in {'no', 'nothing', 'neither', 'none'} or ("not a single" in lowered): return 2 # NO
    if has_neg and any(t in set(words[:4]) for t in UNIVERSAL_TOKENS): return 2 # NO
    if "separate categories" in lowered or "do not belong" in lowered: return 2 # NO
    if any(t in words for t in PARTICULAR_TOKENS): return 3 # SOME
    if any(t in words for t in UNIVERSAL_TOKENS) or not has_neg: return 1 # ALL
    return 2

def get_tree_depth(spacy_sent):
    def walk(node, depth):
        if not list(node.children): return depth
        return max(walk(child, depth + 1) for child in node.children)
    roots = [t for t in spacy_sent if t.head == t]
    return max(walk(r, 1) for r in roots) if roots else 1

# 3. Feature Extraction Loop
processed_rows = []

print(f"Extracting features from {len(raw_data)} syllogisms...")
for idx, item in enumerate(raw_data):
    text = item['syllogism']
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    if len(sentences) < 3: continue
    
    p1, p2, c = sentences[0], sentences[1], sentences[2]
    
    # --- SYNTACTIC FEATURES ---
    doc_text = nlp(text)
    doc_sents = list(doc_text.sents)
    depths = [get_tree_depth(s) for s in doc_sents]
    
    feature_row = {
        'label': 1 if item['validity'] else 0,
        'believability': 1 if item['plausibility'] else 0,
        'sentence_length_total': len(text.split()),
        'clause_count': text.count(',') + text.count(';'),
        'avg_parse_depth': np.mean(depths) if depths else 0,
        'max_parse_depth': np.max(depths) if depths else 0,
    }
    
    # --- LOGICAL STRUCTURE FEATURES ---
    q1 = get_quantifier_type(p1)
    q2 = get_quantifier_type(p2)
    qc = get_quantifier_type(c)
    feature_row['q1_type'] = q1
    feature_row['q2_type'] = q2
    feature_row['qc_type'] = qc
    
    # Negation counts and positioning
    w_p1 = [w.strip(",.?!").lower() for w in p1.split()]
    w_p2 = [w.strip(",.?!").lower() for w in p2.split()]
    w_c = [w.strip(",.?!").lower() for w in c.split()]
    
    feature_row['p1_negations'] = sum(1 for w in w_p1 if w in NEGATION_TOKENS)
    feature_row['p2_negations'] = sum(1 for w in w_p2 if w in NEGATION_TOKENS)
    feature_row['c_negations'] = sum(1 for w in w_c if w in NEGATION_TOKENS)
    feature_row['total_negations'] = feature_row['p1_negations'] + feature_row['p2_negations'] + feature_row['c_negations']

    # --- CONTENT & SEMANTIC FEATURES ---
    # Jaccard Overlap
    stop_words = NEGATION_TOKENS | PARTICULAR_TOKENS | UNIVERSAL_TOKENS | {'are', 'is', 'a', 'an', 'the', 'that', 'of', 'to', 'be', 'also'}
    p_words = (set(w_p1) | set(w_p2)) - stop_words
    c_words = set(w_c) - stop_words
    intersection = p_words & c_words
    union = p_words | c_words
    feature_row['lexical_overlap'] = len(intersection) / len(union) if union else 0
    
    # Entity Frequency
    feature_row['entity_freq_p1'] = len(p_words)
    feature_row['entity_freq_c'] = len(c_words)

    # Semantic Embedding Similarity (Premises vs Conclusion)
    p_emb = embedding_model.encode(p1 + " " + p2)
    c_emb = embedding_model.encode(c)
    feature_row['semantic_similarity'] = np.dot(p_emb, c_emb) / (np.linalg.norm(p_emb) * np.linalg.norm(c_emb))
    
    # Save raw clean text for TF-IDF tracking
    feature_row['raw_text'] = text
    
    processed_rows.append(feature_row)

df = pd.DataFrame(processed_rows)
df.to_csv('extracted_features.csv', index=False)
print("="*60)
print(f" SUCCESS: Feature Matrix Exported to 'extracted_features.csv'")
print(f" Matrix Shape: {df.shape[0]} samples x {df.shape[1]} columns")
print("="*60)