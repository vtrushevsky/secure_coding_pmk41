from webserver import create_app


context = ('instance/certificates/server_certificate/localhost.crt',
           'instance/certificates/server_certificate/localhost.key')
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
