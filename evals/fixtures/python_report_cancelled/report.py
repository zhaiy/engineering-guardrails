"""Small order-count adapter used by the dashboard."""

def summarize(rows):
    """Consume order dictionaries, including streaming query results."""
    counts = {"total": 0, "paid": 0, "open": 0}
    for row in rows:
        counts["total"] += 1
        status = row.get("status")
        if status in ("paid", "open"):
            counts[status] += 1
    return counts
