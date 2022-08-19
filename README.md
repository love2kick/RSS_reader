**RSS-Reader.**
  
_ _Usage:_ _  
rss_reader.py %YOUR URL%
  
_ _options:_ _  
  -h, --help     show this help message and exit  
  --version      Print version info  
  --json         Print result as JSON in stdout  
  --verbose      Outputs verbose status messages  
  --limit LIMIT  Limit news topics if this parameter provided  
  
_ _JSON structure:_ _  
{  
    "content": {  
        "Feed": "%FeedName%",  
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
