import logging
from flask import jsonify, render_template, request
from dateutil import parser as date_parser

from server import app
from server.util.request import api_error_handler
import server.platforms as platforms

logger = logging.getLogger(__name__)


# set up all the views
@app.route('/')
def index():
    logger.debug("homepage request")
    plaform_list = platforms.available_platforms()
    return render_template('index.html', platforms=plaform_list)


def _parse_query():
    data = request.json
    platform_parts = [d.strip() for d in data['platform'].split("/")]
    query = dict(
        terms=data['terms'],
        start_date=date_parser.parse(data['startDate']),
        end_date=date_parser.parse(data['endDate']),
        platform=platform_parts[0],
        platform_source=platform_parts[1]
    )
    return query


@app.route('/api/count-over-time.json', methods=['POST'])
@api_error_handler
def api_count():
    query = _parse_query()
    provider = platforms.provider_for(query['platform'], query['platform_source'])
    results = provider.count_over_time(query['terms'], query['start_date'], query['end_date'])
    return jsonify(results)
