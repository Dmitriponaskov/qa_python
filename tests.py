from main import BooksCollector
import pytest


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # Пример из задания (исправлен: get_books_rating → get_books_genre)
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    # 1. add_new_book: не добавляет дубликат
    def test_add_new_book_duplicate_not_added(self):
        collector = BooksCollector()
        collector.add_new_book("Гарри Поттер")
        collector.add_new_book("Гарри Поттер")
        assert len(collector.get_books_genre()) == 1

    # 2. add_new_book: не добавляет книгу длиннее 40 символов
    def test_add_new_book_too_long_name_not_added(self):
        collector = BooksCollector()
        long_name = "A" * 41
        collector.add_new_book(long_name)
        assert long_name not in collector.get_books_genre()

    # 3. set_book_genre: устанавливает жанр, если книга и жанр валидны
    def test_set_book_genre_valid(self):
        collector = BooksCollector()
        collector.add_new_book("Детектив")
        collector.set_book_genre("Детектив", "Детективы")
        assert collector.get_book_genre("Детектив") == "Детективы"

    # 4. get_book_genre: возвращает жанр книги
    def test_get_book_genre_returns_correct_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Мульт")
        collector.set_book_genre("Мульт", "Мультфильмы")
        assert collector.get_book_genre("Мульт") == "Мультфильмы"

    # 5. get_books_genre: возвращает полный словарь книг
    def test_get_books_genre_returns_full_dict(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга1", "Фантастика")
        result = collector.get_books_genre()
        assert result == {"Книга1": "Фантастика", "Книга2": ""}

    # 6. get_books_with_specific_genre: возвращает книги по жанру
    @pytest.mark.parametrize("genre", ["Фантастика", "Комедии"])
    def test_get_books_with_specific_genre(self, genre):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.set_book_genre("Книга1", genre)
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга2", "Ужасы")
        result = collector.get_books_with_specific_genre(genre)
        assert result == ["Книга1"]

    # 7. get_books_for_children: исключает жанры с возрастным рейтингом
    def test_get_books_for_children_excludes_age_rating(self):
        collector = BooksCollector()
        collector.add_new_book("Мульт")
        collector.set_book_genre("Мульт", "Мультфильмы")
        collector.add_new_book("Ужас")
        collector.set_book_genre("Ужас", "Ужасы")
        result = collector.get_books_for_children()
        assert result == ["Мульт"]

    # 8. add_book_in_favorites: добавляет книгу в избранное
    def test_add_book_in_favorites(self):
        collector = BooksCollector()
        collector.add_new_book("Любимая")
        collector.add_book_in_favorites("Любимая")
        assert collector.get_list_of_favorites_books() == ["Любимая"]

    # 9. delete_book_from_favorites: удаляет книгу из избранного
    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book("Удаляемая")
        collector.add_book_in_favorites("Удаляемая")
        collector.delete_book_from_favorites("Удаляемая")
        assert collector.get_list_of_favorites_books() == []

    # 10. get_list_of_favorites_books: возвращает список избранного
    def test_get_list_of_favorites_books_returns_list(self):
        collector = BooksCollector()
        collector.add_new_book("Фаворит")
        collector.add_book_in_favorites("Фаворит")
        assert collector.get_list_of_favorites_books() == ["Фаворит"]