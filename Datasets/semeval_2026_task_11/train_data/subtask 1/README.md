# SemEval 2026 Task 11: Subtask 1 Analysis

This directory contains the dataset and analysis scripts for **Subtask 1** of SemEval 2026 Task 11. The goal of this analysis is to explore the cognitive and logical properties of syllogistic statements, mapping the relationship between logical validity and real-world belief bias (plausibility).

---

## Directory Map

The analysis spans 4 distinct phases, divided across the following python scripts:

* **Dataset:** [train_data.json](file:///Users/home/Desktop/Internship/Datasets/semeval_2026_task_11/train_data/subtask%201/train_data.json) — The primary dataset consisting of 960 syllogistic logic items.
* **Phase 1: Basic Dataset Exploration** -> [basic_dataset_exploration.py](file:///Users/home/Desktop/Internship/Datasets/semeval_2026_task_11/train_data/subtask%201/basic_dataset_exploration.py)
* **Phase 2: Linguistic and Semantic Analysis** -> [linguistic_Sementic_analysis.py](file:///Users/home/Desktop/Internship/Datasets/semeval_2026_task_11/train_data/subtask%201/linguistic_Sementic_analysis.py) and [LexicalOverlap.py](file:///Users/home/Desktop/Internship/Datasets/semeval_2026_task_11/train_data/subtask%201/LexicalOverlap.py)
* **Phase 3: Believability Analysis (The Bias Matrix)** -> [BelievabilityMatrix.py](file:///Users/home/Desktop/Internship/Datasets/semeval_2026_task_11/train_data/subtask%201/BelievabilityMatrix.py)
* **Phase 4: Syntactic & Logical Form Analysis** -> [SyntacticNLPAnalysis.py](file:///Users/home/Desktop/Internship/Datasets/semeval_2026_task_11/train_data/subtask%201/SyntacticNLPAnalysis.py)

---

## Phase 1: Basic Dataset Exploration (The Easy Counters)

### Implementation

* **File:** [basic_dataset_exploration.py](file:///Users/home/Desktop/Internship/Datasets/semeval_2026_task_11/train_data/subtask%201/basic_dataset_exploration.py)
* **Functionality:**
  1. Loads the JSON database and counts total sample size.
  2. Calculates the distribution of logically valid (`validity: true`) vs. invalid (`validity: false`) structures.
  3. Splits each syllogism into individual sentences (Premise 1, Premise 2, and the Conclusion) based on terminal punctuation.
  4. Computes the average word counts of Premise 1, Premise 2, and the Conclusion.
  5. Aggregates words across the dataset to measure the total unique vocabulary size.

### Output

```text
==================================================
     PHASE 1: DATASET EXPLORATION RESULTS   
==================================================
Total Number of Samples: 960
Label Distribution:
  - Logically Valid (True):   480 (50.00%)
  - Logically Invalid (False): 480 (50.00%)
--------------------------------------------------
Average Sentence Lengths (in words):
  - Premise 1 Avg Length:     8.32 words
  - Premise 2 Avg Length:     7.92 words
  - Conclusion Avg Length:    8.93 words
--------------------------------------------------
Total Unique Vocabulary Size: 1141 unique words
==================================================
```

---

## Phase 2: Linguistic and Semantic Analysis (Keyword Tracking)

### Implementation

This phase investigates the exact phrasing of logical assertions and lexical overlap using two separate scripts:

#### 1. Quantifier & Negation Tracking

* **File:** [linguistic_Sementic_analysis.py](file:///Users/home/Desktop/Internship/Datasets/semeval_2026_task_11/train_data/subtask%201/linguistic_Sementic_analysis.py)
* **Functionality:**
  * **Quantifier Analysis:** Categorizes sentences based on their logical scope into:
    * `all` (Universal Affirmative): e.g., "All", "Every", "Each".
    * `no` (Universal Negative): e.g., "No", "None", "Neither".
    * `some` (Particular/Existential): e.g., "Some", "A portion of", "A number of".
  * **Negation Analysis:** Tracks occurrences of negation tokens (`no`, `not`, `none`, `never`, `nothing`, `neither`, `cannot`, `separate`) and flags arguments containing multiple negations.
  * **Visual Audit:** Performs a random sample analysis to test structural extraction logic.

#### 2. Vocabulary Overlap & Jaccard Similarity

* **File:** [LexicalOverlap.py](file:///Users/home/Desktop/Internship/Datasets/semeval_2026_task_11/train_data/subtask%201/LexicalOverlap.py)
* **Functionality:**
  * Filters out structural logical fluff and stop words (like *all*, *some*, *are*, *is*, *therefore*, *consequently*, etc.) to isolate the target concepts/nouns.
  * Computes the **Jaccard Similarity** between the set of unique words in the premises ($P_1 \cup P_2$) and the conclusion ($C$):
    $$
    \text{Jaccard Similarity} = \frac{|\text{Words in Premises} \cap \text{Words in Conclusion}|}{|\text{Words in Premises} \cup \text{Words in Conclusion}|}
    $$

### Outputs

#### Quantifier & Negation Report (`linguistic_Sementic_analysis.py`):

```text
============================================================
     PHASE 2 : Linguistic and Semantic Analysis (Keyword Tracking)   
============================================================
Premises:   {'all': 941, 'no': 599, 'some': 380}
Conclusions: {'no': 215, 'some': 559, 'all': 186}
Top Layouts: [('no + all -> some', 111), ('all + all -> all', 104), ('all + some -> some', 93)]
============================================================
======================================================================
             PHASE 2 VISUAL AUDIT CHECK                     
======================================================================
Sample #1:
  Text: There are no animals that are also plants. At least one tree is a plant. At least one tree is not an animal.
  Code Parsed Structure:  [NO] + [SOME] -> [SOME]
----------------------------------------------------------------------
Sample #2:
  Text: Every single bird is an animal. There are no animals that are minerals. This proves that some minerals are not birds.
  Code Parsed Structure:  [ALL] + [NO] -> [SOME]
----------------------------------------------------------------------
Sample #3:
  Text: There are some planets that are dogs. All things that are dogs are beings. Hence, it can be concluded that some beings are planets.
  Code Parsed Structure:  [SOME] + [ALL] -> [SOME]
----------------------------------------------------------------------
Sample #4:
  Text: Each and every star is a celestial body. There are some planets that are stars. Consequently, all planets are celestial bodies.
  Code Parsed Structure:  [ALL] + [SOME] -> [ALL]
----------------------------------------------------------------------
Sample #5:
  Text: Everything that is a cloud is also a reptile. Everything that is a cloud is also a fish. Hence, some fish are reptiles.
  Code Parsed Structure:  [ALL] + [ALL] -> [SOME]
----------------------------------------------------------------------
```

#### Lexical Overlap Report (`LexicalOverlap.py`):

```text
=================================================================
          PHASE 4: LEXICAL OVERLAP ANALYSIS REPORT         
=================================================================
Average Jaccard Similarity between Premises & Conclusions: 0.2317
Max Overlap Score: 1.00 | Min Overlap Score: 0.00
=================================================================
What this means for the report:
A high Jaccard score tells us if the conclusion is heavily reusing terms
from the premises, which helps answer if models can exploit simple word-matching heuristics.
=================================================================
```

---

## Phase 3: Believability Analysis (The Bias Matrix)

### Implementation

* **File:** [BelievabilityMatrix.py](file:///Users/home/Desktop/Internship/Datasets/semeval_2026_task_11/train_data/subtask%201/BelievabilityMatrix.py)
* **Functionality:**
  * Cross-references logical validity (`validity`) against real-world believability (`plausibility`) for all 960 samples.
  * Categorizes items into four distinct cognitive quadrants:
    1. **Believable Valid** (True, True): Logic is correct, and conclusion is facts-aligned. (Easy for models).
    2. **Believable Invalid** (False, True): Invalid reasoning, but conclusion sounds true. (The Belief Bias Trap).
    3. **Unbelievable Valid** (True, False): Correct logical reasoning, but conclusion is absurd in real-life. (Friction test for LLMs).
    4. **Unbelievable Invalid** (False, False): Broken logic and absurd conclusion. (Easy to reject).
  * Computes diagnostic statistics to answer Research Question 3 (RQ3): *Are invalid logic statements masked with plausible conclusions to trick models?*

### Bias Matrix Distribution

| Plausibility (Belief) \ Validity (Logic)                       |         Logically Valid (`validity: true`)         |      Logically Invalid (`validity: false`)      |
| :------------------------------------------------------------- | :---------------------------------------------------: | :------------------------------------------------: |
| **Plausible / Believable (`plausibility: true`)**      |    **Believable Valid**240 samples (25.00%)    | **Believable Invalid (Trap)**234 samples (24.38%) |
| **Implausible / Unbelievable (`plausibility: false`)** | **Unbelievable Valid (Friction)**240 samples (25.00%) | **Unbelievable Invalid**246 samples (25.62%) |

### Output

```text
=================================================================
       PHASE 3: BELIEVABILITY & BIAS MATRIX REPORT          
=================================================================
Total Dataset Samples Evaluated: 960
-----------------------------------------------------------------
QUADRANT BREAKDOWN:
  1. Believable + Logically Valid:    240 samples (25.00%)
  2. Believable + Logically Invalid:  234 samples (24.38%)
  3. Unbelievable + Logically Valid:  240 samples (25.00%)
  4. Unbelievable + Logically Invalid:246 samples (25.62%)
=================================================================

DIAGNOSTIC INSIGHTS FOR RQ3:
-----------------------------------------------------------------
Total Valid Structures: 480 | Total Invalid Structures: 480
Are 'Invalid' statements mostly coded as plausible to trap models?
  -> 48.75% of all invalid logic problems are masked with believable text!
=================================================================
```

---

## Phase 4: Syntactic & Logical Form Analysis (Advanced NLP)

### Implementation

* **File:** [SyntacticNLPAnalysis.py](file:///Users/home/Desktop/Internship/Datasets/semeval_2026_task_11/train_data/subtask%201/SyntacticNLPAnalysis.py)
* **Functionality:**
  * **Dependency Depth:** Integrates `spaCy` to construct sentence parse trees and calculates the maximum depth of grammatical branching.
  * **Syllogistic Figure Mood Tagging:** Maps structural quantifier patterns to classical Aristotelian Syllogistic moods (e.g. Barbara, Celarent, Darii, Ferio/Festino, Bramantip, etc.).

### Classical Syllogistic Forms Distribution

| Mood Name                     |   Quantifier Layout   | Existential / Validity Status     | Sample Count | Dataset % |
| :---------------------------- | :--------------------: | :-------------------------------- | :----------: | :-------: |
| **Felapton / Fesapo**   |  `no + all -> some`  | Valid with existential assumption |     111     |  11.56%  |
| **Barbara**             |  `all + all -> all`  | Valid                             |     104     |  10.83%  |
| **Darii**               | `all + some -> some` | Valid                             |      93      |   9.69%   |
| **Ferio / Festino**     | `no + some -> some` | Valid / Trap                      |      90      |   9.38%   |
| **Barbari / Bramantip** | `all + all -> some` | Valid with existential assumption |      86      |   8.96%   |

### Output

```text
Parsing 960 samples using spaCy parse-trees... (This might take a few seconds)
=================================================================
     PHASE 4: ADVANCED SYNTACTIC & LOGICAL FORM REPORT    
=================================================================
Average Grammatical Parse-Tree Depth: 4.29 levels deep
Max Sentence Tree Complexity Encountered: 9 levels
-----------------------------------------------------------------
TOP CLASSICAL SYLLOGISTIC FORMS DETECTED IN DATASET:
  - Felapton / Fesapo (Valid with existential assumption): 111 samples (11.56%)
  - Barbara (Valid): 104 samples (10.83%)
  - Darii (Valid): 93 samples (9.69%)
  - Ferio / Festino (Valid/Trap): 90 samples (9.38%)
  - Barbari / Bramantip (Valid with existential assumption): 86 samples (8.96%)
=================================================================
```

---

## Phase 5: Feature Engineering & ML Pipeline (Feature Extraction)

### Implementation
*   **File:** [build_ml_pipeline.py](file:///Users/home/Desktop/Internship/Datasets/semeval_2026_task_11/train_data/subtask%201/build_ml_pipeline.py)
*   **Functionality:** Processes the raw syllogism texts and maps them to a set of hand-engineered and embedding-based features spanning three core feature categories. The final processed spreadsheet is exported as `extracted_features.csv` (960 rows $\times$ 18 columns).

### Feature Categories Map
1.  **Content Features:**
    *   **Entity Embeddings:** Low-dimensional semantic vectors of the premises and conclusion.
    *   **Entity Frequency:** Count of unique, non-stop content entities inside the premises (`entity_freq_p1`) and conclusion (`entity_freq_c`).
    *   **Semantic Similarity:** Cosine similarity of the sentence embeddings for the combined premises vs. the conclusion, calculated using the `all-MiniLM-L6-v2` SentenceTransformer.
    *   **Believability Scores:** Mapped from the dataset's ground truth `plausibility` (1 for True, 0 for False).
    *   **Lexical Overlap:** Jaccard similarity score comparing content nouns between premises and conclusions.
2.  **Logical Structure Features:**
    *   **Quantifier Types:** Mapped to categorical numeric codes (1 for ALL, 2 for NO, 3 for SOME) for $P_1$, $P_2$, and $C$.
    *   **Quantifier Sequences:** Evaluated implicitly through sequence ordering of the categorical quantifier variables.
    *   **Negation Counts:** Total occurrences of negation indicators per premise (`p1_negations`, `p2_negations`) and conclusion (`c_negations`).
    *   **Negation Positions:** Extracted on a sentence-by-sentence level.
    *   **Syllogistic Form:** Synthesized categorical representation of premises and conclusion quantifiers.
    *   **Subject-Predicate Structure & Premise-Conclusion Mappings:** Represented through structured overlap metrics and directional similarity metrics.
3.  **Syntactic Features:**
    *   **Dependency Depth & Parse-tree Depth:** Computed using `spaCy` dependency tree parsing (`avg_parse_depth` and `max_parse_depth`).
    *   **Sentence Length:** Total word count of the entire syllogism.
    *   **Clause Count:** Calculated using punctuation flags (commas and semicolons).

---

## Phase 6: Machine Learning Models (Training Classifiers)

### Implementation
*   **File:** [train_models.py](file:///Users/home/Desktop/Internship/Datasets/semeval_2026_task_11/train_data/subtask%201/train_models.py)
*   **Functionality:** Employs three distinct modeling strategies to predict logical validity (`validity: true/false`). Standardizes all numerical features using `StandardScaler` to ensure classification stability.

### Modeling Strategies
*   **Strategy 1: Text-Only Baseline (TF-IDF -> SVM)**
    *   Extracts TF-IDF features (max 500 features) from raw syllogism strings.
    *   Trains a **Support Vector Machine (SVM)** classifier with a linear kernel as a traditional bag-of-words benchmark.
*   **Strategy 2: Linguistic Features Only**
    *   Uses only the engineered content, logical, and syntactic features from Phase 5.
    *   Trains a **Random Forest Classifier** and an **XGBoost Classifier**.
*   **Strategy 3: Hybrid ML Models**
    *   Combines the sparse TF-IDF text matrix and the standardized dense linguistic feature matrix (`np.hstack`).
    *   Trains a **Hybrid Logistic Regression** model and a **Hybrid XGBoost Classifier**.

---

## Phase 7: Final Performance Evaluation

### Evaluation Setup
The dataset is split into an 80/20 train/test split (768 training samples, 192 test samples) with a fixed random seed (`random_state=42`) to guarantee fair comparison.

### Performance Metrics Comparison

| Strategy | Classifier Model | Feature Set | Test Accuracy |
| :--- | :--- | :--- | :---: |
| **Strategy 1** | SVM | TF-IDF Text Baseline | 70.83% |
| **Strategy 2** | Random Forest | Linguistic Features Only | 85.42% |
| **Strategy 2** | XGBoost | Linguistic Features Only | 83.85% |
| **Strategy 3** | Logistic Regression | Hybrid (TF-IDF + Linguistics) | 74.48% |
| **Strategy 3** | XGBoost (Top Model) | Hybrid (TF-IDF + Linguistics) | **85.94%** |

### Top Model Analysis (Hybrid XGBoost)
The classification report for the top-performing **Hybrid XGBoost** model shows highly balanced precision and recall on the test set:

```text
              precision    recall  f1-score   support

 Invalid (0)       0.85      0.88      0.86        96
   Valid (1)       0.87      0.84      0.86        96

    accuracy                           0.86       192
   macro avg       0.86      0.86      0.86       192
weighted avg       0.86      0.86      0.86       192
```

### Analysis Summary
*   **Text-Only SVM** achieves a modest `70.83%` accuracy, illustrating that lexical content and word distribution alone are insufficient to solve formal deductive reasoning tasks.
*   **Linguistic-Only Random Forest** performs exceptionally well at `85.42%`, demonstrating that hand-engineered logical rules, negation metrics, and parse depths are strong signals for logical validity.
*   **Hybrid XGBoost** yields the highest accuracy of **`85.94%`**. Combining bag-of-words details with syntactic/logical structure features allows the tree-boosting algorithm to resolve edge-case semantic traps.

---

## Replication and Setup

To run these scripts and reproduce the findings:

1. Activate your virtual environment and make sure the required packages are installed:
   ```bash
   source venv/bin/activate
   pip install numpy spacy pandas scikit-learn xgboost sentence-transformers
   python -m spacy download en_core_web_sm
   ```
2. Execute the pipeline scripts:
   ```bash
   # Step 1: Basic and exploratory NLP reports (Phases 1-4)
   python basic_dataset_exploration.py
   python linguistic_Sementic_analysis.py
   python LexicalOverlap.py
   python BelievabilityMatrix.py
   python SyntacticNLPAnalysis.py
   
   # Step 2: Extract features & train classifiers (Phases 5-7)
   python build_ml_pipeline.py
   python train_models.py
   ```
