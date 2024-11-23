# Why Accuracy Fails for Skewed Datasets

In datasets with imbalanced classes (e.g., rare diseases), accuracy can be misleading:
* Example: If 0.5% of patients have a disease, a model predicting "no disease" (y = 0) for all patients achieves **99.5% accuracy** without being useful.
* Accuracy alone does not reveal how well the model identifies the minority class (y = 1).

---

# Alternative Metrics: Precision and Recall

To evaluate models on imbalanced datasets, use **precision** and **recall**, derived from a **confusion matrix**.

### Confusion Matrix

| **Predicted** | **y = 1** | **y = 0** |
| ---           | ---       | ---       |
| **y = 1**     | TP        | FP        |
| **y = 0**     | FN        | TN        |

- **Rows**: Predicted classes (y = 1, y = 0)
- **Columns**: Actual classes (y = 1, y = 0)
- Four outcomes:
  * **True Positive (TP)**: Predicted y = 1, Actual y = 1 (correctly predicted positives)
  * **True Negative (TN)**: Predicted y = 0, Actual y = 0 (correctly predicted negatives)
  * **False Positive (FP)**: Predicted y = 1, Actual y = 0 (incorrectly predicted positives)
  * **False Negative (FN)**: Predicted y = 0, Actual y = 1 (missed actual positives)

---

### Precision

**Definition**: Of all predicted positives (y = 1), what fraction are correct?

Formula:

$$
\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}
$$

**Interpretation**: Measures how accurate the positive predictions are.
  * Example: \( \text{Precision} = 0.75 \) means 75% of predicted positives are correct.

---

### Recall

**Definition**: Of all actual positives (y = 1), what fraction are correctly predicted?

Formula:

$$
\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}
$$

**Interpretation**: Measures how many actual positives are detected.
  * Example: \( \text{Recall} = 0.6 \) means 60% of actual positives are identified.

---

### Example Calculation

Given a confusion matrix:

| **Actual**     | **Positive (1)** | **Negative (0)** |
| -------------- | ---------------- | ---------------- |
| **Predicted 1**| 15 (TP)          | 5 (FP)           |
| **Predicted 0**| 10 (FN)          | 70 (TN)          |

- **Precision**: 
  $$
  \text{Precision} = \frac{15}{15 + 5} = 0.75 \quad (\text{75\%})
  $$

- **Recall**: 
  $$
  \text{Recall} = \frac{15}{15 + 10} = 0.6 \quad (\text{60\%})
  $$

---

### Why Precision and Recall are Useful

* They uncover issues missed by accuracy:
  * A model predicting y = 0 all the time achieves high accuracy but has zero recall.
  * Precision and recall reveal the trade-offs between predicting too few or too many positives.
* Models with low precision or recall are generally not useful.

---

### Conclusion

When dealing with imbalanced datasets, use **precision** and **recall** to evaluate your model. A good model should:

* Have high precision (accurate predictions for y = 1).
* Have high recall (detects a reasonable fraction of actual positives).

These metrics ensure the algorithm is both **accurate** and **useful** for the target task.
