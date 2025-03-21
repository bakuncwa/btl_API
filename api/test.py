import requests

url = "http://127.0.0.1:5000/predict"
payload = {
    "product_id": "P122900",
    "total_concentration": "0.03900",
    "author_id": "2485269199",
    "product_name": "All About Eyes Eye Cream",
    "brand_name": "CLINIQUE",
    "submission_time": "2023-02-25",
    "rating": 1
}

# payload = {
#     "product_id": "P505346",
#     "total_concentration": "0.208848",
#     "author_id": "6274544266",
#     "product_name": "First Care Activating Serum 25th Anniversary",
#     "brand_name": "Sulwhasoo",
#     "submission_time": "2022-10-25",
#     "rating": 1
# }

response = requests.post(url, json=payload)
print(response.json())
