# color-palette-web
A Python based color picker website made using NumPy, Flask, Bootstrap and Pillow.

# Features
Includes functionality which only allows uploading .png .jpg and .jpeg image files for safety and compatibility reasons. That way we can ensure that users are not able to upload HTML files that would cause XSS problems etc.  
Also uses secure_filename to tranform filename into a safer version. It removes or replaces characters that could be used for malicious purposes, such as directory traversal attacks.

# Preview
![index](https://github.com/Marko-Korn/color-palette-web/assets/9790303/472ee64f-d54f-4c1f-a672-7e7d03fd0168)
![results](https://github.com/Marko-Korn/color-palette-web/assets/9790303/70608557-057e-4585-83f7-7825b7a8dbe2)
