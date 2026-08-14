import subprocess
import urllib.parse

def search_web(query: str) -> str:
    """
    Opens the default Windows web browser and performs a Google search for the given query.
    
    Args:
        query (str): The search term or question to look up.
    """
    try:
        print(f"[DEMON Cell Tool]: Searching the web for '{query}'...")
        # URL encode the query to handle spaces and special characters
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        
        subprocess.run(
            ["powershell.exe", "-Command", f"Start-Process '{search_url}'"], 
            check=True
        )
        return f"I have opened a web search for '{query}' in your browser."
    except Exception as e:
        return f"Failed to execute web search: {str(e)}"

def open_website(url: str) -> str:
    """
    Opens a specific URL in the default Windows web browser.
    
    Args:
        url (str): The full URL of the website to open (e.g., 'https://github.com').
    """
    if not url.startswith("http"):
        url = "https://" + url

    try:
        print(f"[DEMON Cell Tool]: Opening website {url}...")
        subprocess.run(
            ["powershell.exe", "-Command", f"Start-Process '{url}'"], 
            check=True
        )
        return f"Successfully opened {url}."
    except Exception as e:
        return f"Failed to open website: {str(e)}"