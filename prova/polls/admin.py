from django.contrib import admin

from .models import Prova

from .models import Questao

from .models import Opcao

from .models import Usuario

from .models import Resposta

from .models import Historico

from .models import Categoria

admin.site.register(Prova)

admin.site.register(Questao)

admin.site.register(Opcao)

admin.site.register(Usuario)

admin.site.register(Resposta)

admin.site.register(Historico)

admin.site.register(Categoria)