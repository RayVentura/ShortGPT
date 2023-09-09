# To run ShortGPT docker:


First make a .env file with the API keys like this:

```bash
OPENAI_API_KEY=sk-_put_your_openai_api_key_here
ELEVENLABS_API_KEY=put_your_eleven_labs_api_key_here
PEXELS_API_KEY=put_your_pexels_api_key_here
```


To run Dockerfile do this:
```bash
docker build -t short_gpt_docker .
docker run -p 31415:31415 short_gpt_docker --env-file .env
```