How to RunInstall requests:In a command prompt:bash

cd C:\Users\Young_mose\OneDrive\Desktop\POWER LEARN PROJECT\python\week6
pip install requests

or:bash

py -m pip install requests

If permission denied, run as Administrator:Right-click Command Prompt > Run as Administrator.
Then: pip install requests.

Verify:bash

pip show requests

Save the Script:Save as ubuntu_image_fetcher.py in C:\Users\Young_mose\OneDrive\Desktop\POWER LEARN PROJECT\python\week6.

Run the Script:bash

python ubuntu_image_fetcher.py

or:bash

py ubuntu_image_fetcher.py

Test with URLs:Use valid image URLs, e.g., https://picsum.photos/200/300.
Example interaction:

Welcome to the Ubuntu Image Fetcher
A tool for mindfully collecting images from the web

Enter image URLs (one per line, press Enter twice to finish):
https://picsum.photos/200/300
https://picsum.photos/200/300

✓ Successfully fetched: 300
✓ Image saved to Fetched_Images/300
✗ Skipped https://picsum.photos/200/300: Duplicate image found as 300.

Connection strengthened. Community enriched. (1/2 images fetched successfully)

