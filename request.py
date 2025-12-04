# Request parsing (method, path, query, headers, body, form)
from urllib.parse import urlparse, parse_qs 

class Request:
     def __init__(self, raw_text):
         self.raw = raw_text       # is the HTTP request text
         self.method = None        # HTTP methods 
         self.full_path = None     # path + query
         self.path = None          # only path part
         self.query = {}           # dict of lists
         self.headers = {}         # HTTP headers
         self.body = ""
         self.form = {}            # for application/x-www-form-urlencoded
         self.parse()
     
     def parse(self):
         if not self.raw:
             return   
         
         
         # start the split of the request  (request line + headers + body)
         parts = self.raw.split("\r\n\r\n", 1)  
         head = parts[0] 
         self.body = parts[1] if len(parts > 1) else "" # if the body exists ofc 
         
         # another split " parsing the request line"
         lines = head.split("\r\n") # split it using the line ending 
         request_line = lines[0] # extract the request line first
         self.method, self.full_path, _ = request_line.split("",2) # here we have: HTTP method, full request path, Http version
                                                                   # we obtained those with the split method
                                                                   # and are obtained using spaces were limit of the space = 2
                                                                   
         # parsing the path and query parameters: 
         # the URL of the HTTP request has two components: path + query
         
         parsed = urlparse(self.full_path) # here we have a parsed object  
         self.path = parsed.path # ex: after this we obtain "/products/123", a clean URL
         self.query = parse_qs(parsed.query)  # here we obtain the clean query string dictionary
         
         # parsing headers: 
         # here we should start from the second line
         for header_line in lines[1:]:
             # skip the line breaks
             if not header_line:
                continue
             if ": " in header_line:
                 key,val = header_line.split(": ", 1) # the split is done at the first occurrence of ":"
                 self.headers [key.lower()] = val
            # form handling      
         ctype = self.headers.get("content-type", "")
         if "application/x-www-form-urlencoded" in ctype:
          self.form = parse_qs(self.body)         