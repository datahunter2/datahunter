from flask import Flask, request
import mmap
import os

app = Flask(__name__)

def search_in_files(search_string):
    isFound = False
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for file in os.listdir(current_dir):
        if file.endswith(".txt"):
            file_path = os.path.join(current_dir, file)
            with open(file_path, "r", encoding="utf-8") as f:
                mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                for line in iter(mm.readline, b''):
                    if search_string.encode('utf-8') in line:
                        res=line.decode('utf-8')
                        values = res.strip().split(",")
                        document = {
                            "id": values[0].strip('"'),
                            "phone_number": values[3].strip('"'),
                            "name": values[6].strip('"'),
                            "facebook_url": values[9].strip('"'),
                        }
                        isFound = True
                        return {"data": document}
                            
    if not isFound:
        return None
    
@app.route('/', methods=['GET'])
def home():
    return {"dev": "@usfnassar","itsWork":False,"msg":"https://t.me/datahunter0/24"}

@app.route('/s', methods=['GET'])
def search_api_id():
    search_string = request.args.get('key')

    if not search_string:
        return {"error": "you should give the id or phone number are required."}, 400

    result = search_in_files(search_string)

    if result:
        return result
    else:
        return {"message": "NOT FOUND"}, 404
    


if __name__ == '__main__':
    app.run(debug=True)
