**RSS-Reader.**
  
_ _Usage:_ _  
rss_reader.py %YOUR URL% OPTIONS  
  
_ _options:_ _  
  -h, --help     show this help message and exit  
  --version      Print version info  
  --json         Print result as JSON in stdout  
  --verbose      Outputs verbose status messages  
  --limit LIMIT  Limit news topics if this parameter provided  
  
_ _JSON structure:_ _  
{  
    "content": {  
        "feed": "%FeedName%",  
        "items": {  
            "item_%NUM%": {  
                "title": "%title%",  
                "date": "%date%",  
                "link": "%link%",  
                "description": "%desc%"  
            },  
        }  
    }  
}  

Unitests provided by pytest. To run test run pytest tests.  
  
Installation:  
Run _ _pip install ._ _  
  
After installation you can run RSS_reader %OPTIONS% from console.