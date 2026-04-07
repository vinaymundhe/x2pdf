```markdown
# X2PDF 📄

Convert your X (Twitter) posts into a beautifully organized PDF with AI-powered categorization and tweet generation.

## Features

✨ **AI-Powered Categorization** — Automatically organize tweets into categories (Software Development, Tech, Finance, Life Advice, Productivity, Other) using OpenAI GPT-4

📝 **Generate Similar Tweets** — Create new tweets in your writing style using AI analysis of your existing posts

📊 **Styled PDF Export** — Beautiful, organized PDF with your tweets grouped by category, timestamps, and professional formatting

🔐 **Secure Credentials** — Uses environment variables for safe API key management

## Prerequisites

- Python 3.8+
- Twitter Developer Account with API v2 access (attached to a Project)
- OpenAI API key

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/x2pdf.git
   cd x2pdf
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # Windows PowerShell
   source .venv/bin/activate    # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Setup

### Twitter API
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a **Project** and **App** within it
3. Generate a **Bearer Token** from the app's "Keys and tokens" section
4. Add to `.env`:
   ```
   BEARER_TOKEN=your_bearer_token_here
   ```

### OpenAI API
1. Get your API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. Add to `.env`:
   ```
   OPENAI_API_KEY=your_openai_key_here
   ```

### VS Code Configuration
Enable terminal environment file injection:
- Open Settings (`Ctrl+,`)
- Search for `python.terminal.useEnvFile`
- Enable the checkbox

## Usage

### Export tweets to PDF
```bash
python pipeline.py
```
This will:
1. Fetch your latest tweets from X
2. Categorize them using AI
3. Export to X2PDF.pdf

### Generate similar tweets
```python
from generate_posts import generate_similar_tweets
from fetch_tweets import get_tweets, get_user_id

username = "your_handle"
user_id = get_user_id(username)
tweets = get_tweets(user_id)
generated = generate_similar_tweets(tweets, count=5)

for tweet in generated:
    print(tweet)
```

## Project Structure

```
x2pdf/
├── fetch_tweets.py      # Twitter API integration
├── export_pdf.py        # PDF generation & AI categorization
├── generate_posts.py    # AI tweet generation
├── pipeline.py          # Main orchestration script
├── requirements.txt     # Python dependencies
├── .env                 # API keys (not in repo)
├── tweets.json          # Cached tweets
├── fonts/               # PDF fonts (OpenSans)
└── exports/             # Generated PDFs
```

## How It Works

1. **Fetch** — Retrieves tweets from Twitter API v2 with metadata
2. **Categorize** — Uses OpenAI to intelligently categorize each tweet
3. **Group** — Organizes tweets by category
4. **Export** — Generates a styled PDF with proper formatting and typography
5. **Generate** — Analyzes your writing style and creates similar tweets

## Configuration

Edit pipeline.py to change:
- **Twitter handle** — `username = "your_handle"`
- **Number of tweets** — `max_results` parameter in `get_tweets()`
- **PDF output path** — `out_path` parameter in `export_pdf()`

## Requirements

- `requests` — HTTP client for API calls
- `python-dotenv` — Environment variable management
- `fpdf2` — PDF generation
- `openai` — OpenAI API client
- `certifi` — SSL certificate verification

## Costs

- **Twitter API** — Free tier available
- **OpenAI** — ~$0.001-0.01 per tweet categorization; ~$0.05-0.15 per generated tweet (with GPT-4)

## Future Enhancements

- [ ] CLI interface with click/argparse
- [ ] Batch processing for multiple accounts
- [ ] Local LLM option (Ollama) for offline categorization
- [ ] Tweet engagement metrics in PDF
- [ ] Custom categorization rules
- [ ] Pagination support for 1000+ tweets
- [ ] Unit tests and CI/CD

## Troubleshooting

**403 Forbidden Error**
- Ensure your Bearer Token is from a **Project-attached App**
- Check token hasn't expired

**ModuleNotFoundError**
- Verify virtual environment is activated
- Run `pip install -r requirements.txt`

**API Rate Limits**
- X rate limits API calls; add retry logic or wait between requests
- OpenAI pricing applies per request

## Author

[Vinay Mundhe](https://x.com/vinaymundhe_)
```

Just copy and paste the entire block above into your `README.md` file on GitHub!
