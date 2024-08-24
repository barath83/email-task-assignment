from sqlalchemy.exc import IntegrityError


def save_emails(session, emails, Email):
    ingest_count = 0
    for email in emails:
        new_email = Email(**email)
        try:
            session.add(new_email)
            session.commit()
            ingest_count += 1
        except IntegrityError:
            session.rollback()
    return ingest_count