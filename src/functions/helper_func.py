def search_keywords_in_file(file_path, keywords):
    """
    Search for multiple keywords in a single file
    Returns set of keywords found in this file
    """
    found_keywords = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().lower()
            
            for keyword in keywords:
                if keyword.lower() in content:
                    found_keywords.add(keyword)
                    
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
    except UnicodeDecodeError:
        print(f"Error: Cannot decode file {file_path}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return found_keywords