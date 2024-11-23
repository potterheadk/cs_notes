# Introduction: Regression Trees

Decision trees can go beyond just classifying categories (like "cat" vs "dog") to predicting **numerical values**! When a decision tree is generalized for **regression**, it predicts **continuous values** like weight, price, or temperature based on input features.

## Understanding Regression Trees

A **regression tree** predicts a **continuous output** \( Y \) based on input features \( X \). For example, given features like ear shape and face shape, a regression tree could predict the **weight** of an animal. 

- The tree makes predictions by **averaging** the values of the target (output) for all the examples that reach a given leaf node.
- At each leaf node, the tree gives the **average** value of the target variable for all the data points that ended up in that node.

### Example: Predicting Weight
Suppose we use a regression tree to predict an animal’s weight. At a leaf node, the tree might predict the **average weight** of all animals that reached that node.

---

## Choosing Features for Splitting

In a regression tree, **splitting** is based on how much it can **reduce the variance** of the target \( Y \), not entropy as in classification trees.

- **Variance** measures the spread of the target variable. High variance means the values are widely spread out; low variance means the values are close together.
- The goal is to **reduce variance** at each split. If splitting on a particular feature results in subsets with lower variance, then that feature is chosen for the split.

### Formula for Variance
Given a set of data points \( X = \{x_1, x_2, ..., x_n\} \), the variance \( \sigma^2 \) is calculated as:

$$
\sigma^2 = \frac{1}{n} \sum_{i=1}^{n} (x_i - \bar{x})^2
$$

Where:
- \( x_i \) is each data point.
- \( \bar{x} \) is the mean of the data points.

### Information Gain in Regression
The **best feature** to split on is the one that **reduces the variance the most**. The amount of reduction in variance after a split is called **reduction in variance** (or "information gain" in regression trees).

---

## Recursive Splitting Process

Once a feature is selected for a split, the process is **repeated recursively** on the resulting subsets. This continues until a stopping condition is met, such as:

- Reaching a **maximum depth** for the tree.
- Having a **minimum number of data points** in each node.

### How the Tree Grows
1. At each node, the algorithm picks the feature that results in the **biggest reduction in variance**.
2. The data is split based on that feature.
3. The process is repeated for each new subset of data until a stopping criterion is reached.

---

## Summary: Regression Trees in Action

Regression trees are powerful tools for predicting **continuous values**. Instead of classifying into categories, the tree predicts a numeric value by averaging the data points in each leaf node. 

Key differences from classification trees:
- **Splitting criterion**: **Variance reduction** instead of entropy reduction.
- **Prediction**: The predicted value at each leaf node is the **average** of the target values in that node.

By recursively splitting the data based on features that reduce variance the most, regression trees can handle complex prediction tasks and provide valuable insights for numerical data.

