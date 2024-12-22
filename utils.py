import trafilatura
import ast

def URLget_contacts(url):
    # print(type(urls))
    # # url_list=urls['urls']
    # print("url_list",urls)
    # urls = ast.literal_eval(urls)
    data=[]
    # for url in urls:
    print('url',url)
    response = requests.get(url)
    response.raise_for_status() 
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    text = ' '.join(text.split()) 
    data.append({f'site:{url},extract_data:{text}'})
    
    return data




import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def URLdata_get1(url, max_pages=10):

    # Store visited URLs to avoid duplicates
    visited_urls = set()
    # Store extracted text and emails
    all_text = []
    all_emails = set()
    # Store URLs to visit
    urls_to_visit = [url]
    
    def is_valid_url(url):
        """Check if URL belongs to the same domain"""
        parsed_url = urlparse(url)
        return bool(parsed_url.netloc and parsed_url.scheme in ['http', 'https'])
    
    def clean_text(text):
        """Clean extracted text by removing extra whitespace and special characters"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()
    
    try:
        # Set headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        while urls_to_visit and len(visited_urls) < max_pages:
            current_url = urls_to_visit.pop(0)
            
            if current_url in visited_urls:
                continue
                
            # Mark URL as visited
            visited_urls.add(current_url)
            
            # Get page content
            response = requests.get(current_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'header', 'footer', 'nav']):
                element.decompose()
            
            # Extract meaningful text
            text_content = soup.get_text()
            cleaned_text = clean_text(text_content)
            if cleaned_text:
                all_text.append(cleaned_text)
            
            # Find email addresses in the page content
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
            all_emails.update(emails)
            
            # Find all links on the page
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(current_url, href)
                
                # Only add URLs from the same domain
                if (is_valid_url(full_url) and 
                    urlparse(full_url).netloc == urlparse(url).netloc and 
                    full_url not in visited_urls):
                    urls_to_visit.append(full_url)
        
        return {
            'text_content': '\n\n'.join(all_text),
            'emails': list(all_emails)
        }
        
    except Exception as e:
        return {'error': f"Error occurred while scraping: {str(e)}"}

urls = ["https://indianhelpline.com/tamil-nadu"]



if __name__=="__main__":
    # extracted_texts = URLget_contacts(urls)
    extracted_texts=URLdata_get1(urls)
    print(extracted_texts)
# for text in extracted_texts:
#     print(text)  # Print the first 500 characters of each extracted text
