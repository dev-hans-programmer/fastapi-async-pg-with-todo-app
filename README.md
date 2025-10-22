# Project setup
1. Created project using uv init
2. Added linter using ruff
3. Added pre commit hook
    1.After installing the package,  install the hook also: pre-commit install


# Integrate alembic for migration
1. Init alembic in the project: alembic init -t async migrations('migrations' is the folder name which will be created)
2. Set it up properly like seeting the sqlalchemy url and target in the env.py and .mako file of alembic
2. Now you can add or remove any field in the model and create a migration
3. Create a migration: alembic revision --autogenerate -m "Tables creation" - Creates a migration
4. Apply the migration: alembic upgrade head
5. alembic downgeade base - will delete all the tables
