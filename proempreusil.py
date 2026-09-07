import flet as ft
import random
import string
import re
import os

GOOGLE_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg"
PERU_FLAG_URL = "https://upload.wikimedia.org/wikipedia/commons/c/cf/Flag_of_Peru.svg"

db_global = {
    "usuarios": {
        "erickvitanciousil@gmail.com": {
            "nombre": "Erick",
            "password": "123",
            "origen": "Google"
        }
    },
    "sedes": {
        "Instituto de Emprendedores (Independencia)": [
            {
                "id": "p1",
                "nombre": "Puesto #01",
                "referencia": "Esq. Av. Industrial con Av. Pacífico (Puerta Principal IE)",
                "vendedor": "Don Carlos",
                "icon": ft.icons.STOREFRONT,
                "color": "#E05638"
            },
            {
                "id": "p2",
                "nombre": "Puesto #02",
                "referencia": "Av. Pacífico cdra 2 (Frente al paradero)",
                "vendedor": "Sra. María",
                "icon": ft.icons.SHOPPING_BAG,
                "color": "#1E88E5"
            },
            {
                "id": "p3",
                "nombre": "Puesto #03",
                "referencia": "Av. Industrial cdra 4 (Lado de la rotonda)",
                "vendedor": "Don Jorge",
                "icon": ft.icons.STORE,
                "color": "#2E7D32"
            }
        ]
    },
    "pedidos": [
        {
            "id": 1,
            "codigo": "DCE-73Y",
            "cliente": "Erick",
            "detalle": "1x Quinua, 1x Pan con Chicharrón",
            "sede": "Instituto de Emprendedores (Independencia)",
            "puesto": "Puesto #01 (Esq. Av. Industrial con Av. Pacífico)",
            "notas": "Sin mayonesa",
            "total": 4.00,
            "estado": "🟡 En Preparación",
            "pago": "Yape",
            "tiempo_espera": "Máx. 10 minutos"
        }
    ],
    "favoritos": []
}

def validar_correo(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None

def main(page: ft.Page):
    page.title = "Proyecto Empresarial USIL - Desayunos Express"
    page.bgcolor = "#FAFAFA"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    usuario_actual = {"nombre": "Invitado", "correo": "", "rol": "Cliente"}
    sede_actual = "Instituto de Emprendedores (Independencia)"
    puesto_seleccionado = db_global["sedes"][sede_actual][0]

    pedido_temporal = {"detalle": "", "total": 0.0, "metodo_pago": "Yape"}
    filtro_categoria = "Todos"
    busqueda_texto = ""
    vista_actual_cliente = "menu"
    vista_actual_cocina = "pedidos"

    def mostrar_alerta(mensaje):
        sb = ft.SnackBar(content=ft.Text(mensaje, color="white"), bgcolor="#E05638")
        page.overlay.append(sb)
        sb.open = True
        page.update()

    productos = [
        {"cat": "Bebidas", "nombre": "Maca", "precio": 2.50, "icon": ft.icons.LOCAL_DRINK, "desc": "Bebida energizante natural"},
        {"cat": "Bebidas", "nombre": "Emoliente", "precio": 2.50, "icon": ft.icons.LOCAL_DRINK, "desc": "Con linaza y hierbas tradicionales"},
        {"cat": "Bebidas", "nombre": "Quinua", "precio": 2.50, "icon": ft.icons.LOCAL_DRINK, "desc": "Quinua caliente tradicional"},
        {"cat": "Bebidas", "nombre": "Quinua con Leche", "precio": 3.00, "icon": ft.icons.LOCAL_DRINK, "desc": "Quinua cremosa c/ leche"},
        {"cat": "Bebidas", "nombre": "Quacker", "precio": 2.50, "icon": ft.icons.LOCAL_DRINK, "desc": "Avena tradicional bien caliente"},
        {"cat": "Panes", "nombre": "Pan con Pollo", "precio": 1.50, "img": "https://i.ibb.co/q33Y5bSC/Gemini-Generated-Image-do9fwedo9fwedo9f.png", "desc": "Pollo deshilachado c/ mayonesa"},
        {"cat": "Panes", "nombre": "Pan con Palta", "precio": 1.50, "img": "https://i.ibb.co/FLbZ8CZ4/Gemini-Generated-Image-c4he2wc4he2wc4he.png", "desc": "Palta fuerte laminada fresca"},
        {"cat": "Panes", "nombre": "Pan con Chicharrón", "precio": 1.50, "img": "https://i.ibb.co/mr00xwZ1/Gemini-Generated-Image-hxammahxammahxam.png", "desc": "Chicharrón crujiente c/ camote"},
        {"cat": "Panes", "nombre": "Pan con Camote", "precio": 1.50, "img": "https://i.ibb.co/v6GhnfGT/Gemini-Generated-Image-nk9gmknk9gmknk9g.png", "desc": "Camote frito crocante"},
        {"cat": "Panes", "nombre": "Pan con Tamal", "precio": 1.50, "img": "https://i.ibb.co/S4N96Jft/Gemini-Generated-Image-cle3kdcle3kdcle3.png", "desc": "Tamal criollo tradicional"},
        {"cat": "Panes", "nombre": "Pan con Torreja", "precio": 1.50, "img": "https://i.ibb.co/yBm1QzQZ/Gemini-Generated-Image-fqkmbtfqkmbtfqkm.png", "desc": "Torreja de verduras recién hecha"},
        {"cat": "Panes", "nombre": "Pan con Lomo", "precio": 1.50, "img": "https://i.ibb.co/jvw6hnwj/Gemini-Generated-Image-qkazhlqkazhlqkaz.png", "desc": "Lomo saltado jugoso al jugo"}
    ]

    cantidades = {p["nombre"]: 0 for p in productos}
    contenido_principal = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)

    def recibir_actualizacion_global(mensaje):
        try:
            if usuario_actual["rol"] == "Cocina":
                mostrar_cocina(vista_actual_cocina)
            elif usuario_actual["rol"] == "Cliente":
                if vista_actual_cliente in ["menu", "pedidos", "favs"]:
                    mostrar_app_cliente(vista_actual_cliente)
        except Exception:
            pass

    page.pubsub.subscribe(recibir_actualizacion_global)

    def mostrar_login(tipo_login="cliente", sub_accion="login"):
        def ingresar_cliente(e):
            correo = tf_correo.value.strip().lower() if tf_correo.value else ""
            if not correo or not validar_correo(correo):
                mostrar_alerta("⚠️ Ingresa un correo electrónico válido.")
                return
            if not tf_password.value:
                mostrar_alerta("⚠️ Por favor ingresa tu contraseña.")
                return
            if correo not in db_global["usuarios"]:
                mostrar_alerta("❌ Este correo no está registrado. Ve a 'Crear Cuenta Nueva'.")
                return
            usuario_registrado = db_global["usuarios"][correo]
            if usuario_registrado.get("password") != tf_password.value:
                mostrar_alerta("❌ Contraseña incorrecta.")
                return
            usuario_actual["nombre"] = usuario_registrado["nombre"]
            usuario_actual["correo"] = correo
            usuario_actual["rol"] = "Cliente"
            mostrar_alerta(f"¡Bienvenido de nuevo, {usuario_actual['nombre']}!")
            mostrar_app_cliente("menu")

        def registrar_cliente(e):
            correo = tf_correo.value.strip().lower() if tf_correo.value else ""
            nombre = tf_user.value.strip() if tf_user.value else ""
            pass1 = tf_password.value if tf_password.value else ""
            pass2 = tf_confirm_password.value if tf_confirm_password.value else ""

            if not nombre or not correo or not pass1 or not pass2:
                mostrar_alerta("⚠️ Completa todos los campos obligatorios.")
                return
            if not validar_correo(correo):
                mostrar_alerta("⚠️ El correo ingresado no tiene un formato válido.")
                return
            if correo in db_global["usuarios"]:
                mostrar_alerta("⚠️ El correo ya se encuentra registrado. Inicia sesión directamente.")
                return
            if pass1 != pass2:
                mostrar_alerta("❌ Las contraseñas no coinciden. Verifícalas nuevamente.")
                return

            db_global["usuarios"][correo] = {
                "nombre": nombre,
                "password": pass1,
                "origen": "Manual"
            }
            usuario_actual["nombre"] = nombre
            usuario_actual["correo"] = correo
            usuario_actual["rol"] = "Cliente"
            mostrar_alerta("¡Cuenta creada exitosamente!")
            mostrar_app_cliente("menu")

        def continuar_celular(e):
            celular = tf_celular_input.value.strip() if tf_celular_input.value else ""
            if len(celular) < 9:
                mostrar_alerta("⚠️ Ingresa un número de celular válido de 9 dígitos.")
                return
            usuario_actual["nombre"] = f"Celular {celular[-4:]}"
            usuario_actual["correo"] = f"{celular}@movil.pe"
            usuario_actual["rol"] = "Cliente"
            mostrar_alerta(f"¡Código enviado al celular {celular}!")
            mostrar_app_cliente("menu")

        def seleccionar_cuenta_google(correo_Elegido):
            dlg_selector.open = False
            page.update()
            
            correo_g = correo_Elegido.strip().lower()
            if correo_g in db_global["usuarios"]:
                usuario_actual["nombre"] = db_global["usuarios"][correo_g]["nombre"]
                mostrar_alerta(f"¡Bienvenido de nuevo, {usuario_actual['nombre']}!")
            else:
                nombre_ext = correo_g.split("@")[0].capitalize()
                db_global["usuarios"][correo_g] = {
                    "nombre": nombre_ext,
                    "password": "",
                    "origen": "Google"
                }
                usuario_actual["nombre"] = nombre_ext
                mostrar_alerta(f"¡Cuenta asociada con Google! Bienvenido, {nombre_ext}")

            usuario_actual["correo"] = correo_g
            usuario_actual["rol"] = "Cliente"
            mostrar_app_cliente("menu")

        tf_nuevo_g = ft.TextField(
            label="Correo de Google (@gmail.com / @usil.pe)",
            value="erickvitanciousil@gmail.com",
            bgcolor="#FFFFFF",
            border_color="#E0D7CD",
            color="#000000"
        )

        dlg_selector = ft.AlertDialog(
            title=ft.Row([
                ft.Image(src=GOOGLE_LOGO_URL, width=24, height=24),
                ft.Text("Elige una cuenta para Proyecto Empresarial USIL", size=15, weight=ft.FontWeight.BOLD)
            ], spacing=10),
            content=ft.Column([
                ft.Text("Selecciona tu cuenta vinculada:", size=13, color="#7A685D"),
                ft.Container(
                    content=ft.Row([
                        ft.CircleAvatar(content=ft.Text("E", color="white", weight=ft.FontWeight.BOLD), bgcolor="#1A73E8", radius=18),
                        ft.Column([
                            ft.Text("Erick Vitancio", weight=ft.FontWeight.BOLD, size=14, color="#2C221E"),
                            ft.Text("erickvitanciousil@gmail.com", size=12, color="#7A685D")
                        ], spacing=2)
                    ], spacing=12),
                    padding=10,
                    bgcolor="#F8F9FA",
                    border_radius=8,
                    ink=True,
                    on_click=lambda e: seleccionar_cuenta_google("erickvitanciousil@gmail.com")
                ),
                ft.Divider(color="#EFEBE4"),
                tf_nuevo_g
            ], tight=True, spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg_selector, 'open', False) or page.update()),
                ft.TextButton("Continuar con este correo", on_click=lambda e: seleccionar_cuenta_google(tf_nuevo_g.value))
            ]
        )

        def abrir_selector_google(e):
            page.overlay.append(dlg_selector)
            dlg_selector.open = True
            page.update()

        fn_accion = ingresar_cliente if sub_accion == "login" else registrar_cliente

        tf_user = ft.TextField(label="Nombre Completo", bgcolor="#FFFFFF", border_color="#E0D7CD", focused_border_color="#E05638", color="#000000", on_submit=fn_accion, width=340)
        tf_correo = ft.TextField(label="Correo Electrónico", bgcolor="#FFFFFF", border_color="#E0D7CD", focused_border_color="#E05638", color="#000000", on_submit=fn_accion, width=340)
        tf_password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, bgcolor="#FFFFFF", border_color="#E0D7CD", focused_border_color="#E05638", color="#000000", on_submit=fn_accion, width=340)
        tf_confirm_password = ft.TextField(label="Confirmar Contraseña", password=True, can_reveal_password=True, bgcolor="#FFFFFF", border_color="#E0D7CD", focused_border_color="#E05638", color="#000000", on_submit=fn_accion, width=340)

        tf_celular_input = ft.TextField(
            hint_text="Número de teléfono",
            border=ft.InputBorder.NONE,
            bgcolor="#E8F0FE",
            color="#2C221E",
            content_padding=ft.padding.symmetric(horizontal=12, vertical=12),
            expand=True,
            on_submit=continuar_celular
        )

        # Contenedor con la bandera oficial a color del Perú a la izquierda de +51
        campo_celular_estilo = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Row([
                        ft.Image(src=PERU_FLAG_URL, width=20, height=14, fit="contain"),
                        ft.Text("+51", size=14, color="#2C221E", weight=ft.FontWeight.W_500),
                        ft.Icon(ft.icons.ARROW_DROP_DOWN, size=18, color="#5F6368")
                    ], spacing=6, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor="#F1F3F4",
                    padding=ft.padding.symmetric(horizontal=10, vertical=12),
                    border_radius=ft.border_radius.only(top_left=6, bottom_left=6)
                ),
                ft.Container(
                    content=tf_celular_input,
                    padding=0,
                    expand=True
                )
            ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#E8F0FE",
            border_radius=6,
            height=48,
            width=360
        )

        tf_admin_user = ft.TextField(label="Usuario Negocio", value="cocina", bgcolor="#FFFFFF", border_color="#E0D7CD", focused_border_color="#E05638", color="#000000", on_submit=lambda e: ingresar_negocio(e), width=340)
        tf_admin_pass = ft.TextField(label="Contraseña", value="1234", password=True, bgcolor="#FFFFFF", border_color="#E0D7CD", focused_border_color="#E05638", color="#000000", on_submit=lambda e: ingresar_negocio(e), width=340)

        def ingresar_negocio(e):
            if tf_admin_user.value == "cocina" and tf_admin_pass.value == "1234":
                usuario_actual["nombre"] = "Módulo Cocina / Recepción"
                usuario_actual["rol"] = "Cocina"
                mostrar_cocina("pedidos")
            else:
                mostrar_alerta("Credenciales incorrectas (Usa: cocina / 1234).")

        btn_google_estilo = ft.Container(
            content=ft.Row([
                ft.Image(src=GOOGLE_LOGO_URL, width=20, height=20, fit="contain"),
                ft.Text("Continuar con Google", size=14, color="#2C221E", weight=ft.FontWeight.W_600)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            padding=12,
            bgcolor="#FFFFFF",
            border=ft.Border(top=ft.BorderSide(1, "#E0D7CD"), bottom=ft.BorderSide(1, "#E0D7CD"), left=ft.BorderSide(1, "#E0D7CD"), right=ft.BorderSide(1, "#E0D7CD")),
            border_radius=24,
            width=340,
            ink=True,
            on_click=abrir_selector_google
        )

        btn_celular_estilo = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.SMARTPHONE, size=20, color="#5F6368"),
                ft.Text("Continuar con tu celular", size=14, color="#2C221E", weight=ft.FontWeight.W_600)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            padding=12,
            bgcolor="#FFFFFF",
            border=ft.Border(top=ft.BorderSide(1, "#E0D7CD"), bottom=ft.BorderSide(1, "#E0D7CD"), left=ft.BorderSide(1, "#E0D7CD"), right=ft.BorderSide(1, "#E0D7CD")),
            border_radius=24,
            width=340,
            ink=True,
            on_click=lambda e: mostrar_login("cliente", "celular")
        )

        form_contenido = ft.Column(spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        header_app_nombre = ft.Row([
            ft.Icon(ft.icons.BUSINESS_CENTER, size=18, color="#E05638"),
            ft.Text("Proyecto Empresarial USIL", size=14, weight=ft.FontWeight.BOLD, color="#E05638")
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=6)

        if tipo_login == "cliente" and sub_accion == "celular":
            btn_volver_menu = ft.TextButton("← Volver a opciones rápidas", on_click=lambda e: mostrar_login("cliente", "login"), style=ft.ButtonStyle(color="#E05638"))
            vista_celular_sin_tarjeta = ft.Column([
                ft.Container(height=40),
                btn_volver_menu,
                ft.Container(height=20),
                ft.Text("Ingresa tu número de celular", size=26, weight=ft.FontWeight.BOLD, color="#2C221E", text_align=ft.TextAlign.CENTER),
                ft.Text("Te enviaremos un código para confirmarlo", size=14, color="#5F6368", text_align=ft.TextAlign.CENTER),
                ft.Container(height=25),
                campo_celular_estilo,
                ft.Container(height=15),
                ft.TextButton("Enviar código de acceso", style=ft.ButtonStyle(bgcolor="#E05638", color="white", shape=ft.RoundedRectangleBorder(radius=24)), height=48, width=360, on_click=continuar_celular)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6)

            contenido_principal.controls.clear()
            contenido_principal.controls.append(vista_celular_sin_tarjeta)
            page.update()
            return

        if tipo_login == "cliente" and sub_accion == "manual":
            btn_volver_menu = ft.TextButton("← Volver a opciones rápidas", on_click=lambda e: mostrar_login("cliente", "login"), style=ft.ButtonStyle(color="#E05638"))
            form_contenido.controls.extend([
                btn_volver_menu,
                tf_correo,
                tf_password,
                ft.TextButton("Iniciar Sesión", style=ft.ButtonStyle(bgcolor="#E05638", color="white", shape=ft.RoundedRectangleBorder(radius=24)), height=48, width=340, on_click=ingresar_cliente),
            ])
        elif tipo_login == "cliente" and sub_accion == "registro":
            btn_volver_menu = ft.TextButton("← Volver a opciones rápidas", on_click=lambda e: mostrar_login("cliente", "login"), style=ft.ButtonStyle(color="#E05638"))
            form_contenido.controls.extend([
                btn_volver_menu,
                tf_user,
                tf_correo,
                tf_password,
                tf_confirm_password,
                ft.TextButton("Crear Mi Cuenta", style=ft.ButtonStyle(bgcolor="#2E7D32", color="white", shape=ft.RoundedRectangleBorder(radius=24)), height=48, width=340, on_click=registrar_cliente),
            ])
        elif tipo_login == "negocio":
            btn_volver_cliente = ft.TextButton("← Regresar a acceso de Clientes", on_click=lambda e: mostrar_login("cliente", "login"), style=ft.ButtonStyle(color="#E05638"))
            form_contenido.controls.extend([
                btn_volver_cliente,
                ft.Text("🔑 Panel de Administración / Cocina", color="#7A685D", size=13, weight=ft.FontWeight.BOLD),
                tf_admin_user,
                tf_admin_pass,
                ft.TextButton("Ingresar al Panel Recepción", style=ft.ButtonStyle(bgcolor="#2E7D32", color="white", shape=ft.RoundedRectangleBorder(radius=24)), height=48, width=340, on_click=ingresar_negocio)
            ])
        else:
            btn_email_login = ft.TextButton(
                "Ingresar con correo electrónico",
                style=ft.ButtonStyle(bgcolor="#E05638", color="white", shape=ft.RoundedRectangleBorder(radius=24)),
                height=46,
                width=340,
                on_click=lambda e: mostrar_login("cliente", "manual")
            )
            
            btn_crear_cuenta_txt = ft.TextButton(
                "¿No tienes cuenta? Regístrate aquí",
                style=ft.ButtonStyle(color="#7A685D"),
                on_click=lambda e: mostrar_login("cliente", "registro")
            )

            btn_switch_admin = ft.TextButton(
                "Acceso exclusivo para Socios / Cocina",
                style=ft.ButtonStyle(color="#A0938A"),
                on_click=lambda e: mostrar_login("negocio")
            )

            divisor_elegante = ft.Row([
                ft.Container(content=ft.Divider(color="#EFEBE4", thickness=1), expand=True),
                ft.Text("o con tu cuenta", size=12, color="#9A8B80"),
                ft.Container(content=ft.Divider(color="#EFEBE4", thickness=1), expand=True)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10, width=340)

            form_contenido.controls.extend([
                btn_google_estilo,
                btn_celular_estilo,
                ft.Container(height=4),
                divisor_elegante,
                ft.Container(height=4),
                btn_email_login,
                btn_crear_cuenta_txt,
                ft.Divider(color="#F3EFEA", height=15),
                btn_switch_admin
            ])

        elementos_tarjeta = [
            header_app_nombre,
            ft.Divider(color="#EFEBE4", height=15),
            ft.Text("Regístrate o ingresa para continuar", size=22, weight=ft.FontWeight.BOLD, color="#2C221E", text_align=ft.TextAlign.CENTER),
            ft.Text("Elige tu método preferido de acceso rápido", size=13, color="#7A685D", text_align=ft.TextAlign.CENTER),
            ft.Container(height=10),
            form_contenido
        ]

        tarjeta_principal = ft.Container(
            content=ft.Column(elementos_tarjeta, spacing=12, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#FFFFFF",
            padding=36,
            width=460,
            border_radius=16,
            border=ft.Border(
                top=ft.BorderSide(1, "#EFEBE4"),
                bottom=ft.BorderSide(1, "#EFEBE4"),
                left=ft.BorderSide(1, "#EFEBE4"),
                right=ft.BorderSide(1, "#EFEBE4"),
            ),
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color="#0F000000")
        )

        contenido_principal.controls.clear()
        contenido_principal.controls.append(ft.Container(height=10))
        contenido_principal.controls.append(tarjeta_principal)
        page.update()

    def mostrar_app_cliente(vista_activa="menu"):
        nonlocal filtro_categoria, busqueda_texto, sede_actual, puesto_seleccionado, vista_actual_cliente
        vista_actual_cliente = vista_activa
        
        contenedor_cliente = ft.Column(spacing=16, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=1000)

        def cambiar_sede(e):
            nonlocal sede_actual, puesto_seleccionado
            sede_actual = e.control.value
            puesto_seleccionado = db_global["sedes"][sede_actual][0]
            mostrar_alerta(f"Ubicación cambiada a: {sede_actual}")
            mostrar_app_cliente(vista_activa)

        dd_sede = ft.Dropdown(
            label="📍 Tu ubicación / Zona de Trabajo:",
            options=[ft.dropdown.Option(key=s, text=s) for s in db_global["sedes"].keys()],
            value=sede_actual,
            bgcolor="#FFFFFF",
            border_color="#E0D7CD",
            color="#000000",
            width=420
        )
        dd_sede.on_change = cambiar_sede

        mis_p_activos = [p for p in db_global["pedidos"] if p["cliente"] == usuario_actual["nombre"] and "Entregado" not in p["estado"]]
        banner_estado = ft.Container()
        if mis_p_activos:
            p_ultimo = mis_p_activos[-1]
            es_listo = "Listo" in p_ultimo["estado"]
            banner_estado = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.icons.NOTIFICATIONS_ACTIVE if es_listo else ft.icons.ACCESS_TIME, color="white", size=18),
                    ft.Text(f"Pedido #{p_ultimo['codigo']}: {p_ultimo['estado']} en {p_ultimo.get('puesto', '')}", color="white", weight=ft.FontWeight.BOLD, size=13)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                bgcolor="#2E7D32" if es_listo else "#E05638",
                padding=10,
                border_radius=10,
                width=900
            )

        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(f"¡Hola, {usuario_actual['nombre']}! 👋", size=18, weight=ft.FontWeight.BOLD, color="#2C221E"),
                    dd_sede
                ]),
                ft.TextButton(
                    "Cerrar Sesión", 
                    style=ft.ButtonStyle(color="#E05638"),
                    on_click=lambda e: mostrar_login("cliente")
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            width=900
        )

        nav_buttons = ft.Row([
            ft.TextButton("🛒 Menú", style=ft.ButtonStyle(bgcolor="#E05638" if vista_activa == "menu" else "#EFEBE4", color="white" if vista_activa == "menu" else "#2C221E"), on_click=lambda e: mostrar_app_cliente("menu")),
            ft.TextButton("🛵 Mis Pedidos", style=ft.ButtonStyle(bgcolor="#E05638" if vista_activa == "pedidos" else "#EFEBE4", color="white" if vista_activa == "pedidos" else "#2C221E"), on_click=lambda e: mostrar_app_cliente("pedidos")),
            ft.TextButton("❤️ Favoritos", style=ft.ButtonStyle(bgcolor="#E05638" if vista_activa == "favs" else "#EFEBE4", color="white" if vista_activa == "favs" else "#2C221E"), on_click=lambda e: mostrar_app_cliente("favs")),
        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)

        lbl_total = ft.Text("Total: S/ 0.00", size=20, weight=ft.FontWeight.BOLD, color="#E05638")

        def actualizar_total():
            t = sum(cantidades[p["nombre"]] * p["precio"] for p in productos)
            lbl_total.value = f"Total: S/ {t:.2f}"
            page.update()

        def tarjeta_producto(prod):
            lbl_c = ft.Text(str(cantidades[prod["nombre"]]), size=15, weight=ft.FontWeight.BOLD, color="#2C221E")

            def add(e):
                cantidades[prod["nombre"]] += 1
                lbl_c.value = str(cantidades[prod["nombre"]])
                actualizar_total()

            def rem(e):
                if cantidades[prod["nombre"]] > 0:
                    cantidades[prod["nombre"]] -= 1
                    lbl_c.value = str(cantidades[prod["nombre"]])
                    actualizar_total()

            def toggle_fav(e):
                if prod["nombre"] not in db_global["favoritos"]:
                    db_global["favoritos"].append(prod["nombre"])
                    e.control.icon_color = "#E05638"
                else:
                    db_global["favoritos"].remove(prod["nombre"])
                    e.control.icon_color = "#C5B8AB"
                page.update()

            es_fav = prod["nombre"] in db_global["favoritos"]
            fav_color = "#E05638" if es_fav else "#C5B8AB"

            if "img" in prod:
                media_control = ft.Image(src=prod["img"], width=220, height=110, fit="cover")
            else:
                media_control = ft.Icon(prod["icon"], size=50, color="#E05638")

            return ft.Container(
                content=ft.Column([
                    ft.Stack([
                        ft.Container(content=media_control, height=110, width=220, bgcolor="#FDF2E9", border_radius=10),
                        ft.IconButton(ft.icons.FAVORITE, icon_color=fav_color, icon_size=20, top=2, right=2, on_click=toggle_fav)
                    ]),
                    ft.Text(prod["nombre"], weight=ft.FontWeight.BOLD, color="#2C221E", size=14, no_wrap=True),
                    ft.Text(f"S/ {prod['precio']:.2f}", color="#2E7D32", weight=ft.FontWeight.BOLD, size=13),
                    ft.Row([
                        ft.IconButton(ft.icons.REMOVE_CIRCLE_OUTLINE, icon_color="#E05638", on_click=rem),
                        lbl_c,
                        ft.IconButton(ft.icons.ADD_CIRCLE_OUTLINE, icon_color="#2E7D32", on_click=add)
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                bgcolor="#FFFFFF",
                padding=10,
                border_radius=12,
                border=ft.Border(
                    top=ft.BorderSide(1, "#EFEBE4"),
                    bottom=ft.BorderSide(1, "#EFEBE4"),
                    left=ft.BorderSide(1, "#EFEBE4"),
                    right=ft.BorderSide(1, "#EFEBE4"),
                ),
                width=240
            )

        contenido_seccion = ft.Column(spacing=14, width=900, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        if vista_activa == "menu":
            def filtrar_cat(cat):
                nonlocal filtro_categoria
                filtro_categoria = cat
                mostrar_app_cliente("menu")

            def buscar_prod(e):
                nonlocal busqueda_texto
                busqueda_texto = e.control.value.lower()
                mostrar_app_cliente("menu")

            tf_buscar = ft.TextField(
                hint_text="🔍 Buscar quinua, maca, tamal, chicharrón, lomo...",
                bgcolor="#FFFFFF",
                border_color="#E0D7CD",
                focused_border_color="#E05638",
                color="#000000",
                height=45,
                width=600,
                value=busqueda_texto,
                content_padding=14,
                on_change=buscar_prod
            )

            chips_cat = ft.Row([
                ft.TextButton("Todos", style=ft.ButtonStyle(bgcolor="#E05638" if filtro_categoria == "Todos" else "#EFEBE4", color="white" if filtro_categoria == "Todos" else "#2C221E"), on_click=lambda e: filtrar_cat("Todos")),
                ft.TextButton("☕ Bebidas", style=ft.ButtonStyle(bgcolor="#E05638" if filtro_categoria == "Bebidas" else "#EFEBE4", color="white" if filtro_categoria == "Bebidas" else "#2C221E"), on_click=lambda e: filtrar_cat("Bebidas")),
                ft.TextButton("🥖 Panes", style=ft.ButtonStyle(bgcolor="#E05638" if filtro_categoria == "Panes" else "#EFEBE4", color="white" if filtro_categoria == "Panes" else "#2C221E"), on_click=lambda e: filtrar_cat("Panes")),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)

            prods_filtrados = [
                p for p in productos 
                if (filtro_categoria == "Todos" or p["cat"] == filtro_categoria) 
                and (not busqueda_texto or busqueda_texto in p["nombre"].lower() or busqueda_texto in p["desc"].lower())
            ]

            grid_prods = ft.Row(
                [tarjeta_producto(p) for p in prods_filtrados], 
                wrap=True, 
                alignment=ft.MainAxisAlignment.CENTER, 
                spacing=16
            )

            def ir_pago(e):
                items = [f"{cantidades[p['nombre']]}x {p['nombre']}" for p in productos if cantidades[p["nombre"]] > 0]
                tot = sum(cantidades[p["nombre"]] * p["precio"] for p in productos)

                if tot == 0:
                    mostrar_alerta("Elige al menos un producto para continuar.")
                else:
                    pedido_temporal["detalle"] = ", ".join(items)
                    pedido_temporal["total"] = tot
                    mostrar_pago()

            actualizar_total()
            contenido_seccion.controls.extend([
                tf_buscar,
                chips_cat,
                ft.Text(f"📋 Catálogo ({len(prods_filtrados)} opciones)", size=15, weight=ft.FontWeight.BOLD, color="#2C221E"),
                grid_prods,
                ft.Divider(color="#EFEBE4"),
                lbl_total,
                ft.TextButton("💳 Continuar con el Pago", style=ft.ButtonStyle(bgcolor="#E05638", color="white"), height=50, width=300, on_click=ir_pago)
            ])

        elif vista_activa == "pedidos":
            mis_p = [p for p in db_global["pedidos"] if p["cliente"] == usuario_actual["nombre"]]
            if not mis_p:
                contenido_seccion.controls.append(ft.Text("No tienes órdenes activas en este momento.", color="#7A685D"))
            else:
                for p in reversed(mis_p):
                    dd_evaluar = ft.Dropdown(
                        label="Evaluar pedido:",
                        options=[
                            ft.dropdown.Option("⭐ 5 Excelente"),
                            ft.dropdown.Option("⭐ 4 Bueno"),
                            ft.dropdown.Option("⭐ 3 Regular"),
                            ft.dropdown.Option("⭐ 2 Malo"),
                            ft.dropdown.Option("⭐ 1 Pésimo"),
                        ],
                        value="⭐ 5 Excelente",
                        bgcolor="#FFFFFF",
                        border_color="#E0D7CD",
                        color="#000000",
                        width=300
                    )

                    contenido_seccion.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(f"Orden #{p['codigo']}", size=16, weight=ft.FontWeight.BOLD, color="#2C221E"),
                                    ft.Text(p['estado'], weight=ft.FontWeight.BOLD, color="#E05638" if "Preparación" in p['estado'] else "#2E7D32", size=13)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ft.Text(f"Zona: {p.get('sede', '')}", color="#7A685D", size=13),
                                ft.Text(f"Puesto Recojo: {p.get('puesto', '')}", color="#E05638", weight=ft.FontWeight.BOLD, size=13),
                                ft.Text(f"Detalle: {p['detalle']}", color="#2C221E", size=14),
                                ft.Text(f"Notas: {p.get('notas', 'Sin especificaciones')}", color="#7A685D", size=12, italic=True),
                                ft.Text("⏱️ Tiempo máximo de preparación: 10 minutos", color="#2E7D32", size=13, weight=ft.FontWeight.W_500),
                                ft.Text(f"Pago: {p['pago']} | Total: S/ {p['total']:.2f}", color="#7A685D", size=13),
                                ft.Divider(color="#EFEBE4"),
                                dd_evaluar,
                                ft.Row([
                                    ft.TextButton(
                                        "🔄 Repetir pedido", 
                                        style=ft.ButtonStyle(bgcolor="#E05638", color="white", shape=ft.RoundedRectangleBorder(radius=8)),
                                        height=38,
                                        on_click=lambda e: mostrar_alerta("Pedido añadido al carrito.")
                                    )
                                ], alignment=ft.MainAxisAlignment.END)
                            ], spacing=8),
                            padding=16,
                            bgcolor="#FFFFFF",
                            border_radius=12,
                            width=600,
                            border=ft.Border(
                                top=ft.BorderSide(1, "#EFEBE4"),
                                bottom=ft.BorderSide(1, "#EFEBE4"),
                                left=ft.BorderSide(1, "#EFEBE4"),
                                right=ft.BorderSide(1, "#EFEBE4"),
                            )
                        )
                    )

        elif vista_activa == "favs":
            if not db_global["favoritos"]:
                contenido_seccion.controls.append(ft.Text("Aún no has agregado productos favoritos.", color="#7A685D"))
            else:
                for fav_name in db_global["favoritos"]:
                    contenido_seccion.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Text(f"❤️ {fav_name}", color="#2C221E", weight=ft.FontWeight.BOLD, expand=True),
                                ft.TextButton("Repetir", style=ft.ButtonStyle(bgcolor="#E05638", color="white"), on_click=lambda e: mostrar_alerta("Producto añadido a tu lista."))
                            ]),
                            bgcolor="#FFFFFF",
                            padding=12,
                            border_radius=10,
                            width=600,
                            border=ft.Border(
                                top=ft.BorderSide(1, "#EFEBE4"),
                                bottom=ft.BorderSide(1, "#EFEBE4"),
                                left=ft.BorderSide(1, "#EFEBE4"),
                                right=ft.BorderSide(1, "#EFEBE4"),
                            )
                        )
                    )

        contenedor_cliente.controls.extend([banner_estado, header, nav_buttons, contenido_seccion])
        contenido_principal.controls.clear()
        contenido_principal.controls.append(contenedor_cliente)
        page.update()

    def mostrar_pago():
        nonlocal puesto_seleccionado, vista_actual_cliente
        vista_actual_cliente = "pago"
        
        puestos_disponibles = db_global["sedes"][sede_actual]

        icon_puesto = ft.Icon(puesto_seleccionado["icon"], size=40, color=puesto_seleccionado["color"])
        lbl_puesto_nombre = ft.Text(puesto_seleccionado["nombre"], size=16, weight=ft.FontWeight.BOLD, color="#2C221E")
        lbl_puesto_ref = ft.Text(f"📍 Referencia: {puesto_seleccionado['referencia']}", color="#E05638", size=13, weight=ft.FontWeight.W_500)
        lbl_puesto_vend = ft.Text(f"👨‍🍳 Atendido por: {puesto_seleccionado['vendedor']}", color="#7A685D", size=12)

        def al_cambiar_puesto(e):
            nonlocal puesto_seleccionado
            p_id = e.control.value
            for p in puestos_disponibles:
                if p["id"] == p_id:
                    puesto_seleccionado = p
                    break
            icon_puesto.name = puesto_seleccionado["icon"]
            icon_puesto.color = puesto_seleccionado["color"]
            lbl_puesto_nombre.value = puesto_seleccionado["nombre"]
            lbl_puesto_ref.value = f"📍 Referencia: {puesto_seleccionado['referencia']}"
            lbl_puesto_vend.value = f"👨‍🍳 Atendido por: {puesto_seleccionado['vendedor']}"
            page.update()

        dd_puestos = ft.Dropdown(
            label="🏪 Selecciona el Puesto exacto de recojo:",
            options=[ft.dropdown.Option(key=p["id"], text=p["nombre"]) for p in puestos_disponibles],
            value=puesto_seleccionado["id"],
            bgcolor="#FFFFFF",
            border_color="#E0D7CD",
            color="#000000"
        )
        dd_puestos.on_change = al_cambiar_puesto

        card_info_puesto = ft.Container(
            content=ft.Column([
                ft.Row([icon_puesto, lbl_puesto_nombre], spacing=10),
                lbl_puesto_ref,
                lbl_puesto_vend
            ], spacing=6),
            padding=12,
            bgcolor="#FAF7F2",
            border_radius=10,
            border=ft.Border(
                top=ft.BorderSide(1, "#E0D7CD"),
                bottom=ft.BorderSide(1, "#E0D7CD"),
                left=ft.BorderSide(1, "#E0D7CD"),
                right=ft.BorderSide(1, "#E0D7CD"),
            )
        )

        dd_metodo = ft.Dropdown(
            label="Método de Pago",
            options=[
                ft.dropdown.Option("Yape (Cobro automático)"),
                ft.dropdown.Option("Plin"),
                ft.dropdown.Option("Tarjeta de Crédito / Débito"),
                ft.dropdown.Option("Pago Contra Entrega (Efectivo)"),
            ],
            value="Yape (Cobro automático)",
            bgcolor="#FFFFFF",
            border_color="#E0D7CD",
            color="#000000"
        )

        tf_notas = ft.TextField(
            label="Especificaciones / Personalización (Opcional):",
            hint_text="Ej. Sin mayonesa, emoliente con poco dulce...",
            bgcolor="#FFFFFF",
            border_color="#E0D7CD",
            focused_border_color="#E05638",
            color="#000000"
        )

        def confirmar(e):
            b1 = "".join(random.choices(string.ascii_uppercase + string.digits, k=3))
            codigo = f"DCE-{b1}"

            nuevo = {
                "id": len(db_global["pedidos"]) + 1,
                "codigo": codigo,
                "cliente": usuario_actual["nombre"],
                "detalle": pedido_temporal["detalle"],
                "sede": sede_actual,
                "puesto": f"{puesto_seleccionado['nombre']} ({puesto_seleccionado['referencia']})",
                "notas": tf_notas.value if tf_notas.value else "Sin especificaciones",
                "total": pedido_temporal["total"],
                "estado": "🟡 En Preparación",
                "pago": dd_metodo.value.split(" ")[0],
                "tiempo_espera": "Máx. 10 minutos"
            }
            db_global["pedidos"].append(nuevo)

            for k in cantidades:
                cantidades[k] = 0

            page.pubsub.send_all("NUEVO_PEDIDO")
            mostrar_alerta(f"¡Pedido #{codigo} registrado en {puesto_seleccionado['nombre']}!")
            mostrar_app_cliente("pedidos")

        card_pago = ft.Container(
            content=ft.Column([
                ft.Text("💳 Confirmación de Compra", size=20, weight=ft.FontWeight.BOLD, color="#2C221E"),
                ft.Text(f"Resumen: {pedido_temporal['detalle']}", color="#7A685D", size=14),
                ft.Text(f"Total a Pagar: S/ {pedido_temporal['total']:.2f}", size=22, weight=ft.FontWeight.BOLD, color="#2E7D32"),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.TIMER, color="#E05638", size=20),
                        ft.Text("Tiempo máximo de preparación: 10 minutos", color="#E05638", weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    padding=10,
                    bgcolor="#FDF2E9",
                    border_radius=8
                ),
                ft.Divider(color="#EFEBE4"),
                dd_puestos,
                card_info_puesto,
                tf_notas,
                dd_metodo,
                ft.TextButton("🚀 Confirmar y Enviar a Cocina", style=ft.ButtonStyle(bgcolor="#E05638", color="white"), height=48, on_click=confirmar),
                ft.OutlinedButton("⬅️ Volver al Menú", on_click=lambda e: mostrar_app_cliente("menu"))
            ], spacing=14, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=24,
            bgcolor="#FFFFFF",
            border_radius=16,
            width=480,
            border=ft.Border(
                top=ft.BorderSide(1, "#EFEBE4"),
                bottom=ft.BorderSide(1, "#EFEBE4"),
                left=ft.BorderSide(1, "#EFEBE4"),
                right=ft.BorderSide(1, "#EFEBE4"),
            )
        )

        contenido_principal.controls.clear()
        contenido_principal.controls.append(card_pago)
        page.update()

    def mostrar_cocina(sub_panel="pedidos"):
        nonlocal vista_actual_cocina
        vista_actual_cocina = sub_panel
        
        col_contenido = ft.Column(spacing=12, width=800, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        header_cocina = ft.Container(
            content=ft.Row([
                ft.Text(f"👨‍🍳 {usuario_actual['nombre']}", size=18, weight=ft.FontWeight.BOLD, color="#2C221E"),
                ft.TextButton(
                    "Cerrar Sesión", 
                    style=ft.ButtonStyle(color="#E05638"),
                    on_click=lambda e: mostrar_login("negocio")
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            width=800
        )

        nav_cocina = ft.Row([
            ft.TextButton("📋 Pedidos Cocina", style=ft.ButtonStyle(bgcolor="#E05638" if sub_panel == "pedidos" else "#EFEBE4", color="white" if sub_panel == "pedidos" else "#2C221E"), on_click=lambda e: mostrar_cocina("pedidos")),
            ft.TextButton("📊 Métricas de Ventas", style=ft.ButtonStyle(bgcolor="#E05638" if sub_panel == "ventas" else "#EFEBE4", color="white" if sub_panel == "ventas" else "#2C221E"), on_click=lambda e: mostrar_cocina("ventas")),
        ], spacing=12, alignment=ft.MainAxisAlignment.CENTER)

        def actualizar_estado(pedido_id, nuevo_estado):
            for p in db_global["pedidos"]:
                if p["id"] == pedido_id:
                    p["estado"] = nuevo_estado
            page.pubsub.send_all("CAMBIO_ESTADO")

        if sub_panel == "pedidos":
            if not db_global["pedidos"]:
                col_contenido.controls.append(ft.Text("No hay pedidos activos en cocina.", color="#7A685D"))
            else:
                for p in reversed(db_global["pedidos"]):
                    col_contenido.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(f"Orden #{p['codigo']} ({p['cliente']})", size=16, weight=ft.FontWeight.BOLD, color="#2C221E"),
                                    ft.Text(p['estado'], color="#E05638" if "Preparación" in p['estado'] else "#2E7D32", weight=ft.FontWeight.BOLD, size=13)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ft.Text(f"Zona: {p.get('sede', '')}", color="#7A685D", size=13),
                                ft.Text(f"Puesto Destino: {p.get('puesto', '')}", color="#E05638", weight=ft.FontWeight.BOLD, size=13),
                                ft.Text(f"Detalle: {p['detalle']}", size=14, color="#2E7D32", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Notas: {p.get('notas', 'Sin especificaciones')}", size=12, color="#7A685D", italic=True),
                                ft.Text("⏱️ Límite de entrega: Máximo 10 min", size=12, color="#E05638"),
                                ft.Text(f"Pago: {p['pago']} | Total: S/ {p['total']:.2f}", color="#7A685D", size=13),
                                ft.Row([
                                    ft.TextButton("🟡 Preparando", style=ft.ButtonStyle(bgcolor="#FF9800", color="white"), on_click=lambda e, pid=p["id"]: actualizar_estado(pid, "🟡 En Preparación")),
                                    ft.TextButton("🟢 Listo", style=ft.ButtonStyle(bgcolor="#2E7D32", color="white"), on_click=lambda e, pid=p["id"]: actualizar_estado(pid, "🟢 Listo para Recoger")),
                                    ft.TextButton("✅ Entregado", style=ft.ButtonStyle(bgcolor="#1E88E5", color="white"), on_click=lambda e, pid=p["id"]: actualizar_estado(pid, "✅ Entregado")),
                                ], wrap=True, spacing=8)
                            ], spacing=8),
                            padding=14,
                            bgcolor="#FFFFFF",
                            border_radius=12,
                            width=600,
                            border=ft.Border(
                                top=ft.BorderSide(1, "#EFEBE4"),
                                bottom=ft.BorderSide(1, "#EFEBE4"),
                                left=ft.BorderSide(1, "#EFEBE4"),
                                right=ft.BorderSide(1, "#EFEBE4"),
                            )
                        )
                    )
        else:
            total_recaudado = sum(p["total"] for p in db_global["pedidos"])
            cant_ordenes = len(db_global["pedidos"])
            pagos_yape = len([p for p in db_global["pedidos"] if p["pago"] == "Yape"])
            pagos_plin = len([p for p in db_global["pedidos"] if p["pago"] == "Plin"])
            pagos_tarjeta = len([p for p in db_global["pedidos"] if p["pago"] == "Tarjeta"])

            col_contenido.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("📈 Resumen de Ventas - Panel Administrador", size=18, weight=ft.FontWeight.BOLD, color="#2C221E"),
                        ft.Divider(color="#EFEBE4"),
                        ft.Row([
                            ft.Column([
                                ft.Text("Ventas Totales", color="#7A685D", size=13),
                                ft.Text(f"S/ {total_recaudado:.2f}", size=22, weight=ft.FontWeight.BOLD, color="#2E7D32")
                            ]),
                            ft.Column([
                                ft.Text("Órdenes Atendidas", color="#7A685D", size=13),
                                ft.Text(str(cant_ordenes), size=22, weight=ft.FontWeight.BOLD, color="#E05638")
                            ])
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                        ft.Divider(color="#EFEBE4"),
                        ft.Text("💳 Métodos de Pago Preferidos:", weight=ft.FontWeight.BOLD, color="#2C221E", size=14),
                        ft.Text(f"• Yape: {pagos_yape} órdenes", color="#7A685D", size=13),
                        ft.Text(f"• Plin: {pagos_plin} órdenes", color="#7A685D", size=13),
                        ft.Text(f"• Tarjeta / Otros: {pagos_tarjeta} órdenes", color="#7A685D", size=13),
                        ft.Divider(color="#EFEBE4"),
                        ft.Text("⭐ Tiempo Promedio de Entrega: < 8 minutos", color="#2E7D32", weight=ft.FontWeight.BOLD, size=14)
                    ], spacing=10),
                    padding=20,
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    width=600,
                    border=ft.Border(
                        top=ft.BorderSide(1, "#EFEBE4"),
                        bottom=ft.BorderSide(1, "#EFEBE4"),
                        left=ft.BorderSide(1, "#EFEBE4"),
                        right=ft.BorderSide(1, "#EFEBE4"),
                    )
                )
            )

        contenedor_cocina = ft.Column([
            header_cocina,
            nav_cocina,
            col_contenido
        ], spacing=16, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        contenido_principal.controls.clear()
        contenido_principal.controls.append(contenedor_cocina)
        page.update()
    page.controls.clear()
    page.controls.append(contenido_principal)
    page.update()
    mostrar_login("cliente", "login")

import os
import flet_fastapi

# Obtener ruta absoluta de la carpeta assets
assets_path = os.path.abspath("assets")

# Envolver la aplicación de Flet para servidor
app = flet_fastapi.app(
    main, 
    assets_dir=assets_path,
    secret_key="clave_secreta_desayunos_usil"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("proempreusil:app", host="0.0.0.0", port=8000)