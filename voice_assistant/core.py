import sqlite3

import speech_recognition as sr
import google_speech
from .databases import Database


class Assistant:
    """
    Allows to build an assistant, which can:
    - Speak (in different languages)
    - Listen (in different languages)
    - Remember last recognised words
    - Recognise a word in last recognised words
    - Memorize keyword-value pairs
    - Remember values from keywords
    """

    def __init__(self, language='en', database_name='memory', memory_table='memory', listen_log_table='listen_log'):
        self.speak_language = language
        self.listen_language = language
        self.last_recognised = ''

        # Database connection and table creation
        self.DATABASE_NAME = database_name
        self.MEMORY_TABLE = memory_table
        self.LISTEN_LOG_TABLE = listen_log_table

        self.database = Database(database_name='./{}.sqlite'.format(self.DATABASE_NAME))
        self._create_initial_tables()

        # Recognizer and microphone initialization
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.adjust_for_ambient_noise()
        # print('Energy: {}'.format(self.recognizer.energy_threshold))

    def _create_initial_tables(self):
        """Creates initial tables in the database."""

        tables = self.database.get_table_names()

        if self.MEMORY_TABLE not in tables:
            self.database.create_table(table_name=self.MEMORY_TABLE, columns={'key': 'TEXT', 'value': 'TEXT'})

        if self.LISTEN_LOG_TABLE not in tables:
            self.database.create_table(table_name=self.LISTEN_LOG_TABLE, columns={'sentence': 'TEXT'})

    def adjust_for_ambient_noise(self):
        """Listen to get a representative sample of the ambient noise and adjust to be more precise."""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def speak(self, text, language=None):
        speak_language = language if language else self.speak_language
        google_speech.main(text, speak_language, None)

    def listen(self, language=None):
        listen_language = language if language else self.listen_language
        recognised = ''

        with self.microphone as source:
            audio = self.recognizer.listen(source)
            try:
                recognised = self.recognizer.recognize_google(audio, language=listen_language)
                self.database.insert_into(table_name=self.LISTEN_LOG_TABLE, values={'sentence': recognised})
                print('"{}"'.format(recognised))
            except sr.UnknownValueError:
                # Google Speech Recognition could not understand audio
                print('Error: Assistant could not understand audio')
            except sr.RequestError as e:
                # Could not request results from Google STT
                print('Error: Could not request results from server; {}'.format(e))
            except Exception as e:
                print('Unknown error occurred: {}'.format(e))
            finally:
                self.last_recognised = recognised

    def has_heard(self, words):
        """
        The idea behind this function is to support a single word, a list of words or even a regex expression.
        Now regex is not supported.
        """
        if type(words) is str:
            return words in self.last_recognised
        else:
            return any(word in self.last_recognised for word in words)

    def memorize(self, keyword, value):
        """ Memorize a keyword value pair."""
        self.database.insert_into(table_name=self.MEMORY_TABLE, values={'key': keyword, 'value': value})

    def remember(self, keyword):
        """Returns the memorized value of the given keyword."""
        # TODO: This should use a 'Database' class method and not access directly to the cursor.
        try:
            self.database.cursor.execute('SELECT value FROM {} WHERE key="{}"'.format(self.MEMORY_TABLE, keyword))
        except sqlite3.OperationalError:  # Key doesn't exist
            return []

        result = self.database.cursor.fetchall()
        return [sentence for sublist in result for sentence in sublist]

    def remember_last(self, key):
        # TODO: This could be improved querying directly to database instead of calling 'remember' method.
        try:
            return self.remember(key)[-1]
        except IndexError:
            return ''

    def get_all_listened_words(self):
        # TODO: This should use a 'Database' class method and not access directly to the cursor.
        self.database.cursor.execute('SELECT * FROM {}'.format(self.LISTEN_LOG_TABLE))
        result = self.database.cursor.fetchall()
        return [sentence for sublist in result for sentence in sublist]

    def get_last_recognised_from_memory(self):
        # TODO: This could be improved querying directly to database instead of calling 'get_all_listened_words' method.
        try:
            return self.get_all_listened_words()[-1]
        except IndexError:
            return ''

    def forget_listened_words(self):
        # TODO: This should use a 'Database' class method and not access directly to the cursor.
        self.database.cursor.execute('DELETE FROM {}'.format(self.LISTEN_LOG_TABLE))
