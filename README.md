**RSS-Reader.**
  
_Usage:_  
rss_reader.py %YOUR URL% OPTIONS  
  
_ _options:_ _  
  -h, --help     show this help message and exit  
  --version      Print version info  
  --json         Print result as JSON in stdout  
  --verbose      Outputs verbose status messages  
  --limit LIMIT  Limit news topics if this parameter provided  
  --date         Provides content cached previously. Can be used with url.  
  --to-html      Creates an output .html file    
  --to-pdf       Creates an output .pdf file  
  
 _JSON structure:_   
example/example.json  
  
Installation:  
Simple installation: _pip install ._    
Run tests: _python setup.py test_  
  
After installation you can run RSS_reader %OPTIONS% from console.  
   
Fancy RSS_reader is a peace of garbage that i made as an ultimate task to waste a lot of time and learn some software gore.   
It can check feed from url provided by user and return some common info from those pesky feeds.  
  
**Features:**  
It can return feed content (Feedname, Title of article, date, link and short description) in two formats: simply prints in your console or return you a faboulous json.  
It can also cache all this stuff and you can access it anytime by adding --date %Y%m%d and receive those wonderful articles back from sqlite database.  
Verbose will provide you an ultimate experience of sentient software that speaks the human language.  
If you want some more cool software from me - please, don't.  
Have a great day!  

