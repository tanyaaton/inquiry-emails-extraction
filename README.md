# 📬 Yacht Insurance Inquiry Emails Web App 💌

This web application allows users to upload yacht insurance inquiry emails, extract and display relevant information, and export the data for further analysis. The app is built with Streamlit, using OpenAI’s language model for text analysis and processing, and is integrated with additional tools for document analysis and semantic search.

## Technologies Used
- **OpenAI (GPT-4)**: For natural language processing and data extraction.
- **Tavily**: For internet browsing.
- **Pandas**: For managing and displaying extracted data.
- **Streamlit**: For the web application interface.

## Setup and Installation
### Prerequisites
Ensure you have Python installed on your machine (version 3.8 or later).

### Installation Steps
1. **Clone the Repository**:
   ```bash
   git clone github.com/tanyaaton/inquiry-emails-extraction
   cd inquiry-emails-extraction
   ```

2. **Install Dependencies**:
   Install all required packages from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Create a `.env` file in the root directory and set up the following variables:
   - OpenAI sign up [here](https://platform.openai.com/signup)
   - Tavily sign up [here](https://tavily.com/)
   ```env
   OPENAI_API_KEY=your_openai_key
   TAVILY_API_KEY=your_tavily_key
   ```

5. **Run the App**:
   Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Features
- **Upload and Process Emails**: Upload emails for content extraction.
- **Automated Information Extraction**: Uses an LLM model to extract key information fields.
- **Auto Fill Information**: Leverages the Tavily agent to conduct internet searches and automatically fill the not provided data (e.g., yacht specifications, insurance requirements, and regional data).
- **Visibility Toggle**: Select which customer data to display in the main view.
- **Data Export**: Download the processed data as a CSV file.
- **Persistent Storage**: Data is stored within the app's session state for easy access during the session.

## For more information
- 🔗 [Notion link](https://habitual-cabin-851.notion.site/Yacht-Insurance-Inquiry-Emails-13895ef893b2801c8119f0f808f71ca0) 
- 🎥 [Demo VDO](https://drive.google.com/file/d/1lHJ80mMHpHA9xnd9QKVAI2xrrEVf_U1K/view?usp=drive_link)
