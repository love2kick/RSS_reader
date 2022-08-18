**RSS-Reader.**

_ _Usage:_ _
rss_reader.py %YOUR URL%

_ _options:_ _
  -h, --help     show this help message and exit  
  --version      Print version info  
  --json         Print result as JSON in stdout  
  --verbose      Outputs verbose status messages  
  --limit LIMIT  Limit news topics if this parameter provided  



_ _JSON structure:  _ _
{  
    "content": {  
        "Feed": "%FeedName%",  
        "items": {  
            "item": [  
                {  
                    "title": "%ArticleTitle%",  
                    "date": "%PublishingDate%",  
                    "link": "%ArticleLink%",  
                    "description": "%ArticleDescription%"  
                },  
            ]  
        }  
    }  
}  
