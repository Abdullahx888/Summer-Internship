import json
import collections
import spacy

# 1. Load spaCy's English engine and the dataset
nlp = spacy.load('en_core_web_sm')

with open('train_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Dictionary to map quantifier patterns to classical Aristotelian Syllogism names
# These names represent standard configurations used in cognitive psychology reading lists
SYLLOGISM_NAMES = {
    'all + all -> all': 'Barbara (Valid)',
    'no + all -> no': 'Celarent (Valid)',
    'all + some -> some': 'Darii (Valid)',
    'no + some -> some': 'Ferio / Festino (Valid/Trap)',
    'all + all -> some': 'Barbari / Bramantip (Valid with existential assumption)',
    'no + all -> some': 'Felapton / Fesapo (Valid with existential assumption)',
    'some + all -> some': 'Disamis / Datisi (Valid)',
}

tree_depths = []
form_tags = []

# Helper function to compute the max depth of a spaCy grammatical parse tree
def get_parse_tree_depth(spacy_sentence):
    def walk_tree(node, depth):
        if not list(node.children):
            return depth
        return max(walk_tree(child, depth + 1) for child in node.children)
    
    # The root of the sentence is the main verb or anchor point
    roots = [token for token in spacy_sentence if token.head == token]
    if not roots:
        return 1
    return max(walk_tree(root, 1) for root in roots)

# Re-using your non-overfitting Phase 2 structural categorization logic
NEGATION_TOKENS = {'no', 'not', 'none', 'never', 'nothing', 'neither', 'cannot', 'separate'}
PARTICULAR_TOKENS = {'some', 'portion', 'number', 'least', 'few', 'many', 'certain', 'subset'}
UNIVERSAL_TOKENS = {'all', 'every', 'everything', 'anything', 'each', 'any', 'without'}

def get_structural_tag(sentence_text):
    lowered = sentence_text.lower().strip()
    fluff = ["based on this, it must be the case that", "it follows that", "the only logical conclusion is that", "consequently,", "therefore,"]
    for f in fluff:
        if lowered.startswith(f): lowered = lowered[len(f):].strip()
    words = [w.strip(",.?!\"()").lower() for w in lowered.split()]
    if not words: return 'unknown'
    
    has_negation = any(t in words or t in lowered for t in NEGATION_TOKENS)
    first_few = set(words[:4])
    
    if words[0] in {'no', 'nothing', 'neither', 'none'} or ("not a single" in lowered): return 'no'
    if has_negation and any(t in first_few for t in UNIVERSAL_TOKENS): return 'no'
    if "separate categories" in lowered or "do not belong" in lowered: return 'no'
    if any(t in words for t in PARTICULAR_TOKENS): return 'some'
    if any(t in words for t in UNIVERSAL_TOKENS) or not has_negation: return 'all'
    return 'no'

# 2. Process all samples through the NLP pipeline
print("Parsing 960 samples using spaCy parse-trees... (This might take a few seconds)")

for item in data:
    text = item['syllogism']
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    if len(sentences) >= 3:
        p1, p2, c = sentences[0], sentences[1], sentences[2]
        
        # Calculate Syntactic Parse Tree Depths
        doc = nlp(text)
        for sent in doc.sents:
            depth = get_parse_tree_depth(sent)
            tree_depths.append(depth)
            
        # Figure out the logical layout name
        q_p1 = get_structural_tag(p1)
        q_p2 = get_structural_tag(p2)
        q_c = get_structural_tag(c)
        
        layout_pattern = f"{q_p1} + {q_p2} -> {q_c}"
        classical_name = SYLLOGISM_NAMES.get(layout_pattern, f"Custom Mood [{layout_pattern}]")
        form_tags.append(classical_name)

# 3. Generate summaries
avg_complexity = sum(tree_depths) / len(tree_depths)
form_counts = collections.Counter(form_tags)

print("="*65)
print("     PHASE 4: ADVANCED SYNTACTIC & LOGICAL FORM REPORT        ")
print("="*65)
print(f"Average Grammatical Parse-Tree Depth: {avg_complexity:.2f} levels deep")
print(f"Max Sentence Tree Complexity Encountered: {max(tree_depths)} levels")
print("-"*65)
print("TOP CLASSICAL SYLLOGISTIC FORMS DETECTED IN DATASET:")
for form, count in form_counts.most_common(5):
    print(f"  - {form}: {count} samples ({count/len(data)*100:.2f}%)")
print("="*65)