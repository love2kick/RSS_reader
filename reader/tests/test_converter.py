from converter import convert_to_html

def test_to_html():
    test_dict={  
                "content": {  
                    "feed": ["FeedName"],  
                    "items": {  
                        "item0": {  
                            "title": "TestTitle",  
                            "date": "1945-05-10",  
                            "link": "https://www.TEST",  
                            "description": "SomeRandomDescription"  
                            }  
                        }  
                    }  
                } 
    convert_to_html(test_dict)