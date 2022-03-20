from typing import Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()
id_product = 0
product_db = {}

class Product(BaseModel):
    nama: str
    kategori: str
    deskripsi: str
    is_available: bool

class ProductUpdate(BaseModel):
    nama: Optional[str]
    kategori: Optional[str]
    deskripsi: Optional[str]
    is_available: Optional[bool]

def not_found(id_product: int):
    return JSONResponse(
        status_code=404,
        content = {"message":f"Produk dengan id {id_product} tidak ditemukan"}
    )
@app.get("/")
def read_root():
    return {"message": "Welcome"}

@app.get("/product")
def read_all():
    return {"message": "List semua product", "data": product_db}

@app.get("/product/{product_id}")
def read_one(product_id: int):
    try:
        product = product_db[product_id]
        return {"message": f"Product dengan id {product_id}", "data": product_db[product_id]}
    except:
        return not_found(product_id)

@app.post("/product")
def create_product(product: Product):
    global id_product
    id_product +=1
    data = {"id":id_product, **dict(product)}
    product_db[id_product] = data
    return {"message": "produk berhasil ditambahkan", "data": data}

@app.put("/product/{product_id}")
def update_product(product_id:int, product: ProductUpdate):
    if product_id in product_db.keys():
        product = dict(product)
        for field in product.keys():
            if product[field] != None:
                product_db[product_id][field] = product[field]
        return {"message": f"produk dengan id {product_id} berhasil diubah", "data": product_db[product_id]}
    else:
        return not_found(product_id)

@app.delete("/product/{product_id}")
def delete_product(product_id:int):
    try:
        del product_db[product_id]
        return {"message":f"Produk dengan id {product_id} berhasil dihapus"}
    except:
        return not_found(product_id)

@app.post("/file")
def upload_file(files: List[UploadFile]):
    filesname ={}
    count = 1
    for file in files:
        with open(f"files/{file.filename}", "wb") as upload:
            upload.write(file.file.read())
            filesname[f"file-{count}"] = file.filename
            count += 1
    return{"filesname":filesname}
