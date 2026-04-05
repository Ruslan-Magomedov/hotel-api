from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))



from app.api.hotels.hotels import router as router_hotels
from app.config import settings



print(settings.connection_path())



app = FastAPI()
app.include_router(router_hotels)



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
