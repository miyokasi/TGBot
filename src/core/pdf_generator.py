import markdown
from weasyprint import HTML
import tempfile
import os

def html_template(content: str) -> str:
    html_body = markdown.markdown(content, extensions=["fenced_code", "tables"])
    return f"""
        <html>
        <head>
            <meta charset='utf-8'>
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                    @bottom-center {{
                        content: "Згенеровано ботом";
                        font-family: "Times New Roman", serif;
                        font-size: 10pt;
                        color: rgba(0, 0, 0, 0.4);
                    }}
                }}
                body {{
                    font-family: "Times New Roman", serif;
                    font-size: 14pt;
                    line-height: 1.5;
                }}
                code, pre {{
                    background: #f4f4f4;
                    padding: 0.2em;
                    font-family: monospace;
                    font-size: 12pt;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}
                th, td {{
                    border: 1px solid #ccc;
                    padding: 0.5em;
                    text-align: left;
                }}
            </style>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """


def generate_pdf(content: str) -> str:
    html = html_template(content)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        HTML(string=html).write_pdf(f.name)
        return f.name

# Для тестування вручну
if __name__ == "__main__":
    sample_text = """
    Ім'я: Іван Петренко
    Посада: Junior Python Developer
    Освіта: КНУ, Комп'ютерні науки
    Навички: Python, SQL, Flask
    """
    path = generate_pdf(sample_text)
    print(f"PDF збережено в: {path}")