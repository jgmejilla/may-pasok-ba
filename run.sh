# activate venv
cd server
source venv/bin/activate
cd ..

# run app and server concurrently
(cd server && uvicorn main:app --reload) &
(cd app && npm run dev) &
wait