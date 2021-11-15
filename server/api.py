import logging
from flask import jsonify, render_template, request, make_response
from dateutil import parser as date_parser
import io
import csv

from server import app
from server.util.request import api_error_handler, arguments_required
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
def api_count_over_time():
    query = _parse_query()
    provider = platforms.provider_for(query['platform'], query['platform_source'])
    results = provider.count_over_time(query['terms'], query['start_date'], query['end_date'])
    return jsonify(results)


@app.route('/api/count-over-time.csv', methods=['GET'])
@api_error_handler
@arguments_required('platform', 'terms', 'startDate', 'endDate')
def api_count_over_time_csv():
    platform_parts = [d.strip() for d in request.args['platform'].split("/")]
    query = dict(
        terms=request.args['terms'],
        start_date=date_parser.parse(request.args['startDate']),
        end_date=date_parser.parse(request.args['endDate']),
        platform=platform_parts[0],
        platform_source=platform_parts[1]
    )
    provider = platforms.provider_for(query['platform'], query['platform_source'])
    results = provider.count_over_time(query['terms'], query['start_date'], query['end_date'])
    # now send csv
    si = io.StringIO()
    cw = csv.DictWriter(si, fieldnames=results['counts'][0].keys())
    cw.writeheader()
    cw.writerows(results['counts'])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route('/api/normalized-count-over-time.json', methods=['POST'])
@api_error_handler
def api_normalized_count_over_time():
    query = _parse_query()
    provider = platforms.provider_for(query['platform'], query['platform_source'])
    results = provider.normalized_count_over_time(query['terms'], query['start_date'], query['end_date'])
    return jsonify(results)


@app.route('/api/count.json', methods=['POST'])
@api_error_handler
def api_count():
    query = _parse_query()
    provider = platforms.provider_for(query['platform'], query['platform_source'])
    results = provider.count(query['terms'], query['start_date'], query['end_date'])
    return jsonify(results)


@app.route('/api/sample.json', methods=['POST'])
@api_error_handler
def api_sample():
    query = _parse_query()
    provider = platforms.provider_for(query['platform'], query['platform_source'])
    results = provider.sample(query['terms'], query['start_date'], query['end_date'], limit=50)
    return jsonify(results)
