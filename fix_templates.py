import os

def fix_template(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace common encoding artifacts
    content = content.replace('\xc2\xb7', '\xc2\xb7')  # middle dot - ensure it's proper UTF-8
    content = content.replace('\xe2\x80\xa2', '\xe2\x80\xa2')  # bullet
    content = content.replace('\xc2\xb7', '\xc2\xb7')  # middle dot
    content = content.replace('\xe2\x80\x93', '\xe2\x80\x93')  # en dash
    content = content.replace('\xe2\x80\x94', '\xe2\x80\x94')  # em dash
    content = content.replace('\xc2\xb7', '·')  # middle dot as literal
    
    # Also replace the literal characters that might be misencoded
    content = content.replace('\u00b7', '·')
    
    # Write back with explicit UTF-8
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Fixed: {filepath}')

template_dir = 'C:/Users/JOHN/Documents/andc2/templates'
for fname in os.listdir(template_dir):
    if fname.endswith('.html'):
        fix_template(os.path.join(template_dir, fname))

print('All templates fixed')