from __main__ import app, os, send_from_directory

@app.route('/dl/songs/<path:filename>', methods=['GET', 'POST'])
async def download_songs(filename):
    return send_from_directory(
        os.path.abspath('.\\dl\\songs'),
        filename,
        as_attachment=False,
        mimetype=None
    )