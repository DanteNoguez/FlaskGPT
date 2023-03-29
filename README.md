# FlaskGPT

Python and Javascript code to stream responses with Flask, ChatGPT and (partially) Langchain. Perhaps it's too messy (sorry), but you get the idea. 

If you want to run this on a server with Gunicorn and Nginx, go to `/etc/nginx/sites-available/<FlaskGPT>` and set `proxy_buffering off`:

```
location / {
                proxy_buffering off;
        }
```

### Acknowledgements
Big thank you to [oneryalcin](https://gist.github.com/oneryalcin/2921408da70266aa61f9c40cb2973865) and [python273](https://gist.github.com/python273/563177b3ad5b9f74c0f8f3299ec13850) for their ideas.
