# Method References for the Prototype Upgrade

This document summarizes the references used for the upgraded benchmark and
analysis methods. The original baseline models are kept as comparison
references, but they are not presented as paper reproductions.

## Project Story

The first version was a master's coursework baseline built from common
machine-learning practice and public example learning. It included simple
baseline models, a tree-ensemble reference, validation metrics, and a first
Streamlit app.

The later version added reference-supported upgrade methods. Those upgrades
include boosted-tree comparisons, training-only resampling, threshold and cost
analysis, imbalanced metric framing, and permutation-importance artifacts.

The goal is comparison and decision-support storytelling, not paper
reproduction.

## Baseline Group

The baseline group is kept to make the benchmark honest:

- Dummy Majority Baseline
- Logistic Regression + PCA Baseline
- Random Forest Reference

These models came from the original coursework baseline and general public
example learning. They are comparison references, not paper-reproduction
models.

How to read the group:

- Dummy Majority shows why accuracy alone can be misleading.
- Logistic Regression + PCA gives a simple linear baseline.
- Random Forest Reference is the original tree-ensemble comparison model.
- No formal paper reproduction claim is made for this group.

## Upgrade Method References

### XGBoost Cost-Sensitive

Reference:

- Tianqi Chen and Carlos Guestrin, [XGBoost: A Scalable Tree Boosting System](https://www.kdd.org/kdd2016/papers/files/rfp0697-chenAemb.pdf), KDD 2016. DOI: [10.1145/2939672.2939785](https://doi.org/10.1145/2939672.2939785).

Method summary:

XGBoost is a gradient boosted tree method designed for strong tabular
prediction workflows.

Project application:

The project uses XGBoost Cost-Sensitive as an imbalance-aware boosted-tree
comparison with class weighting. It is not a reproduction of the XGBoost paper
and not a research-leading performance claim.

### LightGBM Class-Weighted

Reference:

- Guolin Ke, Qi Meng, Thomas Finley, Taifeng Wang, Wei Chen, Weidong Ma, Qiwei Ye, and Tie-Yan Liu, [LightGBM: A Highly Efficient Gradient Boosting Decision Tree](https://papers.nips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html), NeurIPS 2017.

Method summary:

LightGBM is an efficient gradient boosting decision tree method. It is useful
as a second boosted-tree family for comparison.

Project application:

The project keeps LightGBM Class-Weighted as a secondary boosted-tree
comparison. It is included for method coverage, not because it is the strongest
result in this project.

### XGBoost + Training-only SMOTE

Reference:

- N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, [SMOTE: Synthetic Minority Over-sampling Technique](https://www.jair.org/index.php/jair/article/view/10302), Journal of Artificial Intelligence Research, 16, 321-357, 2002.

Method summary:

SMOTE creates synthetic minority-class examples for training. Synthetic rows are
not real manufacturing observations.

Project application:

This comparison combines the XGBoost method family listed above with
training-only SMOTE. Resampling happens after splitting and only on the
training data. Validation and test rows are not resampled.

## Evaluation and Analysis References

### Cost-Sensitive Threshold Framing

Reference:

- Charles Elkan, [The Foundations of Cost-Sensitive Learning](https://dl.acm.org/doi/10.5555/1642194.1642224), IJCAI 2001. Additional metadata: [DBLP](https://dblp.org/rec/conf/ijcai/Elkan01). Author PDF: [The Foundations of Cost-Sensitive Learning](https://cseweb.ucsd.edu/~elkan/rescale.pdf).

Method summary:

Cost-sensitive learning treats different error types as having different
penalties.

Project application:

The project uses illustrative false-negative and false-positive cost scenarios.
False negatives are missed fail cases. False positives are pass cases flagged
for review. These costs are not validated manufacturing costs and are not
production rules.

### Imbalanced Classification Metrics

Reference:

- Takaya Saito and Marc Rehmsmeier, [The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432), PLOS ONE, 10(3), e0118432, 2015.

Method summary:

Precision-recall views are helpful for rare positive classes because they focus
on positive-class performance.

Project application:

The project emphasizes recall, precision, F2, PR-AUC, balanced accuracy,
confusion counts, and flagged sample rate. Accuracy alone is not enough for the
rare fail class.

### Permutation Importance and Model-Important Sensor Signals

Reference:

- Aaron Fisher, Cynthia Rudin, and Francesca Dominici, [All Models are Wrong, but Many are Useful: Learning a Variable's Importance by Studying an Entire Class of Prediction Models Simultaneously](https://jmlr.org/papers/v20/18-760.html), Journal of Machine Learning Research, 20(177), 1-81, 2019.

Method summary:

Permutation importance estimates how much model performance changes when a
feature is disrupted. It helps describe model reliance on input variables.

Project application:

The project uses permutation importance and feature stability to identify
model-important sensor signals for Random Forest Reference and XGBoost
Cost-Sensitive. The SECOM sensor names are anonymous. These outputs support
investigation, but they are not physical root-cause analysis and not causal
proof.

## Scope Boundaries

- No paper reproduction.
- No research-leading performance claim.
- No final champion model claim.
- No production decision rule.
- No physical root-cause claim.
- No causal explanation claim.
