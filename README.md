# SentinelLog AI: Hybrid Log Analysis Dashboard

SentinelLog AI is a powerful, real-time log analysis platform that combines deterministic security rules with advanced AI insights to detect and respond to threats efficiently. Designed for security operations centers (SOCs) and IT administrators, this dashboard provides a comprehensive overview of log data, flags suspicious activities, and offers intelligent remediation suggestions.

## Approach: Hybrid Rules + AI

Our unique approach integrates two core components:

1.  **Deterministic Rules Engine**: Identifies well-known security patterns such as brute force attacks, geo-shift anomalies, and privilege escalation attempts based on predefined, high-confidence rules.
2.  **AI Insights Engine (Groq/Llama 3.1)**: Leverages the speed and intelligence of Groq with the Llama 3.1-8b-instant model to provide concise, actionable summaries and mitigation steps for detected alerts. This prevents generic recommendations and focuses on specific threats within your environment.

## Tech Stack

*   **Frontend**: Streamlit (for interactive web dashboard)
*   **Backend Logic**: Python
*   **Data Handling**: Pandas (for efficient log parsing and manipulation)
*   **Visualization**: Plotly (for dynamic and interactive charts)
*   **AI Integration**: Groq API (with Llama 3.1-8b-instant model) for fast, intelligent threat analysis.

## Setup Instructions

1.  **Clone the Repository**:
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd SentinelLog AI
    ```

2.  **Create and Activate a Virtual Environment** (recommended):
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Groq API Key**:
    *   Obtain a Groq API key from [Groq Cloud](https://console.groq.com/keys).
    *   Create a `.env` file in the root directory of the project:
        ```
        GROQ_API_KEY=gsk_YOUR_ACTUAL_GROQ_API_KEY_HERE
        ```

5.  **Run the Application**:
    ```bash
    streamlit run src/app.py
    ```

6.  **Upload Sample Logs**:
    *   In the Streamlit sidebar, use the file uploader to select `data/sample_logs.csv`.
    *   Navigate to the "AI Insights" tab and click "Generate AI Insights" to see the AI-powered threat summary.

## Project Status

This project is currently in its initial development phase, focusing on establishing a robust hybrid analysis framework. Future enhancements will include more sophisticated parsing rules, additional AI models, and real-time data streaming capabilities.
