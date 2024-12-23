# Mini Twitter

Esse prejeto consiste no desafio dos trainees em desenvolvimento backend da [EJECT](https://www.ejectufrn.com.br/) que tinha como objetivo a construção de uma API Rest de um mini twitter.

Nessa API será possível realizar a criação de usuários, autenticação utilizando *JSON Web Token*, além de criar, comentar e curtir um post.

## Instalação e Execução

> Para executar esse projeto é necessário ter o Python instalado em sua máquina. Acesse [python.org/downloads](https://www.python.org/downloads/) para mais detalhes de como fazer isso.

1. Faça o clone do repositório e acesse o diretório do projeto:
    ```
    git clone https://github.com/arthurcostaa/mini_twitter.git
    cd mini_twitter
    ```
2. Crie e ative um ambiente virtual utlizando o [venv](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)
    ```
    python -m venv venv
    source venv/bin/activate
    ```
3. Instale os pacote do arquivo `requirements.txt`:
    ```
    pip install -r requirements.txt
    ```
4. Execute as migrações:
    ```
    python manage.py migrate
    ```
5. Crie um superusuário:
   ```
   python manage.py createsuperuser
   ```
6. Execute o projeto:
    ```
    python manage.py runserver
    ```

## Documentação com Swagger e Redoc

Para acessar a documentação com *Swagger* acesse o endereço `http://localhost:8000/swagger/` e para acessar a documentação com *Redoc* acesse `http://localhost:8000/redoc/`.

### Interagindo com a API via Swagger

#### Criação de usuários

Para criar um usuário acesse a seção *users* e `POST /users/` e forneça um *json* com o `email`, `username` e `password`, da seguinte forma:

```json
{
  "email": "johndoe@email.com",
  "username": "johndoe",
  "password": "Strong#Password123"
}
```

#### Autenticação JWT e Refresh do token

Boa parte dos endpoints da API exigem autenticação com token JWT. Para obter o token acesse a seção *auth* e `POST /auth/token/` e envie um *json* com `username` e `password`, da seguinte forma:

```json
{
  "username": "johndoe",
  "password": "Strong#Password123"
}
```

Será retornado um *json* com os campos `refresh` e `access` como o seguinte:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNTA3NzIwMSwiaWF0IjoxNzM0OTkwODAxLCJqdGkiOiJlMmIxM2QzMDg0ODM0Mzg0ODhjODIzMzRhMTczNjYzMyIsInVzZXJfaWQiOjE4fQ.yks3orpHJXucBJa5HMfPD0W1fnYHvjmjXA_O3INWhNI",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0OTkyNjAxLCJpYXQiOjE3MzQ5OTA4MDEsImp0aSI6ImFiMDg0NmU1YWViNDRjYWZhNDJkMzQ0N2IxM2U3N2Y2IiwidXNlcl9pZCI6MTh9.2eo0ParLgPZ0M0EyS9n5QiHyBoEuiusNwxqqugE2ooc"
}
```

O tempo de validade do token é de 30 minutos, após isso é possível renová-lo o token `refresh`. Para isso basta enviar um *json* com esse campo do seguinte modo:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNTA3NzIwMSwiaWF0IjoxNzM0OTkwODAxLCJqdGkiOiJlMmIxM2QzMDg0ODM0Mzg0ODhjODIzMzRhMTczNjYzMyIsInVzZXJfaWQiOjE4fQ.yks3orpHJXucBJa5HMfPD0W1fnYHvjmjXA_O3INWhNI"
}
```

Para utilizar o token JWT em outros endpoints da API basta clicar no botão *Authorize* na parte de cima da página, forcener o token e autenticar-se. Após isso, enquanto esse token for válido será possível utilizar os outros recursos da API.