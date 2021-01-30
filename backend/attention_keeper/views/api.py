from flask_api import FlaskAPI, status


def create_app(config):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(config)

    @app.route('/', methods=['GET'])
    def heath():
        return "Sever is running", status.HTTP_200_OK

    return app
