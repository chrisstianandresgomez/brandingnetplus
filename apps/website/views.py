import smtplib
import subprocess
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template, render_to_string

from apps.website.forms import SuggestForm
from apps.website.functions import MiPaginador
from apps.website.models import Producto, WebSite, BannerPrincipal, Horario, Email, Telefono, Sugerencias, TipoProducto, \
    EnlacesGubernamentales, CategoriaSobreNosotros
from netpluswebsite import settings
from netpluswebsite.settings import EMAIL_HOST_USER


def view(request):
    data = {}
    data['sitio'] = sitio = WebSite.objects.first()
    data['logo_empresa_footer'] = '/static/logo_work.svg'
    data['logo_empresa_header'] = '/static/logo_work.svg'
    data['footer_image'] = "/static/headers/footer-bg.png"
    data['telefonowhastapp'] = "+593994695413"
    data['enlaces'] = EnlacesGubernamentales.objects.all()
    if request.method == 'POST':
        with transaction.atomic():
            if 'action' in request.POST:
                action = request.POST['action']

                if action == 'addsugest':
                    try:
                        data['form'] = form = SuggestForm(request.POST)
                        if form.is_valid():
                            if not float(form.cleaned_data['latitud']) <= 0 or float(form.cleaned_data['latitud']) >=0:
                                return JsonResponse({"result": "error", "mensaje": u"Error en la latitud"})
                            if not float(form.cleaned_data['longitud']) <= 0 or float(form.cleaned_data['longitud']) >=0:
                                return JsonResponse({"result": "error", "mensaje": u"Error en la longitud"})
                            form.save()
                            sug = Sugerencias.objects.all().order_by('-id').first()
                            data['sugerencia'] = sug
                            data['mensaje'] = True
                            data['logo_empresa_header'] = '/static/logov1.png'
                            send_html_mail('Nueva sugerencia recibida', data)
                            return JsonResponse({"result": "ok", "mensaje": u"Solicitud Incorrecta."})
                        else:
                            data['title'] = 'Contactos'
                            data['header_image'] = "/static/headers/banner_3.jpg"
                            data['idmenu'] = 46
                            data['classnav'] = 'hasBreadcrumbs  wrapper-navbar-layout-transparent ltx-pageheader-default'
                            data['horarios'] = Horario.objects.all()
                            data['correos'] = Email.objects.all()
                            data['telefonos'] = Telefono.objects.all()
                            data['form'] = form
                            return render(request, "contactos.html", data)


                    except Exception as e:
                        print(e)
                        transaction.set_rollback(True)
                elif action == 'test2':
                    result = subprocess.run(['speedtest-cli', '--json'], capture_output=True)
                    if result.returncode == 0:
                        return JsonResponse(result.stdout.decode())
                    else:
                        return JsonResponse({'error': 'Speedtest-cli error'})
        return JsonResponse({"result": "bad", "mensaje": u"Solicitud Incorrecta."})
    else:
        data['title'] = u'Matriculas de alumnos'
        if 'action' in request.GET:
            action = request.GET['action']

            if action == 'contactos':
                data['title'] = 'Contactos'
                data['header_image'] = "/static/headers/banner_3.jpg"
                data['idmenu'] = 46
                data['classnav'] = 'hasBreadcrumbs  wrapper-navbar-layout-transparent ltx-pageheader-default'
                data['horarios'] = Horario.objects.all()
                data['correos'] = Email.objects.all()
                data['telefonos'] = Telefono.objects.all()
                data['form'] = SuggestForm()
                return render(request, "contactos.html", data)
            elif action == 'productos':
                s = None
                url_vars = ''
                cat = 0
                if 's' in request.GET:
                    s = request.GET['s']
                    data['s'] = s
                    url_vars += '&s='+s
                if 'cat' in request.GET:
                    try:
                        cat = int(request.GET['cat'])
                        data['cat'] = cat
                        url_vars += '&cat=' + str(cat)
                    except Exception as e:
                        print(e)
                        cat = 0
                data['title'] = 'Productos'
                data['header_image'] = "/static/headers/banner_3_v2.jpg"
                data['idmenu'] = 619
                data['classnav'] = 'hasBreadcrumbs  wrapper-navbar-layout-transparent ltx-pageheader-default'
                productos = Producto.objects.filter(tipo__tipocategoria=1)
                data['categorias'] = categorias = TipoProducto.objects.filter(id__in=productos.values_list('tipo_id', flat=True).distinct()).distinct().order_by('descripcion')
                if cat:
                    productos = productos.filter(tipo_id=cat)
                if s:
                    productos = productos.filter(Q(nombre__icontains=s) | Q(descripcion__icontains=s))
                if 'order' in request.GET:
                    data['orderby'] = request.GET['order']
                    url_vars += '&order='+request.GET['order']
                    if request.GET['order'] == 'minus':
                        productos = productos.order_by('valor')
                    else:
                        productos = productos.order_by('-valor')
                else:
                    productos = productos.order_by('valor')

                totalpagina = 6

                paging = MiPaginador(productos, totalpagina)
                p = 1
                try:
                    paginasesion = 1
                    if 'paginador' in request.session:
                        paginasesion = int(request.session['paginador'])
                    if 'page' in request.GET:
                        p = int(request.GET['page'])
                    else:
                        p = paginasesion
                    try:
                        page = paging.page(p)
                    except:
                        p = 1
                    page = paging.page(p)
                except:
                    page = paging.page(p)
                request.session['paginador'] = p
                data['paging'] = paging
                data['rangospaging'] = paging.rangos_paginado(p)
                data['page'] = page
                data['listado'] = page.object_list
                data['totalpagina'] = len(page.object_list)
                data['list_count'] = len(productos)
                data['cat_sel'] = cat
                data['url_vars'] = url_vars
                return render(request, "productos.html", data)
            elif action == 'about':
                data['title'] = 'Acerca de nosotros'
                data['width_banner'] = 1400
                data['header_image'] = "/static/headers/banner-about-us.jpg"
                data['idmenu'] = 3557
                data['categorias'] = CategoriaSobreNosotros.objects.all()
                return render(request, "about_us.html", data)
            elif action == 'test2':
                result = subprocess.run(['speedtest-cli', '--json'], capture_output=True)
                if result.returncode == 0:
                    return JsonResponse(result.stdout.decode())
                else:
                    return JsonResponse({'error': 'Speedtest-cli error'})
            return HttpResponseRedirect(request.path)
        else:
            data['title'] = 'Website Net Plus'
            data['idmenu'] = 8571
            data['planes'] = planes = Producto.objects.filter(tipo__tipocategoria=0).order_by('valor')
            data['productos'] = Producto.objects.filter(tipo__tipocategoria=1).order_by('valor')
            data['banners'] = BannerPrincipal.objects.all().order_by('orden')
            return render(request, "index.html", data)



def send_html_mail(subject, data):
    try:
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        mailServer.starttls()
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        email_to = 'correonetplusec@gmail.com'
        mensaje = MIMEMultipart()
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = email_to
        mensaje['Subject'] = subject
        empresa = 'NET PLUS'
        content = render_to_string('emails/send_email.html', {'empresa': empresa, 'data': data})
        mensaje.attach(MIMEText(content, 'html'))
        mailServer.sendmail(settings.EMAIL_HOST_USER, email_to, mensaje.as_string())
    except Exception as ex:
        pass