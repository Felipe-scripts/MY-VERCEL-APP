# My Vercel App

This is a Flask application that handles email subscription updates for HubSpot contacts using webhooks.

## Setup

1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies with `pip install -r requirements.txt`.
4. Create a `.env` file in the root directory and add your HubSpot API key:

```
API_KEY=your_hubspot_api_key
```

5. Run the development server with `python api/update_subscriptions.py`.
6. Deploy to Vercel for production.

## API Endpoint

### POST /api/updateSubscriptions

This endpoint updates email subscriptions for a contact based on the data received from a HubSpot webhook.

**Request Body:**

```json
{
  "email": "contact@example.com"
}
```

**Response:**

- `200 OK`: Subscriptions successfully updated.
- `400 Bad Request`: Contact email is required.
- `500 Internal Server Error`: Failed to update subscriptions.

### Deploying to GitHub and Vercel

1. **Initialize a git repository**:

```bash
git init
git add .
git commit -m "Initial commit"
```

2. **Add GitHub remote and push changes**:

```bash
git remote add origin https://github.com/your_username/your_repository.git
git branch -M main
git push -u origin main
```

3. **Deploy to Vercel**:
   - Go to [Vercel](https://vercel.com/), log in and create a new project.
   - Import your GitHub repository to Vercel.
   - Set up environment variables in Vercel with the same key (`API_KEY`) as in `.env`.
   - Deploy the project.
