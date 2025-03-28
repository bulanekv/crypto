# Application Launch Instructions

## Environment Setup

Create a `.env` file with the following configuration:

```
STAGE=DEV
#TEST=TEST
SENTRY_DSN=
AWS_ACCESS_KEY_ID=dummy_access_key
AWS_SECRET_ACCESS_KEY=dummy_secret_key
AWS_DEFAULT_REGION=eu-central-1
COINGECKO_API_KEY=
```

### Environment Variables Explanation:
- `SENTRY_DSN`: Optional key for error tracking
- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: Dummy credentials for local deployment
- `AWS_DEFAULT_REGION`: Set to `eu-central-1`
- `COINGECKO_API_KEY`: Required API key for CoinGecko (must be filled)
- `STAGE=DEV`: Indicates use of local database
- `TEST=TEST` (commented out): Use this to run tests on the test database table

## Deployment Options

### Docker Deployment
To build and run the application using Docker:
```
docker compose up --build
```

#### Access Points:
- Application: `http://0.0.0.0:8190`
- Swagger Documentation: `http://0.0.0.0:8190/docs`

### Local Server Deployment
To start the application without Docker:
```
./localserver.sh
```

## Technology Stack
- Python 3.13
- FastAPI
- DynamoDB
