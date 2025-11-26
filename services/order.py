from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict[str, int]],
        username: str,
        date: str = None
) -> Order:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
    if date:
        Order.objects.filter(id=order.id).update(created_at=date)

    ticket_instances = list()
    for ticket_data in tickets:
        (ticket := Ticket(
            row=ticket_data.get("row"),
            seat=ticket_data.get("seat"),
            movie_session_id=ticket_data.get("movie_session"),
            order=order
        )).full_clean()
        ticket_instances.append(ticket)

    Ticket.objects.bulk_create(ticket_instances)

    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
