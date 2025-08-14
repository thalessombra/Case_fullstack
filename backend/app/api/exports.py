from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import io
import csv
from app.db.models import Client

router = APIRouter()

@router.get("/clients/export")
def export_clients():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Nome", "Email", "Ativo"])
    
   
    clients = Client.select() 
    for c in clients:
        writer.writerow([c.id, c.name, c.email, c.is_active])
    
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=clients.csv"})
