import json
import numpy as np

# 1. Load the dataset
file_path = 'train_data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Basic counters
num_samples = len(data)

# Count label distribution (validity)
valid_count = sum(1 for item in data if item['validity'] is True)
invalid_count = sum(1 for item in data if item['validity'] is False)

# 3. Text Parsing Arrays
premise_1_word_counts = []
premise_2_word_counts = []
conclusion_word_counts = []
all_words = []

for item in data:
    text = item['syllogism']
    
    # Split by sentences (handling standard spacing after the periods)
    # Most samples follow the 3-sentence structure perfectly
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    if len(sentences) >= 3:
        p1 = sentences[0]
        p2 = sentences[1]
        c = sentences[2]
        
        # Calculate word counts (splitting by spaces)
        p1_len = len(p1.split())
        p2_len = len(p2.split())
        c_len = len(c.split())
        
        premise_1_word_counts.append(p1_len)
        premise_2_word_counts.append(p2_len)
        conclusion_word_counts.append(c_len)
        
        # Collect lowercase tokens for global vocabulary statistics
        for sentence in [p1, p2, c]:
            words = [word.strip(",.?!\"()").lower() for word in sentence.split()]
            all_words.extend(words)

# 4. Compute Vocabulary Statistics
unique_vocab = set(all_words)
total_vocabulary_size = len(unique_vocab)

# 5. Print out the structured results for Deliverable D2
print("="*50)
print("     PHASE 1: DATASET EXPLORATION RESULTS     ")
print("="*50)
print(f"Total Number of Samples: {num_samples}")
print(f"Label Distribution:")
print(f"  - Logically Valid (True):   {valid_count} ({valid_count/num_samples*100:.2f}%)")
print(f"  - Logically Invalid (False): {invalid_count} ({invalid_count/num_samples*100:.2f}%)")
print("-"*50)
print("Average Sentence Lengths (in words):")
print(f"  - Premise 1 Avg Length:     {np.mean(premise_1_word_counts):.2f} words")
print(f"  - Premise 2 Avg Length:     {np.mean(premise_2_word_counts):.2f} words")
print(f"  - Conclusion Avg Length:    {np.mean(conclusion_word_counts):.2f} words")
print("-"*50)
print(f"Total Unique Vocabulary Size: {total_vocabulary_size} unique words")
print("="*50)