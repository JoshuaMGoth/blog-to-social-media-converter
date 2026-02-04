# 📱 Social Media Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/JoshuaMGoth/blog-to-social-media-converter?style=social)](https://github.com/JoshuaMGoth/blog-to-social-media-converter)

Transform any blog post into ready-to-publish social media content using AI. Generate optimized posts for Instagram, Facebook, and Pinterest — complete with captions, hashtags, and AI-generated images.

**This is my first open source project!** 🎉 I hope you find it useful.

---

## 📑 Table of Contents

- [Features](#-features)
- [How It Works](#-how-it-works)
- [Platform-Specific Formatting](#-platform-specific-formatting)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Settings Reference](#-settings-reference)
- [Usage Guide](#-usage-guide)
- [API Endpoints](#-api-endpoints)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## ✨ Features

### Core Functionality
| Feature | Description |
|---------|-------------|
| 🔗 **URL Extraction** | Automatically scrapes and extracts content from any blog URL |
| 📸 **Instagram Posts** | Generates captions with emojis, line breaks, and 5-10 relevant hashtags |
| 📘 **Facebook Posts** | Creates scroll-stopping posts with hooks, CTAs, and engagement prompts |
| 📌 **Pinterest Strategies** | Produces 4-6 pin ideas with keywords, board suggestions, and descriptions |
| 🖼️ **AI Image Generation** | Creates custom images from AI-generated prompts using DeepAI |
| ⚙️ **Settings Management** | Store API keys securely with support for multiple AI providers |

### What Makes This Different
- **One-click conversion**: Paste a URL, click generate, copy your content
- **Platform-optimized**: Each platform gets content formatted for its specific best practices
- **Smart image prompts**: AI generates detailed image descriptions, then creates the actual image
- **Fallback handling**: Gracefully handles API errors and unsafe content filters

---

## 🔄 How It Works

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  1. Paste URL   │ ──► │  2. Extract Blog │ ──► │ 3. AI Generates │
│                 │     │     Content      │     │    Platform     │
│                 │     │   (BeautifulSoup)│     │  Specific Post  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  6. Copy/Use    │ ◄── │ 5. Display Post  │ ◄── │ 4. Generate     │
│    Your Post    │     │   + Image        │     │    AI Image     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### Step-by-Step Process

1. **Content Extraction**: The app fetches the blog URL and uses BeautifulSoup to extract clean text content (up to 5,000 characters)
2. **AI Processing**: DeepSeek AI analyzes the content and generates platform-specific posts
3. **Image Prompt Creation**: AI creates a detailed image description based on the blog content
4. **Image Generation**: DeepAI creates an actual image from the prompt (optional)
5. **Output**: You get ready-to-use content with copy buttons for each section

---

## 📋 Platform-Specific Formatting

### 📸 Instagram Post Format

The AI generates Instagram posts with this structure:

```
[Engaging caption with emojis and line breaks]

• Uses conversational tone
• Includes call-to-action
• Maximum 2,200 characters

#hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5
```

**Generated Fields:**
| Field | Description |
|-------|-------------|
| `caption` | The main Instagram caption (max 2,200 chars) |
| `hashtags` | Array of 5-10 relevant hashtags |
| `image_description` | Suggested visual concept for the post |

---

### 📘 Facebook Post Format

Facebook posts follow a **5-part scroll-stopping structure**:

```
🎯 THE HOOK
[1-2 provocative sentences that create curiosity]

💬 THE BODY
[3-5 short paragraphs with emotional, relatable content]

🔗 THE CTA
[Tease what they'll learn + "Read it here: [Link]"]

💭 ENGAGEMENT PROMPT
[Specific question to drive comments]
```

**Generated Fields:**
| Field | Description |
|-------|-------------|
| `hook` | Attention-grabbing opening statement |
| `body` | Main emotional content with short paragraphs |
| `cta` | Call-to-action with link placeholder |
| `engagement_prompt` | Question to drive comments |
| `visuals_guide` | 3 visual options (photo, text graphic, video) |
| `full_post` | Complete formatted post ready to copy |
| `image_description` | Best visual concept for AI image generation |

---

### 📌 Pinterest Strategy Format

Pinterest generates a **complete pin strategy** with multiple pin types:

**Pin Types Generated:**
| Type | Purpose |
|------|---------|
| `title` | Main headline pin with key message |
| `list` | Numbered key takeaways or tips |
| `howto` | Step-by-step guide format |
| `quote` | Inspiring or thought-provoking quote |
| `statistic` | Key data point or finding |

**Generated Fields:**
| Field | Description |
|-------|-------------|
| `summary` | Brief blog summary |
| `keyTopics` | 3-5 main topics |
| `targetAudience` | Who this content is for |
| `pinterestKeywords` | 8-10 SEO keywords for Pinterest search |
| `boardSuggestions` | 3 Pinterest board names |
| `pinStrategies` | Array of 4-6 pin ideas with titles, descriptions, CTAs |
| `image_description` | Visual style recommendation for pin graphics |

**Each Pin Strategy Includes:**
- Pin type and focus
- 3-4 key points
- Call-to-action text
- Pin title (max 60 chars)
- Pinterest-optimized description (max 500 chars)

---

## 💻 Requirements

### System Requirements
- **Python**: 3.9 or higher
- **Git**: For cloning and updates
- **Operating System**: Windows, macOS, or Linux

### Python Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `flask` | 2.3.3 | Web framework |
| `flask-cors` | 4.0.0 | Cross-origin request handling |
| `requests` | 2.31.0 | HTTP requests to APIs |
| `beautifulsoup4` | 4.12.2 | HTML parsing and content extraction |
| `python-dotenv` | 1.0.0 | Environment variable management |
| `Pillow` | (any) | Image processing |

### API Keys Required

| API | Required | Purpose | Get It Here |
|-----|----------|---------|-------------|
| **DeepSeek** | ✅ Yes | Text generation for all posts | [deepseek.com](https://deepseek.com) |
| **DeepAI** | Optional | Image generation | [deepai.org](https://deepai.org) |

---

## 🚀 Installation

### Quick Start (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/JoshuaMGoth/blog-to-social-media-converter.git
cd blog-to-social-media-converter

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
source venv/bin/activate        # Linux/macOS
# OR
venv\Scripts\activate           # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create your .env file (see Configuration section)

# 6. Start the app
python app.py

# 7. Open in browser
# http://127.0.0.1:5000
```

---

## ⚙️ Configuration

### Option 1: Environment Variables (.env file)

Create a `.env` file in the project root:

```env
# Required - for text generation
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Optional - for image generation
DEEPAI_API_KEY=your_deepai_api_key_here
```

### Option 2: Settings Page

1. Start the app: `python app.py`
2. Navigate to http://127.0.0.1:5000/settings
3. Enter your API keys in the form
4. Click "Save Settings"

Keys are stored in `app_settings.json` (this file is git-ignored for security).

---

## 📖 Settings Reference

### Text AI Providers

| Setting | Description | Status |
|---------|-------------|--------|
| **DeepSeek API Key** | Primary AI for generating all social media content | ✅ Active |
| OpenAI API Key | GPT models (future) | 🔮 Planned |
| Anthropic API Key | Claude models (future) | 🔮 Planned |
| Google Gemini API Key | Gemini models (future) | 🔮 Planned |
| Cohere API Key | Cohere models (future) | 🔮 Planned |
| Mistral API Key | Mistral models (future) | 🔮 Planned |
| Groq API Key | Groq inference (future) | 🔮 Planned |
| xAI API Key | Grok models (future) | 🔮 Planned |
| Perplexity API Key | Perplexity AI (future) | 🔮 Planned |

### Image AI Providers

| Setting | Description | Status |
|---------|-------------|--------|
| **DeepAI API Key** | Primary AI for generating images from prompts | ✅ Active |
| OpenAI Image API Key | DALL-E models (future) | 🔮 Planned |
| Stability AI API Key | Stable Diffusion (future) | 🔮 Planned |
| Replicate API Key | Various models (future) | 🔮 Planned |
| Leonardo API Key | Leonardo AI (future) | 🔮 Planned |
| Midjourney API Key | Midjourney (future) | 🔮 Planned |
| Ideogram API Key | Ideogram AI (future) | 🔮 Planned |
| Flux API Key | Flux models (future) | 🔮 Planned |

> **Note**: Currently, only DeepSeek (text) and DeepAI (image) are implemented. Other providers are saved for future integrations.

---

## 📱 Usage Guide

### Basic Workflow

1. **Enter a Blog URL**
   - Paste any publicly accessible blog post URL
   - The app extracts up to 5,000 characters of content

2. **Select Platform**
   - Choose Instagram, Facebook, or Pinterest
   - Each platform has unique formatting

3. **Enable Image Generation** (Optional)
   - Check "Auto-generate AI image"
   - Requires DeepAI API key

4. **Generate Post**
   - Click the generate button
   - Wait 5-15 seconds for AI processing

5. **Copy Your Content**
   - Use the copy buttons for each section
   - Download generated images

### Tips for Best Results

- **Use full blog posts**: More content = better AI output
- **Check the image prompt**: Edit before generating if needed
- **Customize after copying**: AI output is a starting point
- **Try different platforms**: Same blog, different angles

---

## 🔌 API Endpoints

### Frontend Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Main application page |
| `/settings` | GET/POST | API key settings page |

### API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/api/process` | POST | Generate social media post |
| `/api/generate_image` | POST | Generate image from prompt |
| `/api/settings` | GET | Get current settings (keys masked) |
| `/api/mock_image` | GET | Test endpoint (returns sample image) |

### Example: Process Blog

```bash
curl -X POST http://127.0.0.1:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/blog-post",
    "platform": "instagram",
    "generate_image": true
  }'
```

---

## 🔧 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| "DeepSeek API key is required" | Add your API key to `.env` or Settings page |
| Image generation fails | Check DeepAI key; try a different prompt |
| "Unsafe content" error | The app auto-sanitizes and retries; try a different blog |
| Slow generation | AI processing takes 5-15 seconds; be patient |
| Empty output | Ensure the blog URL is publicly accessible |

### Debug Mode

The app runs in debug mode by default. Check the terminal for detailed logs:

```bash
python app.py
# Watch for [DEBUG] and [ERROR] messages
```

Logs are also written to `flask.log` for review.

---

## 🔄 Updating

Get the latest features and bug fixes:

```bash
# Pull latest changes
git pull origin main

# Update dependencies (if changed)
pip install -r requirements.txt

# Restart the app
python app.py
```

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## 🤝 Contributing

Contributions are welcome! This is my first open source project, and I'd love your help making it better.

### Ways to Contribute

- 🐛 **Report bugs**: [Open an issue](https://github.com/JoshuaMGoth/blog-to-social-media-converter/issues)
- 💡 **Suggest features**: [Open an issue](https://github.com/JoshuaMGoth/blog-to-social-media-converter/issues)
- 🔧 **Submit code**: [Open a pull request](https://github.com/JoshuaMGoth/blog-to-social-media-converter/pulls)
- 📖 **Improve docs**: Fix typos, add examples, clarify instructions

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Use privately

---

## 👤 Author

**Joshua Goth**

| | |
|---|---|
| 🌐 Website | [joshuagoth.com](https://joshuagoth.com) |
| 🐙 GitHub | [@JoshuaMGoth](https://github.com/JoshuaMGoth) |
| ✉️ Email | [me@joshuagoth.com](mailto:me@joshuagoth.com) |

---

## 💖 Support

If you find this project helpful:

- ⭐ **Star this repository** — it helps others find it
- 🐛 **Report bugs** — help me improve
- 💡 **Suggest features** — I'm always looking for ideas
- 📣 **Share with others** — spread the word!

---

## 🙏 Acknowledgments

- [DeepSeek](https://deepseek.com) — AI text generation
- [DeepAI](https://deepai.org) — AI image generation
- [Flask](https://flask.palletsprojects.com/) — Python web framework
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) — HTML parsing

---

<p align="center">
  <strong>Made with ❤️ by Joshua Goth</strong><br>
  <em>This is my first open source project — thank you for being here!</em>
</p>
