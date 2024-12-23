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

O tempo de validade do token é de 30 minutos, após isso é possível renová-lo o token `refresh`. Para isso basta enviar um *json* com esse campo do seguinte modo em `POST /auth/token/refresh/`:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNTA3NzIwMSwiaWF0IjoxNzM0OTkwODAxLCJqdGkiOiJlMmIxM2QzMDg0ODM0Mzg0ODhjODIzMzRhMTczNjYzMyIsInVzZXJfaWQiOjE4fQ.yks3orpHJXucBJa5HMfPD0W1fnYHvjmjXA_O3INWhNI"
}
```

Para utilizar o token JWT em outros endpoints da API basta clicar no botão *Authorize* na parte de cima da página, forcener o token e autenticar-se. Após isso, enquanto esse token for válido será possível utilizar os outros recursos da API.

#### Posts

Para criar um novo post é necessário estar autenticado e enviar o seguinte *json* na requisição:

```json
{
  "content": "Hello!"
}
```

Alguns campos do post já serão preenchidos automaticamente pela aplicação, como o autor e a data de criação.

Para atualizar, deletar ou obter um único post basta realizar uma requisão http do tipo `PATCH` ou `PUT`, `DELETE` e `GET`, respectivamente, fornecendo o `id` do post em `/post/{id}/`.

Também é possível obter todos os posts publicados em `GET /posts/`, ordenados pela data de criação, do mais recente para os mais antigos, com uma paginação de 30 elementos por página. Também é possível filtrar os posts pelo nome do author e pelo seu conteúdo.

Um elemento que representa um post conterá o seu *id*, conteúdo, data de criação e atualização, autor, número de likes e comentários e um array contendo todos os comentários.

Para dar like em um post basta enviar uma requisição `POST` em `/posts/{id}/like/` e para remover o like basta fazer uma requisição `DELETE` no mesmo endereço. Para verificar se o usuário curtiu ou não o post basta fazer uma requisição do tipo `GET`.

Para selecionar todos os posts que o usuário curtiu basta fazer uma requisição `GET` em `/posts/liked/`.

#### Comentários

Para criar um comentário é necessário estar autenticado e fornecer um *json* com o conteúdo do comentário e o *id* do post em `/comments/` da seguinte forma:

```json
{
  "comment": "Nice post",
  "post_id": 1
}
```

Também é possível atualizar, obter um único ou excluir um comentário enviando o seu *id* em `/comments/{id}` via uma requisição `PATCH` ou `PUT`, `GET` e `DELETE`, respectivamente. É importante notar que só é possível atualizar um comentário até no máximo 1 hora após a sua data de criação.