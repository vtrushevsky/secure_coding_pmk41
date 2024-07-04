from webserver import create_app


context = ('instance/certificates/localhost.crt',
           'instance/certificates/localhost.key')
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=80, ssl_context=context)
