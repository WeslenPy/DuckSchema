from __future__ import annotations

import typing as t
from math import ceil


class Pagination:


    def __init__(
        self,
        page: int | None = None,
        per_page: int | None = None,
        max_per_page: int | None = 100,
        error_out: bool = True,
        count: bool = True,
        **kwargs: t.Any,
    ) -> None:
        self._query_args = kwargs

        self.page: int = page
        """The current page."""

        self.per_page: int = per_page
        """The maximum number of items on a page."""

        self.max_per_page: int | None = max_per_page
        """The maximum allowed value for ``per_page``."""

        items = self._query_items()

        if not items and page != 1 and error_out:
            return None

        self.items: list[t.Any] = items
        """The items on the current page. Iterating over the pagination object is
        equivalent to iterating over the items.
        """

        if count:
            total = self._query_count()
        else:
            total = None

        self.total: int | None = total
        """The total number of items across all pages."""

  

    @property
    def _query_offset(self) -> int:
    
        return (self.page - 1) * self.per_page

    def _query_items(self) -> list[t.Any]:
     
        raise NotImplementedError

    def _query_count(self) -> int:
        
        raise NotImplementedError

    @property
    def first(self) -> int:
        if len(self.items) == 0:
            return 0

        return (self.page - 1) * self.per_page + 1

    @property
    def last(self) -> int:
 
        first = self.first
        return max(first, first + len(self.items) - 1)

    @property
    def pages(self) -> int:
        if self.total == 0 or self.total is None:
            return 0

        return ceil(self.total / self.per_page)

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    @property
    def prev_num(self) -> int | None:
        if not self.has_prev:
            return None

        return self.page - 1

    def prev(self, *, error_out: bool = False) -> Pagination:

        p = type(self)(
            page=self.page - 1,
            per_page=self.per_page,
            error_out=error_out,
            count=False,
            **self._query_args,
        )
        p.total = self.total
        return p

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def next_num(self) -> int | None:
        if not self.has_next:
            return None

        return self.page + 1

    def next(self, *, error_out: bool = False) -> Pagination:

        p = type(self)(
            page=self.page + 1,
            per_page=self.per_page,
            max_per_page=self.max_per_page,
            error_out=error_out,
            count=False,
            **self._query_args,
        )
        p.total = self.total
        return p

    def iter_pages(
        self,
        *,
        left_edge: int = 2,
        left_current: int = 2,
        right_current: int = 4,
        right_edge: int = 2,
    ) -> t.Iterator[int | None]:
       
        pages_end = self.pages + 1

        if pages_end == 1:
            return

        left_end = min(1 + left_edge, pages_end)
        yield from range(1, left_end)

        if left_end == pages_end:
            return

        mid_start = max(left_end, self.page - left_current)
        mid_end = min(self.page + right_current + 1, pages_end)

        if mid_start - left_end > 0:
            yield None

        yield from range(mid_start, mid_end)

        if mid_end == pages_end:
            return

        right_start = max(mid_end, pages_end - right_edge)

        if right_start - mid_end > 0:
            yield None

        yield from range(right_start, pages_end)

    def __iter__(self) -> t.Iterator[t.Any]:
        yield from self.items

class QueryPagination(Pagination):

    def _query_items(self) -> list[t.Any]:
        query = self._query_args["query"]
        out = query.limit(self.per_page).offset(self._query_offset).all()
        return out  

    def _query_count(self) -> int:
        out = self._query_args["query"].order_by(None).count()
        return out  