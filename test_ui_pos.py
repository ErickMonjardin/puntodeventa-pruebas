import re
from playwright.sync_api import Page, expect

URL_LOGIN = "http://10.21.54.164:8081/vista/"

# FUNCIÓN AUXILIAR (Se ejecuta antes de cada prueba)
# ==========================================
def realizar_login(page: Page):
    """Inicia sesión automáticamente para preparar el sistema para la prueba."""
    page.goto(URL_LOGIN)
    page.fill("id=loginForm:usuario", "ADMIN")
    page.fill("id=loginForm:password", "123456")
    page.locator("id=loginForm:rol").click()
    page.locator("li.ui-selectonemenu-item", has_text="Administrador").click()
    page.locator("button", has_text="Acceder").click()
    page.wait_for_url("**/Inventario.xhtml")
    page.wait_for_timeout(1500)  
# CASO 1: LOGIN EXITOSO
# ==========================================
def test_login_intento(page: Page):
    realizar_login(page)
    expect(page).to_have_url(re.compile(r".*Inventario\.xhtml"))
    print("\n¡Login exitoso y redirección confirmada!")

# CASO 2: CONSULTA DE PRODUCTO POR ID
# ==========================================
def test_consulta_producto(page: Page):
    realizar_login(page)
    
    page.fill("id=formInventario:tabsPrincipal:busqueda", "8") #AJUSTAR ID DE PRODUCTO EXISTENTE
    
    # Clic en el botón buscar
    page.locator("button", has_text="Buscar").first.click()
    page.wait_for_timeout(1000) # Esperar a que AJAX actualice la tabla
    
    # Validamos que el primer renglon de la tabla es visible 
    primera_fila = page.locator("id=formInventario:tabsPrincipal:tablaInventario_data").locator("tr").first
    expect(primera_fila).to_be_visible()

# CASO 3: ALTA DE PRODUCTO
# ==========================================
def test_alta_de_producto(page: Page):
    realizar_login(page)
    
    # 1. Navegar a la pestaña "Altas"
    page.get_by_role("tab", name="Altas").click()
    page.wait_for_timeout(500)
    
    # 2. Desplegar menú de opciones y hacer clic en Registrar Producto
    page.locator("button", has_text="Opciones de alta").click()
    page.locator("a.ui-menuitem-link", has_text="Registrar producto").click()
    
    # 3. Llenar el formulario emergente (dialog)
    page.fill("id=formAltaProducto:nombre", "Producto Test")
    page.fill("id=formAltaProducto:precio", "150")
    page.fill("id=formAltaProducto:stock", "20")
    
    # 4. Seleccionar un Proveedor del Dropdown
    page.locator("id=formAltaProducto:proveedor").click()
    page.locator("li.ui-selectonemenu-item").nth(1).click()
    
    # 5. Guardar registro
    page.locator("id=formAltaProducto").locator("button", has_text="Registrar").click()
    
    expect(page.locator(".ui-growl-message")).to_be_visible()

# CASO 4: REALIZAR ENTRADA DE PRODUCTO
# ==========================================
def test_entrada_producto(page: Page):
    realizar_login(page)
    
    page.get_by_role("tab", name="Movimientos", exact=True).click()
    page.wait_for_timeout(1000)
    
    # 2. Llenar la cantidad en el spinner de la primera fila
    spinner_input = page.locator("id=formInventario:tabsPrincipal:tablaMovimientos_data").locator(".ui-spinner-input").first
    spinner_input.fill("15")
    
    # 3. Clic en el botón "Entrada" de esa misma fila
    page.locator("id=formInventario:tabsPrincipal:tablaMovimientos_data").locator("button", has_text="Entrada").first.click()
    
    # 4. Validar éxito
    expect(page.locator(".ui-growl-message")).to_be_visible()

# CASO 5: BAJA DE UN PRODUCTO
# ==========================================
def test_baja_de_producto(page: Page):
    realizar_login(page)
    
    # 1. Seleccionar la primera fila de la tabla
    primera_fila = page.locator("id=formInventario:tabsPrincipal:tablaInventario_data").locator("tr").first
    primera_fila.click()
    # Damos 1 segundo extra para que el AJAX de PrimeFaces habilite el botón rojo
    page.wait_for_timeout(1000) 
    
    # 2. Clic en el botón Eliminar
    page.locator("button", has_text="Eliminar").first.click()
    # Damos medio segundo para que termine la animación de aparecer del cuadro de diálogo
    page.wait_for_timeout(500)
    
    # 3. Confirmar en el cuadro de diálogo 
    page.locator("button:has-text('Sí'):visible").click()
    
    expect(page.locator(".ui-growl-message")).to_be_visible()