from aqt import mw
from aqt.qt import QAction
from .word_counter import count_words

# Add menu item to Anki
action = QAction("Count Word Appearances", mw)
action.triggered.connect(count_words)
mw.form.menuTools.addAction(action)