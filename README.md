RSS-Reader.

Usage:
rss_reader.py %YOUR URL%

options:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided



JSON structure:
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