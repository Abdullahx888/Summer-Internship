import json

# 1. Load data
with open('train_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

jaccard_scores = []

# List of common structural filler words to ignore so we only look at real entities
stop_words = {
    'all', 'every', 'everything', 'anything', 'each', 'any', 'without', 'exception',
    'some', 'portion', 'number', 'least', 'few', 'many', 'certain', 'subset', 'there', 'exists', 'exist',
    'no', 'not', 'none', 'never', 'nothing', 'neither', 'cannot', 'separate', 'categories', 'belong', 'same', 'group',
    'are', 'is', 'a', 'an', 'the', 'that', 'of', 'to', 'be', 'also', 'it', 'follows', 'this', 'proves', 'hence', 'consequently', 'therefore'
}

for item in data:
    text = item['syllogism']
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    if len(sentences) >= 3:
        p1_words = set([w.strip(",.?!\"()").lower() for w in sentences[0].split()])
        p2_words = set([w.strip(",.?!\"()").lower() for w in sentences[1].split()])
        c_words = set([w.strip(",.?!\"()").lower() for w in sentences[2].split()])
        
        # Combine premise words and remove structural fluff words
        premises_content_words = (p1_words | p2_words) - stop_words
        conclusion_content_words = c_words - stop_words
        
        if not premises_content_words or not conclusion_content_words:
            continue
            
        # Compute Jaccard Similarity: Intersection / Union
        intersection = premises_content_words & conclusion_content_words
        union = premises_content_words | conclusion_content_words
        jaccard = len(intersection) / len(union)
        jaccard_scores.append(jaccard)

print("="*65)
print("          PHASE 4: LEXICAL OVERLAP ANALYSIS REPORT             ")
print("="*65)
print(f"Average Jaccard Similarity between Premises & Conclusions: {sum(jaccard_scores)/len(jaccard_scores):.4f}")
print(f"Max Overlap Score: {max(jaccard_scores):.2f} | Min Overlap Score: {min(jaccard_scores):.2f}")
print("="*65)
print("What this means for the report:")
print("A high Jaccard score tells us if the conclusion is heavily reusing terms")
print("from the premises, which helps answer if models can exploit simple word-matching heuristics.")
print("="*65)