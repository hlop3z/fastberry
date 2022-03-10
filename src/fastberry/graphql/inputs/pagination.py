import strawberry


@strawberry.input
class Pagination:
    page: int = 1
    limit: int = 100
    sort_by: str = "-id"
