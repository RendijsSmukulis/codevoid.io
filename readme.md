Generate your site
------------------

From the site directory, run the pelican command to generate the site:

    pelican content -t themes\html5up-strata --ignore-cache -s publishconf.py

Preview your site
-----------------

    cd output
    python -m pelican.server

Markdown reference for pelican: https://sourceforge.net/p/pelican-edt/wiki/markdown_syntax/