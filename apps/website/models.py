from django.db import models


class WebSite(models.Model):
    descripcion = models.TextField(default='', verbose_name='Descripcion del sitio')
    mision = models.TextField(default='', verbose_name='Mision del sitio')
    vision = models.TextField(default='', verbose_name='Vision del sitio')
    logo = models.FileField(upload_to='logos', blank=True, null=True, verbose_name=u'Imagen de la empresa')

    def __str__(self):
        return '{}'.format(self.descripcion)

    class Meta:
        verbose_name = u"Sitio Web"
        verbose_name_plural = u'Sitios Web'

    def plan_minimo(self):
        return Producto.objects.filter(tipo__tipocategoria=0).order_by('valor').first() if Producto.objects.filter(tipo__tipocategoria=1).exists() else None


tipo_categoria = (
    (0, 'Plan'),
    (1, 'Producto'),
    (2, 'Servicio'),
)


class TipoProducto(models.Model):
    descripcion = models.TextField(default='', verbose_name='Descripcion del tipo de producto')
    tipocategoria = models.IntegerField(default=0, choices=tipo_categoria, verbose_name='Tipo de porducto, plan o servicio')

    def __str__(self):
        return '{}'.format(self.descripcion)

    class Meta:
        verbose_name = u"Tipo de producto"
        verbose_name_plural = u'Tipos de productos'


class Producto(models.Model):
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE, verbose_name='Tipo de producto', blank=True, null=True)
    descripcion = models.TextField(default='', verbose_name='Descripcion del producto', blank=True, null=True)
    nombre = models.CharField(max_length=50, verbose_name='Nombre del producto')
    valor = models.DecimalField(default=0, max_digits=30, decimal_places=2, verbose_name='Valor del producto')
    imagen = models.FileField(upload_to='imagenes', blank=True, null=True, verbose_name='Imagen del producto')
    incluyeiva = models.BooleanField(default=False, verbose_name='Incluye IVA')
    logohtml = models.CharField(max_length=50, verbose_name='Codigo html de logo', default='', blank=True, null=True)
    popular = models.BooleanField(default=False, verbose_name='Marcar como popular')

    def __str__(self):
        return '{} {}'.format(self.nombre, self.valor)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = 'Productos'

    def caracteristicas(self):
        return self.cararteristicaproducto_set.all().values_list('descripcion', flat=True)

    def nombre_completo_producto(self):
        return '{} {}'.format(self.tipo.get_tipocategoria_display(), self.nombre)


class CararteristicaProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Caracteristicas del producto', blank=True, null=True)
    descripcion = models.TextField(default='', verbose_name='Descripcion del producto', blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.producto, self.descripcion)

    class Meta:
        verbose_name = "Cararcteristica del Producto"
        verbose_name_plural = 'Cararcteristicas de los Productos'


TIPO_TELEFONO = (
    (0, 'CELULAR'),
    (1, 'CONVENCIONAL'),
)


class Telefono(models.Model):
    tipo = models.IntegerField(choices=TIPO_TELEFONO, default=0, verbose_name=u"Tipo de telefono")
    telefono = models.TextField(default='', verbose_name='Telefono 1')

    def __str__(self):
        return '{} - {}'.format(self.telefono, self.get_tipo_display())

    class Meta:
        verbose_name = "Telefono"
        verbose_name_plural = 'Telefonos'


class Email(models.Model):
    descripcion = models.TextField(default='', verbose_name='email')

    def __str__(self):
        return '{}'.format(self.descripcion)

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = 'Emails'

dias = (
    (0, 'LUNES'),
    (1, 'MARTES'),
    (2, 'MIERCOLES'),
    (3, 'JUEVES'),
    (4, 'VIERNES'),
    (5, 'SABADO'),
    (6, 'DOMINGO'),
)


class Horario(models.Model):
    dia1 = models.IntegerField(choices=dias, default=0, verbose_name="Dia 1 del horario")
    dia2 = models.IntegerField(choices=dias, default=4, verbose_name="Dia 2 del horario")
    hora1 = models.TimeField( null=True, blank=True, verbose_name="Hora 1 del horario")
    hora2 = models.TimeField( null=True, blank=True, verbose_name="Hora 2 del horario")

    def __str__(self):
        return '{} a {}'.format(self.get_dia1_display(), self.get_dia2_display())

    def get_dias(self):
        return '{} - {}'.format(self.get_dia1_display(), self.get_dia2_display())

    def get_hora_1(self):
        hora = self.hora1.hour-12 if self.hora1.hour > 12 else self.hora1.hour
        hora = '0{}'.format(hora) if hora < 10 else hora
        minutos = '0{}'.format(self.hora1.minute) if self.hora1.minute < 10 else self.hora1.minute
        simbol = 'am' if self.hora1.hour < 12 else 'pm'
        return '{}:{} {}'.format(hora, minutos, simbol)

    def get_hora_2(self):
        hora = self.hora2.hour-12 if self.hora2.hour > 12 else self.hora2.hour
        hora = '0{}'.format(hora) if hora < 10 else hora
        minutos = '0{}'.format(self.hora2.minute) if self.hora2.minute < 10 else self.hora2.minute
        simbol = 'am' if self.hora2.hour < 12 else 'pm'
        return '{}:{} {}'.format(hora, minutos, simbol)

    class Meta:
        verbose_name = "Horario de antencion"
        verbose_name_plural = 'Horarios de antencion'


class BannerPrincipal(models.Model):
    titulo = models.CharField(max_length=50, verbose_name='titulo del banner')
    subtitulo = models.CharField(max_length=50, verbose_name='titulo del banner')
    descripcion = models.TextField(default='', verbose_name='Descripcion del banner', blank=True, null=True)
    valor = models.DecimalField(default=0, max_digits=30, decimal_places=2, verbose_name='Valor en banner')
    imagen = models.FileField(upload_to='imagenes', blank=True, null=True, verbose_name='Imagen del banner')
    imagenul = models.TextField(default='', verbose_name='url de imagen en internet', blank=True, null=True)
    orden = models.IntegerField(default=1, verbose_name='orden de muestra')
    gratis = models.BooleanField(default=False, verbose_name='Promocion gratis')
    muestravalor = models.BooleanField(default=True, verbose_name='Muestra estiqueta del valor')

    def __str__(self):
        return '{}'.format(self.titulo)

    class Meta:
        verbose_name = "Banner principal"
        verbose_name_plural = 'Banners principales'

    def get_imagen(self):
        if not self.imagenul == '':
            return self.imagenul
        elif self.imagen:
            return self.imagen.url
        return ' '

    def get_valor(self):
        return self.valor

    def save(self, *args, **kwargs):
        if BannerPrincipal.objects.count() == 0:
            self.orden = 1
        else:
            contador = BannerPrincipal.objects.all().order_by('orden').last().orden
            self.orden = contador + 1  if not self.pk else  self.orden
        super(BannerPrincipal, self).save(*args, **kwargs)


class Sugerencias(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre completo')
    email = models.CharField(max_length=100, verbose_name='Correo',  blank=False, null=True)
    telefono = models.CharField(max_length=100, verbose_name='Telefono de contacto', blank=False, null=True)
    sugerencia = models.TextField(default='', verbose_name='Comentario o sugerencia')
    longitud = models.CharField(max_length=100,  verbose_name='Longitud',  blank=True, null=True)
    latitud = models.CharField(max_length=100,  verbose_name='Latiud',  blank=True, null=True)


class EnlacesGubernamentales(models.Model):
    descripcion = models.TextField(default='', verbose_name='Enlace', blank=True, null=True)
    imagen = models.FileField(upload_to='imagenes', blank=True, null=True, verbose_name='Archivo')
    url = models.TextField(default='', verbose_name='url', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.descripcion)

    class Meta:
        verbose_name = "Enlace"
        verbose_name_plural = 'Enlaces'


class CategoriaSobreNosotros(models.Model):
    titulo = models.TextField(default='', verbose_name='Titulo Categoria', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.titulo)

    def subcategorias(self):
        return self.subcategoriasobrenosotros_set.all()

    class Meta:
        verbose_name = "Categoria sobre nosotros"
        verbose_name_plural = 'Categorias sobre nosotros'


class SubCategoriaSobreNosotros(models.Model):
    categoria = models.ForeignKey(CategoriaSobreNosotros, on_delete=models.CASCADE, verbose_name='Caracteristicas del producto', blank=True, null=True)
    titulo = models.TextField(default='', verbose_name='Titulo subcategoria', blank=True, null=True)
    descripcion = models.TextField(default='', verbose_name='Descripcion subcategoria', blank=True, null=True)
    imagen = models.FileField(upload_to='imagenes', blank=True, null=True, verbose_name='Archivo')

    def __str__(self):
        return '{}'.format(self.descripcion)


    def get_imagen(self):
        return self.imagen.url if self.imagen else '/static/no_imagen.jpg'

    class Meta:
        verbose_name = "Sub Categoria sobre nosotros"
        verbose_name_plural = 'Sub Categorias sobre nosotros'



