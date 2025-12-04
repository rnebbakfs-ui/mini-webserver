# an app uses the SWF 


from miniweb import MiniApp, Response

app = MiniApp()

@app.route("/", methods=("GET",))
def index(req):
    return "Welcome to MiniWeb!"

@app.route("/hello", methods=("GET",))
def hello(req):
    # get query param ?name=Rayane
    name = req.query.get("name", ["World"])[0]
    return f"Hello {name}!"

@app.route("/form", methods=("POST",))
def form_submit(req):
    # Example: body is application/x-www-form-urlencoded
    username = req.form.get("username", [""])[0]
    return Response(f"Received username: {username}", headers={"Content-Type":"text/plain"})

if __name__ == "__main__":
    app.run(port=8080)
