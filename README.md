[comment]: https://www.jetbrains.com/help/pycharm/markdown.html#code-blocks
[comment]: https://www.markdownguide.org/basic-syntax/
# Description
This is a package to create spherical-looking objects out of images.

# Installation
To install this package, run:

```
python3 setup.py sdist bdist_wheel
pip3 install dist/spherize_texture-0.1.0.0.tar.gz
```

If you want to check out the example spherized objects, look in the folder `spherized/...`

To run the GUI (which is still under construction) use the following code:

```python
import sys
from PyQt5.QtWidgets import QApplication
from spherize_tecture.spherize_texture_gui import get_dark_theme_pallet, Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(get_dark_theme_pallet())

    win = Window()

    win.showMaximized()
    sys.exit(app.exec_())
```

When you open the GUI, you can load an image from File -> Open.
Then you can hit go to get the new spherized image, which you can save by going to File -> Save.

# License 
GNU GPL v3 license.

# Copyright
Copyright (C) 2021 Selewirre Iskvary

# User Support
I would greatly appreciate it if users clearly state that their illustrations and calculations were made 
(partially or completely) with this project.

# Contact
Please report any questions, issues, concerns, suggestions at <selewirre@gmail.com>.
