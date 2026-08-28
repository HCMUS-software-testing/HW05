# Certified Tester AI Testing (CT-AI) Syllabus
**Version 1.0 (2021-10-01)**  
**International Software Testing Qualifications Board (ISTQB®)**

---

## Table of Contents

- [0. Introduction](#0-introduction)
- [1. Introduction to AI](#1-introduction-to-ai)
- [2. Quality Characteristics for AI-Based Systems](#2-quality-characteristics-for-ai-based-systems)
- [3. Machine Learning (ML) – Overview](#3-machine-learning-ml--overview)
- [4. ML - Data](#4-ml---data)
- [5. ML Functional Performance Metrics](#5-ml-functional-performance-metrics)
- [6. ML - Neural Networks and Testing](#6-ml---neural-networks-and-testing)
- [7. Testing AI-Based Systems Overview](#7-testing-ai-based-systems-overview)
- [8. Testing AI-Specific Quality Characteristics](#8-testing-ai-specific-quality-characteristics)
- [9. Methods and Techniques for Testing AI-Based Systems](#9-methods-and-techniques-for-testing-ai-based-systems)
- [10. Test Environments for AI-Based Systems](#10-test-environments-for-ai-based-systems)
- [11. Using AI for Testing](#11-using-ai-for-testing)
- [12. References (Standards, ISTQB Documents, Books, Articles)](#12-references)
- [13. Appendix A – Abbreviations](#13-appendix-a--abbreviations)
- [14. Appendix B – AI Specific and Other Terms (Glossary)](#14-appendix-b--ai-specific-and-other-terms)

---

## 0. Introduction

### 0.1 Purpose of this Syllabus
This syllabus forms the basis for the ISTQB® Certified Tester AI Testing. It provides learning objectives, knowledge areas, and practical competencies for testing AI-based systems and using AI for testing activities.

### 0.2 Cognitive Levels of Knowledge
- **K1 (Remember)**: Recognize, remember, or recall a keyword or concept.
- **K2 (Understand)**: Explain, summarize, compare, or give examples of concepts.
- **K3 (Apply)**: Carry out or use a procedure or technique in a given scenario.
- **K4 (Analyze)**: Break down information, distinguish relationships, or evaluate alternatives.

### 0.3 Hands-on Levels of Competency
- **H0**: Live demo of an exercise or recorded video.
- **H1**: Guided exercise with step-by-step instructions.
- **H2**: Exercise with hints for individual/group problem solving.

---

## 1. Introduction to AI

### 1.1 Definition of AI and AI Effect
- **Artificial Intelligence (AI)**: The capability of an engineered system to acquire, process, create and apply knowledge and skills (ISO/IEC TR 29119-11).
- **AI Effect**: The phenomenon where a system is no longer considered "AI" once the technology becomes common or its internal logic is fully understood (e.g., Deep Blue chess algorithms, rule-based expert systems).

### 1.2 Categories of AI
- **Narrow AI (Weak AI)**: Programmed for a specific, well-defined task with limited context (e.g., spam filters, voice assistants, test generators).
- **General AI (Strong AI)**: Displays human-like general cognitive abilities, reasoning across diverse domains.
- **Super AI**: Far exceeds human cognitive capabilities with massive processing power, unlimited memory, and web-scale knowledge (technological singularity).

### 1.3 AI-Based vs. Conventional Systems
- **Conventional Systems**: Programmed using imperative logic (`if-else`, loops). The transformation from input to output is explicitly designed and traceable.
- **AI-Based Systems (ML)**: Learn patterns from data to deduce decision logic, resulting in non-transparent or probabilistic decision-making.

### 1.4 AI Technologies & Frameworks
- **Technologies**: Fuzzy logic, search algorithms, reasoning engines (deductive classifiers, case-based reasoning), Machine Learning (neural networks, decision trees, SVM, random forests, clustering).
- **Frameworks**: TensorFlow, PyTorch, Scikit-learn, Keras, Apache MxNet, CNTK, IBM Watson Studio.

### 1.5 Hardware for AI
- High parallel processing & low-precision arithmetic (8-bit vs 32-bit): GPUs, Google TPUs, Edge TPUs, ASICs, SoCs, Neuromorphic processors.

### 1.6 AI as a Service (AIaaS) & Pre-Trained Models
- **AIaaS**: Cloud-hosted AI models (e.g., AWS Rekognition, Azure Cognitive Search, IBM Watson Assistant). SLAs typically cover uptime and security, but rarely guarantee ML accuracy.
- **Pre-Trained Models & Transfer Learning**: Reusing base feature layers (e.g., ImageNet, BERT) and fine-tuning top layers on specific datasets.

---

## 2. Quality Characteristics for AI-Based Systems

- **Flexibility & Adaptability**: Handling scenarios outside initial requirements and modifying behavior for changing hardware/environments.
- **Autonomy**: Operating independently without human intervention; defining boundaries for ceding control back to humans.
- **Evolution**: Managing self-learning and adaptation to prevent undesirable drift or reward hacking.
- **Bias**: Algorithmic bias (model parameters/hyperparameters) vs. Sample bias (unrepresentative training data).
- **Ethics**: Fairness, inclusivity, transparency, privacy, and OECD AI principles.
- **Side Effects & Reward Hacking**: Exploiting unintended loopholes to achieve reward goals (gaming the metric).
- **Explainable AI (XAI)**:
  - *Transparency*: Visibility into algorithms and training datasets.
  - *Interpretability*: Understandability of the AI mechanism by stakeholders.
  - *Explainability*: Ease of understanding why a specific prediction/output was made.
- **Safety**: Mitigating risks of harm in probabilistic and non-deterministic systems.

---

## 3. Machine Learning (ML) – Overview

### 3.1 Forms of ML
1. **Supervised Learning**: Training on labeled input-output pairs.
   - *Classification*: Categorical output (binary/multiclass).
   - *Regression*: Continuous numerical output.
2. **Unsupervised Learning**: Discovering intrinsic patterns in unlabeled data.
   - *Clustering*: Grouping similar data points.
   - *Association*: Discovering co-occurrence rules.
3. **Reinforcement Learning (RL)**: Agent interacts with an environment, learning optimal policy via rewards and penalties.

### 3.2 ML Workflow
```mermaid
flowchart LR
    A[Objectives] --> B[Framework] --> C[Data Prep] --> D[Train Model] --> E[Evaluate & Tune] --> F[Test Model] --> G[Deploy] --> H[Monitor & Drift]
```

### 3.3 Overfitting & Underfitting
- **Overfitting**: Model memorizes noise/outliers in training data; fails to generalize to new data.
- **Underfitting**: Model is too simplistic to capture underlying patterns.

---

## 4. ML - Data

### 4.1 Data Preparation Pipeline
- **Data Acquisition**: Identification, gathering, labeling.
- **Data Pre-processing**: Cleaning (handling missing data, outliers), Transformation (normalization, standardization), Augmentation, Sampling.
- **Feature Engineering**: Feature selection (eliminating irrelevant attributes) and Feature extraction (deriving compact informative representations).
- **Exploratory Data Analysis (EDA)**: Interactive exploration and visualization to discover data properties.

### 4.2 Dataset Splitting
- **Training Dataset**: Used to fit model weights.
- **Validation Dataset**: Used for hyperparameter tuning and model selection.
- **Test Dataset (Holdout)**: Unseen dataset used strictly for final evaluation. (Typical ratios: 60:20:20 or 80:10:10).

---

## 5. ML Functional Performance Metrics

### 5.1 Confusion Matrix Metrics (Classification)
$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$
$$\text{Precision} = \frac{TP}{TP + FP}$$
$$\text{Recall (Sensitivity)} = \frac{TP}{TP + FN}$$
$$F_1\text{-score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

### 5.2 Regression & Clustering Metrics
- **Regression**: Mean Squared Error (MSE), $R^2$ (Coefficient of Determination).
- **Clustering**: Intra-cluster distance, Inter-cluster distance, Silhouette Coefficient ($-1$ to $+1$).

---

## 6. ML - Neural Networks and Testing

- **Architecture**: Input layer, hidden layers (nodes/neurons), output layer, connection weights, biases, and activation functions.
- **Coverage Measures for Neural Networks**:
  - *Neuron Coverage*: Proportion of neurons whose activation exceeds 0.
  - *Threshold Coverage*: Proportion of neurons exceeding a threshold (e.g., 0.75 in DeepXplore).
  - *Sign-Change & Value-Change Coverage*: Exercising polarity and magnitude shifts.
  - *Sign-Sign Coverage*: Pairs of neurons in adjacent layers changing signs (analogous to MC/DC).

---

## 7. Testing AI-Based Systems Overview

### 7.1 Testing Challenges & Test Oracle Problem
- Incomplete specifications and probabilistic behavior make defining exact expected results difficult.

### 7.2 Test Levels
1. **Input Data Testing**: Reviewing datasets, EDA, testing the data pipeline.
2. **ML Model Testing**: Evaluating functional performance metrics, non-functional criteria, and white-box coverage.
3. **Component Testing**: Testing surrounding conventional software components.
4. **Component Integration Testing**: Verifying data pipeline and API interactions with the model.
5. **System Testing**: End-to-end testing in representative environments (including adversarial attacks, explainability).
6. **Acceptance Testing**: Validating against user business goals and SLAs.

### 7.3 Automation Bias & Concept Drift
- **Automation Bias**: Humans uncritically accepting AI recommendations or neglecting to monitor semi-autonomous systems.
- **Concept Drift**: Degradation of model accuracy over time due to shifts in the real-world operational environment.

---

## 8. Testing AI-Specific Quality Characteristics

- **Testing Self-Learning & Autonomy**: Establishing operational envelopes, boundary value analysis for human intervention triggers.
- **Testing for Bias**: Independent bias-free validation datasets, subgroup metrics comparison.
- **Explainability Testing**: Applying model-agnostic tools like LIME (Local Interpretable Model-agnostic Explanations) to observe perturbation effects.
- **Test Oracles**: Resolving the test oracle problem using pseudo-oracles, differential testing, and Metamorphic Testing.

---

## 9. Methods and Techniques for Testing AI-Based Systems

### 9.1 Adversarial Attacks & Data Poisoning
- **Adversarial Attacks**: Subtly perturbed inputs (adversarial examples) designed to trigger misclassification. Tested via white-box or black-box adversarial fuzzing.
- **Data Poisoning**: Malicious manipulation of training data (backdoors, corrupted labels). Detected via EDA and anomaly detection.

### 9.2 Combinatorial & Pairwise Testing
- Systematic testing of parameter combinations to maximize fault detection with minimal test suite size.

### 9.3 Back-to-Back (Differential) Testing
- Comparing the outputs of the SUT against an alternative implementation or pseudo-oracle.

### 9.4 A/B Testing
- Statistical comparison of two variants (A vs. B) in production or staging to validate improvements or detect regressions.

### 9.5 Metamorphic Testing (MT)
- Generating follow-up test cases based on **Metamorphic Relations (MR)** when a direct test oracle is unavailable:
  $$\text{If } f(x) = y \implies f(2x) = 2y$$

### 9.6 Experience-Based Testing & Google ML Test Checklist
- **Exploratory Testing Tours**: Data tours, underfitting/overfitting tours.
- **Google ML Test Score**: 28 automated assertions covering ML Data, Model Development, Infrastructure, and Monitoring.

---

## 10. Test Environments for AI-Based Systems

- **Virtual Test Environments**: Simulating dangerous, rare, extreme, or time-intensive operational scenarios.
- **Simulation Platforms**:
  - *Morse*: Robot simulation on Blender engine.
  - *AI Habitat*: 3D embodied agent simulation (Facebook AI).
  - *NVIDIA DRIVE Constellation*: Scalable cloud simulation for autonomous driving.
  - *MATLAB & Simulink*: Synthetic data generation and model-in-the-loop simulation.

---

## 11. Using AI for Testing

1. **Defect Analysis & Triage**: NLP-based clustering of bug reports, duplicate detection, automated assignment.
2. **AI-Driven Test Case Generation**: Generating input sequences and maximize coverage (e.g., Sapienz).
3. **Regression Test Suite Optimization**: Prioritizing test cases based on code churn and defect history.
4. **Defect Prediction**: Machine learning models predicting high-risk components based on organizational and code metrics.
5. **UI & Visual Testing**: Image recognition and AI-based locators to reduce brittleness of GUI test automation.

---

## 12. References

### 12.1 Standards [S]
- `[S01]` **ISO/IEC TR 29119-11:2020**: Guidelines on the testing of AI-based systems.
- `[S02]` **DIN SPEC 92001-1**: AI Quality Meta Model.
- `[S03]` **DIN SPEC 92001-2**: AI Technical and Organizational Requirements.
- `[S04]` **ISO 26262**: Road vehicles – Functional safety.
- `[S05]` **ISO/PAS 21448 (SOTIF)**: Safety of the intended functionality.
- `[S06]` **ISO/IEC 25010:2011**: Systems and software Quality Requirements and Evaluation (SQuaRE).
- `[S07]` **ISO 26262-6:2018**: Product development at the software level.
- `[S08]` **ISO/IEC/IEEE 29119-4:2015**: Software testing – Part 4: Test techniques.

### 12.2 ISTQB® Documents [I]
- `[I01]` ISTQB® Certified Tester Foundation Level Syllabus (CTFL).
- `[I02]` ISTQB® Certified Tester Advanced Level Test Analyst Syllabus (CTAL-TA).
- `[I03]` ISTQB® Certified Tester AI Testing Overview (CT-AI).

---

## 13. Appendix A – Abbreviations

| Abbreviation | Full Term |
|---|---|
| **AI** | Artificial Intelligence |
| **AIaaS** | AI as a Service |
| **API** | Application Programming Interface |
| **AUC** | Area Under Curve |
| **DL** | Deep Learning |
| **DNN** | Deep Neural Network |
| **EDA** | Exploratory Data Analysis |
| **FN / FP** | False Negative / False Positive |
| **GDPR** | General Data Protection Regulation |
| **GPU / TPU** | Graphical Processing Unit / Tensor Processing Unit |
| **GUI** | Graphical User Interface |
| **LIME** | Local Interpretable Model-Agnostic Explanations |
| **MC/DC** | Modified Condition / Decision Coverage |
| **ML** | Machine Learning |
| **MR / MT** | Metamorphic Relation / Metamorphic Testing |
| **MSE** | Mean Square Error |
| **NLP** | Natural Language Processing |
| **ROC** | Receiver Operating Characteristic |
| **SUT** | System Under Test |
| **SVM** | Support Vector Machine |
| **TN / TP** | True Negative / True Positive |
| **XAI** | Explainable AI |

---

## 14. Appendix B – AI Specific and Other Terms (Glossary)

- **Accuracy**: Proportion of correct predictions among total predictions.
- **Activation Function**: Non-linear function in a neuron determining its activation value based on weighted inputs and bias.
- **Adversarial Example**: Intentionally perturbed input designed to cause model misclassification.
- **Algorithmic Bias**: Systematic distortion introduced by model hyperparameters or optimization algorithms.
- **Automation Bias**: Tendency of human operators to unthinkingly trust automated decisions.
- **Concept Drift**: Degradation of model accuracy over time due to changing real-world operational distributions.
- **Ground Truth**: The verified, real-world fact/measurement used as the standard of truth.
- **Metamorphic Relation (MR)**: The necessary relationship between inputs and outputs across multiple test runs.
- **Overfitting**: When a model fits training noise too closely and fails to generalize to unseen data.
- **Test Oracle Problem**: The challenge of determining the correct expected output for a given test input.
- **Transfer Learning**: Reusing representations learned from a source task to accelerate learning on a target task.
