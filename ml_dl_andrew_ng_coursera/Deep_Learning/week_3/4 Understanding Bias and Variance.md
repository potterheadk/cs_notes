
![[C2_W3_BiasVariance.png]]

- **High Bias**: The model is too simple, doesn’t capture patterns well, and has high errors on both training and validation data (underfits).
- **High Variance**: The model is too complex, fits training data well but fails on new data due to capturing noise (overfits).
### Diagnosing Issues

- **High Bias**: High training error signals underfitting.
- **High Variance**: A big gap between training and validation errors suggests overfitting.

### Finding the Right Balance

- Aim for a model with low errors on both training and validation sets. This means the model is complex enough to capture patterns but not too complex to fit noise.

------

### Understanding Regularization and Lambda

- **High Lambda** (e.g., 10,000): Strong regularization, parameters stay small, causing **high bias** and **underfitting** (model is too simple).
- **Low Lambda** (e.g., 0): Weak regularization, model fits training data closely, leading to **high variance** and **overfitting**.

### Choosing the Best Lambda

- Use cross-validation to test different Lambda values.
- Look for a balanced Lambda that keeps both training and validation errors low, avoiding both underfitting and overfitting.

### Error Trends with Lambda

- As Lambda grows, **training error** increases (model fits less).
- **Validation error** forms a U-shape: too low or too high Lambda worsens performance, with an optimal value in between.

( In this context, "worsens performance" means that the model's accuracy or effectiveness decreases. Specifically:

- **When Lambda is too low**: The model may overfit, performing well on training data but poorly on new data (high variance).
- **When Lambda is too high**: The model may underfit, failing to capture patterns in the data (high bias).

So, with either extreme (too low or too high Lambda), the model performs poorly on new or cross-validation data, reducing its general effectiveness or "performance." )


----


### Evaluating Errors

- **Training Error**: The percentage of mistakes the model makes on training data. Example: 10.8% error = 89.2% accuracy.
- **Cross-Validation Error**: Measured on unseen data. If this is much higher than the training error, it suggests **high variance** (overfitting).

### Using Human Performance as a Benchmark

- Human error (e.g., 10.6%) sets a baseline to compare your model. If the training error is close to human error, the model is likely doing well.

### Diagnosing Bias and Variance

- **High Bias**: Large gap between training error and human-level performance (underfitting).
- **High Variance**: Large gap between training and cross-validation errors (overfitting).
- **Both Issues**: Both gaps exist, requiring improvements to address both underfitting and overfitting.


----


### Learning Curves Simplified:
- **What They Show**: Learning curves plot training and cross-validation errors against training set size.  
  - **Cross-Validation Error**: Decreases with more data (better generalization).  
  - **Training Error**: Increases slightly with more data (harder to fit all examples perfectly).

### Diagnosing Bias and Variance:
- **High Bias**: Both errors are high and plateau, more data won’t help (underfitting).  
- **High Variance**: Big gap between training and validation errors; more data can help reduce overfitting.

### Why It Matters:
- Learning curves help decide whether to collect more data or adjust the model to improve performance.

----


### Diagnosing Bias and Variance
- **High Bias**: The model struggles even on training data, underfitting. Solutions:
  - Add more features.
  - Add polynomial features (increase model complexity).
  - Decrease regularization (lower Lambda).

- **High Variance**: The model fits training data well but fails on new data, overfitting. Solutions:
  - Add more training examples.
  - Reduce the feature set (simplify the model).
  - Increase regularization (raise Lambda).

### Key Takeaway
- **High Bias** → Make the model more flexible.
- **High Variance** → Simplify or regularize the model.
  
Understanding and addressing bias and variance will improve your approach to model tuning, a skill that deepens with practice.

---


Here’s a simple summary of how neural networks handle bias and variance:

### Addressing Bias and Variance in Neural Networks
- **Bias-Variance Tradeoff**: Traditional machine learning requires a balance between bias (underfitting) and variance (overfitting) by adjusting model complexity and regularization. With neural networks, this approach changes.
  
- **Neural Networks and High Bias**: If your neural network isn’t performing well on training data (indicating high bias), increasing the network size (more layers or units) can improve accuracy without sacrificing too much on the bias-variance balance, as long as the training data set isn’t too massive.

- **High Variance and Large Data**: If your model has high variance (performing well on training but poorly on validation), adding more data can help. The power of neural networks combined with large datasets often allows you to overcome the tradeoff, achieving both low bias and variance.

- **Regularization**: For large neural networks, regularization (like L2) is crucial to avoid overfitting. Appropriately regularized large networks can outperform smaller ones while still generalizing well.

### Key Takeaways
1. **Large Neural Networks**: Generally improve model performance if regularized correctly, although they may slow down training.
2. **Bias-Variance Adjustment**: In deep learning, tuning network size and adding data often replace the need for strict bias-variance balancing, allowing better overall results.