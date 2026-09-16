from fastapi.testclient import TestClient


def get_auth_headers(client: TestClient) -> dict:
    """Helper fixture para obtener cabeceras de autorización JWT."""
    client.post("/api/v1/auth/signup", json={
        "email": "prodadmin@example.com",
        "full_name": "Product Admin",
        "password": "password123"
    })
    res = client.post("/api/v1/auth/login", json={
        "email": "prodadmin@example.com",
        "password": "password123"
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_and_get_product(client: TestClient):
    headers = get_auth_headers(client)

    payload = {
        "title": "Mouse Gamer Logitech G Pro Wireless",
        "category": "hardware",
        "type": "producto",
        "price": 89900.0,
        "badge": "Top Ventas",
        "image": "https://example.com/mouse.jpg",
        "short_desc": "Sensor HERO 25K de alta precisión.",
        "full_desc": "Mouse inalámbrico liviano diseñado para eSports profesionales.",
        "specs": ["DPI: 25.600", "Peso: 80g", "Conexión: Lightspeed 1ms"],
        "stock": 15
    }

    create_res = client.post("/api/v1/products", json=payload, headers=headers)
    assert create_res.status_code == 201
    created_data = create_res.json()
    assert created_data["title"] == "Mouse Gamer Logitech G Pro Wireless"
    assert created_data["specs"] == ["DPI: 25.600", "Peso: 80g", "Conexión: Lightspeed 1ms"]
    product_id = created_data["id"]

    # Obtener por ID
    get_res = client.get(f"/api/v1/products/{product_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Mouse Gamer Logitech G Pro Wireless"


def test_product_filters(client: TestClient):
    headers = get_auth_headers(client)

    # Crear 3 productos distintos
    client.post("/api/v1/products", headers=headers, json={
        "title": "Teclado Mecánico RGB",
        "category": "hardware",
        "type": "producto",
        "price": 50000.0,
        "image": "img1.jpg",
        "short_desc": "Switches Red",
        "full_desc": "Teclado mecánico con retroiluminación RGB.",
        "specs": []
    })
    client.post("/api/v1/products", headers=headers, json={
        "title": "Notebook Gamer RTX 4070",
        "category": "notebooks",
        "type": "producto",
        "price": 1500000.0,
        "image": "img2.jpg",
        "short_desc": "Laptop i7",
        "full_desc": "Potente notebook para gaming.",
        "specs": []
    })
    client.post("/api/v1/products", headers=headers, json={
        "title": "Limpieza y Mantenimiento PC",
        "category": "servicios",
        "type": "servicio",
        "price": 30000.0,
        "image": "img3.jpg",
        "short_desc": "Limpieza de polvo",
        "full_desc": "Servicio técnico preventivo de PC.",
        "specs": []
    })

    # 1. Filtro por categoría
    res_cat = client.get("/api/v1/products?category=notebooks")
    assert res_cat.status_code == 200
    items_cat = res_cat.json()
    assert len(items_cat) == 1
    assert items_cat[0]["title"] == "Notebook Gamer RTX 4070"

    # 2. Filtro por tipo
    res_type = client.get("/api/v1/products?type=servicio")
    assert res_type.status_code == 200
    items_type = res_type.json()
    assert len(items_type) == 1
    assert items_type[0]["title"] == "Limpieza y Mantenimiento PC"

    # 3. Filtro por búsqueda de texto
    res_search = client.get("/api/v1/products?search=Mecánico")
    assert res_search.status_code == 200
    items_search = res_search.json()
    assert len(items_search) == 1
    assert items_search[0]["title"] == "Teclado Mecánico RGB"

    # 4. Filtro por rango de precio
    res_price = client.get("/api/v1/products?min_price=40000&max_price=100000")
    assert res_price.status_code == 200
    items_price = res_price.json()
    assert len(items_price) == 1
    assert items_price[0]["title"] == "Teclado Mecánico RGB"


def test_update_and_delete_product(client: TestClient):
    headers = get_auth_headers(client)

    # Crear producto
    create_res = client.post("/api/v1/products", headers=headers, json={
        "title": "Producto a Modificar",
        "category": "hardware",
        "type": "producto",
        "price": 10000.0,
        "image": "img.jpg",
        "short_desc": "Desc corta",
        "full_desc": "Desc larga",
        "specs": []
    })
    prod_id = create_res.json()["id"]

    # Editar
    update_res = client.put(f"/api/v1/products/{prod_id}", headers=headers, json={
        "price": 12500.0,
        "title": "Producto Modificado Exitosamente"
    })
    assert update_res.status_code == 200
    updated_data = update_res.json()
    assert updated_data["price"] == 12500.0
    assert updated_data["title"] == "Producto Modificado Exitosamente"

    # Eliminar
    del_res = client.delete(f"/api/v1/products/{prod_id}", headers=headers)
    assert del_res.status_code == 204

    # Verificar que ya no existe
    get_res = client.get(f"/api/v1/products/{prod_id}")
    assert get_res.status_code == 404


def test_create_product_unauthorized(client: TestClient):
    res = client.post("/api/v1/products", json={
        "title": "No Auth Product",
        "category": "hardware",
        "type": "producto",
        "price": 100.0,
        "image": "img.jpg",
        "short_desc": "s",
        "full_desc": "f",
        "specs": []
    })
    assert res.status_code == 401
