from pathlib import Path
import sys

parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from app.Department.routers import router as departments_router
from app.Department.model import Department
from app.Employee.model import Employee
import app.Employee.routers
from app.logger import logger


app = FastAPI()
def run_server():
    uvicorn.run('app.main:app')
app.include_router(departments_router)



@app.get("/", response_class=HTMLResponse)
async def root():
    logger.info("Обращение к корню сервера")
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>University API</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Inter', -apple-system, sans-serif;
                background: #fafafa;
                color: #1a1a1a;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                text-align: center;
                padding: 60px 40px;
            }
            h1 {
                font-size: 2rem;
                font-weight: 300;
                letter-spacing: -0.5px;
                margin-bottom: 12px;
            }
            p {
                color: #666;
                font-size: 0.95rem;
                margin-bottom: 40px;
            }
            .links {
                display: flex;
                gap: 12px;
                justify-content: center;
                flex-wrap: wrap;
            }
            .links a {
                text-decoration: none;
                color: #1a1a1a;
                padding: 10px 24px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                font-size: 0.9rem;
                transition: all 0.2s;
            }
            .links a:hover {
                background: #1a1a1a;
                color: #fff;
                border-color: #1a1a1a;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Department API</h1>
            <div class="links">
                <a href="/docs">API docs</a>

            </div>
        </div>
    </body>
    </html>
    """

if __name__=='__main__':
    run_server()