# Projeto Quiz-Comp

## Descrição

O presente projeto visa ao desenvolvimento de um sistema para... `TODO`.

- Responsável: Murilo de Jesus Santos Silva (@murilojssilva)
- Orientadores: Fabiano Oliveira (@fabiano.oliveira) e Marcelo Schots (@marceloschots)

## Tutorial de instalação do Sistema de Provas do ENADE

### Windows

Django é um framework web que roda a linguagem de programação Python. Para isso, deve-se primeiramente deve-se instalar o Python. Acesse https://python.org/downloads/, selecione o Download Python 2.7.14 e procure por "Instalador Windows x86-64 MSI" (64 bits) ou "Instalador Windows x86 MSI" (32 bits) (Para saber se a sua versão do Windows é 32 ou 64 bits, clique com o botão direito no Menu Iniciar, Sistema e procure a informação "Tipo de Sistema"). Após a instalação do Python, vá no Menu Iniciar e acesse o prompt de comando (cmd), escreva `cd "../.."` e dê Enter. Após, escreva `python --version` e verifique se o Python 2.7 está instalado.

Após isso, instale o pip. Para isso, com o prompt de comando aberto, escreva `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py` e dê enter. Após isso, escreva no prompt de comando `python get-pip.py` e dê enter novamente.

Agora, deve-se instalar o virtualenv. Para isso, com o prompt de comando aberto, escreva `pip install virtualenvwrapper-win` e dê enter. Após isso, no prompt, escreva `mkvirtualenv myproject`. Após isso, é preciso ativar esse ambiente. Para isso, no prompt, escreva `workon myproject`.

Agora vamos instalar o Django. Para isso, no prompt, escreva `pip install django`. Após isso, copie a pasta do projeto no computador. Deixe em um diretório onde seja fácil de ser lembrado. Para acessá-lo, você deve utilizar o prompt de comando. Caso necessite acessar um diretório (caminho de pastas) escreva `cd /nome_da_pasta`. Após isso, escreva no prompt `python manage.py runserver` e acesse o seguinte endereço no navegador: http://localhost:8000.

### Ubuntu

Acesse o terminal e digite os seguintes comandos, na seguinte ordem (ignorando o caractere '$'):
``
$ sudo apt-get install python-django
$ python
$ import django; django.VERSION
$ sudo apt-get install subversion (Digite a senha do administrador)
$ svn co http://code.djangoproject.com/svn/django/trunk/ django-trunk
$ sudo ln -s `pwd`/django-trunk/django /usr/lib/python2.6/dist-packages/django
$ django-admin.py
``

Após isso, copie a pasta do projeto no computador. Deixe em um diretório onde seja fácil de ser lembrado. Para acessá-lo, você deve utilizar o terminal do Ubuntu. Escreva cd /nome_da_pasta. Após isso, escreva no prompt `python manage.py runserver` e acesse no navegador o endereço http://localhost:8000.
