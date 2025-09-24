from main import BooksCollector
import pytest


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # Пример теста (исправлен: get_books_rating → get_books_genre)
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    # 1. Добавление одной книги (успех)
    def test_add_new_book_success(self):
        collector = BooksCollector()
        collector.add_new_book("Гарри Поттер")
        assert "Гарри Поттер" in collector.get_books_genre()
        assert collector.get_books_genre()["Гарри Поттер"] == ''

    # 2. Не добавляется дубликат книги
    def test_add_new_book_duplicate_not_added(self):
        collector = BooksCollector()
        collector.add_new_book("Гарри Поттер")
        collector.add_new_book("Гарри Поттер")
        assert len(collector.get_books_genre()) == 1

    # 3. Книга длиннее 40 символов не добавляется
    def test_add_new_book_too_long_name_not_added(self):
        collector = BooksCollector()
        long_name = "A" * 41
        collector.add_new_book(long_name)
        assert long_name not in collector.get_books_genre()

    # 4. Установка и получение жанра
    def test_set_and_get_book_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Детектив")
        collector.set_book_genre("Детектив", "Детективы")
        assert collector.get_book_genre("Детектив") == "Детективы"

    # 5. Получение книг по жанру (параметризация через pytest внутри класса)
    @pytest.mark.parametrize("genre", ["Фантастика", "Комедии", "Мультфильмы"])
    def test_get_books_with_specific_genre(self, genre):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.set_book_genre("Книга1", genre)
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга2", "Ужасы")

        result = collector.get_books_with_specific_genre(genre)
        assert "Книга1" in result
        assert "Книга2" not in result

    # 6. Книги для детей исключают жанры с возрастным рейтингом
    def test_get_books_for_children_excludes_age_rating(self):
        collector = BooksCollector()
        collector.add_new_book("Мульт")
        collector.set_book_genre("Мульт", "Мультфильмы")
        collector.add_new_book("Ужас")
        collector.set_book_genre("Ужас", "Ужасы")

        children_books = collector.get_books_for_children()
        assert "Мульт" in children_books
        assert "Ужас" not in children_books

    # 7. Добавление книги в избранное
    def test_add_book_in_favorites(self):
        collector = BooksCollector()
        collector.add_new_book("Любимая книга")
        collector.add_book_in_favorites("Любимая книга")
        assert "Любимая книга" in collector.get_list_of_favorites_books()

    # 8. Удаление книги из избранного
    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book("Удаляемая")
        collector.add_book_in_favorites("Удаляемая")
        collector.delete_book_from_favorites("Удаляемая")
        assert "Удаляемая" not in collector.get_list_of_favorites_books()

    # 9. Получение списка избранного
    def test_get_list_of_favorites_books_returns_correct_list(self):
        collector = BooksCollector()
        collector.add_new_book("Фаворит")
        collector.add_book_in_favorites("Фаворит")
        favorites = collector.get_list_of_favorites_books()
        assert favorites == ["Фаворит"]

    # 10. Полный сценарий: добавление → жанр → избранное → детям
    def test_full_scenario(self):
        collector = BooksCollector()
        collector.add_new_book("Мультфильм")
        collector.add_new_book("Детектив")
        collector.set_book_genre("Мультфильм", "Мультфильмы")
        collector.set_book_genre("Детектив", "Детективы")
        collector.add_book_in_favorites("Мультфильм")

        assert collector.get_book_genre("Мультфильм") == "Мультфильмы"
        assert "Мультфильм" in collector.get_books_for_children()
        assert "Мультфильм" in collector.get_list_of_favorites_books()
        assert "Детектив" not in collector.get_books_for_children()
        # Нет фикстур через @pytest.fixture, потому что по условию в каждом тесте создаётся отдельный экземпляр и это правильно для изоляции.