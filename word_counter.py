import os
import re
import time
from aqt import mw
from aqt.qt import QMessageBox
from .ui import select_deck, select_fields, select_folder, show_progress_dialog, update_progress

def read_srt_files(folder_path):
    subtitles_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".srt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                subtitles_text += file.read().lower() + " "
    return subtitles_text

def count_word_occurrences(word, text):
    count = 0
    word = word.lower()
    word_forms = [word, word + "s", word + "es", word + "ed", word + "ing"]
    for form in word_forms:
        count += len(re.findall(r'\b' + re.escape(form) + r"(?:'s|-\w+)*\b", text))
    return count

def count_word_appearances(deck_name, word_field, field_to_update, folder_path):
    subtitles_text = read_srt_files(folder_path)
    note_ids = mw.col.find_notes(f'deck:"{deck_name}"')
    
    total_notes = len(note_ids)
    processed_notes = 0
    skipped_notes = 0
    start_time = time.time()

    progress_dialog = show_progress_dialog(total_notes)

    for current, note_id in enumerate(note_ids, 1):
        if progress_dialog.wasCanceled():
            break

        note = mw.col.getNote(note_id)
        if note[field_to_update].strip():
            skipped_notes += 1
            continue

        word = note[word_field]
        appearances = count_word_occurrences(word, subtitles_text)
        
        note[field_to_update] = str(appearances)
        note.flush()

        processed_notes += 1

        elapsed_time = time.time() - start_time
        avg_speed = processed_notes / elapsed_time if elapsed_time > 0 else 0
        remaining_notes = total_notes - current
        est_time = remaining_notes / avg_speed if avg_speed > 0 else 0

        update_progress(progress_dialog, current, total_notes, processed_notes, skipped_notes, avg_speed, est_time)

    progress_dialog.close()

    mw.col.save()
    QMessageBox.information(mw, "Process Completed", 
                            f"Total notes: {total_notes}\n"
                            f"Processed notes: {processed_notes}\n"
                            f"Skipped notes: {skipped_notes}")

def count_words():
    deck_name = select_deck()
    if not deck_name:
        return

    word_field, field_to_update = select_fields(deck_name)
    if not word_field or not field_to_update:
        return

    folder_path = select_folder()
    if not folder_path:
        return

    count_word_appearances(deck_name, word_field, field_to_update, folder_path)

    mw.reset()