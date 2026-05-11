import glob
import re

with open('mobile_menu.html', 'r', encoding='utf-8') as f:
    new_menu = f.read()

html_files = glob.glob('*.html')
count = 0

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to replace everything between <ul id="primary-menu" class="navbar-nav-button">
    # and its matching closing </ul>.
    # Since regex might not match nested </ul> easily if it's complex,
    # we can use a simple state machine to find the matching closing tag.
    
    start_tag = '<ul id="primary-menu" class="navbar-nav-button">'
    start_idx = content.find(start_tag)
    
    if start_idx != -1:
        # Find the matching closing </ul>
        idx = start_idx + len(start_tag)
        depth = 1
        
        # Regex to find next <ul> or </ul>
        tag_pattern = re.compile(r'<\s*(/?)\s*ul[^>]*>', re.IGNORECASE)
        
        while depth > 0:
            match = tag_pattern.search(content, idx)
            if not match:
                break
            
            if match.group(1) == '/':
                depth -= 1
            else:
                depth += 1
            
            idx = match.end()
            
        if depth == 0:
            end_idx = idx
            
            # Replace
            new_content = content[:start_idx] + new_menu + content[end_idx:]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1

print(f"Replaced mobile menu in {count} HTML files.")
