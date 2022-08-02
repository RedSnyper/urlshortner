This is the base working app for url shortner

Contains only the minimal logic to get the app working
- post urls
- generates shortedned version
- redirects to original based on shortened url provided

The routes are built using fastapi async way however sqlalchemy synchronous session is used.
