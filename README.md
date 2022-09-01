**RSS-Reader.**
  
_Usage:_  
rss_reader.py %YOUR URL% OPTIONS  
  
_ _options:_ _  
  -h, --help     show this help message and exit  
  --version      Print version info  
  --json         Print result as JSON in stdout  
  --verbose      Outputs verbose status messages  
  --limit LIMIT  Limit news topics if this parameter provided  
  --date         Provides content cached previous. Can be used with url.  

 _JSON structure:_   
example/example.json  
  
Unitests provided by pytest.  
To run tests: _run pytest tests_   
  
Installation:  
Simple installation: _pip install ._    
Test installation: _python setup.py test_  
  
After installation you can run RSS_reader %OPTIONS% from console.