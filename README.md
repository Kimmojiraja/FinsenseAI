### 1. FINSENSEAI
## FinSenseAI – Intelligent Financial Transaction Categorization & Insight Engine
This section introduces the official name of the project.
FinSenseAI is a hybrid AI-powered system designed to automatically understand and categorize raw financial transaction text into meaningful spending categories. The title reflects the system’s core capabilities — financial intelligence, automated understanding, and smart insights.

### 2. Short Description
FinSenseAI is an intelligent hybrid system that automatically categorizes raw financial transaction texts into meaningful spending categories using a combination of Deep Learning (Transformer-based model) and a customizable Rule Engine. It simplifies unstructured banking messages, supports bulk CSV processing, generates smart insights, and provides analytics through an intuitive Streamlit interface. The system is designed for real-world use in fintech apps, digital banks, budgeting tools, and expense management platforms.

### 3. Features
FinSenseAI includes a comprehensive set of functionalities designed to deliver accurate categorization, seamless user experience, and meaningful financial insights:

• Single Transaction Categorization
Automatically predicts the category of any raw financial transaction text using a hybrid AI + rule-based pipeline.
• Bulk CSV Processing
Allows users to upload entire transaction files and receive fully categorized outputs along with summary analytics.

• Customizable Rule Engine
Supports merchant-based and keyword-based rules that override model predictions, enabling user-specific personalization.
• Transformer-Based Deep Learning Model
A fine-tuned text classification model trained on realistic financial transaction patterns for high accuracy.
• Smart Insights Generator
Detects unusual spending trends, top categories, and weekly/monthly behavioral patterns using statistical analysis.
• Analytics Dashboard
Provides category-wise distribution, monthly trends, merchant analysis, and spending patterns using interactive charts.
• Feedback Loop for Continuous Improvement
Captures user corrections and stores them for further model retraining to improve accuracy over time.
• Version Tracking & Changelog System
Maintains model version, dataset version, and system updates for auditability and production readiness.
• Modern Streamlit UI
Dark-themed, visually appealing interface with intuitive navigation and user-friendly controls.

### 4. Architecture 
The architecture of FinSenseAI is designed as a hybrid pipeline that ensures high accuracy, personalization, and explainability. The system operates across three primary layers:

• Layer 1: Deep Learning Model (Transformer Classifier)
Processes the raw transaction text, extracts embeddings, and predicts the most probable spending category along with confidence and explanation.

• Layer 2: Rule-Based Engine
Applies merchant-based and keyword-based rules defined by the user. This layer overrides model predictions to ensure personalization and user control.

• Layer 3: Application Layer (Streamlit UI)
Handles all user interactions including single transaction input, bulk processing, analytics visualization, insight generation, feedback logging, and version tracking.
Together, these layers create a seamless workflow where a transaction is cleaned, analyzed, categorized, and visualized with full transparency.

### 5. How to Run the Code
## Follow the steps below to set up and run FinSenseAI on your local machine.

Prerquisites
Before starting, ensure that you have:
Python 3.8+ installed
pip package manager
Git (optional but recommended)
A terminal/command prompt

# Step 1: Clone the Repository

If you have Git installed:
git clone https://github.com/<your-username>/FinSenseAI.git
cd FinSenseAI
If not, simply download the ZIP from GitHub and extract it.

# Step 2: Install Required Python Libraries

Install all dependencies from requirements.txt:
pip install -r requirements.txt
This will install:
Streamlit
Transformers
Pandas
Scikit-learn
Matplotlib / Seaborn
Other utility libraries

# Step 3: Run the Streamlit Application

Execute the command:
streamlit run app.py
This will open the FinSenseAI interface in your browser automatically.

# Step 4: Using the Application

Once the app launches:

Home Page
Enter a raw transaction text
View category, confidence, and explanation
Bulk Upload
Upload CSV files containing transactions
Download the categorized output
Analytics
View charts of category trends, spending insights, merchant analysis
Smart Insights
Read auto-generated spending insights
User Preferences
Add merchant rules
Add keyword rules
Changelog
Track system versions and improvements

### 6. Demo Video Link

A detailed walkthrough video demonstrating the complete functionality of FinSenseAI—including single transaction categorization, bulk upload processing, analytics dashboard, rule engine, and smart insights—is available below:
google drive link : https://drive.google.com/file/d/1ad1LWe0GURP7IPRynvuoIeF6S9y-W-Cm/view?usp=sharing

### 7. Team Members (Optional)
This project was independently developed and implemented by:

👤 Kimmoji Raja

Project Developer – Model Design, Rule Engine, UI/UX, Analytics, and Documentation

As a solo contributor, all aspects of the project—including architecture design, coding, testing, and report preparation—were handled individually.
