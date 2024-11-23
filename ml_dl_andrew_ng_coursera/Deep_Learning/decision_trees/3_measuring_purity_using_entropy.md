### 1. Measuring Purity Using Entropy

Entropy quantifies the impurity of a dataset.

- **If all examples belong to the same class:** Entropy = 0 (pure dataset).
- **If the dataset is a 50-50 mix of two classes:** Entropy = 1 (maximum impurity).

#### Formula for Entropy:

For a dataset with:

- \( p_1 \): Fraction of positive examples (label = 1).
- \( p_0 \): Fraction of negative examples (label = 0, where \( p_0 = 1 - p_1 \)).

The entropy is:

$$
H(p_1) = -p_1 \log_2(p_1) - (1 - p_1) \log_2(1 - p_1)
$$

- **Convention:** Logs are taken to base 2, making the peak value of entropy = 1.
- If \( p_1 = 0 \) or \( p_1 = 1 \), the term \( 0 \log_2(0) \) is defined as 0 for practical computation.

#### Key Observations:

- Entropy is **highest** when \( p_1 = 0.5 \).
- Entropy **decreases** as the dataset becomes more pure.

---

### 2. Information Gain and Feature Selection

**Goal:** Choose the feature to split on that maximizes the reduction in entropy (or impurity). This reduction is called **Information Gain (IG)**.

#### Steps to Compute IG:

1. **Initial Entropy (Root Node):**  
    Calculate entropy at the root node using all examples.
    
2. **Weighted Average Entropy (After Split):**  
    If splitting on a feature creates left and right branches:
    
    -  $$ w^{\text{left}} : Fraction of examples in the left branch.$$
    - $$ w^{\text{right}}: Fraction of examples in the right branch.$$
    
    Weighted entropy after the split:
    
    $$
    H_{\text{weighted}} = w^{\text{left}} \cdot H(p_1^{\text{left}}) + w^{\text{right}} \cdot H(p_1^{\text{right}})
    $$

3. **Information Gain Formula:**
    
    $$
    IG = H(p_1^{\text{root}}) - H_{\text{weighted}}
    $$

    **Choose the feature** with the highest IG to split the node.
    

#### Example:

For three possible features to split on:

1. Calculate entropy for left and right branches for each feature.
2. Compute the weighted average entropy.
3. Calculate IG for each feature and select the one with the highest IG.

---

### 3. Practical Considerations

- If the **IG is too small**, stop splitting to avoid overfitting.
- Other impurity measures like the **Gini Index** can be used, but entropy is commonly preferred.

---

### Summary of the Decision Tree Algorithm:

1. Start at the root node and calculate entropy.
    
2. For each feature:
    
    - Compute the entropy reduction (IG) after splitting.
    - Select the feature with the highest IG.

3. Repeat recursively for child nodes until stopping criteria are met (e.g., no IG or max depth).
    

This approach ensures that at each step, the decision tree moves toward increasing the purity of subsets, ultimately creating a structured tree for decision-making.

---


