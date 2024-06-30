# Jedi Academy

New psychology graduates (aka "Psych Padawans") who are looking to start freelance psychotherapy struggle to build customer trust. This is because unlike other freelancers, their customers face real privacy concerns if they try to publicly detail the procedures/outcomes. This leaves them with one of 2 options:
- **Word of mouth**: doesnt scale as well beyond closed circles
- **Certifications**: too expensive and time consuming.

### Solution

The original models are trained on conversational datasets grounded by reddit descriptions of people from subreddits corresponding to relevant specializations like autism, narcissim and so on. This ensures the automatically score higher on assessment surveys.

For every specialization we re-run the fine-tune on conversation data generated from a subset of all recommendations and then allow psychotherapists to gauge session wise improvement in the model response on the assessment. This allows them to return to relevant checkpoints and try new approaches.

### Training Approach

![Architecture Diagram](https://github.com/never2average/jedi-academy/assets/31365087/8009f621-2dd8-49a3-88ec-0f963f82cc88)
*System Architecture*

#### 1. Data Collection and Specialization Selection
1.1. Identify relevant specializations in the field of study
1.2. Collect data from this torrent: magnet:?xt=urn:btih:32916ad30ce4c90ee4c47a95bd0075e44ac15dd2&dn=RC%5F2015-01.bz2&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969

#### 2. Persona Generation and Conversation Dataset Creation
2.1. Utilize Large Language Models (LLMs) to create grounded personas based on collected data
2.2. Generate multi-turn conversational datasets in the format: (persona_id, specialization, question, answer)

#### 3. Initial Model Fine-tuning
3.1. Select Mistral v0.3 7B as the base model
3.2. Employ Mistral fine-tuning API to train on the generated dataset

#### 4. Benchmark Data Acquisition
4.1. Extract relevant surveys from PubMed corresponding to each specialization
4.2. Establish baseline scores using these surveys

#### 5. Model Evaluation
5.1. Conduct before/after scoring using the established surveys
5.2. Analyze performance improvements and areas for further refinement

#### 6. Dataset Expansion
6.1. Incorporate real interaction data between the model and users
6.2. Generate additional conversations based on these interactions
6.3. Merge new data with the existing dataset

#### 7. Recommendation System Implementation
7.1. Develop an LLM-based preference system for recommendations
7.2. Implement a randomized accept/ignore mechanism based on LLM preferences

#### 8. Model Refinement
8.1. Re-run Mistral fine-tuning API on the expanded dataset
8.2. Point to the Mistral v0.3 7B model with new parameters

#### 9. Final Evaluation
9.1. Conduct another round of before/after scoring using the established surveys
9.2. Compare results with the initial evaluation to measure improvement

#### 10. Iterative Improvement
10.1. Analyze results and identify areas for further enhancement
10.2. Repeat steps 6-9 as necessary to continually improve the model's performance

# Repository Setup Instructions

## Backend Setup

1. **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2. **Create a virtual environment:**
    ```bash
    virtualenv venv
    ```
3. **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```
4. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
5. **Run the backend application:**
    ```bash
    python3 mainapi.py
    ```

## Frontend Setup

1. **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2. **Install the required packages:**
    ```bash
    npm i
    ```
3. **Start the frontend development server:**
    ```bash
    npm run dev
    ```

## Additional Notes

- Ensure you have `virtualenv` installed for setting up the Python virtual environment. If not, you can install it using:
    ```bash
    pip install virtualenv
    ```

- Make sure you have `npm` installed for managing the frontend dependencies. You can download and install Node.js (which includes `npm`) from the [official Node.js website](https://nodejs.org/).

- Always activate your virtual environment before running the backend server to ensure all dependencies are correctly loaded.

- For production deployment, consider using tools like `gunicorn` for the backend and `nginx` to serve the frontend and handle requests.

