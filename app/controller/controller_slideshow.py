#!/usr/bin/python

from bible_api.bibleapi import bible_api
from pptx import Presentation

class ControllerSlideshow:

	def __init__(self):
		self._bibleAPI = bible_api.BibleAPI()
		self._bibleAPI.getBibleVersions()
		self._bibleAPI.getBibleBooks()

	@property
	def bibleAPI(self):
		return self._bibleAPI

	@bibleAPI.setter
	def bibleAPI(self, bibleAPI):
		self._bibleAPI = bibleAPI

	def getDataVerse(self, version = '', book = '', chapter = '', verse = ''):
		if (version and book and chapter and verse):
			self._bibleAPI.currentVersion = version
			self._bibleAPI.currentBook = book
			self._bibleAPI.currentChapter = chapter
			self._bibleAPI.currentVerse = verse

		verse_content = self._bibleAPI.getVerse(
				self._bibleAPI.currentVersion,
				self._bibleAPI.currentBook,
				self._bibleAPI.currentChapter,
				self._bibleAPI.currentVerse
		)

		return {
			"version": self._bibleAPI.bibleVersions[self._bibleAPI.currentVersion],
			"book": self._bibleAPI.bibleBooks[self._bibleAPI.currentBook],
			"chapter": self._bibleAPI.currentChapter,
			"verse": self._bibleAPI.currentVerse,
			"verse_content": verse_content
		}

	def nextVerse(self):
		next_verse = int(self._bibleAPI.currentVerse) + 1
		self._bibleAPI.currentVerse = str(next_verse)

	def previousVerse(self):
		previous_verse = int(self._bibleAPI.currentVerse) - 1
		self._bibleAPI.currentVerse = str(previous_verse)

	def getBibleVersions(self):
		return self._bibleAPI.bibleVersions

	def getBibleBooks(self):
		return self._bibleAPI.bibleBooks
	
	def getBibleChaptersKeys(self, version, book):
		book_chapters = self._bibleAPI.getVersesFromBook(self, version, book)
		return book_chapters.keys()

	def getBibleVersesKeys(self, version, book, chapter):
		book_chapters = self._bibleAPI.getVersesFromBook(self, version, book)
		chapter_verses = book_chapters[chapter]
		return chapter_verses.keys()
