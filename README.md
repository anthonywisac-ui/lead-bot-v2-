# Lead Bot 🤖

WhatsApp Business API bot built with FastAPI. Send and receive messages on WhatsApp.

## Quick Start

### 1. Setup Environment

```bash
# Copy example env
copy .env.example .env

# Edit .env with your details
# WHATSAPP_PHONE_ID: 1312395868620049
# WHATSAPP_TOKEN: EAAZAKYm8R6QgBSOHJuhfOqSNvrjx54...
# BUSINESS_ACCOUNT_ID: 1527222711920899
# VERIFY_TOKEN: any-random-string-you-choose
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally

```bash
python main.py
```

Server runs on: **http://localhost:8000**

### 4. Test Webhook Setup

```bash
# Health check
curl http://localhost:8000/health

# Should return:
# {"status":"ok","service":"lead-bot","whatsapp_configured":true}
```

## Webhook Configuration (Meta Dashboard)

1. Go to: **Meta App Dashboard > WhatsApp > Configuration**

2. Set webhook:
   - **Webhook URL**: `https://your-railway-url.railway.app/webhook`
   - **Verify Token**: Same as `VERIFY_TOKEN` in .env

3. Subscribe to events:
   - ✓ messages
   - ✓ message_template_status_update
   - ✓ message_template_quality_update

## API Endpoints

### GET /health
Health check endpoint.

```bash
curl http://localhost:8000/health
```

### GET /webhook
Webhook verification (used by Meta).

### POST /webhook
Receive messages from WhatsApp.

## Railway Deployment

### 1. Create Git Repo

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/lead-bot.git
git push -u origin main
```

### 2. Connect to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up
```

### 3. Set Environment Variables

In Railway dashboard:
- `WHATSAPP_PHONE_ID`
- `WHATSAPP_TOKEN`
- `BUSINESS_ACCOUNT_ID`
- `VERIFY_TOKEN`
- `PORT` (auto-set)

### 4. Update Meta Webhook

Go back to Meta Dashboard and update webhook URL to Railway URL.

## Features

- ✅ Receive text messages
- ✅ Send text messages
- ✅ Interactive buttons
- ✅ Message status tracking
- ✅ Easy Railway deployment

## File Structure

```
lead-bot/
├── main.py              # FastAPI app
├── requirements.txt     # Dependencies
├── .env.example         # Example environment
├── .env                 # Actual environment (never commit!)
├── .gitignore           # Git ignore
├── Procfile             # Railway config
└── README.md            # This file
```

## Troubleshooting

### Webhook not responding?
- Check `VERIFY_TOKEN` matches Meta Dashboard
- Check URL is publicly accessible
- Ensure FastAPI is running

### Messages not sending?
- Verify `WHATSAPP_TOKEN` is valid
- Check `WHATSAPP_PHONE_ID` is correct
- Ensure phone number is in format: `923351234567` (no +)

### Railway deployment failed?
- Check Procfile is present
- Verify environment variables are set
- Check logs: `railway logs`

## Support

Issues? Check:
1. `.env` file has all required values
2. Phone number includes country code (e.g., 92 for Pakistan)
3. Meta webhook URL is public (not localhost)

---

**Ready to go!** 🚀
