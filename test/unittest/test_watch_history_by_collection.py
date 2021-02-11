import json
from decimal import Decimal
from unittest.mock import patch

from api_errors import HttpError
from api.watch_history_by_collection import handle
from schema import ALLOWED_SORT
from watch_history_db import NotFoundError

TEST_JWT = "eyJraWQiOiIxMjMxMjMxMjM9IiwiYWxnIjoiSFMyNTYifQ.eyJ1c2VybmFtZSI6IlRFU1RfQ0xJRU5UX0lEIn0.ud_dRdguJwmKv4XO-c4JD-dKGffSvXsxuAxZq9uWV-g"


@patch("api.watch_history_by_collection.watch_history_db.get_watch_history")
def test_handler(mocked_get_watch_history):
    mocked_get_watch_history.return_value = {
        "items": {"123": {"collection_name": "anime", "item_id": Decimal(123)}}
    }
    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "pathParameters": {
            "collection_name": "anime"
        },
        "requestContext": {
            "http": {
                "method": "GET"
            }
        }
    }

    ret = handle(event, None)
    assert ret == {
        'body': '{"items": {"123": {"collection_name": "anime", "item_id": 123}}}',
        "statusCode": 200
    }


def test_handler_invalid_sort():
    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "queryStringParameters": {
            "sort": "INVALID"
        },
        "pathParameters": {
            "collection_name": "anime"
        },
        "requestContext": {
            "http": {
                "method": "GET"
            }
        }
    }

    ret = handle(event, None)

    assert ret == {
        "statusCode": 400,
        "body": json.dumps({"error": f"Invalid sort specified. Allowed values: {ALLOWED_SORT}"})
    }


@patch("api.watch_history_by_collection.watch_history_db.get_watch_history")
def test_handler_sort(mocked_get_watch_history):
    mocked_get_watch_history.return_value = [{"collection_name": "test_collection", "item_id": Decimal(123)}]

    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "queryStringParameters": {
            "sort": "dates_watched"
        },
        "pathParameters": {
            "collection_name": "test_collection"
        },
        "requestContext": {
            "http": {
                "method": "GET"
            }
        }
    }

    ret = handle(event, None)

    assert ret == {'body': '[{"collection_name": "test_collection", "item_id": 123}]', 'statusCode': 200}


@patch("api.watch_history_by_collection.watch_history_db.get_watch_history")
def test_handler_limit_and_start(mocked_get_watch_history):
    mocked_get_watch_history.return_value = [{"collection_name": "test_collection", "item_id": Decimal(123)}]

    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "queryStringParameters": {
            "limit": "200",
            "start": "23"
        },
        "pathParameters": {
            "collection_name": "test_collection"
        },
        "requestContext": {
            "http": {
                "method": "GET"
            }
        }
    }

    ret = handle(event, None)

    assert ret == {'body': '[{"collection_name": "test_collection", "item_id": 123}]', 'statusCode': 200}


def test_handler_invalid_limit_type():
    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "queryStringParameters": {
            "limit": "ABC",
        },
        "pathParameters": {
            "collection_name": "anime"
        },
        "requestContext": {
            "http": {
                "method": "GET"
            }
        }
    }

    ret = handle(event, None)

    assert ret == {'body': '{"message": "Invalid limit type"}', 'statusCode': 400}


def test_handler_invalid_start_type():
    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "queryStringParameters": {
            "start": "ABC",
        },
        "pathParameters": {
            "collection_name": "anime"
        },
        "requestContext": {
            "http": {
                "method": "GET"
            }
        }
    }

    ret = handle(event, None)

    assert ret == {'body': '{"message": "Invalid start type"}', 'statusCode': 400}


@patch("api.watch_history_by_collection.watch_history_db.get_watch_history")
def test_handler_not_found(mocked_get_watch_history):
    mocked_get_watch_history.side_effect = NotFoundError

    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "pathParameters": {
            "collection_name": "anime"
        },
        "requestContext": {
            "http": {
                "method": "GET"
            }
        }
    }

    ret = handle(event, None)

    assert ret == {"statusCode": 200, "body": json.dumps({"items": []})}


@patch("api.watch_history_by_collection.watch_history_db.update_item")
def test_handler_post_without_body(mocked_post):
    mocked_post.return_value = True

    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "requestContext": {
            "http": {
                "method": "POST"
            }
        },
        "pathParameters": {
            "collection_name": "anime",
            "item_id": "123"
        }
    }

    ret = handle(event, None)
    assert ret == {'body': 'Invalid post body', 'statusCode': 400}


@patch("api.watch_history_by_collection.watch_history_db.update_item")
def test_handler_post_with_empty_body(mocked_post):
    mocked_post.return_value = True

    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "requestContext": {
            "http": {
                "method": "POST"
            }
        },
        "pathParameters": {
            "collection_name": "anime",
            "item_id": "123"
        },
        "body": ''
    }

    ret = handle(event, None)
    assert ret == {'body': 'Invalid post body', 'statusCode': 400}


@patch("api.watch_history_by_collection.watch_history_db.add_item")
@patch("api.watch_history_by_collection.anime_api.post_anime")
def test_handler_post_anime(mocked_post_anime, mocked_post):
    mocked_post_anime.return_value.json.return_value = {
        "id": "123"
    }
    mocked_post.return_value = True

    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "requestContext": {
            "http": {
                "method": "POST"
            }
        },
        "pathParameters": {
            "collection_name": "anime",
        },
        "body": '{ "api_id": "123", "api_name": "mal" }'
    }

    ret = handle(event, None)
    assert ret == {'statusCode': 204, 'id': "123"}


@patch("api.watch_history_by_collection.watch_history_db.add_item")
@patch("api.watch_history_by_collection.shows_api.post_show")
def test_handler_post_show(mocked_post_show, mocked_post):
    mocked_post_show.return_value.json.return_value = {
        "id": "123"
    }
    mocked_post.return_value = True

    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "requestContext": {
            "http": {
                "method": "POST"
            }
        },
        "pathParameters": {
            "collection_name": "show"
        },
        "body": '{ "api_id": "123", "api_name": "tvmaze" }'
    }

    ret = handle(event, None)
    assert ret == {'statusCode': 204, "id": "123"}


@patch("api.watch_history_by_collection.watch_history_db.add_item")
@patch("api.watch_history_by_collection.movie_api.post_movie")
def test_handler_post_movie(mocked_post_movie, mocked_post):
    mocked_post_movie.return_value.json.return_value = {
        "id": "123"
    }
    mocked_post.return_value = True

    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "requestContext": {
            "http": {
                "method": "POST"
            }
        },
        "pathParameters": {
            "collection_name": "movie"
        },
        "body": '{ "api_id": "123", "api_name": "tmdb" }'
    }

    ret = handle(event, None)
    assert ret == {'statusCode': 204, "id": "123"}


@patch("api.watch_history_by_collection.watch_history_db.update_item")
@patch("api.watch_history_by_collection.anime_api.post_anime")
def test_handler_post_anime_api_error(mocked_get_anime, mocked_post):
    mocked_get_anime.side_effect = HttpError("test_error", 403)
    mocked_post.return_value = True

    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "requestContext": {
            "http": {
                "method": "POST"
            }
        },
        "pathParameters": {
            "collection_name": "anime",
        },
        "body": '{ "api_id": "123", "api_name": "mal" }'
    }

    ret = handle(event, None)
    assert ret == {
        'body': '{"message": "Could not post anime"}',
        'error': 'test_error',
        'statusCode': 403
    }


@patch("api.watch_history_by_collection.watch_history_db.update_item")
def test_handler_post_invalid_collection(mocked_post):
    mocked_post.return_value = True

    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "requestContext": {
            "http": {
                "method": "POST"
            }
        },
        "pathParameters": {
            "collection_name": "INVALID",
            "item_id": "123"
        },
        "body": '{ "api_id": 123 }'
    }

    ret = handle(event, None)
    assert ret == {
        'body': '{"message": "Invalid collection name, allowed values: [\'anime\', \'show\', \'movie\']"}',
        'statusCode': 400
    }


@patch("api.watch_history_by_collection.watch_history_db.update_item")
def test_handler_post_invalid_body(mocked_post):
    mocked_post.return_value = True

    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "requestContext": {
            "http": {
                "method": "POST"
            }
        },
        "pathParameters": {
            "collection_name": "INVALID",
            "item_id": "123"
        },
        "body": "INVALID"
    }

    ret = handle(event, None)
    assert ret == {'body': 'Invalid post body', 'statusCode': 400}


@patch("api.watch_history_by_collection.watch_history_db.update_item")
def test_handler_post_invalid_body_schema(mocked_post):
    mocked_post.return_value = True

    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "requestContext": {
            "http": {
                "method": "POST"
            }
        },
        "pathParameters": {
            "collection_name": "anime",
            "item_id": "123"
        },
        "body": '{"invalid": "val"}'
    }

    ret = handle(event, None)
    assert ret == {
        'body': '{"message": "Invalid post schema", "error": "Additional properties are not allowed (\'invalid\' was unexpected)"}',
        'statusCode': 400
    }


@patch("api.watch_history_by_collection.watch_history_db.add_item")
@patch("api.watch_history_by_collection.shows_api.get_show")
def test_handler_post_show_without_id(mocked_get_show, mocked_post):
    mocked_get_show.return_value = True
    mocked_post.return_value = True

    event = {
        "headers": {
            "authorization": TEST_JWT
        },
        "requestContext": {
            "http": {
                "method": "POST"
            }
        },
        "pathParameters": {
            "collection_name": "show",
        },
        "body": '{"api_name": "tvmaze"}'
    }

    ret = handle(event, None)
    assert ret == {
        'body': '{"message": "Invalid post schema", "error": "\'api_id\' is a required property"}',
        'statusCode': 400
    }
