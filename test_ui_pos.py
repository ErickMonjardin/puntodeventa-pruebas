import pytest
from playwright.sync_api import Page, expect

# Cambiar el localhost por mi IP
URL_LOGIN = "http://localhost:8081/vista/" 

def test_pagina_login_carga(page: Page):
    page.goto(URL_LOGIN)
    
    expect(page.get_by_text("Nombre de Usuario")).to_be_visible()
    expect(page.get_by_text("Contraseña")).to_be_visible()

def test_login_intento(page: Page):
    page.goto(URL_LOGIN)
    
    # Usamos los IDs reales que genera JSF (loginForm:usuario)
    page.fill("id=loginForm:usuario", "ADMIN")
    page.fill("id=loginForm:password", "123456")
    
    # PrimeFaces crea un dropdown especial para el rol, damos clic en la etiqueta para abrirlo
    page.locator("id=loginForm:rol").click()
    # Seleccionamos la opción (cambia "Administrador" por el rol real que uses)
    page.get_by_text("Administrador", exact=True).click()
    
    # Clic en el botón usando su texto
    page.get_by_role("button", name="Acceder").click()
    
    # Aquí puedes agregar un expect para validar si entró al sistema o mostró error