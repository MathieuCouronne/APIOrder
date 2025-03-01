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