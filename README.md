# LANDINGPAGE PlanSmart

Aplicação Flask institucional da PlanSmart, com PostgreSQL, autenticação e
controle de acesso às aplicações da empresa.

## Executar localmente

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
export FLASK_APP=run.py
export FLASK_ENV=development
export SECRET_KEY='configure-em-segredo'
export DATABASE_URL='postgresql://usuario:senha@host/banco'
flask run --port 5106
```

Staging e produção devem usar bancos, usuários, variáveis, serviços, checkouts,
logs e portas separados. Não execute migrations sem a autorização específica
registrada na tarefa.
