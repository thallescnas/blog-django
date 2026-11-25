# Jornal Maricaense

Aplicacao web de blog multi-organizacao desenvolvida com Django, Django REST Framework e PostgreSQL, utilizando Docker Compose.

## Pre-requisitos

- Docker
- Docker Compose

## Configuracao do ambiente

Edite o arquivo `.env.EXAMPLE` na raiz do projeto com os valores desejados e renomeie-o para `.env`.

## Como iniciar o projeto

1. Suba os containers e aplique as migracoes automaticamente:

```bash
docker compose up --build -d
```

2. Em outro terminal, crie um superusuario para acessar o painel administrativo e o sistema:

```bash
docker compose exec django python manage.py createsuperuser
```

3. Vincule o superusuario a uma organizacao:
   - Acesse `http://localhost:8000/admin/` e faca login com o superusuario criado.
   - Em **Core > Perfis**, crie um novo perfil associando o seu usuario a uma **Organizacao** (por exemplo, `Organizacao padrao`) com o papel **Administrador**.
   - Sem um perfil vinculado a uma organizacao, o acesso as paginas do blog retornara `403 Forbidden`.

## Executando os testes

```bash
docker compose run --rm django python manage.py test posts
```
