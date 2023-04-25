html_layout = """
<!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <script>
                function deleteUploadsAndGoHome() {
                    fetch('/delete-uploads')
                    .then(() => {
                        window.location.href = '/';
                    });
                }
            </script>
        </head>
        <body class="dash-template">
            <header>
              <div class="nav-wrapper">
                <a href="#" onclick="deleteUploadsAndGoHome()">
                    <img src="/static/templates/first_Logo.png" class="logo" />
                    <h1>Zur Datenauswahl</h1>
                  </a>
                <nav>
                </nav>
            </div>
            </header>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
"""
