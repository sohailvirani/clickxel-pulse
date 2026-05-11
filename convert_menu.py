from bs4 import BeautifulSoup
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
desktop_menu = soup.find('ul', class_='navbar-nav-1')

def extract_mobile_menu(ul_element):
    mobile_html = '<ul id="primary-menu" class="navbar-nav-button">\n'
    for li in ul_element.find_all('li', recursive=False):
        classes = li.get('class', [])
        # Base classes for mobile li
        mobile_classes = ['menu-item']
        
        has_children = False
        if li.find('ul'):
            has_children = True
            mobile_classes.append('menu-item-has-children')
        
        mobile_html += f'    <li class="{" ".join(mobile_classes)}">\n'
        
        a = li.find('a', recursive=False)
        if a:
            href = a.get('href', '#')
            # Extract text from span.rolling-text or just text
            span = a.find('span', class_='rolling-text')
            if span:
                text = span.get_text(strip=True)
            else:
                text = a.get_text(strip=True)
            
            if has_children:
                svg = '<span><svg height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path class="heroicon-ui" d="M18.59 13H3a1 1 0 0 1 0-2h15.59l-5.3-5.3a1 1 0 1 1 1.42-1.4l7 7a1 1 0 0 1 0 1.4l-7 7a1 1 0 0 1-1.42-1.4l5.3-5.3z"></path></svg></span>'
                mobile_html += f'        <a href="{href}">{text}{svg}</a>\n'
            else:
                mobile_html += f'        <a href="{href}">{text}</a>\n'
                
        # Now handle children
        if has_children:
            mobile_html += '        <ul class="sub-menu">\n'
            
            # The children might be in direct ul.sub-menu or inside mega-menu-01 -> li.single-mega -> ul.main-wrapper
            mega_menus = li.find_all('li', class_='single-mega', recursive=False)
            mega_menu_container = li.find('ul', class_='mega-menu-01')
            if mega_menu_container:
                mega_menus = mega_menu_container.find_all('li', class_='single-mega', recursive=False)
                for mega in mega_menus:
                    mega_title = mega.find('a', class_='tag')
                    mega_text = mega_title.get_text(strip=True) if mega_title else "Submenu"
                    mobile_html += f'            <li class="menu-item menu-item-has-children">\n'
                    mobile_html += f'                <a href="#">{mega_text}{svg}</a>\n'
                    mobile_html += '                <ul class="sub-menu">\n'
                    
                    wrapper = mega.find('ul', class_='main-wrapper')
                    if wrapper:
                        for sub_li in wrapper.find_all('li', recursive=False):
                            sub_a = sub_li.find('a')
                            if sub_a:
                                mobile_html += f'                    <li class="menu-item"><a href="{sub_a.get("href", "#")}">{sub_a.get_text(strip=True)}</a></li>\n'
                    mobile_html += '                </ul>\n'
                    mobile_html += '            </li>\n'
            else:
                # normal nested list
                sub_ul = li.find('ul', class_='sub-menu')
                if not sub_ul:
                    sub_ul = li.find('ul') # fallback
                    
                if sub_ul:
                    for sub_li in sub_ul.find_all('li', recursive=False):
                        sub_has_children = sub_li.find('ul') is not None
                        
                        li_classes = ['menu-item']
                        if sub_has_children:
                            li_classes.append('menu-item-has-children')
                            
                        mobile_html += f'            <li class="{" ".join(li_classes)}">\n'
                        sub_a = sub_li.find('a', recursive=False)
                        if sub_a:
                            href = sub_a.get('href', '#')
                            text = sub_a.get_text(strip=True)
                            if sub_has_children:
                                mobile_html += f'                <a href="{href}">{text}{svg}</a>\n'
                            else:
                                mobile_html += f'                <a href="{href}">{text}</a>\n'
                        
                        if sub_has_children:
                            mobile_html += '                <ul class="sub-menu">\n'
                            third_ul = sub_li.find('ul')
                            for third_li in third_ul.find_all('li', recursive=False):
                                third_a = third_li.find('a')
                                if third_a:
                                    mobile_html += f'                    <li class="menu-item"><a href="{third_a.get("href", "#")}">{third_a.get_text(strip=True)}</a></li>\n'
                            mobile_html += '                </ul>\n'
                        mobile_html += '            </li>\n'
                        
            mobile_html += '        </ul>\n'
            
        mobile_html += '    </li>\n'
        
    mobile_html += '</ul>'
    return mobile_html

with open('mobile_menu.html', 'w', encoding='utf-8') as f:
    f.write(extract_mobile_menu(desktop_menu))

import glob
import os

# Now modify all html files
html_files = glob.glob('*.html')
new_mobile_menu = extract_mobile_menu(desktop_menu)

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We need to replace the content between <ul id="primary-menu" class="navbar-nav-button"> and its matching </ul>
    # A simple regex might be tricky if there are nested <ul>, but bs4 can do it.
    
    soup = BeautifulSoup(content, 'html.parser')
    old_menu = soup.find('ul', id='primary-menu')
    if old_menu:
        # Instead of replacing with bs4 string which messes up formatting, 
        # let's find the string boundaries using regex or bs4 sourcepos?
        pass

# Since bs4 might mess up formatting, I'll print success and do replacement differently.
print("Extracted mobile menu to mobile_menu.html")
