# AME: Accessible Markdown Editor for Screen Readers
It is a simple accessible markdown editor designed for screen readers.

## Download for original AME
* [download for Mac](https://github.com/chigkim/AME/releases/download/v0.1.0/AME-v0.1.0-Mac.zip)
* [download for Windows](https://github.com/chigkim/AME/releases/download/v0.1.0/AME-v0.1.0-Win.zip)

## Shortcuts
On Mac, press command instead of control.

* Open: Ctrl+O
* New: Ctrl+N
* Export to HTML: Ctrl+E
* Copy HTML to Clipboard: Ctrl+Shift+C
* View Markdown: Ctrl+1
* View HTML: Ctrl+2


## Jonathan's additions

Import and export using pandoc is achieved using pypandoc, the Python wrapper to pandoc. This requires an installation of pandoc.

Import is sorted. Hot key is CTRL+SHIFT+O

Next task is to build in the export via pandoc, initially just to html. This should allow maths to be included. N.B. the math will not be rendered correctly using just Python alone.



## updates and alteratons to the original AME

Hints and corrections offered using pylint and blacken tools have been incorporated. Pylint still throws warnings about a few things but they of low significance.

