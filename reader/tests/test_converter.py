import os
from converter import convert_to_html, PDF_converter
from pathlib import Path
import os

test_dict={  
                "content": {  
                    "feed": "TESTFEED",  
                    "items": {  
                        "item0": {  
                            "TITLE": "TestTitle",  
                            "DATE": "1945-05-10",  
                            "LINK": "https://www.TEST",  
                            "DESCRIPTION": "SomeRandomDescription"  
                            }  
                        }  
                    }  
                } 


media_path = os.path.join(Path(os.path.dirname(__file__)).parent, 'media')


def test_to_html():
    convert_to_html(test_dict)
    assert Path(os.path.join(media_path, 'TESTFEED.html')).is_file() == True
    
    
def test_to_pdf():
    PDF_converter(test_dict)
    assert Path(os.path.join(media_path, 'TESTFEED.pdf')).is_file() == True
    
    
def test_cleanup():
    os.remove(Path(os.path.join(media_path, 'TESTFEED.html')))
    os.remove(Path(os.path.join(media_path, 'TESTFEED.pdf')))
    assert Path(os.path.join(media_path, 'TESTFEED.html')).is_file() == False
    assert Path(os.path.join(media_path, 'TESTFEED.pdf')).is_file() == False