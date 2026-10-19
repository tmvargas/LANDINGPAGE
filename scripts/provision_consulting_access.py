#!/usr/bin/env python3
"""Provisiona a conta exclusiva da apresentação, com seleção de ambiente fail-closed."""

import argparse
import os
import sys

from sqlalchemy import select, text


def _required_environment(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Variável obrigatória ausente: {name}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-database", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    _required_environment("DATABASE_URL")
    initial_password = _required_environment("LANDINGPAGE_INITIAL_PASSWORD")

    # A aplicação só pode ser importada após a conexão explícita ser exigida.
    from app import create_app
    from app.db import db
    from app.models.application import Application, user_applications
    from app.models.user import User

    app = create_app("production")
    with app.app_context():
        database_name, server_address, database_user = db.session.execute(
            text("SELECT current_database(), inet_server_addr()::text, current_user")
        ).one()
        print(
            f"Ambiente confirmado: database={database_name} "
            f"server={server_address} user={database_user}"
        )
        if database_name != args.expected_database:
            raise RuntimeError(
                f"Banco divergente: esperado={args.expected_database} efetivo={database_name}"
            )

        normalized_email = args.email.strip().lower()
        if db.session.scalar(select(User).where(User.email == normalized_email)) is not None:
            raise RuntimeError("Provisionamento interrompido: usuário já existe")
        if db.session.scalar(select(Application).where(Application.code == "consultoria-ps")) is not None:
            raise RuntimeError("Provisionamento interrompido: aplicação já existe")

        try:
            user = User(email=normalized_email, name=args.name.strip(), is_active_account=True)
            user.set_password(initial_password)
            application = Application(
                code="consultoria-ps",
                name="Apresentação Consultoria PlanSmart",
                description="Apresentação comercial privada da Consultoria PlanSmart.",
                url="/staging/landingpage/apresentacao/consultoria",
                sort_order=10,
                is_active=True,
            )
            db.session.add_all([user, application])
            db.session.flush()
            db.session.execute(
                user_applications.insert().values(
                    user_id=user.id,
                    application_id=application.id,
                )
            )
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        counts = db.session.execute(
            text(
                "SELECT "
                "(SELECT count(*) FROM users WHERE email = :email), "
                "(SELECT count(*) FROM applications WHERE code = 'consultoria-ps'), "
                "(SELECT count(*) FROM user_applications ua "
                " JOIN users u ON u.id = ua.user_id "
                " JOIN applications a ON a.id = ua.application_id "
                " WHERE u.email = :email AND a.code = 'consultoria-ps')"
            ),
            {"email": normalized_email},
        ).one()
        print(f"Validação: users={counts[0]} applications={counts[1]} grants={counts[2]}")
        if tuple(counts) != (1, 1, 1):
            raise RuntimeError("Validação pós-escrita divergente")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        raise SystemExit(1)
