def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_post_order_wrong_id(client):
    response = client.post('/order', json={
        "product": {
                "id": 123,
                "quantity": 2
        }
    })
    assert response.status_code == 422

def test_post_order_right(client):
    response = client.post('/order', json={
        "product": {
                "id": 1,
                "quantity": 2
        }
    })
    assert response.status_code == 302
    assert response.headers['Location'] == '/order/1'

def test_post_order_nothing(client):
    response = client.post('/order', json={})
    assert response.status_code == 422

def test_get_order_not_found(client):
    response = client.get("/order/999")
    assert response.status_code == 404

def test_get_order_valid(client):
    client.post('/order', json={"product": {"id": 1, "quantity": 2}})
    response = client.get("/order/1")
    assert response.status_code == 200
    data = response.get_json()
    assert "order" in data
    assert data["order"]["id"] == 1

def test_update_order_valid(client):
    client.post('/order', json={ "product": { "id": 1, "quantity": 2 } })

    response = client.put("/order/1", json={
        "order": {
            "email": "test@example.com",
            "shipping_information": {
                "country": "Canada",
                "address": "123 Rue",
                "postal_code": "H3Z1Y7",
                "city": "Montréal",
                "province": "QC"
            }
        }
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["order"]["email"] == "test@example.com"

def test_update_order_not_found(client):
    response = client.put("/order/999", json={
        "order": {
            "email": "test@example.com"
        }
    })
    assert response.status_code == 404

def test_update_order_missing_fields(client):
    client.post('/order', json={ "product": { "id": 1, "quantity": 2 } })

    response = client.put("/order/1", json={
        "order": {
            "shipping_information": {
                "country": "Canada"
            }
        }
    })
    assert response.status_code == 422

def test_pay_order_valid(client):
    client.post('/order', json={ "product": { "id": 1, "quantity": 2 } })

    client.put("/order/1", json={
        "order": {
            "email": "test@example.com",
            "shipping_information": {
                "country": "Canada",
                "address": "123 Rue",
                "postal_code": "H3Z1Y7",
                "city": "Montréal",
                "province": "QC"
            }
        }
    })

    response = client.put("/order/1", json={
        "credit_card": {
            "name": "John Doe",
            "number": "4242 4242 4242 4242",
            "expiration_year": 2026,
            "cvv": "123",
            "expiration_month": 9
        }
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["order"]["paid"] is True
