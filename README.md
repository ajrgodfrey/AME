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

Import is sorted. The user does not need to specify the file type, but Pandoc only imports a small range of files. Hot key is CTRL+SHIFT+O

Export to HTML via pandoc is available. This should allow maths to be included. N.B. the math will not be rendered correctly using just Python alone, or in the AME HTML pane, which is really just a preview pane if any equations are included.

Protection against the user not having Pandoc visible is in need of testing. It needs to be run on a machine that does not have pandoc installed, both for import and export.

Created an installer for the Windows version. This puts a date-based version number in a text file within the installation folder.

## Other updates and alterations to the original AME

Hints and corrections offered using pylint and blacken tools have been incorporated. Pylint still throws warnings about a few things but they of low significance. Most relate to pylint not knowing about the wx use of `(self, e)` style in function definitions.

Small alterations:

1. added a small help note with hotkey `f1`
2. added switch view menu item in the View menu (hotkey is `f4`) and reordered the original items.
3. did a bit of re-factoring on reused code snippets.

