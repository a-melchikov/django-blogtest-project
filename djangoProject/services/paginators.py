from typing import List, Any
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


class GeneralPaginator:
    """
    Класс для разбивки списка объектов на страницы.
    """

    def __init__(self, objects: List[Any], per_page: int = 5):
        """
        Инициализирует экземпляр класса GeneralPaginator.

        args:
            objects (List[Any]): Список объектов для разбиения на страницы.
            per_page (int, optional): Количество объектов на странице. По умолчанию 5.
        """
        self.objects = objects
        self.per_page = per_page
        self.paginator = Paginator(objects, per_page)

    def get_page(self, page_number: int) -> Paginator:
        """
        Возвращает объект Paginator для указанной страницы.

        args:
            page_number (int): Текущий номер страницы.

        return:
            Paginator: Объект Paginator, содержащий объекты для указанной страницы.
        """
        try:
            page_obj = self.paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = self.paginator.page(1)
        except EmptyPage:
            page_obj = self.paginator.page(self.paginator.num_pages)
        return page_obj
