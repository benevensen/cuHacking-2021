from attention_keeper.utils import logger
from attention_keeper.views.api import create_app
import config

LOGGER = logger.get_logger(__name__)


def main(args=None):
    LOGGER.debug('creating app')
    app = create_app(config.get_config())
    LOGGER.debug('Running app')
    app.run(host='0.0.0.0', port=8080, threaded=True)


if __name__ == '__main__':
    main()
