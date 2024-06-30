import os
from aqt import mw
from aqt.qt import QInputDialog, QMessageBox, QFileDialog, QProgressDialog, Qt

def select_deck():
    decks = mw.col.decks.allNames()
    deck_name, ok = QInputDialog.getItem(mw, "Select Deck", "Choose a deck:", decks, 0, False)
    if not ok or not deck_name:
        return None
    return deck_name

def select_fields(deck_name):
    note_ids = mw.col.find_notes(f'deck:"{deck_name}"')
    if not note_ids:
        QMessageBox.information(mw, "No Notes", f"No notes found in deck '{deck_name}'")
        return None, None

    fields = mw.col.models.fieldNames(mw.col.getNote(note_ids[0]).model())

    word_field, ok = QInputDialog.getItem(mw, "Select Word Field", "Choose the field containing the word to count:", fields, 0, False)
    if not ok or not word_field:
        return None, None

    field_to_update, ok = QInputDialog.getItem(mw, "Select Field to Update", "Choose a field to update with word count:", fields, 0, False)
    if not ok or not field_to_update:
        return None, None

    return word_field, field_to_update

def select_folder():
    folder_path = QFileDialog.getExistingDirectory(mw, "Select Subtitles Folder")
    if not folder_path:
        return None
    return folder_path

def show_progress_dialog(total):
    progress_dialog = QProgressDialog("Counting word appearances...", "Cancel", 0, total, mw)
    progress_dialog.setWindowTitle("Processing")
    progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
    progress_dialog.setMinimumDuration(0)
    progress_dialog.forceShow()
    return progress_dialog

def update_progress(progress_dialog, current, total, processed, skipped, avg_speed, est_time):
    progress_dialog.setLabelText(f"Processed {current}/{total} notes\n"
                                 f"Processed: {processed}, Skipped: {skipped}\n"
                                 f"Average speed: {avg_speed:.2f} notes/second\n"
                                 f"Estimated time remaining: {est_time:.2f} seconds")
    progress_dialog.setValue(current)