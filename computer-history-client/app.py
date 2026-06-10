"""
Flask Application for Computing History Agent Client.

This is the main Flask application that provides a web interface
for interacting with the Computing History agent.
"""

from pathlib import Path
import re

from flask import Flask, abort, jsonify, render_template, render_template_string, request, send_from_directory
import markdown
import bleach
from agent_client import AgentClient

ROOT_DIR = Path(__file__).resolve().parent.parent
LABS_DIR = ROOT_DIR / 'Instructions' / 'Labs'

app = Flask(
    __name__,
    template_folder='..',
    static_url_path='/computer-history-client/static',
)


def _set_external_link_attributes(attrs, new=False):
    """Force safe external link attributes for rendered markdown links."""
    href_key = (None, 'href')
    href_value = attrs.get(href_key, '')
    if isinstance(href_value, str) and href_value.startswith(('http://', 'https://')):
        attrs[(None, 'target')] = '_blank'
        attrs[(None, 'rel')] = 'noopener noreferrer nofollow'
    return attrs


def render_markdown_to_safe_html(text: str) -> str:
    """Convert markdown to safe HTML for display in chat bubbles."""
    raw_html = markdown.markdown(
        text,
        extensions=['extra', 'sane_lists', 'nl2br']
    )

    allowed_tags = [
        'p', 'br', 'hr', 'blockquote',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li',
        'strong', 'em', 'code', 'pre',
        'a',
        'table', 'thead', 'tbody', 'tr', 'th', 'td'
    ]
    allowed_attrs = {
        'a': ['href', 'title', 'target', 'rel'],
        'code': ['class']
    }

    safe_html = bleach.clean(
        raw_html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        protocols=['http', 'https', 'mailto'],
        strip=True
    )

    # Linkify plain URLs while leaving code blocks untouched.
    safe_html = bleach.linkify(
        safe_html,
        skip_tags=['pre', 'code'],
        callbacks=[_set_external_link_attributes]
    )
    return safe_html


def render_instruction_markdown_to_safe_html(text: str) -> str:
    """Convert local lab markdown to safe HTML for documentation pages."""
    text = re.sub(r'^---\s.*?---\s*', '', text, flags=re.DOTALL)
    text = text.replace('.md)', '.html)')
    raw_html = markdown.markdown(
        text,
        extensions=['extra', 'sane_lists', 'nl2br']
    )

    allowed_tags = [
        'p', 'br', 'hr', 'blockquote',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li',
        'strong', 'em', 'code', 'pre',
        'a', 'img',
        'table', 'thead', 'tbody', 'tr', 'th', 'td'
    ]
    allowed_attrs = {
        'a': ['href', 'title', 'target', 'rel'],
        'code': ['class'],
        'img': ['src', 'alt', 'title']
    }

    return bleach.clean(
        raw_html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        protocols=['http', 'https', 'mailto'],
        strip=True
    )

# Initialize the agent client
try:
    agent = AgentClient()
except Exception as e:
    print(f"Warning: Failed to initialize agent client: {e}")
    agent = None

@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@app.route('/documentation.html')
def documentation():
    """Render the documentation landing page."""
    return render_template('documentation.html')

@app.route('/Instructions/Labs/<path:lab_name>.html')
def instruction_page(lab_name):
    """Render a local Markdown lab as an HTML page."""
    if Path(lab_name).name != lab_name:
        abort(404)

    lab_path = LABS_DIR / f'{lab_name}.md'
    if not lab_path.is_file():
        abort(404)

    markdown_text = lab_path.read_text(encoding='utf-8')
    title_match = re.search(r'title:\s*(.+)', markdown_text)
    title = title_match.group(1).strip() if title_match else 'Instruction page'
    content_html = render_instruction_markdown_to_safe_html(markdown_text)

    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ title }}</title>
            <link rel="stylesheet" href="/computer-history-client/static/style.css">
        </head>
        <body class="docs-body">
            <main class="docs-page docs-article-page">
                <nav class="docs-nav" aria-label="Documentation navigation">
                    <a class="docs-back-link" href="/documentation.html">Back to documentation</a>
                    <a class="docs-back-link" href="/">Back to chat</a>
                </nav>
                <article class="docs-article">{{ content_html|safe }}</article>
            </main>
        </body>
        </html>
        """,
        title=title,
        content_html=content_html,
    )

@app.route('/Instructions/Labs/media/<path:filename>')
def instruction_media(filename):
    """Serve local lab media when viewing instruction pages in Flask."""
    return send_from_directory(LABS_DIR / 'media', filename)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the user."""
    if not agent:
        return jsonify({
            'error': 'Agent client not initialized. Check your .env configuration.'
        }), 500
    
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    # Validate message length to prevent abuse
    if len(user_message) > 10000:
        return jsonify({'error': 'Message too long'}), 400
    
    # Note: We do NOT escape HTML here because:
    # 1. The agent needs to receive the raw text to understand it properly
    # 2. HTML escaping is performed on the frontend when displaying messages
    # 3. This follows the principle: escape at the point of use (display), not at input
    try:
        response = agent.send_message(user_message)
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 502

    response_html = render_markdown_to_safe_html(response)

    return jsonify({
        'response': response,
        'response_html': response_html
    })

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the conversation history."""
    if agent:
        agent.reset_conversation()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=False, port=5000)
