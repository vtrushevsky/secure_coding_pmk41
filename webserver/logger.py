class Logger(object):

    @staticmethod
    def log(message: str):
        with open('webserver_logs.log', 'a') as f:
            f.write(f'{message}\n')
