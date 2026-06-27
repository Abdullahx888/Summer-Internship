import json
import collections

# 1. Load the dataset
file_path = 'train_data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define clean standalone structural triggers
NEGATION_TOKENS = {'no', 'not', 'none', 'never', 'nothing', 'neither', 'cannot', 'separate'}
PARTICULAR_TOKENS = {'some', 'portion', 'number', 'least', 'few', 'many', 'certain', 'subset'}
UNIVERSAL_TOKENS = {'all', 'every', 'everything', 'anything', 'each', 'any', 'without'}

def generalize_quantifier(sentence_text):
    lowered = sentence_text.lower().strip()
    
    # Clean up common introductory fluff found in conclusions
    fluff_phrases = [
        "based on this, it must be the case that", 
        "it follows that", 
        "the only logical conclusion is that",
        "consequently,", "therefore,"
    ]
    for fluff in fluff_phrases:
        if lowered.startswith(fluff):
            lowered = lowered[len(fluff):].strip()
            
    # Tokenize the sentence to look at individual words
    words = [w.strip(",.?!\"()").lower() for w in lowered.split()]
    if not words:
        return 'unknown'
        
    # Check for explicit negation indicators across the sentence
    has_negation = any(t in words or t in lowered for t in NEGATION_TOKENS)
    
    # Look at the leading words to determine quantity intent
    first_few_words = set(words[:4])
    
    # 1. LOGICAL NO (Universal Negative)
    # Starts with a negative word, OR is a universal statement containing a negation
    if words[0] in {'no', 'nothing', 'neither', 'none'} or ("not a single" in lowered):
        return 'no'
    if has_negation and any(t in first_few_words for t in UNIVERSAL_TOKENS):
        return 'no'
    if "separate categories" in lowered or "do not belong" in lowered:
        return 'no'

    # 2. LOGICAL SOME (Particular / Existential)
    # Checks if any particular descriptor appears near the front or middle
    if any(t in words for t in PARTICULAR_TOKENS):
        return 'some'
        
    # 3. LOGICAL ALL (Universal Affirmative)
    # Default state for natural nouns (e.g., "Meteors are...", "A house is...") if no particular/negation tokens exist
    if any(t in words for t in UNIVERSAL_TOKENS):
        return 'all'
    
    # If a sentence starts with a standard noun phrase (like "Meteors are...", "A house is...")
    # and has no partial quantities or negations, it is structurally a universal statement (ALL).
    if not has_negation:
        return 'all'
    else:
        # If it has a negation but no explicit particular keyword, it falls into "Some are not" or "No"
        # E.g., "Automobiles are not cars" -> Universal statement denied -> NO
        return 'no'

# 2. Storage structures for statistics
premise_quantifiers = []
conclusion_quantifiers = []
quantifier_combinations = []

negation_counts = {'total_premises': 0, 'total_conclusions': 0, 'multiple_negations_cases': 0}

# 3. Run the robust generalized pipeline
for item in data:
    text = item['syllogism']
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    if len(sentences) >= 3:
        p1, p2, c = sentences[0], sentences[1], sentences[2]
        
        q_p1 = generalize_quantifier(p1)
        q_p2 = generalize_quantifier(p2)
        q_c = generalize_quantifier(c)
        
        # Simple token match negation counter
        def count_neg(s):
            w_list = [w.strip(",.?!\"()").lower() for w in s.lower().split()]
            return sum(1 for w in w_list if w in NEGATION_TOKENS)
            
        neg_p1, neg_p2, neg_c = count_neg(p1), count_neg(p2), count_neg(c)
        
        premise_quantifiers.extend([q_p1, q_p2])
        conclusion_quantifiers.append(q_c)
        quantifier_combinations.append(f"{q_p1} + {q_p2} -> {q_c}")
        
        negation_counts['total_premises'] += (neg_p1 + neg_p2)
        negation_counts['total_conclusions'] += neg_c
        if (neg_p1 > 1) or (neg_p2 > 1) or (neg_c > 1) or ((neg_p1 + neg_p2 + neg_c) > 2):
            negation_counts['multiple_negations_cases'] += 1

# 4. Aggregations
p_dist = collections.Counter(premise_quantifiers)
c_dist = collections.Counter(conclusion_quantifiers)
combo_dist = collections.Counter(quantifier_combinations)

print("="*60)
print("     PHASE 2: GENERALIZED NON-OVERFITTING RESULTS     ")
print("="*60)
print(f"Premises:   {dict(p_dist)}")
print(f"Conclusions: {dict(c_dist)}")
print(f"Top Layouts: {combo_dist.most_common(3)}")
print("="*60)
import random

# Pick 5 random samples from your data to audit
random.seed(42)  # Set seed so it's reproducible
sample_audit = random.sample(data, 5)

print("="*70)
print("             PHASE 2 VISUAL AUDIT CHECK                         ")
print("="*70)
for i, item in enumerate(sample_audit, 1):
    text = item['syllogism']
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    p1, p2, c = sentences[0], sentences[1], sentences[2]
    
    # Run our generalized parser on them
    q_p1 = generalize_quantifier(p1)
    q_p2 = generalize_quantifier(p2)
    q_c = generalize_quantifier(c)
    
    print(f"Sample #{i}:")
    print(f"  Text: {text}")
    print(f"  Code Parsed Structure:  [{q_p1.upper()}] + [{q_p2.upper()}] -> [{q_c.upper()}]")
    print("-" * 70)