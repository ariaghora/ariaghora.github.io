import glob
import os
import markdown2


dirname: str = os.path.dirname(__file__)
md_filenames: list = glob.glob(os.path.join(dirname, 'md', '*.md'))


def extract_parts(str_list: list):
    sep_line_idx = 0
    for i, line in enumerate(str_list):
        if line.startswith('---'):
            sep_line_idx = i
            break
    assert sep_line_idx > 0, 'Invalid header format'

    metadata: list[str] = str_list[:sep_line_idx]
    title = ''
    date = ''
    body = ''
    for line in metadata:
        if line.strip().startswith('title'):
            title = line[line.find(':')+1:].strip()
        elif line.strip().startswith('date'):
            date = line[line.find(':')+1:].strip()

    body = ''.join(str_list[sep_line_idx+1:])

    return title, date, body


def compile_md(filename: str):
    with open(filename, 'r') as f:
        raw = f.readlines()
        title, date, body = extract_parts(raw)
        html_title = f'<h2 class="page-title">{title}</h2>'
        html_body = markdown2.markdown(body)
        body_output = html_title + '\n' + html_body

    with open(os.path.join(os.path.dirname(__file__), 'layout.html'), 'r') as f:
        layout = f.read()
        blog_output = layout.replace('__BODY__', body_output)

    return blog_output


fn = md_filenames[0]
out_filename = os.path.join(
    dirname, os.path.basename(fn).rstrip('.md') + '.html')

with open(out_filename, 'w') as f:
    out_html = compile_md(fn)
    f.write(out_html)
