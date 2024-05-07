# Changelog
Alle nennenswerten Änderungen an diesem Projekt werden in dieser Datei dokumentiert.


## [1.0.0] - 07.05.2024

### Neue Funktionen
- Hinzufügen von Aufgaben: Benutzer können jetzt neue Aufgaben hinzufügen.
- Löschen von Aufgaben: Benutzer können Aufgaben aus der Liste, nach einer Bestätigung, löschen.
- Bearbeiten von Aufgaben: Benutzer können den Namen einer Aufgabe bearbeiten.
- Ändern des Aufgabenstatus: Benutzer können den Status einer Aufgabe zwischen "nicht abgeschlossen"
und "abgeschlossen" ändern.

### Verbesserungen
- GUI-Optimierungen: Verbesserungen der Benutzeroberfläche für eine bessere Benutzererfahrung.
- Codeoptimierungen: Optimierungen und Bereinigungen im Code für eine bessere Lesbarkeit und Wartbarkeit.


## Änderungen vor der Basisversion

### 07.05.2024
Refaktorierung: Timer hinzugefügt und Methoden überarbeitet

pomodoriTimer.py:
- Neue Datei erstellt für den Pomodoro-Timer
- Hinzufügen von Methoden zur Steuerung des Timers und deren Speicherung

main.py:
- Hinzufügen einer Methode zur Auswahl des Timers
- Hinzufügen einer Methode zum Starten des Timers

allTask.py:
- Überarbeitung der Scroll-Methode, um Überschneidungen im Hauptfenster zu vermeiden


### 06.05.2024
Refaktorierung: Hinzufügen einer Scrollleiste in main.py

main.py:
- Neue Methode __create_scrollbar für die Erstellung der Scrollleiste hinzugefügt
- Hinzufügen eines neuen Frames für das Treeview und die Scrollleiste
- Entfernen der Methode „expand“ von __tree_frame und __tree
- Festlegen der Höhe des Treeview auf 10


### 06.05.2024
Refaktorierung: Hinzufügen einer Scrollleiste in allTask.py

allTask.py
- Neue Methode __create_scrollbar zur Erstellung der Scrollleiste hinzugefügt
- Neue Methode __setup_window zur Erstellung und Ausführung der Methoden hinzugefügt
- Neue Methode __on_mouse_wheel zum scrollen im Fenster hinzugefügt
- Neue Methode __resize_window zum Anpassen der Fenstergröße hinzugefügt


### 04.05.2024
Refaktorierung: Hinzufügen neuer Methoden und Überarbeitung bestehender Funktionen

main.py:
- Neue Methode hinzugefügt: __resize_window zur Anpassung der Fenstergröße
- Überarbeitete Methode: __create_list zur Anpassung der Breite der ersten Spalte

newTask.py:
- Überarbeitete Methode: __save_data zur Anpassung der Breite der ersten Spalte nach dem Speichern

allTask.py:
- Verschoben in den Ordner AllTask
- Klasse von AllTask zu AllTaskGUI umbenannt
- Methoden __change_stat, __delete und __edit nach controller.py verschoben

controller.py:
- Neue Datei erstellt: controller.py im Ordner AllTask enthält Funktionen aus allTask.py


### 03.05.2024
allTask.py: Neue Methode __change_tag hinzugefügt und __delete überarbeitet
- Neue Methode __change_tag hinzugefügt, um die Farbe vom Treeview anzupassen
- Methode __delete überarbeitet, um die Aufgabe vollständig zu löschen


### 03.05.2024
added, data.py, newTask.py, allTask.py